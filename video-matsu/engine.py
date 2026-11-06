# ส่วนกลางสำหรับตัดคลิป MATSU ทุกคลิป (render1.py / render2.py / render3.py เรียกใช้ไฟล์นี้)
# - ปรับแสงและสีของแต่ละช็อตอัตโนมัติให้เท่ากัน (วัดจากภาพจริงของช็อตนั้น)
# - ซูมเข้าช้า ๆ + ภาพจางสั้น ๆ ตอนเปลี่ยนฉาก
# - ข้อความทุกชิ้นเป็นแบบมีกรอบเหมือนกันหมด (ทำเป็นรูปด้วย Pillow ให้สระ/วรรณยุกต์ไทยถูกต้อง)
import glob, math, os, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = '/root/.claude/uploads/b982627e-a661-5c91-8e6b-77c2b9210699'
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_BIG = os.path.join(HERE, 'fonts', 'Kanit-ExtraBold.ttf')
FONT_SMALL = os.path.join(HERE, 'fonts', 'Kanit-SemiBold.ttf')
YELLOW, WHITE = '#fcd543', '#ffffff'
XF = 0.08                     # ภาพจางระหว่างช็อต (วินาที) — สั้นเพื่อไม่ให้เวียนหัว
BOX_ALPHA = 140               # ความทึบของกรอบดำ (0–255)
LABEL_Y = 0.20                # ข้อความกลางคลิป: ตำแหน่งจากด้านบน (สัดส่วนของจอ)
PANEL_Y = 1150                # ข้อความปิดท้าย: ตำแหน่งขอบบนของกรอบ (พิกเซล)

# เป้าหมายแสงและสี ที่ทุกช็อตจะถูกปรับเข้าหา
TARGET_LUMA = 0.33            # ความสว่างเฉลี่ย
TARGET_RG, TARGET_BG = 1.33, 0.78   # สมดุลสี (แดง/เขียว, น้ำเงิน/เขียว) — อุ่นแบบธรรมชาติ
PULL_LIGHT, PULL_COLOR = 0.8, 0.7   # ปรับเข้าหาเป้าหมายกี่ส่วน (1 = เท่ากันเป๊ะ)


def src(name):
    if name.startswith('IMG'):
        return glob.glob(f'{SRC}/*image.jpg')[0]
    return sorted(glob.glob(f'{SRC}/*{name}*'))[0]


def image_base(name, length):
    if name == 'IMG@pan':     # ภาพเต็มจอ เลื่อนจากซ้ายไปขวา (เร่งช้า-ผ่อนช้า)
        x0, x1 = 200 * 2.65, 1300 * 2.65
        return f"scale=-2:3840,crop=2160:3840:x='{x0}+({x1 - x0})*(1-cos(PI*t/{length}))/2':y=0,scale=1080:1920"
    return f'crop=815:1449:{int(name[4:])}:0,scale=1080:1920'


# ---------- ปรับแสงและสี ----------
def measure(name, ss, length):
    """อ่านภาพเล็ก ๆ ของช็อตนั้นมาวัดค่าแสงและสี"""
    if name.startswith('IMG'):
        inp = ['-loop', '1', '-t', '1', '-i', src(name)]
        vf = image_base(name, 1.0) + ',fps=4,scale=90:160'
    else:
        inp = ['-ss', f'{ss}', '-t', f'{length}', '-i', src(name)]
        vf = 'fps=4,scale=90:160'
    raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error'] + inp + ['-vf', vf, '-f', 'rawvideo',
                          '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 3).astype(float) / 255


def grade(name, ss, length):
    px = measure(name, ss, length)
    black = np.percentile(px, 0.5, axis=0) * 0.9            # จุดดำจริงของแต่ละสี (เอาความฟุ้งออก)
    px = np.clip((px - black) / (1 - black), 0, 1)
    m = px.mean(0)
    # สมดุลสี: ดึงแดง/น้ำเงินเทียบกับเขียวเข้าหาเป้าหมาย
    gr = (TARGET_RG / (m[0] / m[1])) ** PULL_COLOR
    gb = (TARGET_BG / (m[2] / m[1])) ** PULL_COLOR
    g = np.array([gr, 1.0, gb])
    g /= (np.array([0.2126, 0.7152, 0.0722]) @ g)            # คงความสว่างเดิมไว้ก่อน
    px = np.clip(px * g, 0, 1)
    # ความสว่าง: ใช้เส้นโค้งกำลัง (ยกส่วนกลาง ไม่ทำให้ส่วนสว่างขาวโพลน)
    y = float(np.mean(px @ [0.2126, 0.7152, 0.0722]))
    target = math.exp(math.log(y) + PULL_LIGHT * (math.log(TARGET_LUMA) - math.log(y)))
    gamma = math.log(target) / math.log(y)                   # <1 = สว่างขึ้น
    gamma = min(max(gamma, 0.55), 1.4)
    lv = ':'.join(f'{c}imin={black[i]:.4f}:{c}imax={min(1, black[i] + (1 - black[i]) / g[i]):.4f}'
                  for i, c in enumerate('rgb'))
    f = (f'format=gbrp,colorlevels={lv},'
         f"lutrgb=r='maxval*pow(val/maxval\\,{gamma:.3f})':g='maxval*pow(val/maxval\\,{gamma:.3f})'"
         f":b='maxval*pow(val/maxval\\,{gamma:.3f})',"
         "curves=all='0/0 0.25/0.21 0.75/0.79 1/1',"           # คอนทราสต์เล็กน้อย ไม่ฟุ้ง
         'eq=saturation=1.08,format=yuv420p')
    return f, y


