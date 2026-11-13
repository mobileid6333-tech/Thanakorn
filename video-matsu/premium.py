# ชุดตั้งค่าหน้าตาตาม CI ของ MATSU สำหรับคลิปชุด 10 คลิป (Japanese Premium)
# - ใช้ร่วมกับ engine.py แต่ไม่แก้ค่าของคลิปขอนแก่น 3 คลิปเดิม
# - ฟอนต์ Kanit ทั้งหมด / ข้อความขาว คำเด่นทอง #FCD543 / พื้นดำเป็นฐาน ทองเป็นสีเน้น
# - ข้อความวางบนแถบดำโปร่งที่ค่อย ๆ จางออก (ไม่มีกรอบทึบ)
# - ฉากจบพื้นดำ MATSU สีทอง + ชื่อสาขา
import glob, os, shutil, subprocess
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
engine.TARGET_RG, engine.TARGET_BG = 1.46, 0.66
# โทนอุ่นเพิ่ม: ส่วนมืดออกน้ำตาล ส่วนกลาง/สว่างออกส้มทองอ่อน ๆ (ผู้ใช้ขอโทนวอมขึ้น)
WARM = 'colorbalance=rs=0.03:bs=-0.05:rm=0.05:gm=0.01:bm=-0.06:rh=0.03:bh=-0.04'


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


BRANCH = 'สาขาอุบลราชธานี'     # ชื่อสาขาในฉากจบ


