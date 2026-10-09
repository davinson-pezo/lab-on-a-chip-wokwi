# Presentación Técnica y Pedagógica: Lab-on-a-Chip (LOC) con Arduino Uno, Wokwi y Antigravity 2.0

**Formato:** Guión de Diapositivas (Texto Plano sin Maquetar)  
**Propósito:** Base para la creación de diapositivas en PowerPoint / Google Slides y definición de requerimientos de imágenes ilustrativas.  
**Relación de Aspecto Objetivo:** 16:9 (Panorámica Widescreen, 1920 × 1080 px).

---

## Índice General de la Presentación

1. **Slide 1:** Portada — Democratización de la Instrumentación Científica con LOC, Wokwi y Antigravity 2.0
2. **Slide 2:** La Brecha Educativa — El Desafío de Enseñar HPLC e Instrumentación Analítica
3. **Slide 3:** El Ecosistema Virtual — Wokwi + Antigravity 2.0 como Gemelo Digital
4. **Slide 4:** ¿Qué Podemos Simular Antes de Tocar Hardware Físico?
5. **Slide 5:** Caso de Estudio — Micro-HPLC y Sistema FIA Virtual Desarrollado
6. **Slide 6:** El Corazón del Simulador — El Custom Chip Químico en C / WebAssembly
7. **Slide 7:** Procesamiento Digital de Señales (DSP) y Resultados Experimentales
8. **Slide 8:** La Práctica de Laboratorio para los Alumnos (Metodología Activa)
9. **Slide 9:** El Puente al Mundo Físico — De la Simulación a la Mesa de Laboratorio
10. **Slide 10:** Lista de Materiales y Presupuesto Real en Amazon (BOM de Bajo Coste)
11. **Slide 11:** Comparativa: Equipo Comercial ($25k) vs. Gemelo Digital + Prototipo DIY ($80)
12. **Slide 12:** Conclusiones y Próximos Pasos

---

## Desglose Diapositiva por Diapositiva

---

### SLIDE 1: Portada
* **Título Principal:** Lab-on-a-Chip (LOC) & Micro-HPLC Virtual
* **Subtítulo:** Diseño, Simulación e Implementación de Instrumentación Analítica de Bajo Coste con Arduino Uno, Wokwi y Antigravity 2.0
* **Audiencia Objetivo:** Estudiantes de Ingeniería Biomédica, Química Analítica, Bioelectrónica y Sistemas Embebidos.
* **Mensaje Clave:** Es posible diseñar, simular y validar instrumental científico de precisión sin coste inicial y transferirlo a hardware real por menos de 80 €.
* **Contenido en Viñetas:**
  - De la ecuación físico-química al firmware funcional.
  - Simulación de gemelos digitales mediante Custom Chips en WebAssembly.
  - Validación de algoritmos DSP en tiempo real antes de construir hardware.
  - Prototipo físico abierto, replicable y de bajo coste.
* **Notas para el Ponente:**
  - Dar la bienvenida destacando que la instrumentación científica tradicional suele ser una "caja negra" inaccesible para los alumnos.
  - Explicar cómo la combinación de simuladores web modernos y agentes de inteligencia artificial permite que cada estudiante diseñe su propio cromatógrafo funcional.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Render conceptual de un microchip de cristal fluídico con canales microscópicos iluminados en azul/cian fluorescente, interconectado visualmente con una placa Arduino Uno, un display OLED y un gráfico de pico cromatográfico en estilo futurista limpio.

---

### SLIDE 2: La Brecha Educativa — El Desafío de Enseñar Instrumentación
* **Título:** La Problemática en la Enseñanza de Instrumentación Analítica
* **Subtítulo:** ¿Por qué los estudiantes no interactúan a fondo con cromatógrafos reales?
* **Contenido en Viñetas:**
  - **Barrera de Coste:** Un cromatógrafo HPLC comercial cuesta entre 20.000 € y 80.000 €. Pocas universidades pueden asignar un equipo por estudiante.
  - **Miedo al Error:** El riesgo de romper celdas de flujo de cuarzo, quemar bombas de alta presión o saturar columnas costosas limita la experimentación libre.
  - **La Limitación de los Simuladores Convencionales:**
    - Simuladores como Tinkercad o Wokwi básico solo tienen componentes electrónicos estándar (pulsadores, potenciómetros, LEDs).
    - No existe el concepto de "inyección de muestra", "flujo de solvente", "deriva de línea base" ni "ruido gaussiano".
  - **La Solución:** Crear un *Gemelo Digital Físico-Químico* que emule la física real dentro del simulador.
