# เพลงแนวญี่ปุ่นแบบไม่มีกลอง ให้ความรู้สึกตื่นเต้น 120 BPM
# พิณโคโตะดีดรัว + เบสเดินจังหวะ + เสียงพื้นหลังแบบเครื่องสาย + ขลุ่ยชาคุฮาจิ
# จุดเปลี่ยนฉากใช้เสียงพิณกวาดสาย และมีเสียงลมฟิ้วก่อนเข้าช่วงใหม่
# วิธีใช้: python3 music.py ไฟล์ผลลัพธ์.wav ความยาว(วินาที) จุดตัด1 จุดตัด2 ...
import sys, wave
import numpy as np

SR = 48000
out_path, total = sys.argv[1], float(sys.argv[2])
cuts = [float(x) for x in sys.argv[3:]]
END = cuts[-1]                       # จุดขึ้นข้อความปิดท้าย
BREAK = END - 2.5                    # ช่วงภาพเด่น: เบาลงก่อนปิด
N = int(SR * (total + 0.1))
rng = np.random.default_rng(11)


class Track:
    def __init__(self):
        self.L = np.zeros(N); self.R = np.zeros(N)

    def add(self, sig, t, vol=1.0, pan=0.0):
        i = int(t * SR)
        if i >= N or i < 0:
            return
        sig = sig[: N - i] * vol
        self.L[i:i + len(sig)] += sig * (1 - max(0, pan))
        self.R[i:i + len(sig)] += sig * (1 + min(0, pan))


def env(n, decay):
    return np.exp(-np.arange(n) / (SR * decay))


def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.ones_like(f)
    if hi:
        g *= 1 / (1 + (f / hi) ** 4)
    if lo:
        g *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X * g, len(x))


def hz(name):
    names = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    n = names[name[0]] + 12 * (int(name[-1]) + 1)
    return 440 * 2 ** ((n - 69) / 12)


# ---------- เสียงเครื่องดนตรี ----------
_kcache = {}
def koto(name, dur=0.9, bright=0.55):
    key = (name, dur, bright)
    if key in _kcache:
        return _kcache[key]
    n = int(SR * dur); p = int(SR / hz(name))
    buf = rng.uniform(-1, 1, p)
    buf = np.convolve(buf, [bright, 1 - bright], 'same')
    out = np.empty(n)
    for i in range(n):
        j = i % p
        out[i] = buf[j]
        buf[j] = 0.995 * 0.5 * (buf[j] + buf[(j + 1) % p])
    out *= env(n, dur * 0.45) * 0.5
    out[-480:] *= np.linspace(1, 0, 480)          # ปิดท้ายนุ่ม ๆ กันเสียงคลิก
    _kcache[key] = out
    return out


def flute(name, dur, vib=True):
    n = int(SR * dur); t = np.arange(n) / SR
    f = hz(name) * (1 + (0.006 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.3) if vib else 0))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    breath = fft_filter(rng.standard_normal(n), lo=1500, hi=5000) * 0.12
    a = np.minimum(1, t / 0.04) * np.minimum(1, (dur - t) / 0.06).clip(0)
    return (s + breath) * a * 0.28


def saw(f, n, detune=0.0):
    t = np.arange(n) / SR
    ph = (t * f * (1 + detune) + rng.random()) % 1
    return 2 * ph - 1


def strum(chord, dur=1.6):
    out = np.zeros(int(SR * (dur + 0.1)))
    for k, nm in enumerate(chord):
        s = koto(nm, dur, 0.4); i = int(k * 0.018 * SR)
        out[i:i + len(s)] += s
    return fft_filter(out, hi=5000) * 0.7


# ---------- คอร์ดและทำนอง (บันไดเสียง D มินโย) ----------
CHORDS = [  # (เบส, โน้ตคอร์ด, โน้ตพิณดีดรัว)
    ('D2', ['D4', 'F4', 'A4', 'C5'], ['D5', 'A4', 'F5', 'A4', 'C6', 'A5', 'F5', 'A4']),
    ('C2', ['C4', 'D4', 'G4', 'C5'], ['C5', 'G4', 'D5', 'G4', 'G5', 'D5', 'C5', 'G4']),
    ('F2', ['F4', 'G4', 'A4', 'C5'], ['F5', 'C5', 'G5', 'C5', 'A5', 'G5', 'F5', 'C5']),
    ('G2', ['G4', 'C5', 'D5', 'G5'], ['G5', 'D5', 'C6', 'D5', 'G5', 'D5', 'C5', 'D5']),
]
MELODY = [  # (เวลา, โน้ต, ความยาว)
    (5.0, 'A5', .75), (5.75, 'G5', .25), (6.0, 'F5', .5), (6.5, 'D5', .5), (7.0, 'F5', .5), (7.5, 'G5', 1.0),
    (8.5, 'A5', .5), (9.0, 'C6', .75), (9.75, 'A5', .25), (10.0, 'G5', .5), (10.5, 'F5', .5), (11.0, 'G5', 1.5),
    (12.5, 'A5', .5), (13.0, 'F5', .5), (13.5, 'G5', .5), (14.0, 'D5', 1.0),
    (15.0, 'D6', .75), (15.75, 'C6', .25), (16.0, 'A5', .5), (16.5, 'G5', .5), (17.0, 'A5', .5), (17.5, 'C6', .5),
    (18.0, 'D6', 1.0), (19.0, 'C6', .5), (19.5, 'A5', .5), (20.0, 'G5', .5), (20.5, 'F5', .5), (21.0, 'G5', .5),
    (21.5, 'A5', .5), (22.0, 'C6', .5), (22.5, 'D6', .5),
]

