# Lab-on-a-Chip (LOC): Sistema Micro-Cromatográfico y FIA Virtual

## 1. Visión y Propósito Pedagógico

El objetivo de este proyecto es transformar una simulación convencional de microcontroladores en un **banco de pruebas de instrumentación analítica y bioingeniería**. 

Tradicionalmente, en simuladores como Wokwi o Proteus, los estudiantes se limitan a leer sensores comerciales preconfigurados o variar un potenciómetro a mano. En este proyecto se rompe esa barrera mediante la arquitectura **Híbrida Simulación-Emulación**:
- **Wokwi** simula la electrónica digital, actuadores mecatrónicos (motores paso a paso, servoválvulas, pantallas OLED y pulsadores) y la ejecución del microcontrolador (Arduino UNO / ESP32).
- Un **Wokwi Custom Chip en C** modela rigurosamente el fenómeno fisicoquímico (inyección de muestra, dispersión hidrodinámica, elución en columna cromatográfica con picos gaussianos y ruido estocástico).
- El **firmware embebido** implementa los algoritmos reales de la química analítica instrumental: temporización determinista, filtrado digital de señal, corrección de línea base, detección de picos en tiempo real, integración trapezoidal y cálculo de platos teóricos ($N$).
- Un **agente de IA (Antigravity)** asiste a los alumnos no escribiendo código a ciegas, sino respondiendo a una secuencia estructurada de prompts de ingeniería por fases.

---

## 2. Fundamentos de la Técnica: Micro-HPLC e Inyección en Flujo (FIA)

Un cromatógrafo líquido de alta resolución (HPLC) o un sistema FIA consta de cuatro subsistemas críticos:

```
 [ Reservorio Fase Móvil ] 
           │
           ▼
 [ Bomba de Flujo Continuo ] ──(Pulsos a frecuencia constante)
           │
           ▼
 [ Válvula de Inyección ]    ──(Bucle de muestra: Load / Inject)
           │
           ▼
 [ Columna de Separación ]   ──(Retención diferencial de analitos)
           │
           ▼
 [ Celda de Flujo UV-Vis ]   ──(Absorbancia según Ley de Beer-Lambert)
           │
           ▼
 [ Desecho / Fracciones ]
```

### 2.1. Dinámica del Detector UV-Vis y Ley de Beer-Lambert
La señal de absorbancia $A(t)$ registrada por el detector responde a:
$$A(t) = -\log_{10}\left(\frac{I(t)}{I_0}\right) = \varepsilon \cdot b \cdot C(t)$$
Donde:
- $I_0$: Intensidad óptica con fase móvil pura (línea base).
- $I(t)$: Intensidad transmitida al pasar la banda de analito.
- $\varepsilon$: Absortividad molar del analito a la longitud de onda de detección.
- $b$: Paso óptico de la celda de flujo (microcanal).
- $C(t)$: Concentración instantánea del analito en la celda.

En nuestro circuito, el amplificador de transimpedancia del detector entrega un voltaje analógico proporcional a la absorbancia:
$$V_{out}(t) = V_{base} + k \cdot A(t) + \eta(t)$$
Donde $V_{base} \approx 0.50\text{ V}$, $k$ es la ganancia del detector y $\eta(t)$ es el ruido de Johnson / térmico.

### 2.2. Ecuación del Cromatograma (Distribución Gaussiana)
Tras inyectar una mezcla binaria (por ejemplo, Cafeína y Teobromina), cada analito viaja a distinta velocidad relativa según su coeficiente de partición ($k'$). A la salida de la columna, el perfil de concentración $C(t)$ sigue una distribución normal:
$$C(t) = \sum_{i=1}^{M} A_i \cdot \exp\left( - \frac{(t - t_{Ri})^2}{2 \sigma_i^2} \right)$$
Donde:
- $t_{Ri}$: Tiempo de retención del analito $i$.
- $A_i$: Amplitud máxima del pico (proporcional a la concentración inyectada).
- $\sigma_i$: Desviación estándar del pico (relacionada con la dispersión en columna).
- $W_i = 4\sigma_i$: Ancho de base del pico.

### 2.3. Parámetros de Calidad Analítica
El firmware del microcontrolador calcula y reporta:
1. **Área del Pico ($S$):** Regla del trapecio numérica:
   $$S = \sum_{k=start}^{end} \frac{(V_k - V_{base}) + (V_{k+1} - V_{base})}{2} \cdot \Delta t$$
2. **Eficiencia de Columna (Número de Platos Teóricos $N$):**
   $$N = 16 \left( \frac{t_R}{W} \right)^2 \quad \text{o bien} \quad N = 5.54 \left( \frac{t_R}{W_{1/2}} \right)^2$$
3. **Resolución Cromatográfica ($R_s$):**
   $$R_s = \frac{2 (t_{R2} - t_{R1})}{W_1 + W_2}$$
   Una resolución $R_s \ge 1.5$ indica separación completa a línea base.