* **Notas para el Ponente:**
  - Enfatizar que cuando un alumno usa un HPLC comercial, solo hace "click en Start" en un software propietario; no comprende qué ocurre a nivel de transductor, ruido, muestreo ni cálculo de integrales.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Comparativa visual dividida en dos: A la izquierda, un voluminoso y costoso equipo HPLC de laboratorio con un candado de "Acceso Restringido". A la derecha, un estudiante programando en su portátil con un entorno accesible de simulación y prototipado.

---

### SLIDE 3: El Ecosistema Virtual — Wokwi + Antigravity 2.0
* **Título:** El Ecosistema Tecnológico: Wokwi + Antigravity 2.0
* **Subtítulo:** Plataforma de simulación de nivel industrial + Copiloto de Inteligencia Artificial
* **Contenido en Viñetas:**
  - **¿Qué aporta Wokwi?:**
    - Simulación de ciclo de reloj preciso de microcontroladores (Arduino Uno / ATmega328P, ESP32, RP2040).
    - Periféricos reales: Driver de motores A4988, display OLED SSD1306, buses I2C y SPI.
    - **Capacidad Clave:** *Custom Chips en C* compilados a WebAssembly (WASM), permitiendo crear componentes virtuales a medida que interactúan con los pines del microcontrolador.
  - **¿Qué aporta Antigravity 2.0?:**
    - Guía de ingeniería paso a paso: descompone el problema en fases pedagógicas modulares.
    - Modelado de ecuaciones fenomenológicas (distribución gaussiana, difusión molecular).
    - Asistencia en programación no bloqueante (`millis()` / FSM) y filtros digitales (EMA).
    - Generación de scripts de análisis de datos y gráficos científicos automáticos.
* **Notas para el Ponente:**
  - Explicar la sinergia: Wokwi pone el motor de ejecución en el navegador y Antigravity actúa como el tutor de ingeniería que guía al alumno sin hacer el trabajo por él, sino planteándole las preguntas de diseño correctas.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Diagrama esquemático moderno que muestre la interacción bidireccional entre el usuario, el copiloto de IA (Antigravity 2.0) y la plataforma Wokwi en el navegador.

---

### SLIDE 4: ¿Qué Cosas Podemos Simular Antes de Pasar a Hardware Físico?
* **Título:** Validación Virtual Integral: ¿Qué Podemos Simular?
* **Subtítulo:** Prototipado completo sin gastar un solo céntimo en componentes físicos
* **Contenido en Viñetas:**
  - **1. Cinemática de Fluidos y Bombeo:**
    - Generación precisa de trenes de pulsos para drivers de motores paso a paso (A4988 + NEMA 17).
    - Control de caudal constante en $\mu\text{L/min}$ y prevención de bloqueos de CPU.
  - **2. Hidrodinámica y Cinética de Separación:**
    - Dispersión en banda cromatográfica, tiempos de retención ($t_R$) y ensanchamiento de picos.
  - **3. Fenómenos Instrumentales Reales:**
    - Ruido electrónico estocástico (ruido térmico Johnson-Nyquist modelado con Box-Muller).
    - Deriva lenta de línea base por calentamiento de la fuente de luz UV o variaciones de solvente.
  - **4. Procesamiento Digital de Señales (DSP) en Tiempo Real:**
    - Filtrado recursivo IIR/EMA, detección de umbrales dinámicos, cálculo del área trapezoidal en microcontrolador de 8 bits.
  - **5. Interfaz Hombre-Máquina (HMI) y Telemetría:**
    - Gráficos en display OLED I2C de 128x64 y transmisión de tramas CSV por UART a 115200 baudios.
* **Notas para el Ponente:**
  - Resaltar que en la simulación los estudiantes descubren los errores típicos de temporización (como usar `delay()` y perder pasos del motor o muestras del ADC) antes de quemar un driver o sobrepresionar una jeringa.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Infografía circular o en cuadrícula de 5 módulos destacando los 5 dominios simulados: Fluídica, Química, Electrónica, DSP y Firmware.

---

