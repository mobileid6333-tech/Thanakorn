# แต่งเพลงแนวเทศกาลญี่ปุ่น 120 BPM ให้กลองไทโกะตีตรงจุดเปลี่ยนฉาก
# วิธีใช้: python3 music.py ไฟล์ผลลัพธ์.wav ความยาว(วินาที) จุดตัด1 จุดตัด2 ...
import sys, wave
import numpy as np

SR = 48000
out_path, total = sys.argv[1], float(sys.argv[2])
cuts = [float(x) for x in sys.argv[3:]]
END = cuts[-1]                      # จุดขึ้นข้อความปิดท้าย
BEAT = 0.5                          # 120 BPM
N = int(SR * (total + 0.1))
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)


def add(sig, t, vol=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[: N - i] * vol
    L[i:i + len(sig)] += sig * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * (1 + min(0, pan))


def env(n, decay):
    return np.exp(-np.arange(n) / (SR * decay))


def lowpass(x, a):
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc); y[i] = acc
    return y


def sweep(f0, f1, dur, k):
    t = np.arange(int(SR * dur)) / SR
    f = f1 + (f0 - f1) * np.exp(-t * k)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


# ---------- เสียงเครื่องดนตรี ----------
def taiko(big=False):
    d = 1.6 if big else 0.9
    n = int(SR * d)
    body = sweep(140, 62, d, 18) * env(n, 0.45 if big else 0.25)
    skin = lowpass(rng.standard_normal(n), 0.08) * env(n, 0.05) * 3
    s = body + skin
    return np.tanh(s * 1.6) * 0.9


def shime():
    n = int(SR * 0.18)
    tone = sweep(620, 430, 0.18, 30) * env(n, 0.04)
    noise = rng.standard_normal(n) * env(n, 0.012) * 0.5
    return (tone + noise) * 0.5


def kick():
    n = int(SR * 0.4)
    return np.tanh(sweep(150, 48, 0.4, 35) * env(n, 0.12) * 2.2) * 0.8


def clap():
    n = int(SR * 0.25)
    x = rng.standard_normal(n)
    x = x - lowpass(x, 0.15)
    e = env(n, 0.06)
    for off in (0.0, 0.012, 0.024):
        k = int(off * SR); e[k:k + 200] += 0.6
    return x * e * 0.35


def hat(open_=False):
    n = int(SR * (0.25 if open_ else 0.05))
    x = rng.standard_normal(n)
    x = x - lowpass(x, 0.5)
    return x * env(n, 0.07 if open_ else 0.012) * 0.22


def kakko():                          # เสียงไม้ "ก๊อก"
    n = int(SR * 0.08)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1800 * t) + 0.5 * np.sin(2 * np.pi * 2700 * t)) * env(n, 0.012) * 0.3


def koto(freq, dur=1.4, bright=0.5):  # พิณโคโตะแบบดีดสาย (Karplus-Strong)
    n = int(SR * dur)
    p = int(SR / freq)
    buf = rng.uniform(-1, 1, p)
    buf = lowpass(buf, bright)
    out = np.empty(n)
    for i in range(n):
        j = i % p
        out[i] = buf[j]
        buf[j] = 0.996 * 0.5 * (buf[j] + buf[(j + 1) % p])
    # ดีดแล้วเสียงสูงขึ้นเล็กน้อย เหมือนกดสายโคโตะ
    return out * env(n, 0.5) * 0.55


def bass(freq, dur=0.45):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(4 * np.pi * freq * t)
    a = np.minimum(1, t / 0.005)
    return np.tanh(s * 1.3) * a * env(n, 0.22) * 0.45


def crash(dur=2.5):
    n = int(SR * dur)
    x = rng.standard_normal(n)
    x = x - lowpass(x, 0.35)
    return x * env(n, 0.7) * 0.12


# ---------- โน้ต (บันไดเสียงมินโย D F G A C) ----------
NOTE = {'D4': 293.66, 'F4': 349.23, 'G4': 392.0, 'A4': 440.0, 'C5': 523.25,
        'D5': 587.33, 'F5': 698.46, 'G5': 783.99, 'A5': 880.0, 'C4': 261.63, 'A3': 220.0}