arp, bass, pad, lead, fx = Track(), Track(), Track(), Track(), Track()
nbars = int(np.ceil(total / 2))

for b in range(nbars):
    t0 = b * 2.0
    root, chord, pat = CHORDS[b % 4]
    # พิณดีดรัว (โน้ตละ 1/16) — ตลอดเพลงจนถึงจุดปิด
    for s in range(16):
        t = t0 + s * 0.125
        if t >= END:
            break
        nm = pat[s % 8]
        v = 0.55 if s % 4 == 0 else 0.38
        if t >= BREAK:
            v *= 0.55
        arp.add(koto(nm, 0.45), t, v, pan=-0.35 if s % 2 else 0.35)
        if 15.0 <= t < BREAK and s % 2 == 0:      # ช่วงงานคึกคัก: เพิ่มชั้นเสียงสูง
            up = nm[:-1] + str(int(nm[-1]) + 1)
            if hz(up) < 1400:
                arp.add(koto(up, 0.35), t + 0.0625, 0.18, pan=0.5)
    # เบสเดิน 1/8 (ตูม-ตูม แบบรู้สึกเร่ง)
    if 1.5 <= t0 + 2 and t0 < BREAK:
        for s in range(8):
            t = t0 + s * 0.25
            if t < 1.5 or t >= BREAK:
                continue
            f = hz(root) * (2 if s % 2 else 1)
            n = int(SR * 0.24); tt = np.arange(n) / SR
            sig = np.tanh((np.sin(2 * np.pi * f * tt) + 0.5 * saw(f, n)) * 1.4)
            sig *= np.minimum(1, tt / 0.008) * env(n, 0.12)
            bass.add(sig, t, 0.5)
    # เสียงพื้นหลังแบบเครื่องสาย
    if t0 < END:
        n = int(SR * 2.3); tt = np.arange(n) / SR
        sig = sum(saw(hz(nm), n, d) for nm in chord for d in (-0.004, 0.004))
        swell = np.minimum(1, tt / 0.6) * np.minimum(1, (2.3 - tt) / 0.3)
        lvl = 0.10 if t0 < 5 else 0.13
        if t0 >= BREAK - 0.5:
            lvl = 0.16
        pad.add(sig * swell, t0, lvl)

# ขลุ่ยชาคุฮาจิ
for t, nm, d in MELODY:
    lead.add(flute(nm, d + 0.05), t, 1.0, pan=0.1)

# ---------- เสียงพิณกวาดสายตรงจุดเปลี่ยนฉาก ----------
def chord_at(t):
    return CHORDS[int(t // 2) % 4][1]
for c in cuts[:-1]:
    big = c in (0.0, 5.0, 15.0)
    fx.add(strum(chord_at(c) + (['D5', 'A5'] if big else [])), c, 0.9 if big else 0.6, pan=-0.1)

# ---------- เสียงลมฟิ้วก่อนเข้าช่วงใหม่ ----------
def riser(dur):
    n = int(SR * dur); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    out = np.zeros(n); seg = 2048
    for i in range(0, n, seg):
        p = i / n
        out[i:i + seg] = fft_filter(x[i:i + seg], lo=300 + 3000 * p, hi=800 + 7000 * p)
    return out * (t / dur) ** 2 * 0.35
for t_hit, d in ((5.0, 1.5), (15.0, 2.0), (END, 2.5)):
    fx.add(riser(d), t_hit - d, 1.0)

# ช่วงภาพเด่น: ขลุ่ยเสียงยาวค่อย ๆ ขึ้น
lead.add(flute('A5', 1.2), BREAK, 0.8); lead.add(flute('C6', 1.25), BREAK + 1.25, 0.9)

# ---------- ปิดท้าย ----------
fx.add(strum(['D3', 'A3', 'D4', 'F4', 'A4', 'D5'], 4.0), END, 1.3)
lead.add(flute('D6', 3.6), END + 0.05, 1.0)
n = int(SR * 4.5); tt = np.arange(n) / SR
endpad = sum(saw(hz(nm), n, d) for nm in ['D3', 'A3', 'D4', 'F4', 'A4'] for d in (-0.004, 0.004))
pad.add(endpad * np.minimum(1, tt / 0.2) * env(n, 2.0), END, 0.14)

# ---------- ผสมเสียง ----------
for tr in (pad,):
    tr.L, tr.R = fft_filter(tr.L, hi=1800), fft_filter(tr.R, hi=1800)
for tr in (arp,):
    tr.L, tr.R = fft_filter(tr.L, hi=6000), fft_filter(tr.R, hi=6000)
for tr in (bass,):
    tr.L, tr.R = fft_filter(tr.L, hi=900), fft_filter(tr.R, hi=900)
L = arp.L + bass.L + pad.L + lead.L + fx.L
R = arp.R + bass.R + pad.R + lead.R + fx.R


def reverb(x, dur=2.0, mix=0.25):
    n = int(SR * dur)
    ir = fft_filter(rng.standard_normal(n), hi=4000) * env(n, 0.45)
    ir /= np.sqrt((ir ** 2).sum())
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x + mix * y


L, R = reverb(L), reverb(R)
end_i = int(SR * total); fade_n = int(SR * 1.5)
for ch in (L, R):
    ch[end_i - fade_n:end_i] *= np.linspace(1, 0, fade_n)
st = np.stack([L, R], 1)[:end_i]
st = np.tanh(st / np.abs(st).max() * 1.3) * 0.89
with wave.open(out_path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('music ok', round(total, 2), 'sec, cuts:', cuts)