### SLIDE 5: Caso de Estudio — Micro-HPLC & Sistema FIA Virtual
* **Título:** Caso de Estudio: Micro-HPLC y Sistema FIA Virtual
* **Subtítulo:** Arquitectura mecatrónica y analítica desarrollada en el proyecto
* **Contenido en Viñetas:**
  - **Objetivo Analítico:** Separar y cuantificar una mezcla de dos xantinas naturales: **Teobromina** ($t_R \approx 12\text{ s}$) y **Cafeína** ($t_R \approx 25\text{ s}$).
  - **Subsistemas del Instrumento:**
    - **Bomba de Infusión:** Motor NEMA 17 controlado por driver A4988 (Pines D2 DIR, D3 STEP).
    - **Válvula de Inyección:** Disparo de pulso lógico en Pin D4 ($500\text{ ms}$) sincronizado con la bomba.
    - **Detector Microfluídico (Custom Chip):** Transductor óptico UV-Vis en Pin A0 ($0–5\text{ V}$).
    - **Controlador Central:** Arduino Uno R3 ejecutando una FSM no bloqueante de 6 estados.
    - **Interfaz de Usuario:** Pantalla OLED SSD1306 (I2C A4/A5), pulsadores START (D7) y CAL (D8), y LEDs de estado.
* **Notas para el Ponente:**
  - Mostrar la arquitectura completa del banco de pruebas en Wokwi. Indicar que el proyecto ya está corriendo en la URL pública de Wokwi y se puede clonar en un clic.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Diagrama de bloques sinóptico de alta definición con el cableado completo de Arduino, driver A4988, motor NEMA 17, Custom Chip y pantalla OLED.

---

### SLIDE 6: El Corazón del Simulador — El Custom Chip Químico en C
* **Título:** El Corazón del Simulador: Wokwi Custom Chip en C
* **Subtítulo:** Modelado físico de transporte molecular en código compilado a WebAssembly
* **Contenido en Viñetas:**
  - **El Reto Técnico:** Los simuladores no tienen entradas analógicas que varíen solas siguiendo leyes físicas.
  - **La Solución Implementada (`chips/flow_cell_detector/chip.c`):**
    - Temporizador nativo a $25\text{ Hz}$ (`chip_timer_start`).
    - Detección de flanco de inyección en pin digital `INJ`.
    - Generación de perfil de absorbancia gaussiano superpuesto:
      $$V(t) = V_{\text{base}} + \Delta V_{\text{drift}} + \sum A_i \exp\left(-\frac{(t - t_{Ri})^2}{2\sigma_i^2}\right) + \text{Ruido}$$
    - Algoritmo de Box-Muller para ruido pseudo-aleatorio de distribución normal ($\sigma = 8\text{ mV}$).
    - Salida de tensión continua mediante la API del DAC de Wokwi (`pin_dac_write`).
* **Notas para el Ponente:**
  - Destacar que los alumnos aprenden C puro interactuando directamente con el motor de Wokwi, entendiendo cómo se programa un simulador científico por dentro.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Fragmento de código C del chip resaltado con sintaxis elegante, acompañado de un gráfico ilustrativo mostrando la inyección, la dispersión gaussiana y la inyección de ruido estocástico.

---

### SLIDE 7: Procesamiento de Señal y Resultados Experimentales
* **Título:** Procesamiento Digital de Señales (DSP) y Validación Experimental
* **Subtítulo:** Datos reales obtenidos durante la corrida en Wokwi
* **Contenido en Viñetas:**
  - **Filtro Digital EMA ($\alpha = 0.20$):**
    $$y[n] = \alpha \cdot x[n] + (1 - \alpha) \cdot y[n-1]$$
    Elimina el ruido de alta frecuencia manteniendo la simetría y posición del ápice.
  - **Línea Base Dinámica:** Calibración automática en reposo ($V_{\text{base}} = 0.4976\text{ V}$).
  - **Cuantificación por Regla del Trapecio en Arduino:**
    - **Pico 1 (Teobromina):** $t_R = 12.18\text{ s}$ | Área $= 4.791\text{ V}\cdot\text{s}$ | $N = 75$ platos teóricos.
    - **Pico 2 (Cafeína):** $t_R = 25.16\text{ s}$ | Área $= 9.637\text{ V}\cdot\text{s}$ | $N = 136$ platos teóricos.
  - **Resolución Cromatográfica ($R_s$):**
    $$R_s = \frac{2(t_{R2} - t_{R1})}{W_1 + W_2} = 1.83 \ge 1.50 \quad \text{(Separación Cuantitativa a Línea Base)}$$
* **Notas para el Ponente:**
  - Explicar la importancia de obtener $R_s = 1.83$: significa que no hay solapamiento de picos y la muestra de cafeína y teobromina se puede cuantificar con precisión farmacéutica.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* El gráfico experimental generado en alta resolución (`docs/chromatogram_run.png`), mostrando ambos picos sombreados, los ápices anotados y la curva neta $\Delta V$.

