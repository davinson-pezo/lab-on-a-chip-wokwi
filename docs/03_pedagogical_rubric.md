# Rúbrica Pedagógica y Criterios de Evaluación

## 1. Competencias y Resultados de Aprendizaje

Al completar este proyecto, el estudiante habrá demostrado competencia en:
1. **Instrumentación Científica y Bioelectrónica:** Comprensión de los subsistemas de un cromatógrafo (bombeo, inyección, columna, detección espectrofotométrica).
2. **Modelado Físico Virtual (Wokwi Custom Chips):** Capacidad de representar ecuaciones diferenciales o fenomenológicas en lenguaje C compilado a WebAssembly.
3. **Programación Concurrente y Determinista en Sistemas Embebidos:** Manejo de temporizadores, interrupciones y máquinas de estado no bloqueantes (`millis()` / `micros()`).
4. **Procesamiento Digital de Señales (DSP) en Tiempo Real:** Filtrado de ruido, seguimiento de deriva de línea base y algoritmos de discriminación de picos.
5. **Cálculo Numérico e Integración:** Implementación computacional de la regla del trapecio, cálculo de platos teóricos ($N$) y resolución cromatográfica ($R_s$).
6. **Interacción con Agentes de Inteligencia Artificial:** Capacidad de descomponer problemas complejos en prompts modulares de ingeniería en lugar de solicitar soluciones monolíticas.

---

## 2. Matriz de Evaluación (Rúbrica)

| Criterio | Excelente (90–100%) | Satisfactorio (70–89%) | En Desarrollo (<70%) |
| :--- | :--- | :--- | :--- |
| **1. Modelado del Custom Chip (C)** | El chip modela fielmente la superposición gaussiana, ruido realista, respuesta al pulso de inyección y deriva de línea base. Código en C limpio y eficiente. | El chip genera los picos pero el ruido es plano/nulo o la temporización no es exacta. | Picos con errores de cálculo o el chip causa inestabilidad en la simulación. |
| **2. Arquitectura de Firmware y FSM** | Código 100% no bloqueante, máquina de estados clara, temporización periódica estricta (25 Hz) para el ADC y pulsos limpios al A4988. | Uso de algún `delay()` menor que no destruye el flujo o transiciones de estado poco estructuradas. | Código bloqueante con `delay()`, pérdida de muestras o estados inconsistentes. |
| **3. Procesamiento de Señal y Filtro** | Filtro digital eficaz que elimina el ruido de alta frecuencia sin distorsionar el ápice ni retrasar excesivamente la señal. | Filtro funcional pero con retardo visible o atenuación excesiva del pico. | Señal cruda sin filtrar o filtro mal calibrado que altera el área analítica. |
| **4. Integración y Cálculo Analítico** | Detección automática precisa de inicio, ápice ($t_R$) y fin del pico. Área trapezoidal con error $< 3\%$. Cálculo correcto de $N$ y $R_s$. | Identifica picos pero el corte de línea base es impreciso o el cálculo de platos teóricos tiene errores de fórmula. | No detecta los picos de forma autónoma o el área calculada difiere fuertemente del valor teórico. |
| **5. Interfaz de Usuario y Telemetría** | Pantalla OLED fluida con información clara en cada estado. Telemetría CSV por puerto serie impecable e integrable en Python. | Pantalla informativa pero con parpadeo; telemetría serie funcional con formateo básico. | Pantalla bloqueante o sin datos analíticos en vivo. |
| **6. Uso Metodológico de la IA** | El alumno utilizó los prompts por fases, iteró sobre los resultados, detectó y corrigió fallos junto al agente. | El alumno siguió la guía pero aceptó código sin verificar límites físicos. | El alumno solicitó soluciones completas sin comprender la lógica interna. |
