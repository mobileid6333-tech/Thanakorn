# คลิปที่ 2: MATSU HAND ROLL TACO แนว FOMO "เหลืออีก 2 วันสุดท้าย!" ยาว 24.5 วินาที
# ทุกช็อตค่อย ๆ ซูมเข้าช้า ๆ และเปลี่ยนช็อตแบบภาพจางเข้าหากัน 0.2 วินาที
# วิธีใช้: python3 render2.py
import glob, os, shutil, subprocess

SRC = '/root/.claude/uploads/b982627e-a661-5c91-8e6b-77c2b9210699'
OUT = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(OUT, 'parts2')
FINAL = os.path.join(OUT, 'clip2', 'MATSU_Clip2_FOMO_9x16.mp4')
TH = os.path.join(OUT, 'fonts', 'Kanit-ExtraBold.ttf')
EN = subprocess.check_output(['fc-match', '-f', '%{file}', 'Inter Display:style=ExtraBold'], text=True)
EN2 = subprocess.check_output(['fc-match', '-f', '%{file}', 'Inter:style=Medium'], text=True)
YEL = '0xFCD543'
XF = 0.2                     # ความยาวภาพจางระหว่างช็อต
SECTIONS = '3,10'            # FOOD HERO เริ่ม 3 วิ, EVENT VIBE เริ่ม 10 วิ

# (ที่มา, เริ่ม(วิ), ยาว(วิ), ชนิด, ระดับซูม)
#  ที่มา: รหัสคลิป หรือ IMG@ตำแหน่งตัดภาพนิ่ง
#  ชนิด: none / hook = ข้อความต้นคลิป / cta = ข้อความชวนมา / end = ปิดท้าย
SHOTS = [
    # 0–3 HOOK
    ('IMG@300', 0, 1.0, 'hook', 0.08),
    ('07756', 0.0, 1.0, 'hook', 0.06),
    ('07755', 4.0, 1.0, 'hook', 0.06),
    # 3–10 FOOD HERO
    ('07626', 2.0, 1.0, 'none', 0.06),
    ('07629', 3.5, 1.0, 'none', 0.06),
    ('07648', 0.0, 1.0, 'none', 0.06),
    ('07753', 1.5, 1.5, 'none', 0.06),
    ('07875', 0.0, 1.0, 'none', 0.06),
    ('07756', 1.0, 1.5, 'none', 0.06),
    # 10–18 EVENT VIBE
    ('08269', 0.0, 1.5, 'none', 0.05),
    ('07872', 1.5, 1.0, 'none', 0.05),
    ('07864', 1.0, 1.0, 'none', 0.05),
    ('07841', 3.0, 1.5, 'none', 0.05),
    ('07877', 0.3, 1.0, 'none', 0.05),
    ('07878', 3.0, 1.0, 'none', 0.05),
    ('07879', 6.0, 1.0, 'none', 0.05),
    # 18–24.5 CTA
    ('07866', 2.0, 1.5, 'none', 0.06),
    ('IMG@750', 0, 2.0, 'cta', 0.12),
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
hook = write('hook.txt', 'เหลืออีก 2 วันสุดท้าย!')
cta = write('cta.txt', 'ยังไม่ได้ลอง ต้องมาแล้ว!')
t1 = write('t1.txt', 'MATSU HAND ROLL TACO')
t3 = write('t3.txt', '7–8 NOV  |  CENTRAL KHON KAEN')
BOX = 'box=1:boxcolor=black@0.55:boxborderw=28'

parts, cuts, t = [], [], 0.0
for i, (name, ss, dur, kind, zoom) in enumerate(SHOTS):
    last = i == len(SHOTS) - 1
    length = dur if last else dur + XF          # เผื่อท้ายไว้ให้ภาพจางทับช็อตถัดไป
    frames = round(length * 25)
    if name.startswith('IMG@'):
        x = int(name[4:])
        inp = ['-loop', '1', '-t', f'{length}', '-i', src(name)]
        base = f'crop=815:1449:{x}:0,scale=1080:1920,setsar=1,eq=contrast=1.04:saturation=1.12:brightness=0.03'
    else:
        inp = ['-ss', f'{ss}', '-t', f'{length}', '-i', src(name)]
        base = 'scale=1080:1920,setsar=1,eq=contrast=1.06:saturation=1.12'
    # ซูมเข้าช้า ๆ แบบลื่น: ขยายภาพเป็น 2 เท่าก่อน แล้วค่อยครอปทีละเฟรม
    vf = (f'{base},fps=25,scale=2160:3840:flags=lanczos,'
          f"zoompan=z='1+{zoom}*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=25")
    if kind == 'hook':
        a = "'min(1,t/0.15)'" if i == 0 else '1'
        vf += f",drawtext=fontfile={TH}:textfile={hook}:fontsize=88:fontcolor={YEL}:{BOX}:x=(w-tw)/2:y=h*0.20:alpha={a}"
    elif kind == 'cta':
        vf += f",drawtext=fontfile={TH}:textfile={cta}:fontsize=84:fontcolor={YEL}:{BOX}:x=(w-tw)/2:y=h*0.20:alpha='min(1,max(0,(t-{XF})/0.2))'"
    elif kind == 'end':
        vf += (f",colorchannelmixer=rr=0.85:gg=0.85:bb=0.85,drawbox=x=0:y=1150:w=1080:h=390:color=black@0.62:t=fill"
               f",drawtext=fontfile={TH}:textfile={cta}:fontsize=72:fontcolor={YEL}:x=(w-tw)/2:y=1190"
               f",drawbox=x=440:y=1310:w=200:h=4:color={YEL}@1:t=fill:enable='gte(t,0.4)'"
               f",drawtext=fontfile={EN}:textfile={t1}:fontsize=76:fontcolor=white:x=(w-tw)/2:y=1345:alpha='min(1,max(0,(t-0.4)/0.4))'"
               f",drawtext=fontfile={EN2}:textfile={t3}:fontsize=44:fontcolor=white:x=(w-tw)/2:y=1450:alpha='min(1,max(0,(t-0.7)/0.4))'"
               f",fade=t=out:st={dur - 0.4}:d=0.4")
    p = os.path.join(TMP, f'p{i:02d}.mp4')
    run(inp + ['-vf', vf, '-an', '-frames:v', str(frames), '-c:v', 'libx264', '-preset', 'medium',
               '-crf', '17', '-pix_fmt', 'yuv420p', p])
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
