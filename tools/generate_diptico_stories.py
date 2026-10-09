#!/usr/bin/env python3
"""
tools/generate_diptico_stories.py
Generates a 2-page WhatsApp/Instagram Story diptych (1080 x 1920 px, 9:16)
for today's 17:00-18:00 h class, focused on Proposal 5 (Maker & Low-Cost Hardware < 80 €).
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFilter, ImageFont

DOCS_DIR = "docs"
os.makedirs(DOCS_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# STORY 1: Portada Visual Full-Bleed con Investigador y Arduino
# -------------------------------------------------------------------------
def make_story_01():
    w_target, h_target = 1080, 1920
    raw_path = os.path.join(DOCS_DIR, "researcher_crop_test.jpg")
    if not os.path.exists(raw_path):
        src_path = "/Users/davinson/.gemini/antigravity/brain/8e12afaf-961a-4d0d-80bb-55cf3f84969f/slide_problem_academic_1791532390375.jpg"
        src_im = Image.open(src_path)
        raw_im = src_im.crop((690, 0, 1376, 768))
        raw_im.save(raw_path, quality=95)
    else:
        raw_im = Image.open(raw_path)

    scale = h_target / raw_im.height
    new_w = int(raw_im.width * scale)
    im_scaled = raw_im.resize((new_w, h_target), Image.Resampling.LANCZOS)

    # Center crop around researcher and bench setup
    offset = int((new_w - w_target) * 0.38)
    base_img = im_scaled.crop((offset, 0, offset + w_target, h_target)).convert('RGBA')

    # Gradient overlays for text contrast
    overlay = Image.new('RGBA', (w_target, h_target), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Top gradient (ends right before researcher's hair)
    for y in range(480):
        alpha = int(230 * ((480 - y) / 480.0) ** 1.2)
        draw_ov.line([(0, y), (w_target, y)], fill=(11, 17, 32, alpha))

    # Bottom gradient
    for y in range(1550, 1920):
        alpha = int(220 * ((y - 1550) / 370.0) ** 1.3)
        draw_ov.line([(0, y), (w_target, y)], fill=(11, 17, 32, alpha))

    composite = Image.alpha_composite(base_img, overlay)
    draw = ImageDraw.Draw(composite)

    font_bold = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
    f_badge = ImageFont.truetype(font_bold, 27)
    f_title_main = ImageFont.truetype(font_bold, 74)
    f_title_sub = ImageFont.truetype(font_bold, 54)
    f_desc = ImageFont.truetype(font_bold, 31)
    f_pill = ImageFont.truetype(font_bold, 25)
    f_cta = ImageFont.truetype(font_bold, 33)

    def draw_centered_text(y, text, font, fill, shadow_fill=(0, 0, 0, 240), dy_shadow=3):
        bb = font.getbbox(text)
        tw = bb[2] - bb[0]
        tx = (w_target - tw) // 2
        if shadow_fill:
            draw.text((tx, y + dy_shadow), text, font=font, fill=shadow_fill)
        draw.text((tx, y), text, font=font, fill=fill)

    # Top Badge
    badge_text = 'CLASE EN VIVO  •  HOY 17:00 A 18:00 H'
    bbox = f_badge.getbbox(badge_text)
    bw = bbox[2] - bbox[0] + 54
    bh = 52
    bx = (w_target - bw) // 2
    by = 55

    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=26,
                           fill=(15, 23, 42, 220), outline=(56, 189, 248, 255), width=2)
    draw.ellipse([bx + 20, by + 18, bx + 36, by + 34], fill=(34, 197, 94, 255))
    draw.text((bx + 46, by + 11), badge_text, font=f_badge, fill=(255, 255, 255, 255))

    # Main Hook Titles
    draw_centered_text(130, 'LAB-ON-A-CHIP', f_title_main, (56, 189, 248, 255))
    draw_centered_text(215, '& MICRO-HPLC CON ARDUINO', f_title_sub, (255, 255, 255, 255))
    draw_centered_text(285, 'Instrumental Científico de Precisión por < 80 €', f_desc, (226, 232, 240, 255))

    # Subtle divider
    draw.line([(280, 338), (800, 338)], fill=(56, 189, 248, 220), width=3)

    # Bottom Pills
    pills = ['Simulación en Wokwi', 'Salto a Hardware Real', '100% Práctico']
    pill_w = 310
    gap = 20
    total_pills_w = 3 * pill_w + 2 * gap
    start_px = (w_target - total_pills_w) // 2
    py = 1680

    for i, ptext in enumerate(pills):
        px = start_px + i * (pill_w + gap)
        draw.rounded_rectangle([px, py, px + pill_w, py + 52], radius=16,
                               fill=(15, 23, 42, 220), outline=(56, 189, 248, 200), width=2)
        p_bb = f_pill.getbbox(ptext)
        p_tw = p_bb[2] - p_bb[0]
        draw.text((px + (pill_w - p_tw) // 2, py + 12), ptext, font=f_pill, fill=(241, 245, 249, 255))

    # Bottom CTA Bar
    cta_text = '¡TRAE TU PORTÁTIL! • ACCESO LIBRE EN VIVO'
    cta_w = 970
    cta_h = 78
    cta_x = (w_target - cta_w) // 2
    cta_y = 1765

    draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=24,
                           fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=2)
    cta_bb = f_cta.getbbox(cta_text)
    cta_tw = cta_bb[2] - cta_bb[0]
    draw.text((cta_x + (cta_w - cta_tw) // 2, cta_y + 20), cta_text, font=f_cta, fill=(15, 23, 42, 255))

    out_file = os.path.join(DOCS_DIR, "diptico_whatsapp_story_01.jpg")
    final_img = composite.convert('RGB')
    final_img.save(out_file, quality=95)
    print(f"[OK] Rendered Diptych Page 1 (Story 1) -> {out_file}")


# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# STORY 2: Agenda Minuto a Minuto y Qué vamos a aprender (Letras Grandes)
# -------------------------------------------------------------------------
def make_story_02():
    W, H = 1080, 1920
    img = Image.new('RGB', (W, H), (15, 23, 42)) # #0f172a
    draw = ImageDraw.Draw(img)

    font_bold = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'

    f_badge = ImageFont.truetype(font_bold, 28)
    f_main_title = ImageFont.truetype(font_bold, 58)
    f_sub_title = ImageFont.truetype(font_bold, 30)

    f_step_num = ImageFont.truetype(font_bold, 32)
    f_card_title = ImageFont.truetype(font_bold, 36)
    f_card_sub = ImageFont.truetype(font_bold, 27)

    f_kit_title = ImageFont.truetype(font_bold, 38)
    f_kit_sub = ImageFont.truetype(font_bold, 26)
    f_kit_note = ImageFont.truetype(font_bold, 24)

    f_cta = ImageFont.truetype(font_bold, 34)

    # 1. Header Badge
    badge_text = 'AGENDA EN VIVO  •  HOY 17:00 A 18:00 H'
    bb = f_badge.getbbox(badge_text)
    bw = bb[2] - bb[0] + 54
    bx = (W - bw) // 2
    by = 70
    draw.rounded_rectangle([bx, by, bx + bw, by + 54], radius=27,
                           fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    draw.ellipse([bx + 20, by + 19, bx + 36, by + 35], fill=(34, 197, 94))
    draw.text((bx + 46, by + 12), badge_text, font=f_badge, fill=(255, 255, 255))

    # 2. Main Title
    title_text = '¿QUÉ VAMOS A APRENDER?'
    t_bb = f_main_title.getbbox(title_text)
    t_w = t_bb[2] - t_bb[0]
    draw.text(((W - t_w) // 2, 155), title_text, font=f_main_title, fill=(255, 255, 255))

    sub_text = '4 Pasos Prácticos en 60 Minutos'
    s_bb = f_sub_title.getbbox(sub_text)
    s_w = s_bb[2] - s_bb[0]
    draw.text(((W - s_w) // 2, 230), sub_text, font=f_sub_title, fill=(56, 189, 248))

    # Divider line
    draw.line([(180, 285), (900, 285)], fill=(51, 65, 85), width=2)

    # 3. 4 Agenda Cards (Big, bold, readable)
    cards = [
        ('17:00', '1. EL GEMELO DIGITAL', 'Simula la química y los sensores en Wokwi',
         (56, 189, 248), (14, 43, 70), (2, 132, 199)),
        ('17:15', '2. FIRMWARE & MOTOR', 'Bomba de jeringa y control de caudal en C++',
         (52, 211, 153), (6, 55, 40), (16, 185, 129)),
        ('17:30', '3. PROCESAMIENTO DSP', 'Filtro en tiempo real y detección de picos',
         (251, 191, 36), (69, 26, 3), (217, 119, 6)),
        ('17:45', '4. SALTO AL HARDWARE', 'El mismo código grabado en tu placa real',
         (192, 132, 252), (46, 16, 80), (124, 58, 237))
    ]

    card_w = 940
    card_h = 160
    start_x = (W - card_w) // 2
    card_y = 320
    card_gap = 35

    for i, (time_tag, c_title, c_sub, col_accent, col_bg, col_border) in enumerate(cards):
        cy = card_y + i * (card_h + card_gap)
        draw.rounded_rectangle([start_x, cy, start_x + card_w, cy + card_h], radius=22,
                               fill=col_bg, outline=col_border, width=3)
        
        # Time pill on top left inside card
        t_pill_w = 145
        t_pill_h = 50
        draw.rounded_rectangle([start_x + 25, cy + 25, start_x + 25 + t_pill_w, cy + 25 + t_pill_h],
                               radius=14, fill=col_border)
        t_bb = f_step_num.getbbox(time_tag)
        t_w = t_bb[2] - t_bb[0]
        draw.text((start_x + 25 + (t_pill_w - t_w) // 2, cy + 31), time_tag, font=f_step_num, fill=(255, 255, 255))
        
        # Title
        draw.text((start_x + 195, cy + 30), c_title, font=f_card_title, fill=col_accent)
        
        # Subtitle / description
        draw.text((start_x + 35, cy + 98), c_sub, font=f_card_sub, fill=(226, 232, 240))

    # 4. Amazon Hardware Highlight Box
    hw_y = 1130
    hw_h = 240
    draw.rounded_rectangle([start_x, hw_y, start_x + card_w, hw_y + hw_h], radius=24,
                           fill=(30, 41, 59), outline=(148, 163, 184), width=2)

    hw_title = 'KIT HARDWARE MAKER: < 80 € EN AMAZON'
    h_bb = f_kit_title.getbbox(hw_title)
    h_w = h_bb[2] - h_bb[0]
    draw.text(((W - h_w) // 2, hw_y + 35), hw_title, font=f_kit_title, fill=(255, 255, 255))

    hw_sub = 'Arduino Uno + Sensor Óptico + Motor + Jeringa + Chasis 3D'
    hs_bb = f_kit_sub.getbbox(hw_sub)
    hs_w = hs_bb[2] - hs_bb[0]
    draw.text(((W - hs_w) // 2, hw_y + 105), hw_sub, font=f_kit_sub, fill=(56, 189, 248))

    hw_note = '¡Un HPLC comercial cuesta 30.000 €; tu equipo DIY cuesta 75 €!'
    hn_bb = f_kit_note.getbbox(hw_note)
    hn_w = hn_bb[2] - hn_bb[0]
    draw.text(((W - hn_w) // 2, hw_y + 165), hw_note, font=f_kit_note, fill=(203, 213, 225))

    # 5. What you take home banner
    deliv_y = 1420
    deliv_h = 240
    draw.rounded_rectangle([start_x, deliv_y, start_x + card_w, deliv_y + deliv_h], radius=24,
                           fill=(6, 78, 59), outline=(52, 211, 153), width=2)

    d_title = 'LO QUE TE LLEVAS PUESTO A LAS 18:00 H:'
    dt_bb = f_kit_title.getbbox(d_title)
    dt_w = dt_bb[2] - dt_bb[0]
    draw.text(((W - dt_w) // 2, deliv_y + 30), d_title, font=f_kit_title, fill=(52, 211, 153))

    points = [
        '• Tu simulador funcionando en tu propio navegador',
        '• Código C++ del firmware 100% probado y sin bugs',
        '• Guía completa con 5 prácticas de laboratorio'
    ]
    f_pt = ImageFont.truetype(font_bold, 28)
    for j, pt in enumerate(points):
        draw.text((start_x + 45, deliv_y + 90 + j * 45), pt, font=f_pt, fill=(255, 255, 255))

    # 6. Bottom CTA Button
    cta_text = '¡TRAE TU PORTÁTIL! • 100% PRÁCTICO'
    cta_h = 80
    cta_y = 1750
    draw.rounded_rectangle([start_x, cta_y, start_x + card_w, cta_y + cta_h], radius=24,
                           fill=(56, 189, 248), outline=(255, 255, 255), width=2)
    c_bb = f_cta.getbbox(cta_text)
    c_w = c_bb[2] - c_bb[0]
    draw.text(((W - c_w) // 2, cta_y + 20), cta_text, font=f_cta, fill=(15, 23, 42))

    out_file = os.path.join(DOCS_DIR, "diptico_whatsapp_story_02.jpg")
    img.save(out_file, quality=95)
    print(f"[OK] Rendered Diptych Page 2 (Story 2) -> {out_file}")

if __name__ == "__main__":
    make_story_01()
    make_story_02()
