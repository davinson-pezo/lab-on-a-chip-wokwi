# Guía de Prácticas de Laboratorio: Micro-HPLC y Sistema FIA Virtual

**Asignatura:** Instrumentación Biomédica / Química Analítica Instrumental / Sistemas Embebidos y Bioelectrónica  
**Plataforma:** Simulador Wokwi + Microcontrolador Arduino Uno + Chip Custom C/WASM + Antigravity  
**Proyecto Wokwi:** [Wokwi Micro-HPLC Instrument](https://wokwi.com/projects/477384442337984513)  
**Versión del Firmware:** 2.0 (FSM No Bloqueante + DSP en Tiempo Real)

---

## 1. Objetivos de Aprendizaje

Al finalizar estas prácticas de laboratorio, el estudiante será capaz de:
1. **Comprender la instrumentación físico-química** detrás de un cromatógrafo de líquidos de alta resolución miniaturizado (*Lab-on-a-Chip* / FIA).
2. **Analizar la respuesta de un detector fotométrico UV-Vis** en presencia de dispersión molecular, deriva térmica y ruido estocástico gaussiano.
3. **Evaluar algoritmos de procesamiento digital de señales (DSP)** ejecutados en tiempo real sobre un microcontrolador de 8 bits (filtro EMA, seguimiento de línea base, detección de umbral de pendiente).
4. **Calcular parámetros de calidad cromatográfica fundamentales:** tiempos de retención ($t_R$), platos teóricos ($N$), altura de plato ($H$), factor de asimetría ($A_s$) y resolución ($R_s$).
5. **Realizar cuantificación analítica** mediante integración numérica trapezoidal de áreas bajo la curva.

---

## 2. Marco Teórico y Ecuaciones Fundamentales

### 2.1. Dinámica de Elución Cromatográfica
En un microcanal cromatográfico, una mezcla de analitos inyectada como un pulso de volumen finito se separa debido a la partición diferencial entre la fase móvil (líquido eluyente impulsado por la bomba de microjeringa) y la fase estacionaria funcionalizada en las paredes o lecho del chip.

La concentración de salida $C_i(t)$ para cada analito $i$ responde al modelo de difusión y convección expresado como una distribución gaussiana:

$$C_i(t) = \frac{M_i}{F \cdot \sigma_t \sqrt{2\pi}} \exp\left( -\frac{(t - t_{Ri})^2}{2\sigma_t^2} \right)$$

Donde:
- $t_{Ri}$: Tiempo de retención característico del analito $i$ [s].
- $\sigma_t$: Desviación estándar del pico en escala temporal [s].
- $M_i$: Masa total inyectada del compuesto [mol].
- $F$: Caudal volumétrico de la fase móvil [$\mu$L/min].

### 2.2. Detección Espectrofotométrica UV-Vis (Ley de Beer-Lambert)
El micro-detector óptico mide la transmitancia luminosa $T = I / I_0$ a través del canal óptico de longitud de paso $b$. La absorbancia $A(t)$ es proporcional a la concentración del soluto:

$$A(t) = -\log_{10}(T) = \varepsilon \cdot b \cdot C(t)$$

El transductor óptico (fotodiodo de silicio + amplificador de transimpedancia) convierte esta señal en una tensión eléctrica:

$$V_{det}(t) = V_{base} + \kappa \cdot A(t) + \eta(t)$$

Donde $V_{base} \approx 0.50\text{ V}$ representa la señal oscura/blanco del solvente, $\kappa$ es la sensibilidad del detector [$\text{V/UA}$], y $\eta(t) \sim \mathcal{N}(0, \sigma^2)$ representa el ruido electrónico blanco ($\sigma \approx 8\text{ mV}$).

### 2.3. Parámetros Cromatográficos Esenciales

| Parámetro | Ecuación | Interpretación Física |
| :--- | :--- | :--- |
| **Tiempo de Retención ($t_R$)** | Registro temporal del ápice | Tiempo que tarda el analito en recorrer el chip desde la inyección hasta la celda de detección. |
| **Ancho en la Base ($W$)** | $W = t_{fin} - t_{inicio} \approx 4\sigma$ | Dispersión hidrodinámica del frente del analito. |
| **Platos Teóricos ($N$)** | $N = 16 \left(\frac{t_R}{W}\right)^2$ | Medida de la eficiencia cinética de la microcolumna (capacidad de mantener picos estrechos). |
| **Altura Equivalente de Plato ($H$)** | $H = \frac{L}{N}$ | Longitud física de canal requerida para un equilibrio de partición ($L = 50\text{ mm}$). |
| **Resolución ($R_s$)** | $R_s = \frac{2(t_{R2} - t_{R1})}{W_1 + W_2}$ | Grado de separación entre dos bandas adyacentes ($R_s \ge 1.5$ indica separación completa a línea base). |
| **Área del Pico ($Area$)** | $Area = \int_{t_{ini}}^{t_{fin}} [V(t) - V_{base}] \, dt$ | Proporcional a la masa/concentración del compuesto eluido. |

---

## 3. Arquitectura del Banco de Pruebas Virtual

El sistema en Wokwi emula el flujo completo de un instrumento comercial de laboratorio:

```
[ PUSHBUTTONS ] ────> [ ARDUINO UNO R3 ] ────> [ DRIVER A4988 ] ──> [ MOTOR PASO A PASO ]
(START / CAL)            │      │                                    (Bomba HPLC)
                         │      └────────────> [ DISPLAY OLED ] ──> Visualización gráfica
                         │                     (SSD1306 I2C)        y parámetros DSP
                         │
                         ├─ Pin D4 (INJECT Pulse) ──> [ FLOW CELL DETECTOR ]
                         └─ Pin A0 (Analog Read)  <── (Custom Chip C/WASM)
```

1. **Bomba Micro-HPLC:** Motor paso a paso NEMA 17 gobernado por pulsos periódicos de temporizador no bloqueante en el pin `D3` (STEP) y `D2` (DIR).
2. **Inyector Automático:** Pulso lógico TTL en `D4` que conmuta la válvula y desencadena el proceso de inyección.
3. **Detector Microfluídico (Custom Chip `flow-cell-detector`):** Simula la física de transporte cromatográfico, eluyendo Teobromina ($t_{R1} \approx 12.0\text{ s}$) y Cafeína ($t_{R2} \approx 25.0\text{ s}$) con ruido Gaussiano.
4. **Adquisición y DSP:** Arduino muestrea el pin `A0` a $25\text{ Hz}$ estricto, aplica un filtro EMA con $\alpha = 0.20$, calibra dinámicamente la línea base e integra numéricamente el área.
5. **Interfaz de Usuario:** Pantalla OLED SSD1306 ($128 \times 64$) que despliega el cromatograma en tiempo real y la telemetría serie en formato CSV a $115200\text{ bps}$.

---

## 4. Guía de Ejecución de las Prácticas

### Práctica 1: Caracterización de la Línea Base y Estimación del Ruido (LOD y LOQ)

#### Objetivo
Determinar la estabilidad del instrumento antes de la inyección, calculando el ruido pico a pico ($V_{p-p}$), el ruido eficaz ($\mathrm{RMS}$) y los límites analíticos del sistema.

#### Procedimiento
1. Abra el proyecto en Wokwi y presione el botón de simulación (Play ▶).
2. En la consola serie aparecerá:
   ```
   [SYSTEM] Ready. Press START to begin chromatographic run.
   ```
3. Presione el pulsador **START** (verde). Observe la fase de calibración de línea base durante los primeros segundos ($t = 0$ a $t = 3\text{ s}$).
4. Tome una ventana de 25 muestras consecutivas de la columna `RAW_V` antes de que comience el pico (por ejemplo, entre $t = 1.0\text{ s}$ y $t = 2.0\text{ s}$).
5. Calcule en su cuaderno u hoja de cálculo:
   - **Tensión media de línea base:** $\bar{V}_{base} = \frac{1}{M}\sum_{i=1}^M V_i$
   - **Desviación estándar del ruido:** $s = \sqrt{\frac{1}{M-1}\sum_{i=1}^M (V_i - \bar{V}_{base})^2}$
   - **Ruido pico a pico ($V_{p-p}$):** $V_{\max} - V_{\min}$ dentro de la ventana en reposo.

#### Preguntas de Análisis
- ¿Coincide el valor calculado con la línea base reportada por el firmware ($V_{base} \approx 0.497\text{ V}$)?
- Sabiendo que el Límite de Detección ($LOD$) se define como $3 \cdot s$ y el Límite de Cuantificación ($LOQ$) como $10 \cdot s$, ¿cuál es el voltaje neto mínimo necesario para detectar inequívocamente un compuesto en este instrumento?

---

### Práctica 2: Identificación de Analitos y Evaluación de Platos Teóricos ($N$)

#### Objetivo
Identificar los dos compuestos presentes en la mezcla inyectada y evaluar la eficiencia de la columna cromatográfica virtual.

#### Procedimiento
1. Deje transcurrir la corrida cromatográfica completa ($35\text{ segundos}$).
2. Copie los datos emitidos por el puerto serie o examine el cromatograma experimental generado.
3. Para cada uno de los dos picos observados, registre:
   - Tiempo de retención del ápice ($t_R$).
   - Altura máxima neta: $H = V_{peak\_max} - V_{base}$.
   - Tiempo de inicio ($t_{ini}$) y tiempo de fin ($t_{fin}$) calculados al cruzar el umbral del detector ($\Delta V \ge 0.08\text{ V}$).
   - Ancho del pico en la base: $W = t_{fin} - t_{ini}$.
4. Calcule el número de platos teóricos $N$ para ambos analitos usando la fórmula:
   $$N = 16 \left( \frac{t_R}{W} \right)^2$$
5. Asumiendo una longitud de canal microfluídico $L = 5.0\text{ cm}$ ($50\text{ mm}$), calcule la altura equivalente de plato teórico ($HETP$ o $H$) en micrómetros ($\mu\text{m}$):
   $$H = \frac{L}{N}$$

#### Tabla de Resultados a Completar por el Estudiante

| Analito | $t_R$ experimental [s] | $H$ neta [V] | $W$ base [s] | Platos $N$ [calc.] | Platos $N$ [firmware] | $HETP$ [$\mu\text{m}$] |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Pico 1: Teobromina** | | | | | | |
| **Pico 2: Cafeína** | | | | | | |

#### Preguntas de Análisis
- ¿Por qué el Pico 2 (Cafeína) exhibe un mayor número de platos teóricos que el Pico 1 ($N_2 > N_1$)?
- Si aumentáramos la longitud del microcanal al doble ($L = 10.0\text{ cm}$) manteniendo constante la velocidad del eluyente, ¿qué ocurriría con $t_R$, con $N$ y con el ancho del pico $W$?

---

### Práctica 3: Cuantificación Analítica e Integración Numérica (Regla del Trapecio)

#### Objetivo
Implementar el algoritmo de integración numérica trapezoidal para determinar el área bajo la curva de absorción, comparando el cálculo manual/computacional con el valor computado en tiempo real por el firmware.

#### Fundamento Matemático
La absorbancia neta es $\Delta V(t) = V_{filt}(t) - V_{base}$. El área bajo el pico discretizado se aproxima mediante la regla del trapecio:

$$Area = \sum_{k=1}^{K-1} \frac{\Delta V(t_k) + \Delta V(t_{k+1})}{2} \cdot (t_{k+1} - t_k)$$

#### Procedimiento
1. Utilizando el registro de datos CSV generado en la corrida:
   - Para el **Pico 1** (desde $t \approx 9.14\text{ s}$ hasta $t \approx 14.68\text{ s}$).
   - Para el **Pico 2** (desde $t \approx 20.36\text{ s}$ hasta $t \approx 28.94\text{ s}$).
2. Aplique la fórmula del trapecio en una hoja de cálculo (Excel / Google Sheets) o mediante un script de Python.
3. Compare su área calculada con los valores reportados en la consola del firmware:
   - Firmware Pico 1: `Area = 4.798 V*s`
   - Firmware Pico 2: `Area = 9.637 V*s`
4. Calcule el porcentaje de error relativo:
   $$\% \text{Error} = \frac{|Area_{\text{alumno}} - Area_{\text{firmware}}|}{Area_{\text{firmware}}} \times 100$$

#### Preguntas de Análisis
- ¿Por qué la Cafeína tiene un área aproximadamente el doble que la Teobromina si ambas fueron inyectadas en la misma corrida? (Relacione esto con la absortividad molar $\varepsilon_{\lambda}$ a $272\text{ nm}$ y la concentración inyectada).
- Si un estudiante comete el error de integrar la señal cruda `RAW_V` en lugar de la señal filtrada `FILTERED_V`, ¿cómo se ve afectada la variabilidad del área resultante entre corridas sucesivas?

---

### Práctica 4: Resolución Cromatográfica y Criterio de Separación

#### Objetivo
Determinar si la separación obtenida en el microchip cumple con los estándares analíticos internacionales para cuantificación inequívoca.

#### Procedimiento
1. Utilizando los valores de $t_{R1}$, $t_{R2}$, $W_1$ y $W_2$ obtenidos en la Práctica 2, calcule la resolución cromatográfica $R_s$:
   $$R_s = \frac{2(t_{R2} - t_{R1})}{W_1 + W_2}$$
2. Evalúe el valor obtenido frente al criterio estándar:
   - $R_s < 1.0$: Picos fuertemente solapados; separación deficiente.
   - $1.0 \le R_s < 1.5$: Separación aceptable pero con leve cruce en la base.
   - $R_s \ge 1.5$: Separación cuantitativa completa a línea base (solapamiento $< 0.1\%$).
3. Compare el resultado con la resolución reportada en la telemetría final del sistema:
   ```
   [DSP] Resolution Rs = 1.83
   ```

#### Preguntas de Análisis
- Con un valor de $R_s = 1.83$, ¿es posible inyectar una muestra con mayor concentración sin riesgo de que los picos se interfieran mutuamente? Justifique su respuesta.
- Si el caudal de la bomba se duplicara mediante el driver A4988 (reduciendo el periodo de paso a la mitad), ¿aumentaría o disminuiría la resolución $R_s$? Explique con base en la ecuación de Van Deemter.

---

### Práctica 5: Efecto del Filtro Digital EMA en la Integridad de la Señal

#### Objetivo
Analizar el compromiso entre reducción de ruido y distorsión de la forma de onda al variar el factor de suavizado $\alpha$ del filtro exponencial.

#### Fundamento
El firmware implementa un filtro de media móvil exponencial de primer orden (EMA):

$$y[n] = \alpha \cdot x[n] + (1 - \alpha) \cdot y[n-1]$$

Donde $\alpha \in (0, 1]$. Si $\alpha \to 1$, no hay filtrado. Si $\alpha \to 0$, el filtrado es muy agresivo pero introduce retardo de fase y aplana el pico.

#### Actividad Práctica
1. Observe la comparativa gráfica entre `RAW_V` (puntos dispersos) y `FILTERED_V` (línea continua azul marina) en el cromatograma.
2. Identifique el retardo de fase temporal introducido por el filtro en el ápice de ambos picos.
3. Modifique en `sketch.ino` el valor de `#define EMA_ALPHA 0.20f` probando dos valores extremos:
   - Caso A: $\alpha = 0.80$ (filtro muy leve).
   - Caso B: $\alpha = 0.05$ (filtro hiper-suavizado).
4. Vuelva a ejecutar la simulación en Wokwi para cada caso y registre:
   - ¿Qué sucede con la detección del ápice? ¿Se desplaza en el tiempo?
   - ¿Se altera el área calculada o el número de platos teóricos $N$?

---

## 5. Formato de Entrega del Informe de Laboratorio

Cada equipo de estudiantes deberá entregar un informe técnico en formato PDF o Markdown que contenga las siguientes secciones:

1. **Carátula:** Nombres de los integrantes, fecha, asignatura y enlace a su bifurcación (*fork*) de Wokwi.
2. **Resumen Ejecutivo (Abstract):** Descripción breve (máx. 150 palabras) del sistema LOC emulado y los principales resultados analíticos obtenidos.
3. **Tablas de Datos Experimentales:** Valores tabulados de las Prácticas 1 a 4.
4. **Cromatograma Gráfico:** Gráfico exportado con la representación de las curvas `RAW_V`, `FILTERED_V`, línea base y áreas sombreadas (generado con `tools/plot_run.py` o software de su preferencia).
5. **Cálculos y Memoria Analítica:** Desarrollo paso a paso de $N$, $HETP$, $Area$ y $R_s$.
6. **Discusión y Respuestas al Cuestionario:** Análisis crítico de las preguntas planteadas en cada práctica.
7. **Conclusiones de Ingeniería:** Tres conclusiones concretas sobre el diseño del firmware, la estabilidad del sensor y las ventajas de la microfluídica digital.

---

## 6. Rúbrica de Calificación del Laboratorio

| Criterio | Ponderación | Nivel Excelente (5.0) | Nivel Bueno (4.0) | Nivel Aceptable (3.0) | Insuficiente (< 3.0) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Recolección y Tratamiento de Datos** | 20% | Datos completos, sin errores de formato, análisis de ruido y línea base riguroso. | Datos completos pero con ligeras inconsistencias en la selección de ventanas. | Datos parciales o errores en el cálculo de media y dispersión. | Datos inventados o sin registro experimental. |
| **Cálculos Cromatográficos ($t_R, N, R_s$)** | 25% | Todas las fórmulas aplicadas correctamente con unidades; discrepancias justificadas. | Cálculos correctos pero falta interpretación analítica o unidades físicas. | Errores en la determinación de $W$ o confusión en la fórmula de platos teóricos. | Cálculos erróneos o ausentes. |
| **Integración Numérica y Cuantificación** | 25% | Regla del trapecio programada con exactitud; error respecto al firmware $< 2\%$. | Integración correcta con error $< 5\%$; explicación elemental. | Integración con errores de intervalo o sin restar la línea base. | No realiza la integración numérica. |
| **Análisis Crítico y Preguntas Teóricas** | 20% | Respuestas fundamentadas en principios de transferencia de masa, óptica y DSP. | Respuestas correctas pero basadas únicamente en intuición cualitativa. | Respuestas superficiales o con errores conceptuales en instrumentación. | Preguntas sin responder o con plagio. |
| **Presentación y Calidad del Informe** | 10% | Gráficos con calidad de publicación, redacción técnica impecable y estructura formal. | Buen formato pero figuras con etiquetas incompletas o baja resolución. | Formato descuidado, figuras borrosas o sin leyendas. | Presentación deficiente o fuera de plazo. |