# ---------- ข้อความ (มีกรอบทุกชิ้น) ----------
def _font(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)


def label(path, text, size=86):
    f = _font(FONT_BIG, size)
    x0, y0, x1, y1 = f.getbbox(text)
    pad = 28
    im = Image.new('RGBA', (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), (0, 0, 0, BOX_ALPHA))
    ImageDraw.Draw(im).text((pad - x0, pad - y0), text, font=f, fill=YELLOW)
    im.save(path)


def panel(path, lines):
    """กรอบเดียวกว้างเต็มจอ ข้อความหลายบรรทัดกึ่งกลาง  lines = [(ข้อความ, ขนาด, สี, ตัวหนา?)] หรือ '---' = เส้นคั่น"""
    rows, h = [], 40
    for ln in lines:
        if ln == '---':
            rows.append(('---', h)); h += 34; continue
        text, size, color, bold = ln
        f = _font(FONT_BIG if bold else FONT_SMALL, size)
        x0, y0, x1, y1 = f.getbbox(text)
        rows.append(((text, f, color, x0, y0, x1 - x0), h)); h += (y1 - y0) + 26
    h += 14
    im = Image.new('RGBA', (1080, h), (0, 0, 0, BOX_ALPHA))
    d = ImageDraw.Draw(im)
    for r, top in rows:
        if r == '---':
            d.rectangle([440, top + 8, 640, top + 11], fill=YELLOW); continue
        text, f, color, x0, y0, w = r
        d.text(((1080 - w) // 2 - x0, top - y0), text, font=f, fill=color)
    im.save(path)


# ---------- ประกอบคลิป ----------
def run(args):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + args, check=True)


def build(shots, final, sections, tmp_name):
    """shots = [(ที่มา, เริ่ม, ยาว, ซูม, ข้อความ)]  ข้อความ = None | ('label', 'ข้อความ') | ('panel', [...])"""
    tmp = os.path.join(HERE, tmp_name)
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    parts, cuts, t, seen = [], [], 0.0, None
    for i, (name, ss, dur, zoom, text) in enumerate(shots):
        last = i == len(shots) - 1
        length = dur if last else dur + XF
        frames = round(length * 25)
        if name.startswith('IMG'):
            inp = ['-loop', '1', '-t', f'{length}', '-i', src(name)]
            base = image_base(name, length)
        else:
            inp = ['-ss', f'{ss}', '-t', f'{length}', '-i', src(name)]
            base = 'scale=1080:1920'
        g, y = grade(name, ss, length)
        vf = (f'{base},setsar=1,{g},fps=25,scale=2160:3840:flags=lanczos,'
              f"zoompan=z='1+{zoom}*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=25")
        fc, post, cur = f'[0:v]{vf}[b0]', '', '[b0]'
        if text:
            kind, content = text
            png = os.path.join(tmp, f't{i:02d}.png')
            if kind == 'label':
                label(png, content)
                pos, fade = f'(W-w)/2:H*{LABEL_Y}', (content != seen)   # ข้อความเดิมต่อเนื่อง ไม่ต้องจางเข้าใหม่
                seen = content
            else:
                panel(png, content)
                pos, fade = f'0:{PANEL_Y}', True
                post = f',fade=t=out:st={dur - 0.4:.2f}:d=0.4'
            inp += ['-loop', '1', '-t', f'{length}', '-i', png]
            fin = f',fade=t=in:st={0.3 if kind == "panel" else 0}:d=0.25:alpha=1' if fade else ''
            fc += f';[1:v]format=rgba{fin}[o];[b0][o]overlay={pos}:shortest=1[b1]'
            cur = '[b1]'
        else:
            seen = None
        fc += f';{cur}null{post}[out]'
        p = os.path.join(tmp, f'p{i:02d}.mp4')
        run(inp + ['-filter_complex', fc, '-map', '[out]', '-an', '-frames:v', str(frames),
                   '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', p])
        parts.append(p); cuts.append(t); t += dur
        print(f'{i + 1:2d}/{len(shots)} {name:8} {cuts[-1]:5.1f}s  แสงเดิม {y:.2f}', flush=True)

    total = t - 0.04
    music = os.path.join(tmp, 'music.wav')
    subprocess.run(['python3', os.path.join(HERE, 'music.py'), music, f'{total}'] + [f'{c}' for c in cuts],
                   check=True, env={**os.environ, 'SECTIONS': sections})
    inputs, chain, prev = [], '', '[0:v]'
    for p in parts:
        inputs += ['-i', p]
    for k in range(1, len(parts)):
        chain += f'{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={cuts[k]}[v{k}];'
        prev = f'[v{k}]'
    inputs += ['-i', music]
    chain += f'[{len(parts)}:a]loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false[a]'
    os.makedirs(os.path.dirname(final), exist_ok=True)
    run(inputs + ['-filter_complex', chain, '-map', prev, '-map', '[a]',
                  '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '25',
                  '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', f'{total}', final])
    shutil.rmtree(tmp)
    print('done', final)
