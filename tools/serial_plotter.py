#!/usr/bin/env python3
"""
tools/serial_plotter.py
Chromatography Live Telemetry & Peak Visualizer for Virtual Micro-HPLC / FIA

Reads the serial CSV stream emitted by the Arduino (or simulated data) and
renders a real-time chromatogram with baseline subtraction, peak highlighting,
and analytical metrics.

Usage:
    python3 serial_plotter.py --port /dev/tty.usbmodem1101 --baud 115200
    python3 serial_plotter.py --mock   # Test without physical serial hardware
"""

import sys
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

try:
    import serial
except ImportError:
    serial = None


class ChromatographyPlotter:
    def __init__(self, port=None, baud=115200, mock=False):
        self.port = port
        self.baud = baud
        self.mock = mock
        self.serial_conn = None

        # Data buffers
        self.time_data = []
        self.raw_data = []
        self.filtered_data = []
        self.baseline_data = []
        self.state_data = []

        # Peak detection tracking
        self.peaks_found = []

        # Mock generator state
        self.mock_start_time = None

        if not self.mock and self.port:
            if serial is None:
                print("[ERROR] pyserial is not installed. Install via: pip install pyserial")
                sys.exit(1)
            try:
                self.serial_conn = serial.Serial(self.port, self.baud, timeout=0.1)
                print(f"[SERIAL] Connected to {self.port} at {self.baud} baud.")
            except Exception as e:
                print(f"[ERROR] Could not open serial port {self.port}: {e}")
                print("[INFO] Falling back to MOCK mode.")
                self.mock = True

    def generate_mock_sample(self):
        """Generates realistic synthetic chromatographic data for offline testing."""
        if self.mock_start_time is None:
            self.mock_start_time = time.time()

        t = time.time() - self.mock_start_time
        base = 0.50 + 0.0005 * t
        noise = np.random.normal(0, 0.008)

        # Peak 1 (Theobromine): tR = 12s, Amp = 1.8V, sigma = 1.2s
        p1 = 1.80 * np.exp(-((t - 12.0) ** 2) / (2 * 1.2 ** 2))
        # Peak 2 (Caffeine): tR = 25s, Amp = 2.4V, sigma = 1.8s
        p2 = 2.40 * np.exp(-((t - 25.0) ** 2) / (2 * 1.8 ** 2))

        v_raw = base + p1 + p2 + noise
        v_filt = base + p1 + p2 + (noise * 0.2)
        state = 3 if t <= 35.0 else 4
        return t, v_raw, v_filt, base, state

    def read_serial_line(self):
        if self.mock or not self.serial_conn:
            return self.generate_mock_sample()

        try:
            line = self.serial_conn.readline().decode("utf-8", errors="ignore").strip()
            if not line or "," not in line or line.startswith("TIME_S") or line.startswith("[") or line.startswith("{"):
                return None
            parts = line.split(",")
            if len(parts) >= 5:
                t = float(parts[0])
                v_raw = float(parts[1])
                v_filt = float(parts[2])
                base = float(parts[3])
                state = int(parts[4])
                return t, v_raw, v_filt, base, state
        except Exception:
            return None
        return None

    def start(self):
        fig, (ax_main, ax_res) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]})
        fig.canvas.manager.set_window_title("Micro-HPLC & FIA Real-Time Chromatogram")

        # Top plot: Chromatogram
        line_raw, = ax_main.plot([], [], color="#a0c4ff", lw=1.0, alpha=0.7, label="Señal Bruta (ADC A0)")
        line_filt, = ax_main.plot([], [], color="#001219", lw=2.0, label="Señal Filtrada (EMA)")
        line_base, = ax_main.plot([], [], color="#94d2bd", lw=1.5, ls="--", label="Línea Base Estimada")

        ax_main.set_xlim(0, 36)
        ax_main.set_ylim(0.3, 3.5)
        ax_main.set_ylabel("Respuesta Detector UV-Vis [V]", fontsize=11, fontweight='bold')
        ax_main.set_title("CROMATOGRAMA EN TIEMPO REAL - Lab-on-a-Chip", fontsize=13, fontweight='bold')
        ax_main.grid(True, linestyle=":", alpha=0.6)
        ax_main.legend(loc="upper left")

        # Bottom plot: Net signal & Peak areas
        line_net, = ax_res.plot([], [], color="#ee9b00", lw=1.8, label="Absorbancia Neta (V - Vbase)")
        ax_res.set_xlim(0, 36)
        ax_res.set_ylim(-0.1, 3.0)
        ax_res.set_xlabel("Tiempo de Elución [s]", fontsize=11, fontweight='bold')
        ax_res.set_ylabel("ΔV [V]", fontsize=11, fontweight='bold')
        ax_res.grid(True, linestyle=":", alpha=0.6)
        ax_res.legend(loc="upper left")

        # Metrics text box
        text_info = ax_main.text(
            0.75, 0.70, "Estado: STANDBY\nEsperando inyección...",
            transform=ax_main.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#e9d8a6", alpha=0.8),
            fontsize=10
        )

        def update(frame):
            # Read multiple available points per frame
            for _ in range(5):
                sample = self.read_serial_line()
                if sample:
                    t, v_raw, v_filt, base, state = sample
                    self.time_data.append(t)
                    self.raw_data.append(v_raw)
                    self.filtered_data.append(v_filt)
                    self.baseline_data.append(base)
                    self.state_data.append(state)

            if not self.time_data:
                return line_raw, line_filt, line_base, line_net, text_info

            # Keep window bounds dynamic if needed
            max_t = max(36, self.time_data[-1] + 2)
            ax_main.set_xlim(0, max_t)
            ax_res.set_xlim(0, max_t)

            line_raw.set_data(self.time_data, self.raw_data)
            line_filt.set_data(self.time_data, self.filtered_data)
            line_base.set_data(self.time_data, self.baseline_data)

            # Net signal
            net_vals = [f - b for f, b in zip(self.filtered_data, self.baseline_data)]
            line_net.set_data(self.time_data, net_vals)

            # Update metrics box
            current_t = self.time_data[-1]
            current_v = self.filtered_data[-1]
            current_base = self.baseline_data[-1]
            status_names = {0: "IDLE", 1: "CALIBRANDO", 2: "INYECCION", 3: "ELUCION", 4: "COMPLETO"}
            state_str = status_names.get(self.state_data[-1], "RUN")

            info_msg = (
                f"Estado: {state_str}\n"
                f"Tiempo: {current_t:.1f} s\n"
                f"Detector: {current_v:.3f} V\n"
                f"Línea base: {current_base:.3f} V\n"
                f"ΔV Neto: {(current_v - current_base):.3f} V"
            )
            text_info.set_text(info_msg)

            return line_raw, line_filt, line_base, line_net, text_info

        ani = animation.FuncAnimation(fig, update, interval=100, blit=False)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live Chromatography Plotter")
    parser.add_argument("--port", type=str, default=None, help="Serial port (e.g. /dev/ttyUSB0 or COM3)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("--mock", action="store_true", help="Run with simulated synthetic data")
    args = parser.parse_args()

    # If no port provided and not mock, default to mock with warning
    if not args.port and not args.mock:
        print("[NOTICE] No serial port specified. Running in simulated MOCK mode.")
        args.mock = True

    plotter = ChromatographyPlotter(port=args.port, baud=args.baud, mock=args.mock)
    plotter.start()
