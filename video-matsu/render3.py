# คลิปที่ 3: MATSU HAND ROLL TACO "LAST DAY! วันนี้วันสุดท้าย" ยาว 19.5 วินาที
# ทุกช็อตค่อย ๆ ซูมเข้าช้า ๆ และเปลี่ยนช็อตแบบภาพจางเข้าหากัน 0.2 วินาที
# วิธีใช้: python3 render3.py
import glob, os, shutil, subprocess

SRC = '/root/.claude/uploads/b982627e-a661-5c91-8e6b-77c2b9210699'
OUT = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(OUT, 'parts3')
FINAL = os.path.join(OUT, 'clip3', 'MATSU_Clip3_LastDay_9x16.mp4')
TH = os.path.join(OUT, 'fonts', 'Kanit-ExtraBold.ttf')
EN = subprocess.check_output(['fc-match', '-f', '%{file}', 'Inter Display:style=ExtraBold'], text=True)
EN2 = subprocess.check_output(['fc-match', '-f', '%{file}', 'Inter:style=Medium'], text=True)
YEL = '0xFCD543'
XF = 0.2                     # ความยาวภาพจางระหว่างช็อต
SECTIONS = '3,8'             # FOOD & CHEF เริ่ม 3 วิ, EVENT MOMENT เริ่ม 8 วิ

# (ที่มา, เริ่ม(วิ), ยาว(วิ), ชนิด, ระดับซูม)
#  ที่มา: รหัสคลิป หรือ IMG@ตำแหน่งตัดภาพนิ่ง
#  ชนิด: none / hook = ข้อความต้นคลิป / cta = ข้อความชวนมา / end = ปิดท้าย
SHOTS = [
    # 0–3 HOOK: แฮนด์โรลที่น่าทานที่สุด สลับกับเชฟเสิร์ฟ
    ('IMG@750', 0, 1.0, 'hook', 0.08),
    ('07866', 2.5, 1.0, 'hook', 0.05),
    ('07755', 4.0, 1.0, 'hook', 0.06),
    # 3–8 FOOD & CHEF
    ('07753', 1.5, 1.0, 'none', 0.06),
    ('07626', 2.0, 1.0, 'none', 0.06),
    ('07875', 0.0, 1.0, 'none', 0.06),
    ('07756', 0.0, 1.0, 'none', 0.06),
    ('07841', 3.0, 1.0, 'none', 0.05),
    # 8–14 EVENT MOMENT: ตัดเร็วตามจังหวะ
    ('08269', 0.0, 1.0, 'none', 0.05),
    ('07864', 1.0, 0.5, 'none', 0.04),
    ('07872', 1.5, 0.5, 'none', 0.04),
    ('07877', 0.3, 1.0, 'none', 0.05),
    ('07866', 5.0, 1.0, 'none', 0.05),
    ('07878', 3.0, 1.0, 'none', 0.05),
    ('07879', 6.0, 1.0, 'none', 0.05),
    # 14–19.5 FINAL CTA
    ('IMG@pan', 0, 2.5, 'cta', 0.0),
    ('07879', 2.5, 3.0, 'end', 0.05),
]


def src(name):
    if name.startswith('IMG@'):
        return glob.glob(f'{SRC}/*image.jpg')[0]
    return sorted(glob.glob(f'{SRC}/*{name}*'))[0]


def run(args):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + args, check=True)


def write(name, text):
    p = os.path.join(TMP, name)
    open(p, 'w').write(text)
    return p


shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
t1 = write('t1.txt', 'MATSU HAND ROLL TACO')
t3 = write('t3.txt', '8 NOV  |  CENTRAL KHON KAEN')


def label(name, text, size, box):
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype(TH, size, layout_engine=ImageFont.Layout.RAQM)
    x0, y0, x1, y1 = f.getbbox(text)
    pad = 28 if box else 4
    im = Image.new('RGBA', (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), (0, 0, 0, 140 if box else 0))
    ImageDraw.Draw(im).text((pad - x0, pad - y0), text, font=f, fill='#fcd543')
    path = os.path.join(TMP, name)
    im.save(path)
    return path


HOOK_PNG = label('hook.png', 'LAST DAY! วันนี้วันสุดท้าย', 88, True)
CTA_PNG = label('cta.png', 'โอกาสสุดท้ายที่จะได้ลอง!', 84, True)
END_PNG = label('end.png', 'โอกาสสุดท้ายที่จะได้ลอง!', 72, False)

