# 06 — Estado del arte: ¿existe esta combinación?

**Fecha del barrido:** 9 de octubre de 2026
**Pregunta:** ¿existe en el mundo un instrumento analítico *simulado* (Arduino + Wokwi),
con la química modelada por un chip propio y un agente de IA pilotándolo, usado para
enseñar química analítica?

**Método:** búsqueda web con 14 consultas cruzadas (Wokwi × química/cromatografía,
MCP × instrumentación, gemelo digital × HPLC, Arduino × microfluídica × docencia),
más verificación por lectura directa de las tres fuentes más cercanas.

> ⚠️ **Límite del método:** esto es una búsqueda web, **no una revisión sistemática**.
> Sirve para situarse con honestidad, **no** para reclamar novedad en una publicación.

---

## 1. Veredicto

**No somos los primeros en el mundo.** Cada pieza por separado tiene precedente
publicado, y hay vecinos muy cercanos. **Pero la combinación concreta no aparece.**

Lo honesto y defendible: *"no es un invento sin precedentes; es un cruce poco frecuente,
en la frontera"* — puntero, no pionero absoluto.

---

## 2. Los cinco vecinos más cercanos

| # | Trabajo | Qué hace | Diferencia con el nuestro |
|---|---|---|---|
| 1 | **HPLC Training for All: AI Avatars in VR Digital Twin Laboratories** — UCL School of Pharmacy (ChemRxiv 2024, doi:10.26434/chemrxiv-2024-q511z) | Gemelo digital de un HPLC en **realidad virtual** + avatar de IA multilingüe que tutoriza a estudiantes. Motivación idéntica: el HPLC es caro y conceptualmente difícil. | La IA es un **tutor conversacional en VR**, no un agente que pilota el instrumento. No hay simulación de hardware ni firmware. |
| 2 | **Students' interactions with an AI assistant in a remote chemistry laboratory** — *Front. Educ.* 2025 (doi:10.3389/feduc.2025.1712743) | Asistente GPT-4o dentro de un laboratorio **remoto** de valoración ácido-base; hace de tutor, ayuda con cálculos y **redacta informes**. | Laboratorio **remoto con hardware real** (LabsLand). La IA asiste al alumno, no opera el instrumento. |
| 3 | **Wokwi CLI + servidor MCP** (Agentic Index, verificado 2026-10-08) | Un agente de IA arranca/para la simulación, lee y escribe la consola serie, lee pines, cambia controles de sensores, hace capturas y exporta el analizador lógico. | Su caso de uso documentado es **firmware embebido/IoT**, no instrumentación analítica. Nosotros usamos esa misma capacidad *para química*. |
| 4 | **Building an Arduino-Based Open-Source Programmable Multichannel Syringe Pump** — *J. Chem. Educ.* 2024 (doi:10.1021/acs.jchemed.4c00033) | Bomba de jeringa multicanales con Arduino, de bajo coste, para microfluídica y química de flujo en docencia. | **Hardware real**, sin simulación y sin IA. Nuestro proyecto usa el mismo concepto de bomba de jeringa, pero simulado. |
| 5 | **Simuladores de HPLC para docencia** — p. ej. *An Advanced, Interactive, HPLC Simulator* (*J. Chem. Educ.* 2013), *Practical HPLC Simulator* (UniGE), *Online HPLC Simulator* (Remote Labs), C-HPLC (2025) | Simulan cromatogramas y permiten variar parámetros (caudal, fase móvil, temperatura). | Son **apps a medida**: das parámetros y te devuelven el cromatograma. No hay hardware simulado, ni firmware, ni gemelo digital, ni agente. |

### Otras piezas que existen (contexto)
- **Wokwi en docencia**: extendido en electrónica/física/IoT. Investigación propia: *Utilization of Wokwi Technology as a Modern Electronics Learning Media* (2025), *Using WOKWI Simulator to Support Engineering Student Learning in Microcontrollers and Sensors* (2024).
- **Custom Chips de Wokwi** (API en C, beta): diseñados explícitamente para crear sensores y hardware propio. La comunidad modela **componentes electrónicos** (p. ej. un multiplexor CD4052B, chips I²C), no física química.
- **Arduino en química analítica**: campo maduro y publicado — HPLC open-source (*ChromatograDIY*), DAQ Arduino para cromatografía (*J. Chem. Educ.* 2021), colector de fracciones (*HardwareX* 2023), *Low-Cost and Open-Source Strategies for Chemical Separations* (2021). Todo con **hardware real**.
- **Microfluídica en docencia**: *"Learning on a chip": Microfluidics for formal and informal science education* (Rackus et al., *Biomicrofluidics* 2019); *Lab-on-a-Chip: Frontier Science in the Classroom* (*J. Chem. Educ.*).
- **Agentes de IA sobre instrumentos**: *Operating advanced scientific instruments with AI agents that learn on the job* (*Nature* 2026), ChemGraph (Argonne), MCP Design Strategies for AI Agents in Chemical Engineering (2025). Sobre instrumentos **reales** o simulación de proceso.
- **MCP para Arduino**: varios servidores MCP que conectan agentes a hardware Arduino (p. ej. `mixelpixx/Arduino-Agent`; Arduino App Lab 0.10 "Agentic Mode", agosto 2026).

---

## 3. Lo que NO se encontró

Ningún trabajo que reúna **las tres cosas a la vez**:

1. un instrumento analítico **simulado en el navegador** (Wokwi), sin hardware, con la
   **química modelada por un chip propio** (elución gaussiana, ruido, deriva de línea base);
2. **firmware real** con procesamiento de señal (filtrado, detección e integración de picos)
   que **es el mismo código que se graba luego en la placa física**;
3. un **agente de IA que pilota el instrumento por MCP** (pulsa START, lee la consola serie,
   valida el cromatograma y redacta el informe) en un contexto de **docencia de química analítica**.

---

## 4. Cómo posicionarlo sin exagerar

**Decir:** "gemelo digital de un cromatógrafo de bajo coste; puntero, no pionero".
**No decir:** "primero del mundo" (no sostenible con este barrido).

Lo genuinamente diferencial es la **tríada**:
1. **Simulación** → coste cero, sin reactivos, cualquiera desde su navegador.
2. **El mismo código va a la placa real** → a diferencia de un simulador didáctico al uso,
   las competencias transfieren al hardware (~80 € frente a ~30.000 € de un HPLC comercial).
3. **La IA como copiloto del instrumento**, no como chatbot de teoría: arranca, mide, valida y escribe.

---

## 5. Si se quiere reclamar novedad (trabajo pendiente)

Una afirmación de novedad exige, como mínimo:
- barrido sistemático en **Scopus / Web of Science** (no solo web);
- revisión dirigida de **J. Chem. Educ.**, **Education for Chemical Engineers**,
  **Analytical and Bioanalytical Chemistry**, **Journal of Chemical Education Research**;
- revisión de repositorios docentes (Remote Labs, LabsLand, PhET, Merlot);
- y comparación explícita con los cinco vecinos de la tabla anterior.

Mientras eso no esté hecho, en la clase y en el repositorio conviene usar
"**combinación poco frecuente / en la frontera**", no "primera del mundo".