---

### SLIDE 8: La Práctica de Laboratorio para los Alumnos
* **Título:** La Experiencia Práctica del Estudiante
* **Subtítulo:** Estructura de la guía de laboratorio (`docs/04_lab_manual.md`)
* **Contenido en Viñetas:**
  - **Práctica 1: Caracterización de Ruido y Límites Analíticos:**
    - Registro de señal en reposo, cálculo de media y dispersión ($s$), estimación de $LOD$ ($3s$) y $LOQ$ ($10s$).
  - **Práctica 2: Identificación y Platos Teóricos ($N$):**
    - Medición experimental de $t_R$ y ancho en la base $W$; cálculo de eficiencia de columna y $HETP$ para $L = 50\text{ mm}$.
  - **Práctica 3: Cuantificación e Integración Numérica:**
    - Implementación de la regla del trapecio en Python/Excel y comparación con el valor reportado por el firmware.
  - **Práctica 4: Resolución y Efecto del Caudal:**
    - Cálculo de $R_s$ y discusión teórica del comportamiento de la curva de Van Deemter ($H$ vs. $u$).
  - **Práctica 5: Sensibilidad del Filtro Digital:**
    - Modificación del parámetro $\alpha$ ($0.05$ vs. $0.80$) para evaluar distorsión de pico y retardo de fase.
* **Notas para el Ponente:**
  - Resaltar que el estudiante no es un mero espectador: tiene que tomar datos, procesar matrices en Python o Excel y contrastar la teoría física con las limitaciones reales del microcontrolador.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Composición visual mostrando la guía de laboratorio, fórmulas matemáticas clave ($N$, $R_s$, trapecio) y una captura de la pantalla OLED desplegando los resultados en vivo.

---

### SLIDE 9: El Puente al Mundo Físico — De Wokwi a la Mesa de Trabajo
* **Título:** Del Gemelo Digital al Prototipo Físico Real
* **Subtítulo:** ¿Por qué la transición de Wokwi a hardware físico es 100% directa?
* **Contenido en Viñetas:**
  - **Firmware Idéntico:** El archivo `sketch.ino` se compila directamente en el IDE de Arduino y se carga en la placa física sin cambiar una sola línea.
  - **Conexiones Idénticas:** La asignación de pines de `diagram.json` coincide exactamente con la placa física y la protoboard.
  - **Sustitución de la Parte Virtual por Sensores Reales:**
    - La bomba virtual se convierte en un motor NEMA 17 acoplado a un husillo roscado T8 que empuja una jeringa plástica de $5\text{ mL}$.
    - El Custom Chip se reemplaza por un fotodiodo integrado (OPT101 / TSL257) enfrentado a un LED UV o azul ($405\text{ nm}$) a través de un capilar de teflón o celda impresa en 3D.
  - **Cero Riesgo de Rotura:** Cuando el alumno conecta el hardware real, el código ya está 100% probado y depurado.
* **Notas para el Ponente:**
  - Explicar que este método se llama *Model-Based Design* o prototipado guiado por simulación, la misma metodología usada en la industria automotriz y aeroespacial.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Fotografía o render comparativo "Antes y Después": a la izquierda la simulación de Wokwi con sus cables virtuales de colores; a la derecha el montaje físico real en protoboard con la jeringa y el motor.

---