parts, cuts, t = [], [], 0.0
for i, (name, ss, dur, kind, zoom) in enumerate(SHOTS):
    last = i == len(SHOTS) - 1
    length = dur if last else dur + XF          # เผื่อท้ายไว้ให้ภาพจางทับช็อตถัดไป
    frames = round(length * 25)
    if name.startswith('IMG@'):
        inp = ['-loop', '1', '-t', f'{length}', '-i', src(name)]
        look = 'eq=contrast=1.04:saturation=1.12:brightness=0.03'
        if name == 'IMG@pan':
            # ภาพเต็มจอ ค่อย ๆ เลื่อนจากซ้ายไปขวา (เร่งช้า-ผ่อนช้า) ให้เห็นหลายเมนู
            x0, x1 = 200 * 2.65, 1300 * 2.65
            base = (f"scale=-2:3840,crop=2160:3840:x='{x0}+({x1 - x0})*(1-cos(PI*t/{length}))/2':y=0,"
                    f'scale=1080:1920,setsar=1,{look}')
        elif name == 'IMG@full':
            # ภาพเต็ม (ทุกเมนู) วางกลางจอ พื้นหลังเป็นภาพเดียวกันแบบเบลอ
            base = (f'split[a][b];[a]crop=815:1449:880:0,scale=1080:1920,boxblur=30:2,eq=brightness=-0.12[bg];'
                    f'[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2,setsar=1,{look}')
        else:
            x = int(name[4:])
            base = f'crop=815:1449:{x}:0,scale=1080:1920,setsar=1,{look}'
    else:
        inp = ['-ss', f'{ss}', '-t', f'{length}', '-i', src(name)]
        base = 'scale=1080:1920,setsar=1,eq=contrast=1.06:saturation=1.12'
    # ซูมเข้าช้า ๆ แบบลื่น: ขยายภาพเป็น 2 เท่าก่อน แล้วค่อยครอปทีละเฟรม
    vf = (f'{base},fps=25,scale=2160:3840:flags=lanczos,'
          f"zoompan=z='1+{zoom}*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=25")
    # ข้อความไทยทำเป็นรูปภาพด้วย Pillow (วางสระ/วรรณยุกต์ซ้อนได้ถูกต้อง) แล้วแปะทับวิดีโอ
    over, post = [], ''
    if kind == 'hook':
        over.append((HOOK_PNG, 'H*0.20-28', 0 if i == 0 else None))
    elif kind == 'cta':
        over.append((CTA_PNG, 'H*0.20-28', XF))
    elif kind == 'end':
        vf += (f",colorchannelmixer=rr=0.85:gg=0.85:bb=0.85,drawbox=x=0:y=1150:w=1080:h=390:color=black@0.62:t=fill"
               f",drawbox=x=440:y=1310:w=200:h=4:color={YEL}@1:t=fill:enable='gte(t,0.4)'"
               f",drawtext=fontfile={EN}:textfile={t1}:fontsize=76:fontcolor=white:x=(w-tw)/2:y=1345:alpha='min(1,max(0,(t-0.4)/0.4))'"
               f",drawtext=fontfile={EN2}:textfile={t3}:fontsize=44:fontcolor=white:x=(w-tw)/2:y=1450:alpha='min(1,max(0,(t-0.7)/0.4))'")
        over.append((END_PNG, '1180', None))
        post = f",fade=t=out:st={dur - 0.4}:d=0.4"
    fc, cur = f'[0:v]{vf}[b0]', '[b0]'
    for j, (png, y, fade_at) in enumerate(over):
        inp += ['-loop', '1', '-t', f'{length}', '-i', png]
        fin = f',fade=t=in:st={fade_at}:d=0.15:alpha=1' if fade_at is not None else ''
        fc += f';[{j + 1}:v]format=rgba{fin}[o{j}];{cur}[o{j}]overlay=x=(W-w)/2:y={y}:shortest=1[b{j + 1}]'
        cur = f'[b{j + 1}]'
    fc += f';{cur}null{post}[out]'
    p = os.path.join(TMP, f'p{i:02d}.mp4')
    run(inp + ['-filter_complex', fc, '-map', '[out]', '-an', '-frames:v', str(frames), '-c:v', 'libx264',
               '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', p])
    parts.append(p); cuts.append(t); t += dur
    print(f'{i + 1:2d}/{len(SHOTS)} {name} {cuts[-1]:.1f}s', flush=True)

TOTAL = t - 0.04
music = os.path.join(TMP, 'music.wav')
subprocess.run(['python3', os.path.join(OUT, 'music.py'), music, f'{TOTAL}'] + [f'{c}' for c in cuts],
               check=True, env={**os.environ, 'SECTIONS': SECTIONS})

# ต่อทุกช็อตด้วยภาพจาง (เริ่มจางตรงจุดตัดพอดี ให้ตรงจังหวะเพลง)
inputs, chain = [], ''
for p in parts:
    inputs += ['-i', p]
prev = '[0:v]'
for k in range(1, len(parts)):
    lab = f'[v{k}]'
    chain += f'{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={cuts[k]}{lab};'
    prev = lab
inputs += ['-i', music]
na = len(parts)
chain += f'[{na}:a]loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false[a]'
os.makedirs(os.path.dirname(FINAL), exist_ok=True)
run(inputs + ['-filter_complex', chain, '-map', prev, '-map', '[a]',
              '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '25',
              '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', f'{TOTAL}', FINAL])
shutil.rmtree(TMP)
print('done', FINAL)
