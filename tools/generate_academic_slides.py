#!/usr/bin/env python3
"""
tools/generate_academic_slides.py
Generates clean, academic, publication-grade slide graphics in Spanish
with zero AI-neon/sci-fi glow, using matplotlib and PIL.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw

SLIDES_DIR = "docs/slides"
os.makedirs(SLIDES_DIR, exist_ok=True)

# -------------------------------------------------------------
# SLIDE 1: Cover Slide with Title in Spanish + Real Photo
# -------------------------------------------------------------
def make_slide_01():
    photo_path = "/Users/davinson/.gemini/antigravity/brain/8e12afaf-961a-4d0d-80bb-55cf3f84969f/slide_cover_academic_1791532367875.jpg"
    img = Image.open(photo_path).convert("RGBA")
    w, h = 1920, 1080
    img = img.resize((w, h), Image.Resampling.LANCZOS)

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    card_w, card_h = 1380, 260
    card_x, card_y = 50, 45
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=16,
        fill=(15, 23, 42, 225),
        outline=(59, 130, 246, 200),
        width=3
    )
    draw.rounded_rectangle([card_x + 35, card_y + 25, card_x + 360, card_y + 60], radius=8, fill=(30, 58, 138, 255))

    img = Image.alpha_composite(img, overlay)

    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    ax.imshow(img)
    ax.set_axis_off()

    ax.text(0.045, 0.908, "BIOELECTRÓNICA & QUÍMICA ANALÍTICA",
            fontsize=12, fontweight='bold', color='#93c5fd', transform=ax.transAxes)

    ax.text(0.045, 0.840, "Lab-on-a-Chip (LOC) & Micro-HPLC Virtual",
            fontsize=32, fontweight='bold', color='#ffffff', transform=ax.transAxes)

    ax.text(0.045, 0.785, "Diseño, Simulación e Implementación de Instrumentación Analítica de Bajo Coste\ncon Arduino Uno, Wokwi y Antigravity 2.0",
            fontsize=16, color='#cbd5e1', linespacing=1.35, transform=ax.transAxes)

    foot_box = dict(boxstyle='round,pad=0.6', facecolor='#0f172a', edgecolor='#475569', alpha=0.92, lw=1.5)
    ax.text(0.96, 0.05, "Proyecto de Instrumentación Científica Abierta • Prototipado Virtual a Hardware Físico",
            fontsize=12, color='#e2e8f0', ha='right', va='bottom', transform=ax.transAxes, bbox=foot_box)

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    out_file = os.path.join(SLIDES_DIR, "slide_01.jpg")
    plt.savefig(out_file, dpi=100, format='jpg')
    plt.close()
    print(f"[OK] Rendered academic Slide 1 -> {out_file}")


# -------------------------------------------------------------
# SLIDE 2: Problem Comparison (Real Photo + Academic Overlay)
# -------------------------------------------------------------
def make_slide_02():
    photo_path = "/Users/davinson/.gemini/antigravity/brain/8e12afaf-961a-4d0d-80bb-55cf3f84969f/slide_problem_academic_1791532390375.jpg"
    img = Image.open(photo_path).convert("RGBA")
    w, h = 1920, 1080
    img = img.resize((w, h), Image.Resampling.LANCZOS)

    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    ax.imshow(img)
    ax.set_axis_off()

    header_box = dict(boxstyle='square,pad=0.5', facecolor='#0f172a', edgecolor='none', alpha=0.92)
    ax.text(0.5, 0.955, "LA BRECHA EDUCATIVA EN QUÍMICA ANALÍTICA E INSTRUMENTACIÓN",
            fontsize=21, fontweight='bold', color='#ffffff', ha='center', va='top', transform=ax.transAxes, bbox=header_box)

    left_card = (
        "HPLC COMERCIAL TRADICIONAL\n"
        "───────────────────────────────\n"
        "• Coste: 25.000 € – 80.000 €\n"
        "• Acceso Restringido: Demostraciones pasivas\n"
        "• Riesgo: Miedo a averías en bombas de zafiro\n"
        "• 'Caja Negra': Software propietario cerrado"
    )
    ax.text(0.04, 0.15, left_card, fontsize=13, fontweight='bold', color='#fecaca', va='bottom',
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#450a0a', edgecolor='#dc2626', alpha=0.92, lw=2.0))

    right_card = (
        "GEMELO DIGITAL & PROTOTIPO DIY\n"
        "───────────────────────────────\n"
        "• Coste Simulación: 0,00 € (Navegador Web)\n"
        "• Prototipo Físico: < 80 € (Materiales accesibles)\n"
        "• Aprendizaje Activo: 1 equipo por estudiante\n"
        "• Transparencia: Código abierto en C/C++ y DSP"
    )
    ax.text(0.96, 0.15, right_card, fontsize=13, fontweight='bold', color='#bbf7d0', va='bottom', ha='right',
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#052e16', edgecolor='#16a34a', alpha=0.92, lw=2.0))

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    out_file = os.path.join(SLIDES_DIR, "slide_02.jpg")
    plt.savefig(out_file, dpi=100, format='jpg')
    plt.close()
    print(f"[OK] Rendered academic Slide 2 -> {out_file}")


# -------------------------------------------------------------
# SLIDE 3: Ecosystem (Wokwi + Antigravity 2.0) Architecture Diagram
# -------------------------------------------------------------
def make_slide_03():
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#f8fafc')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_axis_off()

    ax.text(50, 93, "EL ECOSISTEMA TECNOLÓGICO: WOKWI + ANTIGRAVITY 2.0",
            fontsize=24, fontweight='bold', color='#0f172a', ha='center')
    ax.text(50, 88.5, "Plataforma de Simulación Embebida Web + Copiloto de Inteligencia Artificial para Ingeniería",
            fontsize=15, color='#475569', ha='center')

    c1 = patches.FancyBboxPatch((4, 20), 20, 60, boxstyle="round,pad=1.2", facecolor='#ffffff', edgecolor='#94a3b8', lw=2)
    ax.add_patch(c1)
    ax.text(14, 75, "1. DOCENCIA &\nPROBLEMA ANALÍTICO", fontsize=14, fontweight='bold', color='#1e293b', ha='center')
    desc1 = (
        "• Separación de Teobromina\n  y Cafeína en microcanal.\n\n"
        "• Requisitos de bombeo:\n  Caudal continuo pulso a pulso.\n\n"
        "• Detección espectrofotométrica:\n  Muestreo a 25 Hz por ADC.\n\n"
        "• Criterio de calidad:\n  Resolución Rs >= 1.5."
    )
    ax.text(6, 64, desc1, fontsize=11.5, color='#334155', va='top', linespacing=1.35)

    c2 = patches.FancyBboxPatch((27, 20), 20, 60, boxstyle="round,pad=1.2", facecolor='#eff6ff', edgecolor='#3b82f6', lw=2.5)
    ax.add_patch(c2)
    ax.text(37, 75, "2. COPILOTO IA:\nANTIGRAVITY 2.0", fontsize=14, fontweight='bold', color='#1d4ed8', ha='center')
    desc2 = (
        "• Descomposición en 5 fases\n  de ingeniería modular.\n\n"
        "• Modelado de elución en C:\n  Distribución gaussiana.\n\n"
        "• Firmware no bloqueante:\n  Máquina de estados FSM.\n\n"
        "• Diseño DSP:\n  Filtro EMA e integrador."
    )
    ax.text(29, 64, desc2, fontsize=11.5, color='#1e3a8a', va='top', linespacing=1.35)

    c3 = patches.FancyBboxPatch((50, 20), 21, 60, boxstyle="round,pad=1.2", facecolor='#f0fdf4', edgecolor='#22c55e', lw=2.5)
    ax.add_patch(c3)
    ax.text(60.5, 75, "3. SIMULADOR WEB:\nWOKWI (WASM)", fontsize=14, fontweight='bold', color='#15803d', ha='center')
    desc3 = (
        "• Emulación de ciclo de reloj:\n  ATmega328P a 16 MHz.\n\n"
        "• Driver A4988 + NEMA 17:\n  Pulsos de paso reales.\n\n"
        "• Custom Chip en C/WASM:\n  Química sintética con ruido.\n\n"
        "• Cero instalación:\n  100% en navegador web."
    )
    ax.text(52, 64, desc3, fontsize=11.5, color='#14532d', va='top', linespacing=1.35)

    c4 = patches.FancyBboxPatch((74, 20), 22, 60, boxstyle="round,pad=1.2", facecolor='#fefce8', edgecolor='#eab308', lw=2)
    ax.add_patch(c4)
    ax.text(85, 75, "4. VALIDACIÓN &\nTELEMETRÍA EN VIVO", fontsize=14, fontweight='bold', color='#a16207', ha='center')
    desc4 = (
        "• Pantalla OLED SSD1306:\n  Cromatograma y métricas.\n\n"
        "• Telemetría Serie CSV:\n  115200 bps hacia Python.\n\n"
        "• Validación experimental:\n  N1=75, N2=136, Rs=1.83.\n\n"
        "• Transición a físico:\n  Firmware idéntico en placa."
    )
    ax.text(76, 64, desc4, fontsize=11.5, color='#713f12', va='top', linespacing=1.35)

    arrow_props = dict(arrowstyle="simple,tail_width=2.5,head_width=8,head_length=8", color='#475569')
    ax.annotate("", xy=(26.5, 50), xytext=(24.5, 50), arrowprops=arrow_props)
    ax.annotate("", xy=(49.5, 50), xytext=(47.5, 50), arrowprops=arrow_props)
    ax.annotate("", xy=(73.5, 50), xytext=(71.5, 50), arrowprops=arrow_props)

    summary_box = dict(boxstyle='round,pad=0.8', facecolor='#0f172a', edgecolor='#334155', lw=1.5)
    ax.text(50, 9, "Sinergia Clave: El alumno programa y valida el 100% del firmware y la física antes de comprar hardware",
            fontsize=13, fontweight='bold', color='#ffffff', ha='center', bbox=summary_box)

    plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
    out_file = os.path.join(SLIDES_DIR, "slide_03.jpg")
    plt.savefig(out_file, dpi=100, format='jpg')
    plt.close()
    print(f"[OK] Rendered academic Slide 3 -> {out_file}")


# -------------------------------------------------------------
# SLIDE 4: Simulation Domains (Clean Academic Layout)
# -------------------------------------------------------------
def make_slide_04():
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_axis_off()

    ax.text(50, 94, "¿QUÉ PODEMOS SIMULAR ANTES DE PASAR A HARDWARE FÍSICO?",
            fontsize=23, fontweight='bold', color='#0f172a', ha='center')
    ax.text(50, 89.5, "Los 5 Dominios Fundamentales de la Instrumentación Analítica Embebida",
            fontsize=15, color='#475569', ha='center')

    domains = [
        ("1. Mecatrónica",
         "• Pulsos A4988 deterministas\n• Micropasos sin jitter\n• Caudal continuo estricto\n• Control de presión jeringa\n• Prevención atascos de bomba",
         "#1e3a8a", "#eff6ff", 3.0),
        ("2. Fisicoquímica",
         "• Difusión y transporte canal\n• Elución de analitos (Gauss)\n• Retención: tR1=12s, tR2=25s\n• Ensanchamiento de picos (W)\n• Capacidad de carga en chip",
         "#065f46", "#ecfdf5", 22.5),
        ("3. Ruido Instrumental",
         "• Ruido blanco (Box-Muller 8mV)\n• Deriva térmica de línea base\n• Estimación real de S/N ratio\n• Cálculo riguroso LOD (3s)\n• Cálculo riguroso LOQ (10s)",
         "#701a75", "#fdf4ff", 42.0),
        ("4. DSP en Vivo",
         "• Filtro recursivo EMA (a=0.2)\n• Detección inicio/ápice/fin\n• Integración trapezoidal 25Hz\n• Cálculo de platos teóricos N\n• Resolución analítica Rs>=1.5",
         "#9a3412", "#fff7ed", 61.5),
        ("5. Interfaz HMI",
         "• Display gráfico OLED SSD1306\n• Máquina FSM no bloqueante\n• Pulsadores START/CAL activos\n• Trama serie CSV a 115200 bps\n• Integración con Python/PC",
         "#1f2937", "#f3f4f6", 81.0),
    ]

    for title, desc, border_col, fill_col, x_pos in domains:
        card = patches.FancyBboxPatch((x_pos, 16), 16.0, 68, boxstyle="round,pad=0.8",
                                      facecolor=fill_col, edgecolor=border_col, lw=2.2)
        ax.add_patch(card)
        ax.text(x_pos + 8.0, 78.5, title, fontsize=13.0, fontweight='bold', color=border_col, ha='center')
        ax.text(x_pos + 1.2, 71.0, desc, fontsize=11.0, color='#1e293b', va='top', linespacing=1.55)

    ax.text(50, 7.5, "Ventaja Crítica: Todos los errores de temporización, muestreo y cálculo se depuran virtualmente a coste cero",
            fontsize=13, fontweight='bold', color='#0f172a', ha='center',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#e2e8f0', edgecolor='#94a3b8', lw=1.2))

    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    out_file = os.path.join(SLIDES_DIR, "slide_04.jpg")
    plt.savefig(out_file, dpi=100, format='jpg')
    plt.close()
    print(f"[OK] Rendered academic Slide 4 -> {out_file}")


# -------------------------------------------------------------
# SLIDE 5: Refined Engineering Schematic Diagram
# -------------------------------------------------------------
def make_slide_05():
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_axis_off()

    ax.text(50, 94, "ARQUITECTURA DEL INSTRUMENTO VIRTUAL (MICRO-HPLC & FIA)",
            fontsize=23, fontweight='bold', color='#0f172a', ha='center')
    ax.text(50, 89.5, "Esquema Mecatrónico y Conexiones del Banco de Pruebas en Wokwi",
            fontsize=15, color='#475569', ha='center')

    # Top Fluidic Line (Left to Right flow)
    # 1. Bomba
    b_pump = patches.FancyBboxPatch((5, 52), 26, 28, boxstyle="round,pad=0.8", facecolor='#eff6ff', edgecolor='#2563eb', lw=2)
    ax.add_patch(b_pump)
    ax.text(18, 74, "BOMBA HPLC DE INFUSIÓN", fontsize=13, fontweight='bold', color='#1d4ed8', ha='center')
    ax.text(7, 68, "• Motor NEMA 17 (200 pasos/rev)\n• Driver A4988 (Paso / Dirección)\n• Control por Pin D2 (DIR) y D3 (STEP)\n• Caudal continuo sin vibraciones",
            fontsize=10.5, color='#1e293b', va='top', linespacing=1.3)

    # 2. Inyector
    b_inj = patches.FancyBboxPatch((37, 52), 26, 28, boxstyle="round,pad=0.8", facecolor='#fffbeb', edgecolor='#d97706', lw=2)
    ax.add_patch(b_inj)
    ax.text(50, 74, "VÁLVULA DE INYECCIÓN", fontsize=13, fontweight='bold', color='#b45309', ha='center')
    ax.text(39, 68, "• Inyector de bucle de muestra\n• Pulso lógico TTL de 500 ms\n• Control por Pin D4 (INJ)\n• Sincronización exacta con bombeo",
            fontsize=10.5, color='#1e293b', va='top', linespacing=1.3)

    # 3. Detector Chip
    b_det = patches.FancyBboxPatch((69, 52), 26, 28, boxstyle="round,pad=0.8", facecolor='#ecfdf5', edgecolor='#059669', lw=2)
    ax.add_patch(b_det)
    ax.text(82, 74, "CELDA DE FLUJO (CUSTOM CHIP)", fontsize=13, fontweight='bold', color='#047857', ha='center')
    ax.text(71, 68, "• Microcanal óptico en C/WASM\n• Elución Teobromina y Cafeína\n• Ruido Gaussiano (Box-Muller 8 mV)\n• Salida de Voltaje analógica a Pin A0",
            fontsize=10.5, color='#1e293b', va='top', linespacing=1.3)

    # Horizontal Fluidic Pipe Arrows (thin and clean)
    ax.annotate("", xy=(36.5, 66), xytext=(31.5, 66),
                arrowprops=dict(arrowstyle="->", lw=2.5, color='#0284c7'))
    ax.text(34, 68.5, "Fase Móvil", fontsize=10, fontweight='bold', color='#0284c7', ha='center')

    ax.annotate("", xy=(68.5, 66), xytext=(63.5, 66),
                arrowprops=dict(arrowstyle="->", lw=2.5, color='#0284c7'))
    ax.text(66, 68.5, "Muestra", fontsize=10, fontweight='bold', color='#0284c7', ha='center')

    # Bottom Control Unit (Arduino Uno)
    b_ard = patches.FancyBboxPatch((20, 14), 60, 28, boxstyle="round,pad=1.0", facecolor='#0f172a', edgecolor='#334155', lw=2.5)
    ax.add_patch(b_ard)
    ax.text(50, 36.5, "UNIDAD DE CONTROL: ARDUINO UNO R3 (ATmega328P @ 16 MHz)",
            fontsize=14, fontweight='bold', color='#ffffff', ha='center')

    ard_details = (
        "• FSM No Bloqueante a 25 Hz   • Filtro Digital Recursivo EMA (alpha = 0.20)\n"
        "• Integración Numérica Trapezoidal   • Detección Automática de Ápices y Platos N\n"
        "• Bus I2C (A4/A5) -> Display OLED SSD1306 (128x64)   • Salida Serie UART (115200 bps)\n"
        "• Entradas Digitales: Pulsador START (Pin D7) y Pulsador CAL (Pin D8)"
    )
    ax.text(50, 24, ard_details, fontsize=11, color='#94a3b8', ha='center', va='center', linespacing=1.4)

    # Vertical Control Bus Wires
    bus_kw = dict(arrowstyle="->", lw=2.0, color='#475569')
    ax.annotate("", xy=(18, 51.5), xytext=(28, 42.5), arrowprops=dict(connectionstyle="angle,angleA=0,angleB=90,rad=5", **bus_kw))
    ax.text(20, 46.5, "D2, D3 (STEP/DIR)", fontsize=9.5, fontweight='bold', color='#2563eb')

    ax.annotate("", xy=(50, 51.5), xytext=(50, 42.5), arrowprops=bus_kw)
    ax.text(51, 46.5, "D4 (INJ)", fontsize=9.5, fontweight='bold', color='#d97706')

    ax.annotate("", xy=(72, 42.5), xytext=(82, 51.5), arrowprops=dict(connectionstyle="angle,angleA=-90,angleB=180,rad=5", **bus_kw))
    ax.text(78, 46.5, "A0 (ADC 25 Hz)", fontsize=9.5, fontweight='bold', color='#059669')

    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    out_file = os.path.join(SLIDES_DIR, "slide_05.jpg")
    plt.savefig(out_file, dpi=100, format='jpg')
    plt.close()
    print(f"[OK] Rendered academic Slide 5 -> {out_file}")


# -------------------------------------------------------------
# SLIDE 6: Refined Custom Chip with Dark IDE Card
# -------------------------------------------------------------
def make_slide_06():
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor('#ffffff')

    fig.text(0.5, 0.94, "EL CORAZÓN DEL SIMULADOR: WOKWI CUSTOM CHIP EN C",
             fontsize=23, fontweight='bold', color='#0f172a', ha='center')
    fig.text(0.5, 0.895, "Modelado Físico-Químico en Lenguaje C Compilado a WebAssembly en el Navegador",
             fontsize=15, color='#475569', ha='center')

    # Left: Code Card
    ax_bg = fig.add_axes([0.04, 0.10, 0.45, 0.76])
    ax_bg.set_facecolor('#0f172a')
    ax_bg.set_axis_off()

    card = patches.FancyBboxPatch((0.0, 0.0), 1.0, 1.0, boxstyle="round,pad=0.02",
                                  facecolor='#0f172a', edgecolor='#334155', lw=2, transform=ax_bg.transAxes)
    ax_bg.add_patch(card)

    bar = patches.Rectangle((0.0, 0.92), 1.0, 0.08, facecolor='#1e293b', edgecolor='none', transform=ax_bg.transAxes)
    ax_bg.add_patch(bar)
    ax_bg.text(0.04, 0.96, "●  ●  ●   chips/flow_cell_detector/chip.c (C/WASM)", fontsize=11, fontweight='bold',
               color='#94a3b8', va='center', transform=ax_bg.transAxes)

    code_text = (
        "#include \"wokwi-api.h\"\n"
        "#include <math.h>\n\n"
        "// Parámetros Cromatográficos de Elución\n"
        "#define TR1  12.0f   // Teobromina (s)\n"
        "#define SIG1  1.2f   // Ancho pico 1\n"
        "#define AMP1  1.8f   // Altura pico 1 (V)\n"
        "#define TR2  25.0f   // Cafeína (s)\n"
        "#define SIG2  2.0f   // Ancho pico 2\n"
        "#define AMP2  2.4f   // Altura pico 2 (V)\n\n"
        "static float gaussian_elution(float t, float tr, float sig, float a) {\n"
        "    float dt = t - tr;\n"
        "    return a * expf(-(dt * dt) / (2.0f * sig * sig));\n"
        "}\n\n"
        "// Ruido Blanco Gaussiano (Algoritmo Box-Muller)\n"
        "static float box_muller_noise(float sigma) {\n"
        "    float u1 = ((float)rand() + 1.0f) / (RAND_MAX + 1.0f);\n"
        "    float u2 = ((float)rand() + 1.0f) / (RAND_MAX + 1.0f);\n"
        "    return sigma * sqrtf(-2.0f * logf(u1)) * cosf(2.0f * M_PI * u2);\n"
        "}\n\n"
        "// Callback del Temporizador Nativo a 25 Hz\n"
        "void chip_timer_callback(void *user_data) {\n"
        "    float v = V_BASE + v_drift + p1 + p2 + box_muller_noise(0.008f);\n"
        "    pin_dac_write(chip->pin_out, v); // Emisión analógica a A0\n"
        "}"
    )
    ax_bg.text(0.04, 0.88, code_text, fontsize=10.8, fontfamily='monospace', color='#38bdf8', va='top',
               linespacing=1.28, transform=ax_bg.transAxes)

    # Right: Plot
    ax_plot = fig.add_axes([0.53, 0.12, 0.43, 0.72])
    t = np.linspace(0, 35, 700)
    p1 = 1.8 * np.exp(-((t - 12.0)**2) / (2.0 * 1.2**2))
    p2 = 2.4 * np.exp(-((t - 25.0)**2) / (2.0 * 2.0**2))
    noise = np.random.normal(0, 0.008, len(t))
    v_total = 0.50 + p1 + p2 + noise

    ax_plot.plot(t, v_total, color='#1e3a8a', lw=1.8, label='Señal Sintetizada DAC Pin A0 ($V_{\\mathrm{total}}$)')
    ax_plot.plot(t, 0.50 + p1, color='#0284c7', ls='--', lw=1.5, label='Banda 1: Teobromina ($t_{R1} = 12$ s)')
    ax_plot.plot(t, 0.50 + p2, color='#ea580c', ls='--', lw=1.5, label='Banda 2: Cafeína ($t_{R2} = 25$ s)')
    ax_plot.axhline(0.50, color='#dc2626', ls=':', lw=1.2, label='Línea Base ($V_{\\mathrm{base}} = 0.50$ V)')

    ax_plot.set_title('Modelo Físico de Elución Superpuesta (Ecuación de Difusión)', fontsize=13, fontweight='bold', pad=10)
    ax_plot.set_xlabel('Tiempo de Corrida $t$ [s]', fontsize=11, fontweight='bold')
    ax_plot.set_ylabel('Tensión Analógica Generada [V]', fontsize=11, fontweight='bold')
    ax_plot.set_xlim(0, 35)
    ax_plot.set_ylim(0.40, 3.20)
    ax_plot.grid(True, linestyle=':', alpha=0.6)
    ax_plot.legend(loc='upper right', fontsize=10, framealpha=0.92)

    model_box = (
        "Ecuación Fenomenológica:\n"
        "$V(t) = V_{\\mathrm{base}} + \\Delta V_{\\mathrm{drift}} + \\sum A_i e^{-\\frac{(t - t_{Ri})^2}{2\\sigma_i^2}} + \\eta(t)$"
    )
    ax_plot.text(0.04, 0.93, model_box, transform=ax_plot.transAxes, verticalalignment='top',
                 fontsize=10.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#cbd5e1'))

    out_file = os.path.join(SLIDES_DIR, "slide_06.jpg")
    plt.savefig(out_file, dpi=100, format='jpg')
    plt.close()
    print(f"[OK] Rendered academic Slide 6 -> {out_file}")


# -------------------------------------------------------------
# SLIDE 8: Fix Header (Remove generic UNIVERSITY banner, replace with clean Spanish title)
# -------------------------------------------------------------
def make_slide_08():
    raw_path = "/Users/davinson/.gemini/antigravity/brain/8e12afaf-961a-4d0d-80bb-55cf3f84969f/slide_lab_practice_1791530834987.jpg"
    img = Image.open(raw_path).convert("RGB")
    w, h = 1920, 1080
    img = img.resize((w, h), Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 115], fill=(15, 23, 42))

    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    ax.imshow(img)
    ax.set_axis_off()

    ax.text(0.5, 0.955, "GUÍA DE PRÁCTICAS DE LABORATORIO: ANÁLISIS CROMATOGRÁFICO",
            fontsize=21, fontweight='bold', color='#ffffff', ha='center', va='center', transform=ax.transAxes)
    ax.text(0.5, 0.915, "Metodología Activa: 5 Prácticas Experimentales para los Estudiantes (docs/04_lab_manual.md)",
            fontsize=13, color='#94a3b8', ha='center', va='center', transform=ax.transAxes)

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    out_file = os.path.join(SLIDES_DIR, "slide_08.jpg")
    plt.savefig(out_file, dpi=100, format='jpg')
    plt.close()
    print(f"[OK] Rendered cleaned academic Slide 8 -> {out_file}")


# -------------------------------------------------------------
# SLIDE 11: Academic Comparison Table (Clean, Sober, Publication Grade)
# -------------------------------------------------------------
def make_slide_11():
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_axis_off()

    ax.text(50, 94, "ANÁLISIS COMPARATIVO: HPLC COMERCIAL vs. SISTEMA LOC DIY",
            fontsize=23, fontweight='bold', color='#0f172a', ha='center')
    ax.text(50, 89.5, "Democratización Radical del Instrumental Científico sin Renunciar al Rigor Metrológico",
            fontsize=15, color='#475569', ha='center')

    col_x = [4, 34, 67]
    col_w = [28, 31, 31]

    headers = [
        ("CRITERIO DE EVALUACIÓN", "#334155", "#f1f5f9"),
        ("HPLC COMERCIAL TRADICIONAL", "#b91c1c", "#fef2f2"),
        ("GEMELO DIGITAL WOKWI + ARDUINO", "#15803d", "#f0fdf4"),
    ]

    for i in range(3):
        title, tc, bg = headers[i]
        hb = patches.FancyBboxPatch((col_x[i], 78), col_w[i], 7, boxstyle="round,pad=0.5", facecolor=bg, edgecolor=tc, lw=2)
        ax.add_patch(hb)
        ax.text(col_x[i] + col_w[i]/2, 81.5, title, fontsize=13, fontweight='bold', color=tc, ha='center', va='center')

    rows = [
        ("Coste de Adquisición", "25.000 € – 80.000 €\n(Inalcanzable para cada alumno)", "0,00 € (Simulación Web)\n< 80 € (Prototipo físico completo)"),
        ("Disponibilidad en el Aula", "1 equipo compartido para 30 alumnos\n(Uso mayoritariamente demostrativo)", "1 simulador por estudiante en su PC\n(100% interactivo y práctico)"),
        ("Transparencia del Sistema", "Caja negra con software propietario\n(No se ve el código ni el transductor)", "Código abierto en C/C++ transparente\n(El alumno programa cada algoritmo)"),
        ("Mantenimiento y Repuestos", "Muy costoso, servicio técnico oficial\n(Sustitución de piezas por miles de €)", "Componentes estándar de Amazon / Maker\n(Repuestos económicos en 24h)"),
        ("Riesgo Operativo & Seguridad", "Alta presión (>100 bar) y solventes tóxicos\n(Riesgo alto de roturas caras)", "Baja presión (<2 bar), microvolúmenes\n(100% seguro para estudiantes)"),
        ("Curva de Aprendizaje", "Operador de software comercial\n(Poco entendimiento de metrología)", "Ingeniería de instrumentación real\n(Física + Mecatrónica + DSP en vivo)")
    ]

    y = 75
    row_h = 9.5
    for idx, (crit, hplc, loc) in enumerate(rows):
        y -= row_h
        bg_col = '#f8fafc' if idx % 2 == 0 else '#ffffff'

        b1 = patches.Rectangle((col_x[0], y), col_w[0], row_h - 1, facecolor=bg_col, edgecolor='#cbd5e1')
        ax.add_patch(b1)
        ax.text(col_x[0] + 1.5, y + (row_h-1)/2, crit, fontsize=11.5, fontweight='bold', color='#1e293b', va='center')

        b2 = patches.Rectangle((col_x[1], y), col_w[1], row_h - 1, facecolor=bg_col, edgecolor='#cbd5e1')
        ax.add_patch(b2)
        ax.text(col_x[1] + 1.5, y + (row_h-1)/2, hplc, fontsize=10.5, color='#991b1b', va='center', linespacing=1.2)

        b3 = patches.Rectangle((col_x[2], y), col_w[2], row_h - 1, facecolor=bg_col, edgecolor='#cbd5e1')
        ax.add_patch(b3)
        ax.text(col_x[2] + 1.5, y + (row_h-1)/2, loc, fontsize=10.5, fontweight='bold', color='#166534', va='center', linespacing=1.2)

    ax.text(50, 7.5, "Conclusión: El sistema abierto no sustituye el control de calidad farmacéutico, pero supera al comercial como herramienta pedagógica",
            fontsize=12.5, fontweight='bold', color='#0f172a', ha='center',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#f1f5f9', edgecolor='#94a3b8', lw=1.2))

    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    out_file = os.path.join(SLIDES_DIR, "slide_11.jpg")
    plt.savefig(out_file, dpi=100, format='jpg')
    plt.close()
    print(f"[OK] Rendered academic Slide 11 -> {out_file}")


# -------------------------------------------------------------
# SLIDE 12: Academic Conclusion & Next Steps
# -------------------------------------------------------------
def make_slide_12():
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_axis_off()

    ax.text(50, 94, "CONCLUSIONES Y PRÓXIMOS PASOS",
            fontsize=24, fontweight='bold', color='#0f172a', ha='center')
    ax.text(50, 89.5, "Una Nueva Metodología para la Enseñanza de la Bioelectrónica e Instrumentación Analítica",
            fontsize=15, color='#475569', ha='center')

    card_l = patches.FancyBboxPatch((5, 18), 45, 68, boxstyle="round,pad=1.2", facecolor='#f8fafc', edgecolor='#cbd5e1', lw=2)
    ax.add_patch(card_l)
    ax.text(27.5, 80, "HITOS ALCANZADOS EN EL PROYECTO", fontsize=15, fontweight='bold', color='#1e293b', ha='center')

    achievements = (
        "1. Gemelo Digital Operativo al 100%:\n"
        "   Simulación web completa en Wokwi sin coste inicial,\n"
        "   con química real modelada en C/WebAssembly.\n\n"
        "2. Firmware Determinista de Grado Industrial:\n"
        "   Máquina de estados FSM no bloqueante con muestreo a 25 Hz\n"
        "   y filtro digital EMA que elimina el ruido sin alterar el ápice.\n\n"
        "3. Validación Analítica Cuantitativa:\n"
        "   Separación completa de Teobromina y Cafeína con Rs = 1.83 (>= 1.5)\n"
        "   y eficiencia de columna calculada en tiempo real (N1=75, N2=136).\n\n"
        "4. Guía Pedagógica y Rúbrica de Evaluación:\n"
        "   Manual de 5 prácticas de laboratorio listas para docencia\n"
        "   universitaria y proyectos fin de grado (TFG/TFM)."
    )
    ax.text(8, 73, achievements, fontsize=12, color='#334155', va='top', linespacing=1.35)

    card_r = patches.FancyBboxPatch((53, 18), 42, 68, boxstyle="round,pad=1.2", facecolor='#f0fdf4', edgecolor='#22c55e', lw=2)
    ax.add_patch(card_r)
    ax.text(74, 80, "TRANSFERENCIA Y EVOLUCIÓN", fontsize=15, fontweight='bold', color='#15803d', ha='center')

    next_steps = (
        "• Fase Física (Montaje en Laboratorio):\n"
        "  - Impresión 3D del chasis para la bomba de infusión.\n"
        "  - Ensayos con colorantes alimentarios (Amarillo 5 y Azul 1)\n"
        "    y fotodiodo OPT101 con LED de 405 nm.\n\n"
        "• Expansión IoT & Telemetría en la Nube:\n"
        "  - Migración a ESP32 con servidor web integrado.\n"
        "  - Dashboard MQTT para monitorización remota en el aula.\n\n"
        "• Proyecto Disponible en Vivo en Wokwi:\n"
        "  https://wokwi.com/projects/477384442337984513\n"
        "  (Código y esquema listos para ejecutar con un solo clic)"
    )
    ax.text(56, 73, next_steps, fontsize=12, color='#14532d', va='top', linespacing=1.35)

    ax.text(50, 8.5, "Democratizando la Instrumentación Científica: De la Simulación Virtual al Laboratorio Real",
            fontsize=13, fontweight='bold', color='#ffffff', ha='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#0f172a', edgecolor='#334155', lw=1.5))

    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    out_file = os.path.join(SLIDES_DIR, "slide_12.jpg")
    plt.savefig(out_file, dpi=100, format='jpg')
    plt.close()
    print(f"[OK] Rendered academic Slide 12 -> {out_file}")

if __name__ == "__main__":
    make_slide_01()
    make_slide_02()
    make_slide_03()
    make_slide_04()
    make_slide_05()
    make_slide_06()
    make_slide_08()
    make_slide_11()
    make_slide_12()
