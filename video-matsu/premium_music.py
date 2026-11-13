# เพลงสำหรับคลิป MATSU ชุด 10 คลิป (แนวพรีเมียม สงบ อบอุ่น) — แต่งเองทั้งหมด ไม่ติดลิขสิทธิ์
# 70 BPM: เสียงพื้นหลังนุ่ม ๆ + พิณโคโตะดีดห่าง ๆ มีเสียงสะท้อน + ขลุ่ยชาคุฮาจิโน้ตยาว
# ตอนขึ้นฉากจบ: เสียงทุ้มต่ำ "ตุ้ม" เบา ๆ + พิณกวาดสาย แล้วค่อย ๆ จางหาย
# วิธีใช้: python3 premium_music.py ไฟล์ผลลัพธ์.wav ความยาว(วินาที) เวลาเริ่มฉากจบ
import sys, wave
import numpy as np

SR = 48000
out_path, total, END = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
N = int(SR * (total + 0.1))
BEAT = 60 / 70
rng = np.random.default_rng(7)


def hz(name):
    names = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    n = names[name[0]] + (-1 if 'b' in name[1:-1] else 0) + 12 * (int(name[-1]) + 1)
    return 440 * 2 ** ((n - 69) / 12)


def lowpass(x, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / (1 + (f / hi) ** 4), len(x))


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


_kc = {}
def koto(name, dur=2.5, bright=0.5):
    key = (name, dur, bright)
    if key in _kc:
        return _kc[key]
    n = int(SR * dur); p = int(SR / hz(name))
    buf = np.convolve(rng.uniform(-1, 1, p), [bright, 1 - bright], 'same')
    out = np.empty(n)
    for i in range(n):
        j = i % p
        out[i] = buf[j]
        buf[j] = 0.996 * 0.5 * (buf[j] + buf[(j + 1) % p])
    out *= np.exp(-np.arange(n) / (SR * dur * 0.4)) * 0.5
    out[-480:] *= np.linspace(1, 0, 480)
    _kc[key] = out
    return out


def flute(name, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    f = hz(name) * (1 + 0.005 * np.sin(2 * np.pi * 5 * t) * np.minimum(1, t / 0.6))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.2 * np.sin(2 * ph) + 0.05 * np.sin(3 * ph)
    breath = lowpass(rng.standard_normal(n), 4000) * 0.15
    a = np.minimum(1, t / 0.35) * np.minimum(1, (dur - t) / 0.6).clip(0)
    return (s + breath) * a * 0.22


def pad(notes, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    out = np.zeros(n)
    for nm in notes:
        for d in (-0.004, 0.0, 0.004):
            ph = (t * hz(nm) * (1 + d) + rng.random()) % 1
            out += 2 * ph - 1
    out = lowpass(out, 900) / (len(notes) * 3)
    a = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2).clip(0)
    return out * a * 0.35


def boom(dur=4.0):
    n = int(SR * dur); t = np.arange(n) / SR
    f = 55 * (1 + 0.6 * np.exp(-t * 6))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.1)
    return s * np.minimum(1, t / 0.01) * 0.6


bg, kt, fl, fx = Track(), Track(), Track(), Track()

# เสียงพื้นหลัง: Dm9 → Bbmaj7 → Gm9 → Asus  ทุก 4 จังหวะ จนถึงฉากจบ
CH = [['D3', 'A3', 'E4', 'F4'], ['Bb2', 'F3', 'A3', 'D4'], ['G2', 'D3', 'A3', 'Bb3'], ['A2', 'E3', 'G3', 'D4']]
bar = 4 * BEAT
t, k = 0.0, 0
while t < END:
    d = min(bar + 1.2, END - t + 1.2)
    bg.add(pad(CH[k % 4], d), t, 1.0)
    t += bar; k += 1

# พิณดีดห่าง ๆ (มีเสียงสะท้อนซ้ำเบาลง ซ้าย-ขวา)
PL = ['A4', 'D5', 'E5', 'F5', None, 'A5', 'E5', None, 'D5', 'F5', 'A5', 'C6', None, 'A5', 'G5', 'E5']
for i, nm in enumerate(PL * 4):
    tt = 0.4 + i * BEAT / 2 * 1.0
    if tt >= END - 0.2:
        break
    if nm and (i % 2 == 0 or rng.random() < 0.55):
        s = koto(nm, 2.0)
        kt.add(s, tt, 0.55, -0.3 + 0.6 * (i % 3) / 2)
        kt.add(s, tt + BEAT * 0.75, 0.22, 0.4)
        kt.add(s, tt + BEAT * 1.5, 0.09, -0.4)

# ขลุ่ยโน้ตยาว ช่วงกลางคลิป
for tt, nm, d in [(BEAT * 4, 'A4', BEAT * 3), (BEAT * 7.5, 'D5', BEAT * 2.5),
                  (BEAT * 10.5, 'C5', BEAT * 1.5), (BEAT * 12, 'A4', END - BEAT * 12 + 0.4)]:
    if tt < END:
        fl.add(flute(nm, d), tt, 0.8, 0.15)

# ฉากจบ: ทุ้มต่ำ + พิณกวาดสาย Dm(add9) แล้วปล่อยให้ก้องจนจบ
fx.add(boom(), END, 0.9)
for j, nm in enumerate(['D4', 'A4', 'D5', 'E5', 'F5', 'A5']):
    s = koto(nm, 4.0, 0.45)
    fx.add(s, END + j * 0.035, 0.5, -0.4 + j * 0.16)
    fx.add(s, END + j * 0.035 + BEAT, 0.15, 0.4 - j * 0.16)
fx.add(pad(['D3', 'A3', 'E4', 'F4'], total - END + 0.1), END, 0.8)

L = bg.L + kt.L + fl.L + fx.L
R = bg.R + kt.R + fl.R + fx.R
tt = np.arange(N) / SR
fade = np.minimum(1, tt / 0.3) * np.clip((total - tt) / 1.5, 0, 1)
L, R = L * fade, R * fade
peak = max(np.abs(L).max(), np.abs(R).max(), 1e-9)
st = (np.stack([L, R], 1) / peak * 0.8 * 32767).astype(np.int16)
with wave.open(out_path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
