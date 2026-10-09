# Guía de Prompts Pedagógicos para el Alumno (Trabajo con Antigravity / IA)

Esta guía contiene la secuencia estructurada de **prompts de ingeniería** que los estudiantes deben utilizar para guiar a Antigravity (o cualquier agente de IA) en el desarrollo guiado del instrumento cromatográfico.

> [!IMPORTANT]
> **Regla de oro para el alumno:** No solicites "hazme todo el proyecto". La ingeniería analítica se construye y valida por módulos independientes. Cada prompt corresponde a una fase de desarrollo, verificación y pruebas.

---

## Índice de Fases

1. [Fase 1: El Emulador Químico (Wokwi Custom Chip en C)](#fase-1-el-emulador-químico-wokwi-custom-chip-en-c)
2. [Fase 2: Conexión del Circuito y Diagrama Wokwi (`diagram.json`)](#fase-2-conexión-del-circuito-y-diagrama-wokwi-diagramjson)
3. [Fase 3: Mecatrónica y Máquina de Estados (Firmware Base)](#fase-3-mecatrónica-y-máquina-de-estados-firmware-base)
4. [Fase 4: Procesamiento Digital de Señal (DSP) e Integración de Picos](#fase-4-procesamiento-digital-de-señal-dsp-e-integración-de-picos)
5. [Fase 5: Interfaz OLED y Telemetría en Vivo (Python)](#fase-5-interfaz-oled-y-telemetría-en-vivo-python)

---

## Fase 1: El Emulador Químico (Wokwi Custom Chip en C)

### Prompt 1.1: Generación del Custom Chip Analógico
```text
Actúa como un ingeniero experto en microcontroladores y en la API C de Wokwi Custom Chips.
Necesito implementar un Custom Chip llamado "flow-cell-detector" que simule la salida de una celda de flujo UV-Vis de un micro-cromatógrafo.

Requisitos técnicos del chip:
1. Pines: VCC, GND, INJ (entrada digital), STEP (entrada digital de pulsos de bomba), AOUT (salida analógica DAC).
2. Cuando el pin INJ recibe un flanco de subida, se inicia el cronómetro de elución (t = 0 s).
3. Debe generar en el pin AOUT (mediante pin_dac_write):
   - Línea base constante de 0.50 V con ligera deriva (+0.001 V/s).
   - Ruido gaussiano estocástico con amplitud aproximada de ±8 mV.
   - Pico 1 (Analito A): centrado en tR1 = 12.0 s, amplitud de 1.8 V, desviación estándar sigma = 1.2 s.
   - Pico 2 (Analito B): centrado en tR2 = 25.0 s, amplitud de 2.4 V, desviación estándar sigma = 1.8 s.
4. Usa un timer periódico en Wokwi (timer_init, timer_start a 10 ms / 100 Hz) para actualizar suavemente el voltaje DAC.
5. Proporciona el archivo chip.json y chip.c completos y libres de advertencias de compilación.
```

### Prompt 1.2: Validación y Calibración del Modelo Físico
```text
Revisa el código C de chip.c generado para el Custom Chip.
¿Cómo podemos hacer que el tiempo de elución de los picos varíe de forma realista si la frecuencia de pulsos en el pin STEP disminuye (simulando que la bomba entrega menor caudal y por ende los analitos tardan más en eluir)?
Implementa un factor de escala de tiempo dependiente de la frecuencia media medida en el pin STEP.
```

---

## Fase 2: Conexión del Circuito y Diagrama Wokwi (`diagram.json`)

### Prompt 2.1: Diseño del Esquema de Conexiones
```text
Actúa como diseñador de hardware para Wokwi. Necesito el contenido completo de diagram.json para un sistema micro-cromatográfico basado en Arduino UNO.
Debe incluir:
- Arduino Uno (wokwi-arduino-uno).
- Driver de motor paso a paso A4988 (wokwi-a4988).
- Motor paso a paso NEMA 17 (wokwi-stepper-motor).
- Pantalla OLED SSD1306 128x64 I2C (wokwi-ssd1306).
- 2 Pulsadores (START en D2 y STOP en D3) con resistencias pull-up internas.
- 2 LEDs con resistencias de 220 ohm: LED RUN (Verde en D7) y LED BUSY (Amarillo en D8).
- El Custom Chip "chip-flow-cell-detector" conectado con INJ en D10, STEP en D5 y AOUT en A0.
Genera el archivo JSON con todas las partes y conexiones organizadas claramente.
```

---

## Fase 3: Mecatrónica y Máquina de Estados (Firmware Base)

### Prompt 3.1: Arquitectura de Software y Máquina de Estados
```text
Actúa como desarrollador de sistemas embebidos en C++ para Arduino.
Diseña el esqueleto del firmware con una Máquina de Estados Finita (FSM) no bloqueante utilizando millis() o micros(), sin usar delay().

Estados requeridos:
- STATE_IDLE: Espera a que el usuario pulse START.
- STATE_BASELINE_CAL: La bomba arranca a caudal nominal (pulsos en pin D5), y durante 3 segundos se promedian lecturas en A0 para fijar la línea base.
- STATE_INJECT: Conmuta la válvula D6, envía un pulso de 20 ms en D10 al Custom Chip y pasa a elución.
- STATE_ELUTION: Mantiene el flujo de la bomba, realiza muestreo del ADC a 25 Hz durante 35 segundos.
- STATE_REPORT: Detiene la bomba, muestra resumen en la pantalla y vuelve a IDLE.

Incluye la gestión de rebotes (debounce) para los pulsadores y el control no bloqueante del motor A4988.
```

---

## Fase 4: Procesamiento Digital de Señal (DSP) e Integración de Picos

### Prompt 4.1: Filtrado y Detección de Picos en Tiempo Real
```text
Actúa como especialista en instrumentación analítica y procesamiento de señales.
En el estado STATE_ELUTION, recibo lecturas analógicas del detector UV-Vis en el pin A0 cada 40 ms (25 Hz).
La señal contiene ruido térmico y una línea base que puede derivar.

Diseña una clase o módulo en C++ para Arduino que implemente:
1. Filtro Digital EMA (Exponential Moving Average): Y[k] = alpha * X[k] + (1 - alpha) * Y[k-1], con alpha ajustable.
2. Estimador de derivada de primer orden (pendiente dV/dt) con una ventana de 3 puntos para amortiguar ruido.
3. Detección automática de picos:
   - Detección de inicio de pico (cuando dV/dt supera un umbral positivo sostenido).
   - Detección de ápice (cuando dV/dt cruza por cero de positivo a negativo): registra tR y altura máxima H.
   - Detección de fin de pico (cuando la señal regresa al umbral de línea base y dV/dt se estabiliza).
4. Integración numérica del área del pico usando la Regla del Trapecio: Area += 0.5 * (V[k] + V[k-1] - 2 * V_base) * dt.
5. Cálculo analítico al finalizar el pico:
   - Ancho de base del pico W.
   - Número de platos teóricos N = 16 * (tR / W)^2.
   - Almacenar los datos de hasta 4 picos por corrida cromatográfica.
```

### Prompt 4.2: Cálculo de Resolución Cromatográfica ($R_s$)
```text
Una vez completada la corrida y detectados los dos picos principales, escribe la función que calcule:
- La resolución cromatográfica Rs = 2 * (tR2 - tR1) / (W1 + W2).
- Determina si la separación es cuantitativa (Rs >= 1.5) o si hay solapamiento.
- Emite un mensaje de diagnóstico por el puerto serie.
```

---

## Fase 5: Interfaz OLED y Telemetría en Vivo (Python)

### Prompt 5.1: Gráficos y Texto en Display OLED SSD1306
```text
Diseña el módulo de visualización para la pantalla OLED SSD1306 (128x64, librería Adafruit_SSD1306).
Durante la corrida (STATE_ELUTION), debe mostrar:
- Estado actual y tiempo transcurrido (ej. "RUN: 18.4s").
- Voltaje actual del detector y barra de nivel o mini-gráfico de tendencia.
- Cantidad de picos detectados hasta el momento.
Al finalizar (STATE_REPORT):
- Pantalla dividida con los resultados:
  P1: tR=12.1s, S=3.8 V·s, N=158
  P2: tR=25.2s, S=5.9 V·s, N=312
  Rs: 1.85 (Aceptable)
```

### Prompt 5.2: Script Python de Adquisición y Graficado en Vivo
```text
Actúa como desarrollador científico en Python.
Crea un script utilizando pyserial y matplotlib (o PyQtGraph) llamado serial_plotter.py.
El script debe:
1. Conectarse al puerto serie virtual de Wokwi o al Arduino físico a 115200 baudios.
2. Parsear el stream de datos transmitido en formato CSV:
   "TIEMPO_MS,VOLTAJE_RAW,VOLTAJE_FILTRADO,LINEA_BASE,ESTADO"
3. Dibujar en tiempo real:
   - El cromatograma dinámico (Voltaje vs Tiempo en segundos).
   - La línea base en color gris punteado.
   - Sombreado de color bajo el área de los picos cuando se detectan.
   - Cuadro de texto con tR, Área y Platos Teóricos N calculados en vivo.
4. Botón o comando para guardar el cromatograma en PDF/PNG y los datos numéricos en un archivo .csv.
```
