# ชุดหน้าตาสำหรับคลิปโปร MATSU Premium 999 NET (24–30 พ.ย. 69) — เลียนแบบโปสเตอร์โปรของร้าน
# ฉากจบ = ภาพอาหารด้านบน + ครึ่งล่างไล่เป็นดำ + โลโก้ทองมุมซ้ายบน + ข้อความโปร + บรรทัดสาขา / make it meaningful.
# ฟอนต์ Kanit ตัวบาง (Light/ExtraLight) ได้จากแพ็กเกจฟรี @fontsource/kanit (ไฟล์ .woff แยกชุดอักษรไทย/อังกฤษ)
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, 'fonts')
LOGO = os.path.join(HERE, 'logo', 'matsu-logo.png')
W, H = 1080, 1920
GOLD = (252, 213, 67)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)


def _fonts(weight, size):
    th = {200: 'kanit-thai-200-normal.woff', 300: 'kanit-thai-300-normal.woff', 400: 'kanit-thai-400-normal.woff',
          600: 'Kanit-SemiBold.ttf'}[weight]
    la = {200: 'kanit-latin-200-normal.woff', 300: 'kanit-latin-300-normal.woff', 400: 'kanit-latin-400-normal.woff',
          600: 'Kanit-SemiBold.ttf'}[weight]
    mk = lambda f: ImageFont.truetype(os.path.join(F, f), size, layout_engine=ImageFont.Layout.RAQM)
    return mk(th), mk(la)


def _runs(text):
    """แบ่งข้อความเป็นช่วงอักษรไทย / ไม่ใช่ไทย (ฟอนต์บางแยกไฟล์ตามชุดอักษร)"""
    out, cur, is_th = [], '', None
    for ch in text:
        t = '฀' <= ch <= '๿' or (ch == ' ' and is_th)
        if is_th is None or t == is_th:
            cur += ch
        else:
            out.append((cur, is_th)); cur = ch
        is_th = t
    if cur:
        out.append((cur, is_th))
    return out


def text(d, xy, s, weight, size, fill, anchor='l', spacing=0):
    """วาดข้อความผสมไทย/อังกฤษ  anchor: l = ชิดซ้าย, r = ชิดขวา  y = เส้นฐานบรรทัด"""
    th, la = _fonts(weight, size)
    runs = [(r, th if t else la) for r, t in _runs(s)]
    width = sum(d.textlength(r, font=f) for r, f in runs) + spacing * max(0, len(s) - 1)
    x, y = xy
    if anchor == 'r':
        x -= width
    for r, f in runs:
        if spacing:
            for ch in r:
                d.text((x, y), ch, font=f, fill=fill, anchor='ls'); x += d.textlength(ch, font=f) + spacing
        else:
            d.text((x, y), r, font=f, fill=fill, anchor='ls'); x += d.textlength(r, font=f)
    return width


def end_overlay(path, branch, headline=('คัดมาแล้ว', 'ทุกคำ')):
    """ภาพโปร่งใส 1080x1920 วางทับวิดีโอช่วงท้าย (เหมือนครึ่งล่างของโปสเตอร์)"""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # ไล่สีดำจากกลางจอลงล่าง
    y = np.arange(H)[:, None]
    a = np.clip((y - H * 0.30) / (H * 0.28), 0, 1) ** 1.2 * 245
    shade = np.zeros((H, W, 4), np.uint8); shade[..., 3] = np.repeat(a, W, 1).astype(np.uint8)
    im.alpha_composite(Image.fromarray(shade, 'RGBA'))
    # โลโก้มุมซ้ายบน
    if os.path.exists(LOGO):
        lg = Image.open(LOGO).convert('RGBA'); lg.thumbnail((150, 170))
        im.alpha_composite(lg, (64, 70))
    d = ImageDraw.Draw(im)
    L, R = 70, W - 70
    # เรียงบนลงล่าง (จอแนวตั้งแคบกว่าโปสเตอร์): หัวเรื่อง → ขีดทอง → 999 NET/ท่าน → รายละเอียด
    yb = 985
    for ln in headline:
        text(d, (L, yb), ln, 400, 92, WHITE); yb += 106
    d.rectangle([L, yb - 38, L + 70, yb - 35], fill=GOLD)
    text(d, (L, yb + 40), 'แพ็กเกจ PREMIUM MATSU', 400, 34, WHITE, spacing=1)
    w = text(d, (L - 8, yb + 330), '999', 200, 300, WHITE)
    text(d, (L + w + 24, yb + 330), 'NET / ท่าน', 400, 54, GOLD, spacing=2)
    text(d, (L, yb + 420), 'รวมเครื่องดื่มสำหรับสายปาร์ตี้', 400, 46, GOLD)
    text(d, (L, yb + 482), '24 – 30 พ.ย. 69 · ทานได้ 2 ชม.', 300, 38, WHITE)
    text(d, (L, yb + 534), 'ราคาสุทธิ ไม่บวกเพิ่ม · สำรองที่นั่งทาง Inbox', 300, 34, GREY)
    # เส้นคั่น + บรรทัดสาขา
    d.rectangle([L, 1782, R, 1783], fill=(255, 255, 255, 90))
    text(d, (L, 1852), f'MATSU {branch}', 400, 36, WHITE)
    text(d, (R, 1852), 'make it meaningful.', 300, 34, WHITE, 'r')
    im.save(path)


if __name__ == '__main__':
    import subprocess, sys
    src, ss = sys.argv[1], sys.argv[2]
    out = os.path.join(HERE, 'preview'); os.makedirs(out, exist_ok=True)
    bg = os.path.join(out, '_bg.png')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', ss, '-i', src, '-frames:v', '1',
                    '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920', bg], check=True)
    for br, name in [('อุบลราชธานี', 'ubon'), ('ขอนแก่น', 'khonkaen')]:
        ov = os.path.join(out, f'_ov_{name}.png'); end_overlay(ov, br)
        frame = Image.open(bg).convert('RGBA'); frame.alpha_composite(Image.open(ov))
        frame.convert('RGB').save(os.path.join(out, f'promo999_end_{name}.png')); os.remove(ov)
    os.remove(bg)
    print('ok')
