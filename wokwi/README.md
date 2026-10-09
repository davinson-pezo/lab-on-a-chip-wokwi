# 🧪 Archivos del Simulador Wokwi (Guía para el Alumno)

Esta carpeta contiene **todos los archivos necesarios** para ejecutar el cromatógrafo virtual Micro-HPLC en **[Wokwi Web](https://wokwi.com)** o en **VS Code con la extensión Wokwi**.

---

## 📋 Correspondencia de Archivos con Wokwi Web

| Archivo Local | Pestaña / Nombre en Wokwi Web | Descripción |
| :--- | :--- | :--- |
| **`sketch.ino`** | `sketch.ino` | Firmware completo en C++ (FSM, control de motor, filtro EMA y cálculo de platos $N$ y resolución $R_s$). |
| **`diagram.json`** | `diagram.json` | Esquema de circuito: Arduino Uno, pantalla OLED SSD1306, driver A4988, motor NEMA 17, botones y detector. |
| **`libraries.txt`** | `libraries.txt` | Dependencias automáticas: `Adafruit SSD1306` y `Adafruit GFX Library`. |
| **`flow-cell-detector.chip.c`** | `flow-cell-detector.chip.c` *(Crear con `+`)* | Código fuente en C del Custom Chip químico (emula la elución de Teobromina y Cafeína y el ruido óptico). |
| **`flow-cell-detector.chip.json`** | `flow-cell-detector.chip.json` *(Crear con `+`)* | Definición de pines y metadatos del Custom Chip. |
| **`wokwi.toml`** | *(Solo para VS Code)* | Archivo de configuración si ejecutas Wokwi localmente en tu editor. |

---

## 🚀 Cómo Lanzar la Simulación en Wokwi Web (Paso a Paso)

1. **Crear nuevo proyecto:** Entra a [https://wokwi.com/projects/new/arduino-uno](https://wokwi.com/projects/new/arduino-uno).
2. **Pegar Firmware:** Abre la pestaña `sketch.ino` y reemplaza todo su contenido con el archivo [`sketch.ino`](file:///Users/davinson/Documents/Milton%20project/LOC/wokwi/sketch.ino).
3. **Pegar Circuito:** Ve a la pestaña `diagram.json` y reemplaza su contenido con el archivo [`diagram.json`](file:///Users/davinson/Documents/Milton%20project/LOC/wokwi/diagram.json).
4. **Agregar el Custom Chip Químico:**
   - Haz clic en la pestaña con el icono **`+`** (nuevo archivo).
   - Escribe exactamente el nombre: `flow-cell-detector.chip.json` y pega el contenido de [`flow-cell-detector.chip.json`](file:///Users/davinson/Documents/Milton%20project/LOC/wokwi/flow-cell-detector.chip.json).
   - Haz clic otra vez en **`+`**, escribe el nombre: `flow-cell-detector.chip.c` y pega el contenido de [`flow-cell-detector.chip.c`](file:///Users/davinson/Documents/Milton%20project/LOC/wokwi/flow-cell-detector.chip.c).
5. **Iniciar:** Pulsa el botón verde **Play (Iniciar Simulación)**.

---

## 🎮 Controles de la Simulación

* **Pulsador START (Pin D2, verde):** Inicia la calibración de línea base (3 s), activa la bomba de jeringa e inyecta la muestra.
* **Pulsador STOP (Pin D3, rojo):** Parada de emergencia inmediata.
* **Pantalla OLED:** Muestra el cromatograma en tiempo real, tiempo de retención ($t_R$), áreas y resolución ($R_s$).
* **Monitor Serie:** Emite la telemetría CSV a 115200 baudios para procesar con Python o Excel.
