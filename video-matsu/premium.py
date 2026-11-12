# ชุดตั้งค่าหน้าตาตาม CI ของ MATSU สำหรับคลิปชุด 10 คลิป (Japanese Premium)
# - ใช้ร่วมกับ engine.py แต่ไม่แก้ค่าของคลิปขอนแก่น 3 คลิปเดิม
# - ฟอนต์ Kanit ทั้งหมด / ข้อความขาว คำเด่นทอง #FCD543 / พื้นดำเป็นฐาน ทองเป็นสีเน้น
# - ข้อความวางบนแถบดำโปร่งที่ค่อย ๆ จางออก (ไม่มีกรอบทึบ)
# - ฉากจบพื้นดำ MATSU สีทอง + "Make It Meaningful."
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import engine

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_BOLD = os.path.join(HERE, 'fonts', 'Kanit-ExtraBold.ttf')
FONT_SEMI = os.path.join(HERE, 'fonts', 'Kanit-SemiBold.ttf')
LOGO = os.path.join(HERE, 'logo', 'matsu-logo.png')   # วางไฟล์โลโก้จริงไว้ตรงนี้ (ถ้ามี)

GOLD = (252, 213, 67)          # #FCD543 สีหลักของ CI
GOLD_DEEP = (190, 145, 40)     # ทองเข้ม ใช้ไล่เฉดให้เหมือนโลโก้ทองบนพื้นดำ
WHITE = (255, 255, 255)
W, H = 1080, 1920

# โทนสีภาพ: อุ่นสีอำพัน เงามืดลึกกว่าคลิปขอนแก่น แต่สีอาหารยังธรรมชาติ
engine.TARGET_LUMA = 0.29
engine.TARGET_RG, engine.TARGET_BG = 1.38, 0.74


def _font(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)


def _spaced(draw, xy, text, font, fill, spacing):
    """วาดตัวอักษรแบบเว้นระยะกว้าง (ใช้กับคำภาษาอังกฤษเท่านั้น)"""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing


def _spaced_width(draw, text, font, spacing):
    return sum(draw.textlength(c, font=font) for c in text) + spacing * (len(text) - 1)


def caption(path, parts, size=66):
    """ข้อความ 1 บรรทัด  parts = [('ข้อความ', 'white'|'gold'), ...]  บนแถบดำโปร่งที่จางขอบบน-ล่าง"""
    f = _font(FONT_SEMI, size)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    widths = [tmp.textlength(t, font=f) for t, _ in parts]
    band = 260
    im = Image.new('RGBA', (W, band), (0, 0, 0, 0))
    a = np.sin(np.linspace(0, np.pi, band)) ** 1.5 * 120          # โปร่งที่ขอบ ทึบสุดตรงกลาง
    im.putalpha(Image.fromarray(np.repeat(a[:, None], W, 1).astype(np.uint8)))
    d = ImageDraw.Draw(im)
    x = (W - sum(widths)) / 2
    _, y0, _, y1 = f.getbbox('มาก')
    y = (band - (y1 - y0)) / 2 - y0
    for (t, c), w in zip(parts, widths):
        d.text((x, y), t, font=f, fill=GOLD if c == 'gold' else WHITE)
        x += w
    im.save(path)


def end_card(path):
    """ฉากจบ: พื้นดำ แสงอุ่นจาง ๆ ตรงกลาง  โลโก้ (หรือคำว่า MATSU ชั่วคราว) + Make It Meaningful."""
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.46) / H) ** 2)
    glow = np.clip(1 - r / 0.55, 0, 1) ** 2
    bg = np.stack([glow * 30, glow * 20, glow * 10], -1).astype(np.uint8)   # น้ำตาลเข้มไล่ไปดำ
    im = Image.fromarray(bg, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    cy = int(H * 0.44)
    if os.path.exists(LOGO):
        logo = Image.open(LOGO).convert('RGBA')
        logo.thumbnail((560, 560))
        im.alpha_composite(logo, ((W - logo.width) // 2, cy - logo.height // 2 - 40))
        bottom = cy + logo.height // 2 - 40
    else:
        # ยังไม่มีไฟล์โลโก้: พิมพ์ MATSU ตัวทองไล่เฉด เว้นระยะกว้างแบบโลโก้
        f = _font(FONT_SEMI, 150)
        sp = 38
        w = _spaced_width(d, 'MATSU', f, sp)
        _, y0, _, y1 = f.getbbox('MATSU')
        mask = Image.new('L', (W, H), 0)
        _spaced(ImageDraw.Draw(mask), ((W - w) / 2, cy - (y1 - y0) / 2 - y0), 'MATSU', f, 255, sp)
        t = np.linspace(0, 1, H)[:, None, None]
        g = (np.array(GOLD) * (1 - t) + np.array(GOLD_DEEP) * t)
        g = np.clip((g - np.array(GOLD)) * ((np.arange(H)[:, None, None] - (cy - 80)) / 160).clip(0, 1)
                    + np.array(GOLD), 0, 255)
        gold = Image.fromarray(np.broadcast_to(g, (H, W, 3)).astype(np.uint8), 'RGB').convert('RGBA')
        gold.putalpha(mask)
        im.alpha_composite(gold)
        bottom = cy + (y1 - y0) / 2
    # เส้นทองบาง ๆ + คำขวัญ
    ly = int(bottom + 70)
    d.rectangle([W // 2 - 60, ly, W // 2 + 60, ly + 2], fill=GOLD)
    f2 = _font(FONT_SEMI, 40)
    sp2 = 6
    w2 = _spaced_width(d, 'Make It Meaningful.', f2, sp2)
    _spaced(d, ((W - w2) / 2, ly + 50), 'Make It Meaningful.', f2, GOLD, sp2)
    im.convert('RGB').save(path)


if __name__ == '__main__':
    # ทำภาพตัวอย่างไว้ดูหน้าตา (ยังไม่ใช้ฟุตเทจจริง)
    out = os.path.join(HERE, 'preview')
    os.makedirs(out, exist_ok=True)
    caption(os.path.join(out, '_cap.png'), [('ทุกชิ้น ', 'white'), ('ผ่านมือเชฟ', 'gold')])
    end_card(os.path.join(out, 'premium_endcard.png'))

    # ภาพจำลองฉากมืดแสงอุ่น (แทนฟุตเทจ) + ข้อความ
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W * 0.55) / W) ** 2 + ((yy - H * 0.55) / H) ** 2)
    glow = np.clip(1 - r / 0.45, 0, 1) ** 1.6
    frame = np.stack([18 + glow * 190, 12 + glow * 110, 6 + glow * 45], -1).astype(np.uint8)
    fr = Image.fromarray(frame, 'RGB').convert('RGBA')
    cap = Image.open(os.path.join(out, '_cap.png'))
    fr.alpha_composite(cap, (0, int(H * 0.72)))
    fr.convert('RGB').save(os.path.join(out, 'premium_caption.png'))
    os.remove(os.path.join(out, '_cap.png'))

    # รวม 2 ภาพไว้ดูคู่กัน
    a = Image.open(os.path.join(out, 'premium_caption.png')).resize((540, 960))
    b = Image.open(os.path.join(out, 'premium_endcard.png')).resize((540, 960))
    both = Image.new('RGB', (1120, 960), (60, 60, 60))
    both.paste(a, (0, 0)); both.paste(b, (580, 0))
    both.save(os.path.join(out, 'premium_preview.png'))
    print('done', out)