### SLIDE 10: Lista de Materiales y Presupuesto Real en Amazon (BOM)
* **Título:** Lista de Materiales (BOM) y Coste Real en Amazon
* **Subtítulo:** Construyendo un cromatógrafo funcional por menos de 80 € / $
* **Contenido en Viñetas (Tabla de Componentes):**
  - **1. Placa Arduino Uno R3 (o compatible ATmega328P):** ~9,50 €
  - **2. Pantalla OLED 0.96" I2C SSD1306 (128x64 px):** ~4,80 €
  - **3. Motor Paso a Paso NEMA 17 (1.5 A, 42x40 mm):** ~12,50 €
  - **4. Controlador Driver A4988 con disipador térmico:** ~2,90 €
  - **5. Sensor Óptico Fotodiodo + Amplificador (OPT101 o TSL257):** ~6,50 €
  - **6. LED de Detección UV/Violeta (405 nm / 275 nm alta potencia):** ~3,20 €
  - **7. Mecanismo de Bomba de Jeringa (Husillo T8 + varillas + piezas 3D):** ~14,00 €
  - **8. Tubo Capilar de Teflón PTFE (OD 1/16", ID 0.5 mm, 2 metros):** ~5,50 €
  - **9. Protoboard, cables jumper, pulsadores y LEDs:** ~7,00 €
  - **10. Fuente de Alimentación 12V 2A DC (Jack 5.5 mm):** ~8,50 €
  - **COSTE TOTAL DEL HARDWARE COMPLETO:** **~74,40 €** (IVA incluido)
* **Notas para el Ponente:**
  - Enfatizar que todos estos componentes están disponibles en Amazon con entrega rápida en 24-48 horas.
  - Aclarar que con una inversión inferior a la de un libro de texto universitario, un laboratorio puede dotar a cada equipo de estudiantes de un instrumento físico real.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Collage estilo "Unboxing / Kit de Componentes" con las fotografías reales de los 10 productos de Amazon, sus etiquetas de precio en euros/dólares y la suma total destacada en verde fosforescente.

---

### SLIDE 11: Comparativa: Cromatógrafo Comercial vs. Gemelo Digital + DIY
* **Título:** Análisis Comparativo: HPLC Comercial vs. Sistema LOC DIY
* **Subtítulo:** Democratización radical del instrumental científico
* **Contenido en Viñetas (Tabla Comparativa):**
  - **HPLC Comercial Tradicional:**
    - Coste: $25.000 – $80.000 €
    - Disponibilidad: 1 equipo compartido por 30 alumnos (o solo demostrativo).
    - Mantenimiento: Muy costoso, requiere servicio técnico autorizado.
    - Curva de Aprendizaje: Caja negra; software propietario.
    - Seguridad: Altas presiones (> 100 bar), riesgo de rotura de capilares.
  - **Sistema LOC con Wokwi + Arduino + Antigravity 2.0:**
    - Coste Simulación: **0,00 €** (100% gratuito en el navegador).
    - Coste Prototipo Físico: **~75 €**.
    - Disponibilidad: 1 simulador por estudiante en su propia casa o aula.
    - Mantenimiento: Componentes genéricos reemplazables de inmediato.
    - Curva de Aprendizaje: Transparente; el alumno programa cada línea de código.
    - Seguridad: Baja presión (< 2 bar), seguro para docencia universitaria y secundaria.
* **Notas para el Ponente:**
  - Subrayar que el objetivo no es reemplazar un HPLC de grado farmacéutico analítico para control de calidad hospitalario, sino enseñar los fundamentos de metrología, fluidos y DSP de manera activa e inolvidable.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Gráfico comparativo de radar o barras contrastando Coste, Accesibilidad, Flexibilidad de Aprendizaje y Comprensión del Sistema.

---

### SLIDE 12: Conclusiones y Futuro de la Educación en Bioingeniería
* **Título:** Conclusiones y Próximos Pasos
* **Subtítulo:** Una nueva era en la enseñanza de la bioelectrónica e instrumentación
* **Contenido en Viñetas:**
  - **Logros Alcanzados en el Proyecto:**
    1. Construcción de un gemelo digital completo con química simulada en C/WASM.
    2. Firmware no bloqueante de grado industrial para Arduino Uno con FSM y DSP en tiempo real.
    3. Validación analítica rigurosa: $R_s = 1.83$, $N = 75$ y $136$ platos teóricos.
    4. Guía de laboratorio estructurada y rúbrica pedagógica completa.
  - **El Papel de la Inteligencia Artificial (Antigravity 2.0):**
    - Acelera la formulación de modelos y la depuración del código sin eliminar el esfuerzo analítico del estudiante.
  - **Próximos Pasos Recomendados:**
    - Impresión 3D del chasis para la bomba de jeringa.
    - Pruebas con colorantes alimentarios reales (Amarillo 5 y Azul 1) en capilar transparente.
    - Integración de conectividad WiFi/Bluetooth con ESP32 para telemetría en la nube (IoT Lab).
* **Notas para el Ponente:**
  - Cerrar con una llamada a la acción motivadora: invitar a los profesores y alumnos a abrir el enlace de Wokwi, pulsar el botón START y experimentar por sí mismos.
* **Requerimiento de Imagen (Fase 2):**
  - *Dimensiones:* 1920 × 1080 (16:9).
  - *Concepto Visual:* Imagen inspiradora de cierre con el logo de Wokwi, Arduino y Antigravity, un código QR apuntando al proyecto en Wokwi y una frase de impacto sobre la democratización de la ciencia.

---