def end_card(path, branch=BRANCH):
    """ฉากจบ: พื้นดำ แสงอุ่นจาง ๆ ตรงกลาง  โลโก้ (หรือคำว่า MATSU ชั่วคราว) + ชื่อสาขา"""
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
    # เส้นทองบาง ๆ + ชื่อสาขา (ภาษาไทย ไม่เว้นระยะตัวอักษร เพื่อให้สระ/วรรณยุกต์ถูกที่)
    ly = int(bottom + 70)
    d.rectangle([W // 2 - 60, ly, W // 2 + 60, ly + 2], fill=GOLD)
    f2 = _font(FONT_SEMI, 52)
    w2 = d.textlength(branch, font=f2)
    _, by0, _, _ = f2.getbbox(branch)
    d.text(((W - w2) / 2, ly + 46 - by0), branch, font=f2, fill=GOLD)
    im.convert('RGB').save(path)


# ---------- ประกอบคลิป ----------
# โฟลเดอร์ฟุตเทจสาขาอุบล (ไฟล์ที่ผู้ใช้อัปโหลด) — เปลี่ยนได้ด้วยตัวแปร MATSU_SRC
SRC = os.environ.get('MATSU_SRC', '/root/.claude/uploads/61b06ac1-a793-5aee-9c3b-075edfb9ae9d')
SLOW = 2.0          # ฟุตเทจ 50 ภาพ/วินาที เล่นที่ 25 = ภาพช้า 2 เท่า แต่ยังลื่น
XF = 0.12           # ภาพจางระหว่างช็อต (วินาที)
CAP_Y = int(H * 0.72)


def src(name):
    return sorted(glob.glob(f'{SRC}/*{name}*'))[0]


engine.src = src    # ให้ส่วนปรับแสง/สีของ engine.py อ่านฟุตเทจชุดนี้


def _run(args):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + args, check=True)


def build(shots, final, tmp_name, end_len=3.0, branch=BRANCH, slow=SLOW, bpm=70, pre=''):
    """shots = [(รหัสไฟล์, เริ่ม(วิในไฟล์), ยาว(วิในไฟล์), ซูม, ข้อความ|None, ความดังเสียงจริง)]
    ความยาวในคลิป = ยาว x slow (ภาพช้า)  ข้อความ = [('ข้อความ','white'|'gold'), ...]
    pre = ตัวกรองภาพก่อนเริ่ม เช่น หมุนภาพแนวนอนเป็นแนวตั้ง"""
    tmp = os.path.join(HERE, tmp_name)
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    parts, cuts, sounds, t = [], [], [], 0.0
    for i, (name, ss, ln, zoom, cap, vol) in enumerate(shots):
        dur = ln * slow
        length = dur + XF
        frames = round(length * 25)
        g, y = engine.grade(name, ss, ln)
        vf = (f'setpts={slow}*PTS,tpad=stop_mode=clone:stop_duration=1,{pre + "," if pre else ""}fps=25,scale=1080:1920,setsar=1,{g},{WARM},scale=2160:3840:flags=lanczos,'
              f"zoompan=z='1+{zoom}*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=25")
        inp = ['-ss', f'{ss}', '-t', f'{length / slow + 0.1}', '-i', src(name)]
        fc = f'[0:v]{vf}[b0]'
        out = '[b0]'
        if cap:
            png = os.path.join(tmp, f'c{i:02d}.png'); caption(png, cap)
            inp += ['-loop', '1', '-t', f'{length}', '-i', png]
            fc += (f';[1:v]format=rgba,fade=t=in:st=0.25:d=0.4:alpha=1,'
                   f'fade=t=out:st={dur - 0.45:.2f}:d=0.4:alpha=1[o];[b0][o]overlay=0:{CAP_Y}:shortest=1[b1]')
            out = '[b1]'
        p = os.path.join(tmp, f'p{i:02d}.mp4')
        _run(inp + ['-filter_complex', fc, '-map', out, '-an', '-frames:v', str(frames),
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', p])
        if vol:
            a = os.path.join(tmp, f'a{i:02d}.wav')
            _run(['-ss', f'{ss}', '-t', f'{ln}', '-i', src(name), '-vn',
                  '-af', f'atempo={1 / slow:.4f},volume={vol},afade=t=in:d=0.15,afade=t=out:st={dur - 0.3:.2f}:d=0.3',
                  '-ar', '48000', '-ac', '2', a])
            sounds.append((a, t))
        parts.append(p); cuts.append(t); t += dur
        print(f'{i + 1:2d}/{len(shots)} {name:9} {cuts[-1]:5.2f}s  ยาว {dur:.2f}s  แสงเดิม {y:.2f}', flush=True)

    # ฉากจบ: ภาพดำค่อย ๆ สว่างขึ้นเป็นโลโก้ + ชื่อสาขา
    endpng = os.path.join(tmp, 'end.png'); end_card(endpng, branch)
    p = os.path.join(tmp, 'pend.mp4')
    _run(['-loop', '1', '-t', f'{end_len}', '-i', endpng, '-vf',
          f'fps=25,format=yuv420p,fade=t=in:st=0:d=0.7', '-frames:v', str(round(end_len * 25)),
          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', p])
    parts.append(p); cuts.append(t); end_at = t; total = t + end_len

    music = os.path.join(tmp, 'music.wav')
    subprocess.run(['python3', os.path.join(HERE, 'premium_music.py'), music, f'{total}', f'{end_at}'], check=True,
                   env={**os.environ, 'BPM': str(bpm)})
    inputs, chain, prev = [], '', '[0:v]'
    for q in parts:
        inputs += ['-i', q]
    for k in range(1, len(parts)):
        chain += f'{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={cuts[k] - XF / 2:.3f}[v{k}];'
        prev = f'[v{k}]'
    inputs += ['-i', music]
    mix = [f'[{len(parts)}:a]']
    for j, (a, at) in enumerate(sounds):
        inputs += ['-i', a]
        chain += f'[{len(parts) + 1 + j}:a]adelay={int(at * 1000)}|{int(at * 1000)}[s{j}];'
        mix.append(f'[s{j}]')
    chain += (f'{"".join(mix)}amix=inputs={len(mix)}:normalize=0,'
              'loudnorm=I=-15:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false[a]')
    os.makedirs(os.path.dirname(final), exist_ok=True)
    _run(inputs + ['-filter_complex', chain, '-map', prev, '-map', '[a]',
                   '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '25',
                   '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', f'{total}', final])
    vd = float(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                               'stream=duration', '-of', 'csv=p=0', final], capture_output=True, text=True).stdout)
    assert abs(vd - total) < 0.2, f'ภาพยาว {vd} ไม่ตรงกับ {total}'
    shutil.rmtree(tmp)
    print(f'done {final}  ยาว {total:.2f} วิ')


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
