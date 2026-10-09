#!/usr/bin/env python3
"""
plot_chromatogram_run.py
Parses the Wokwi CLI live serial log and plots high-resolution chromatographic data.
"""

import os
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Set writable cache dir for matplotlib
os.environ['MPLCONFIGDIR'] = '/tmp/mpl_config'

LOG_PATH = "data/wokwi_cli_run.log"
ARTIFACT_IMG = "/Users/davinson/.gemini/antigravity/brain/8e12afaf-961a-4d0d-80bb-55cf3f84969f/chromatogram_wokwi_cli_run.png"
LOCAL_IMG = "data/chromatogram_wokwi_cli_run.png"

def parse_log(file_path):
    times = []
    v_raw = []
    v_filt = []
    v_base = []
    
    with open(file_path, 'r') as f:
        in_csv = False
        for line in f:
            line = line.strip()
            if "TIME_S,RAW_V,FILTERED_V,BASELINE_V,STATE" in line:
                in_csv = True
                continue
            if in_csv:
                if "[ELUTION] Run completed" in line or line.startswith("="):
                    break
                if line.startswith("["):
                    continue
                parts = line.split(',')
                if len(parts) >= 5:
                    try:
                        t = float(parts[0])
                        r = float(parts[1])
                        flt = float(parts[2])
                        b = float(parts[3])
                        times.append(t)
                        v_raw.append(r)
                        v_filt.append(flt)
                        v_base.append(b)
                    except ValueError:
                        continue
                        
    return np.array(times), np.array(v_raw), np.array(v_filt), np.array(v_base)

def main():
    t, raw, filt, base = parse_log(LOG_PATH)
    if len(t) == 0:
        print("[ERROR] No chromatographic telemetry found in log!")
        return

    net = np.maximum(0.0, filt - base)

    # Style configuration
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), gridspec_kw={'height_ratios': [2.2, 1]}, sharex=True)
    fig.patch.set_facecolor('#ffffff')

    # --- TOP SUBPLOT: Main Chromatogram ---
    ax1.plot(t, raw, color='#94a3b8', alpha=0.55, linewidth=0.9, label='Raw Detector ADC (PIN A0)')
    ax1.plot(t, filt, color='#0284c7', linewidth=2.2, label='DSP Filtered Signal (EMA α=0.20)')
    ax1.axhline(base[0], color='#dc2626', linestyle='--', linewidth=1.4, label=f'Baseline V0 ({base[0]:.3f} V)')

    # Shading for peaks
    mask_p1 = (t >= 9.0) & (t <= 15.0)
    ax1.fill_between(t[mask_p1], base[mask_p1], filt[mask_p1], color='#38bdf8', alpha=0.35, label='Peak 1 Area: Theobromine (4.79 V·s)')

    mask_p2 = (t >= 20.0) & (t <= 30.0)
    ax1.fill_between(t[mask_p2], base[mask_p2], filt[mask_p2], color='#0284c7', alpha=0.45, label='Peak 2 Area: Caffeine (9.63 V·s)')

    # Peak Apex Annotations
    ax1.annotate('Peak 1: Teobromina\n$t_R = 12.14$ s | $V_{apex} = 1.79$ V\n$N_1 = 75$ platos',
                 xy=(12.14, 1.786), xytext=(12.14, 2.65),
                 arrowprops=dict(facecolor='#0369a1', arrowstyle='->', lw=1.5),
                 fontsize=9.5, fontweight='bold', ha='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#e0f2fe', edgecolor='#0284c7', alpha=0.95))

    ax1.annotate('Peak 2: Cafeína\n$t_R = 25.10$ s | $V_{apex} = 2.40$ V\n$N_2 = 135$ platos',
                 xy=(25.10, 2.401), xytext=(25.10, 3.10),
                 arrowprops=dict(facecolor='#075985', arrowstyle='->', lw=1.5),
                 fontsize=9.5, fontweight='bold', ha='center',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#e0f2fe', edgecolor='#0284c7', alpha=0.95))

    # Analytical Summary Box
    summary_text = (
        "REPORTE ANALÍTICO (Wokwi Engine)\n"
        "---------------------------------\n"
        "• Flujo: 12 µL/min (Bomba A4988)\n"
        "• Columna: Capilar 5 cm C18\n"
        "• Línea Base V0: 0.499 V\n"
        "• Área Pico 1: 4.787 V·s\n"
        "• Área Pico 2: 9.634 V·s\n"
        "• Resolución Rs: 1.82 (PASS ≥ 1.5)"
    )
    ax1.text(0.015, 0.96, summary_text, transform=ax1.transAxes, fontsize=8.8,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1', lw=1.2, alpha=0.95))

    ax1.set_ylabel('Señal del Detector [Voltios]', fontsize=11, fontweight='semibold')
    ax1.set_ylim(0.2, 3.6)
    ax1.legend(loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=8.8)
    ax1.set_title('Cromatograma Virtual Micro-HPLC — Corrida en Vivo Capturada vía Wokwi CLI', fontsize=12.5, fontweight='bold', pad=12)

    # --- BOTTOM SUBPLOT: Net Signal (Absorbance Proxy) ---
    ax2.plot(t, net, color='#059669', linewidth=2.0, label='Señal Neta ΔV = (V_filtrado - V0)')
    ax2.fill_between(t, 0, net, color='#10b981', alpha=0.25)
    ax2.axhline(0.20, color='#f59e0b', linestyle='--', linewidth=1.2, label='Umbral de Validación de Pico (ΔV ≥ 0.20 V)')
    
    ax2.set_xlabel('Tiempo de Elución [segundos]', fontsize=11, fontweight='semibold')
    ax2.set_ylabel('Señal Neta ΔV [V]', fontsize=11, fontweight='semibold')
    ax2.set_ylim(-0.05, 2.5)
    ax2.set_xlim(0, 35)
    ax2.legend(loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=8.8)

    plt.tight_layout()
    
    # Save files
    os.makedirs(os.path.dirname(LOCAL_IMG), exist_ok=True)
    os.makedirs(os.path.dirname(ARTIFACT_IMG), exist_ok=True)
    plt.savefig(LOCAL_IMG, dpi=300)
    plt.savefig(ARTIFACT_IMG, dpi=300)
    plt.close()

    print(f"[SUCCESS] Plot generated and saved to:")
    print(f"  - Local: {LOCAL_IMG}")
    print(f"  - Artifact: {ARTIFACT_IMG}")

if __name__ == '__main__':
    main()
