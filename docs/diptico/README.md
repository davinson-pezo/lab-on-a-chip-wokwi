# 📱 Díptico Digital (Formato WhatsApp / Instagram Stories)

Este directorio contiene las dos páginas del díptico informativo para la clase práctica de hoy (17:00 a 18:00 h), optimizadas en formato vertical **9:16 ($1080 \times 1920\text{ px}$)** para difusión inmediata por estados de WhatsApp y redes sociales.

---

## 🖼️ Páginas del Díptico

### 1. Página 1 (Story 1) - Portada Visual & Gancho
* **Archivo:** [`diptico_whatsapp_story_01.jpg`](diptico_whatsapp_story_01.jpg)
* **Contenido:**
  * Fotografía real de laboratorio a sangre completa (*full-bleed*) mostrando al investigador cableando la protoboard junto a la placa Arduino Uno, la bomba de jeringa y el ordenador portátil.
  * Título de alto impacto: **LAB-ON-A-CHIP & MICRO-HPLC CON ARDUINO**.
  * Subtítulo: *Instrumental Científico de Precisión por < 80 €*.
  * Píldoras clave: `Simulación en Wokwi`, `Salto a Hardware Real`, `100% Práctico`.
  * Llamada a la acción: *¡Trae tu portátil! • Acceso libre en vivo*.

### 2. Página 2 (Story 2) - Agenda & Kit Maker de Amazon
* **Archivo:** [`diptico_whatsapp_story_02.jpg`](diptico_whatsapp_story_02.jpg)
* **Contenido:**
  * Tipografía de gran tamaño y alto contraste, legible al instante en cualquier pantalla móvil.
  * **Agenda en 4 pasos (60 min):**
    * **17:00:** *1. El Gemelo Digital* (química y sensores en Wokwi).
    * **17:15:** *2. Firmware & Motor* (bomba de jeringa y control de caudal en C++).
    * **17:30:** *3. Procesamiento DSP* (filtro en tiempo real y detección de picos).
    * **17:45:** *4. Salto al Hardware* (mismo código grabado en la placa real).
  * **Caja de Hardware (< 80 € en Amazon):** Arduino + Sensor Óptico + Motor + Jeringa (75 € DIY vs 30.000 € comercial).
  * **Entregables:** Simulador corriendo, código libre de bugs y guía de laboratorio.

---

## 🛠️ Regeneración de Imágenes

Para volver a generar o modificar el diseño de las dos imágenes:

```bash
python3 tools/generate_diptico_stories.py
```
Las imágenes se guardan automáticamente en esta carpeta.