RIFFS = [
    ['D5', None, 'A4', 'C5', 'D5', None, 'F5', 'D5'],
    ['G5', 'F5', 'D5', 'C5', 'A4', None, 'C5', 'D5'],
    ['D5', None, 'A4', 'C5', 'D5', None, 'G5', 'F5'],
    ['F5', None, 'D5', 'C5', 'A4', 'G4', 'A4', None],
]
BASS = [73.42, 65.41, 87.31, 98.0]     # D2 C2 F2 G2 ทีละห้อง
cache = {}
def k(name):
    if name not in cache:
        cache[name] = koto(NOTE[name])
    return cache[name]

K, C, HC, HO, SH, KA = kick(), clap(), hat(), hat(True), shime(), kakko()
nbars = int(np.ceil(END / 2))

for b in range(nbars):
    t0 = b * 2.0
    full = t0 >= 4.0                     # ช่วงแรกเบากว่าเล็กน้อย
    chef = 5.0 <= t0 < 15.0
    for s in range(8):                   # ทีละครึ่งจังหวะ
        t = t0 + s * 0.25
        if t >= END - 2.5 and t < END:   # ช่วงภาพเด่น: เบาลง สร้างความคาดหวัง
            continue
        if t >= END:
            break
        add(HC, t, 0.8 if s % 2 else 0.5, pan=0.3)
        if s % 2 == 1 and full:
            add(HO if s == 7 else HC, t + 0.0, 0.6, pan=0.3)
        if s in (0, 4) or (full and s == 5):
            add(K, t, 1.0 if s != 5 else 0.6)
        if s in (2, 6) and full:
            add(C, t, 1.0, pan=-0.1)
        if s in (3, 7):
            add(KA, t + 0.125, 0.7, pan=-0.4)
        # เบส
        if full and s in (0, 3, 4, 7):
            f = BASS[b % 4] * (2 if s == 3 else 1)
            add(bass(f), t, 1.0)
        # พิณโคโตะ
        note = RIFFS[b % 4][s]
        if note:
            add(k(note), t, 0.9 if full else 0.75, pan=-0.25)
    # กลองเล็กรัวท้ายห้อง ช่วงเชฟทำอาหาร
    if chef:
        for q in range(6):
            add(SH, t0 + 1.5 + q * (0.5 / 6), 0.5 + q * 0.08, pan=0.2)

# ช่วงภาพเด่น: โคโตะช้า ๆ + กลองเล็กรัวเร่งขึ้น
for i, nm in enumerate(['D5', 'A4', 'C5', 'D5', 'F5']):
    add(k(nm), END - 2.5 + i * 0.5, 1.3, pan=-0.2)
roll = END - 1.0
for q in range(16):
    add(SH, roll + q * (1.0 / 16), 0.25 + q * 0.05, pan=0.15)

# ---------- กลองไทโกะตรงจุดเปลี่ยนฉาก ----------
for c in cuts[:-1]:
    big = c in (0.0, 5.0, 15.0)
    add(taiko(big), c, 0.9 if big else 0.6)
# ปิดท้าย: กลองใหญ่ + ฉาบ + คอร์ดโคโตะ
add(taiko(True), END, 1.1); add(K, END, 1.0); add(crash(), END, 1.0)
for nm in ('D4', 'A4', 'D5', 'F5'):
    add(koto(NOTE[nm], 4.0, 0.4), END + 0.02, 0.7)
add(taiko(False), END + 0.5, 0.5); add(taiko(True), END + 1.0, 0.7)

# ---------- เสียงก้อง (reverb) ----------
def reverb(x, dur=1.6, mix=0.18):
    n = int(SR * dur)
    ir = rng.standard_normal(n) * env(n, 0.35)
    ir = lowpass(ir, 0.3); ir /= np.sqrt((ir ** 2).sum())
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x + mix * y

L, R = reverb(L), reverb(R)
fade_n = int(SR * 1.2)
end_i = int(SR * total)
for ch in (L, R):
    ch[end_i - fade_n:end_i] *= np.linspace(1, 0, fade_n)
    ch[end_i:] = 0
mx = max(np.abs(L).max(), np.abs(R).max())
st = np.stack([L, R], 1)[:end_i] / mx * 0.89
with wave.open(out_path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('music ok', round(total, 2), 'sec, cuts:', cuts)
