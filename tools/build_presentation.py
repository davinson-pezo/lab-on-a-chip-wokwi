#!/usr/bin/env python3
"""
tools/build_presentation.py
Assembles the complete 16:9 PowerPoint presentation (.pptx)
with embedded custom slide images and full speaker notes.
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def build_presentation():
    slides_dir = "docs/slides"
    os.makedirs(slides_dir, exist_ok=True)

    # Map of images in docs/slides
    local_images = {}
    for num in range(1, 13):
        jpg_path = os.path.join(slides_dir, f"slide_{num:02d}.jpg")
        png_path = os.path.join(slides_dir, f"slide_{num:02d}.png")
        if os.path.exists(jpg_path):
            local_images[num] = jpg_path
        elif os.path.exists(png_path):
            local_images[num] = png_path
        else:
            print(f"[WARN] No slide image found for slide {num}")

    # Slide metadata & notes
    slides_data = [
        {
            "num": 1,
            "title": "Lab-on-a-Chip (LOC) & Micro-HPLC Virtual",
            "subtitle": "Diseño, Simulación e Implementación de Instrumentación Analítica de Bajo Coste con Arduino Uno, Wokwi y Antigravity 2.0",
            "notes": (
                "BIENVENIDA Y PROPÓSITO:\n"
                "La instrumentación científica tradicional suele ser una 'caja negra' inaccesible para los alumnos por su alto coste.\n"
                "En esta sesión demostramos cómo, mediante la combinación de un simulador embebido en la nube (Wokwi), "
                "un copiloto de inteligencia artificial (Antigravity 2.0) y un Custom Chip en C/WASM, "
                "es posible diseñar y validar un cromatógrafo líquido completo antes de comprar un solo componente, "
                "pudiendo luego transferirlo a hardware físico por menos de 80 €."
            )
        },
        {
            "num": 2,
            "title": "La Problemática en la Enseñanza de Instrumentación Analítica",
            "subtitle": "¿Por qué los estudiantes no interactúan a fondo con cromatógrafos reales?",
            "notes": (
                "PUNTOS CLAVE PARA EL PONENTE:\n"
                "1. Barrera económica: Un HPLC comercial de grado analítico cuesta entre 20.000 € y 80.000 €. "
                "En la universidad, un solo equipo debe compartirse entre decenas de alumnos, limitándose a demostraciones pasivas.\n"
                "2. Miedo al error: Romper una cubeta de cuarzo o sobrepresionar una bomba de zafiro cuesta miles de euros.\n"
                "3. Simuladores clásicos: Tinkercad o Wokwi básico solo tienen potenciómetros y pulsadores; carecen de fluidos, "
                "cinética química o dispersión cromatográfica.\n"
                "4. La solución: Desarrollar un 'Gemelo Digital Físico-Químico' que modele la química real dentro del simulador."
            )
        },
        {
            "num": 3,
            "title": "El Ecosistema Tecnológico: Wokwi + Antigravity 2.0",
            "subtitle": "Plataforma de simulación de ciclo de reloj + Copiloto de IA de ingeniería",
            "notes": (
                "SINERGIA TECNOLÓGICA:\n"
                "- Wokwi: Emula fielmente el microcontrolador ATmega328P de Arduino Uno, driver A4988, buses I2C y SPI. "
                "Su gran ventaja competitiva es el soporte de Custom Chips en C compilados a WebAssembly (WASM).\n"
                "- Antigravity 2.0: Asiste al estudiante y al docente descomponiendo el desarrollo en 5 fases modulares, "
                "formulando las ecuaciones de transporte molecular, optimizando la máquina de estados finitos (FSM) no bloqueante "
                "y guiando el procesamiento digital de señales (DSP)."
            )
        },
        {
            "num": 4,
            "title": "Validación Virtual Integral: ¿Qué Podemos Simular?",
            "subtitle": "Prototipado completo sin gastar un solo céntimo en componentes físicos",
            "notes": (
                "LOS 5 DOMINIOS SIMULADOS:\n"
                "1. Mecatrónica y Fluidos: Trenes de pulsos precisos para el driver A4988 y motor NEMA 17 para caudal volumétrico estricto.\n"
                "2. Cinética Química: Dispersión en banda cromatográfica, tiempos de retención y ensanchamiento difusivo.\n"
                "3. Ruido Instrumental: Ruido blanco estocástico gaussiano (algoritmo Box-Muller, sigma = 8 mV) y deriva de línea base.\n"
                "4. DSP en Tiempo Real: Filtro recursivo EMA (alpha = 0.20), detección de umbral de pendiente e integración trapezoidal.\n"
                "5. HMI y Telemetría: Pantalla OLED SSD1306 fluida y tramas CSV hacia el puerto serie para análisis en Python/MATLAB."
            )
        },
        {
            "num": 5,
            "title": "Caso de Estudio: Micro-HPLC & Sistema FIA Virtual",
            "subtitle": "Arquitectura completa del instrumento diseñado en el proyecto",
            "notes": (
                "OBJETIVO ANALÍTICO:\n"
                "Separar y cuantificar una mezcla de dos xantinas naturales: Teobromina (tR ~ 12 s) y Cafeína (tR ~ 25 s).\n\n"
                "SUBSISTEMAS:\n"
                "- Bomba HPLC: NEMA 17 + Driver A4988 (D2 DIR, D3 STEP).\n"
                "- Válvula de Inyección: Pulso lógico TTL en Pin D4 (500 ms).\n"
                "- Detector Óptico: Custom Chip emulando celda UV-Vis a 272 nm en Pin A0 (0 a 5 V).\n"
                "- Controlador Central: Arduino Uno ejecutando FSM no bloqueante a 25 Hz.\n"
                "- HMI: OLED SSD1306 (I2C) y pulsadores START/CAL."
            )
        },
        {
            "num": 6,
            "title": "El Corazón del Simulador: Wokwi Custom Chip en C",
            "subtitle": "Modelado físico de transporte molecular en código C / WebAssembly",
            "notes": (
                "INGENIERÍA DEL CUSTOM CHIP:\n"
                "El chip corre código C nativo en el navegador mediante la API de Wokwi Chips.\n"
                "- Temporizador de precisión a 25 Hz (chip_timer_start).\n"
                "- Detección de flanco de inyección en pin INJ.\n"
                "- Perfil de elución gaussiano superpuesto con ruido estocástico Box-Muller.\n"
                "- Salida continua analógica vía pin_dac_write.\n"
                "Esto permite a los alumnos entender las leyes de transporte químico y programar simuladores por dentro."
            )
        },
        {
            "num": 7,
            "title": "Procesamiento Digital de Señales (DSP) y Validación Experimental",
            "subtitle": "Resultados de la corrida experimental real obtenida en Wokwi (35 s)",
            "notes": (
                "DATOS EXPERIMENTALES CLAVE:\n"
                "- Línea base calibrada: Vbase = 0.4976 V.\n"
                "- Filtro EMA (alpha = 0.20): Suprime el ruido blanco sin retrasar los ápices.\n"
                "- Pico 1 (Teobromina): tR1 = 12.18 s, H1 = 1.785 V, Área = 4.791 V*s, Platos N1 = 75.\n"
                "- Pico 2 (Cafeína): tR2 = 25.16 s, H2 = 2.405 V, Área = 9.637 V*s, Platos N2 = 136.\n"
                "- Resolución cromatográfica: Rs = 1.83 (>= 1.5, separación cuantitativa completa a línea base).\n"
                "La gráfica muestra los 2 paneles: señal completa arriba y absorbancia neta Delta V abajo."
            )
        },
        {
            "num": 8,
            "title": "La Guía de Prácticas de Laboratorio para los Alumnos",
            "subtitle": "Estructura pedagógica formal (docs/04_lab_manual.md)",
            "notes": (
                "CONTENIDO DE LAS 5 PRÁCTICAS:\n"
                "- Práctica 1: Estabilidad de línea base, ruido RMS y cálculo de LOD (3s) y LOQ (10s).\n"
                "- Práctica 2: Identificación de analitos, dispersión en banda y cálculo de platos teóricos N y HETP.\n"
                "- Práctica 3: Cuantificación analítica mediante regla del trapecio en Python/Excel vs. cálculo del firmware.\n"
                "- Práctica 4: Resolución cromatográfica Rs y optimización de caudal según Van Deemter.\n"
                "- Práctica 5: Sensibilidad del filtro EMA ante variaciones de alpha (0.05 a 0.80).\n"
                "Incluye cuestionario de 6 preguntas analíticas y plantilla formal de informe."
            )
        },
        {
            "num": 9,
            "title": "Del Gemelo Digital al Prototipo Físico Real",
            "subtitle": "¿Por qué la transición de Wokwi a hardware físico es 100% directa?",
            "notes": (
                "TRANSFERENCIA DIRECTA 1:1:\n"
                "1. El firmware sketch.ino es idéntico y se graba en el Arduino Uno real sin cambios.\n"
                "2. El cableado coincide pin a pin con diagram.json.\n"
                "3. Sustitución de componentes virtuales:\n"
                "   - Bomba virtual -> Motor NEMA 17 acoplado a husillo T8 empujando jeringa de 5 mL.\n"
                "   - Custom chip -> Fotodiodo OPT101 / TSL257 frente a LED UV/azul (405 nm) a través de capilar de teflón.\n"
                "4. Cero riesgo: el código ya está 100% verificado y libre de bugs antes de encender la fuente."
            )
        },
        {
            "num": 10,
            "title": "Lista de Materiales (BOM) y Presupuesto Real en Amazon",
            "subtitle": "Construyendo un equipo analítico completo por ~74,40 €",
            "notes": (
                "DESGLOSE DE COMPONENTES DISPONIBLES EN AMAZON (ENTREGA RÁPIDA):\n"
                "1. Arduino Uno R3 compatible: 9,50 €\n"
                "2. Pantalla OLED 0.96 I2C (128x64): 4,80 €\n"
                "3. Motor Paso a Paso NEMA 17 (1.5A): 12,50 €\n"
                "4. Driver A4988 con disipador: 2,90 €\n"
                "5. Sensor óptico OPT101 / TSL257: 6,50 €\n"
                "6. LED UV/Violeta 405 nm: 3,20 €\n"
                "7. Mecanismo de bomba jeringa T8 + varillas: 14,00 €\n"
                "8. Tubería capilar PTFE (2 m): 5,50 €\n"
                "9. Protoboard, cables y botones: 7,00 €\n"
                "10. Fuente 12V 2A DC: 8,50 €\n"
                "TOTAL ESTIMADO: ~74,40 € (frente a 25.000 € de un equipo comercial)."
            )
        },
        {
            "num": 11,
            "title": "Análisis Comparativo: HPLC Comercial vs. Sistema LOC DIY",
            "subtitle": "Democratización radical del instrumental científico",
            "notes": (
                "TABLA COMPARATIVA:\n"
                "- Coste: 25.000 €–80.000 € vs. 0 € (simulación) / 75 € (hardware).\n"
                "- Accesibilidad: 1 equipo para toda la clase vs. 1 gemelo digital por alumno en su portátil.\n"
                "- Transparencia: Software cerrado 'caja negra' vs. código abierto y transparente.\n"
                "- Mantenimiento: Muy costoso con servicio oficial vs. repuestos estándar de 5 € en Amazon.\n"
                "- Seguridad: Alta presión (>100 bar) vs. baja presión segura (<2 bar).\n"
                "El objetivo es la excelencia pedagógica y el aprendizaje activo de la instrumentación."
            )
        },
        {
            "num": 12,
            "title": "Conclusiones y Próximos Pasos",
            "subtitle": "Una nueva era en la enseñanza de bioelectrónica e instrumentación",
            "notes": (
                "RESUMEN Y LLAMADA A LA ACCIÓN:\n"
                "1. Demostramos que es viable simular sistemas físico-químicos complejos en Wokwi.\n"
                "2. La inteligencia artificial (Antigravity 2.0) actúa como multiplicador pedagógico.\n"
                "3. El proyecto está disponible en Wokwi para ser clonado y ejecutado en un clic:\n"
                "   https://wokwi.com/projects/477384442337984513\n"
                "4. Próxima evolución: Impresión 3D del chasis y migración a ESP32 para IoT Lab."
            )
        }
    ]

    # Create Presentation
    prs = Presentation()
    # 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide layout

    for item in slides_data:
        slide = prs.slides.add_slide(blank_layout)
        num = item["num"]

        # Insert high-resolution visual
        if num in local_images and os.path.exists(local_images[num]):
            img_path = local_images[num]
            # Embed image full-bleed 16:9
            slide.shapes.add_picture(img_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

        # Add speaker notes
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = f"{item['title']}\n{item['subtitle']}\n\n{item['notes']}"

    output_pptx = "docs/presentacion_loc_wokwi_antigravity.pptx"
    prs.save(output_pptx)
    print(f"[OK] Generated PowerPoint presentation: {output_pptx}")

if __name__ == "__main__":
    build_presentation()
