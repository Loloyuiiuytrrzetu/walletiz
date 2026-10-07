# Original tropical / afro-house cue for Smar Home ad B (120 BPM, 20 s) + SFX synced to ad.html
import numpy as np, wave, sys
SR = 48000; DUR = 20.0; N = int(SR * DUR)
BPM = 120; B = 60 / BPM            # beat = 0.5 s, bar = 2 s
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(3)

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i + len(sig) <= 0: return
    j = min(N, i + len(sig)); s = sig[:j - i] * gain
    L[i:j] += s * np.sqrt(0.5 * (1 - pan)) * 1.414; R[i:j] += s * np.sqrt(0.5 * (1 + pan)) * 1.414

def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=0.003, dec=0.3):
    t = tt(d); return np.minimum(1, t / a) * np.exp(-t / dec)
def lp(x, a):  # one-pole lowpass, a in (0,1)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y
def hp(x, a): return x - lp(x, a)
def mtof(m): return 440 * 2 ** ((m - 69) / 12)

# ---------------- instruments
def kick():
    t = tt(0.35); f = 48 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.16) + 0.25 * rng.standard_normal(len(t)) * np.exp(-t / 0.004)
def clap():
    t = tt(0.25); n = rng.standard_normal(len(t)); n = hp(n, 0.25)
    e = np.zeros(len(t))
    for o in (0, 0.009, 0.018): e += (t >= o) * np.exp(-np.clip(t - o, 0, None) / (0.012 if o < 0.018 else 0.09))
    return n * e * 0.6
def shaker(acc):
    t = tt(0.06); n = hp(rng.standard_normal(len(t)), 0.6)
    return n * np.minimum(1, t / 0.008) * np.exp(-t / 0.018) * (0.3 if acc else 0.16)
def conga(m):
    t = tt(0.25); f = mtof(m) * (1 + 0.15 * np.exp(-t / 0.02))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.08)
def bass(m, d):
    t = tt(d); f = mtof(m)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    s = np.tanh(1.6 * s) * np.minimum(1, t / 0.005) * np.exp(-t / (d * 0.7))
    return s * np.minimum(1, (d - t) / 0.01)
def steel(m, d=0.7):  # steel-pan-ish additive + light FM
    t = tt(d); f = mtof(m)
    mod = 0.8 * np.exp(-t / 0.05) * np.sin(2 * np.pi * f * 2 * t)
    s = (np.sin(2 * np.pi * f * t + mod) + 0.45 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t / 0.18)
         + 0.25 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t / 0.09) + 0.12 * np.sin(2 * np.pi * f * 4.2 * t) * np.exp(-t / 0.05))
    return s * np.minimum(1, t / 0.004) * np.exp(-t / 0.32)
def marimba(m, d=0.4):
    t = tt(d); f = mtof(m)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / 0.03)) * np.minimum(1, t / 0.002) * np.exp(-t / 0.14)
def pad(ms, d):
    t = tt(d); s = np.zeros(len(t))
    for m in ms:
        for det in (-0.08, 0.08):
            f = mtof(m + det); s += ((2 * ((f * t) % 1) - 1))
    s = lp(s, 0.05) / len(ms)
    return s * np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.2)

# ---------------- FX
def whoosh(d=0.45, up=True):
    t = tt(d); n = rng.standard_normal(len(t)); x = t / d
    e = (x ** 2.2) if up else (1 - x) ** 2
    # sweep via 2 lowpasses at different cutoffs blended
    a = lp(n, 0.04); b = lp(n, 0.35) - lp(n, 0.08)
    s = a * (1 - x) + b * x if up else a * x + b * (1 - x)
    return s * e * 1.6
def pop(f0=500, f1=1100, d=0.12):
    t = tt(d); f = f0 + (f1 - f0) * np.minimum(1, t / 0.05)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.002) * np.exp(-t / 0.045)
def impact():
    t = tt(0.9); f = 38 + 70 * np.exp(-t / 0.06)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35)
    n = lp(rng.standard_normal(len(t)), 0.2) * np.exp(-t / 0.12)
    return s + 0.5 * n
def slam():
    t = tt(0.4); f = 70 + 120 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12) + 0.5 * hp(rng.standard_normal(len(t)), 0.3) * np.exp(-t / 0.03)
def click():
    t = tt(0.05); return (hp(rng.standard_normal(len(t)), 0.5) * np.exp(-t / 0.004) + np.sin(2 * np.pi * 2400 * t) * np.exp(-t / 0.01))
def ding():
    t = tt(1.4); s = np.zeros(len(t))
    for r, a, dc in ((1, 1, .6), (2.0, .5, .4), (3.0, .3, .25), (4.16, .2, .15)):
        s += a * np.sin(2 * np.pi * 1318.5 * r * t) * np.exp(-t / dc)
    return s * np.minimum(1, t / 0.002)

# ---------------- music
CH = {'C': [48, 52, 55, 60, 64, 67], 'G': [43, 47, 50, 55, 59, 62], 'Am': [45, 48, 52, 57, 60, 64], 'F': [41, 45, 48, 53, 57, 60]}
prog = ['C', 'G', 'Am', 'F', 'C', 'G', 'Am', 'F', 'F', 'C']   # bars of 2 s
mel = {'C': [76, 72, 79, 76, 74, 72, 74], 'G': [74, 71, 79, 74, 76, 74, 71], 'Am': [72, 76, 81, 79, 76, 72, 76],
       'F': [72, 77, 81, 77, 76, 74, 72]}
mel_rhythm = [0, 0.75, 1.5, 2.0, 2.5, 3.0, 3.5]  # 3-3-2 soca feel (beats)
DROP = (16.0, 16.5)   # break before end card

for bar, ch in enumerate(prog):
    t0 = bar * 2.0
    for beat in range(4):
        tb = t0 + beat * B
        inbreak = DROP[0] <= tb < DROP[1]
        if not inbreak:
            add(kick(), tb, 0.95)
            if beat in (1, 3): add(clap(), tb, 0.55, 0.1)
        for s16 in range(4):
            ts = tb + s16 * B / 4
            if not (DROP[0] <= ts < DROP[1]): add(shaker(s16 == 2), ts, 0.55, 0.35 if s16 % 2 else -0.3)
        # bass: offbeat bounce + syncopation
        root = CH[ch][0] - 12 + 12 if CH[ch][0] < 45 else CH[ch][0] - 12
        if not inbreak:
            add(bass(root, 0.22), tb + B / 2, 0.55)
            if beat in (1, 3): add(bass(root + 12 if beat == 3 else root + 7, 0.14), tb + B * 0.75, 0.38)
        # congas tumbao
        if not inbreak:
            add(conga(62), tb + B * 0.75, 0.22, -0.5)
            if beat % 2 == 1: add(conga(57), tb + B * 0.25, 0.22, 0.5)
    add(pad(CH[ch][1:4], 2.0), t0, 0.12)
    # steel melody: enters fully from bar 0, simplified in bars 6-7 (zones -> marimba arps)
    if bar < 9:
        for k, (r, m) in enumerate(zip(mel_rhythm, mel[ch])):
            tm = t0 + r * B
            if DROP[0] <= tm < DROP[1]: continue
            if bar in (6, 7) and k % 2 == 1: continue
            add(steel(m), tm, 0.42, 0.15)
    # marimba arps in bars 2-7
    if 2 <= bar <= 8:
        for k in range(8):
            tm = t0 + k * B / 2
            if DROP[0] <= tm < DROP[1]: continue
            add(marimba(CH[ch][3 + (k % 3)] + 12), tm + B / 4, 0.16, -0.4)
# final chord (end card)
for m in (72, 76, 79, 84): add(steel(m, 2.2), 18.0, 0.22)
add(pad([60, 64, 67, 72], 2.0), 18.0, 0.18)

# ---------------- SFX synced to ad.html
add(impact(), 0.0, 0.9); add(whoosh(0.5, False), 0.0, 0.4)
add(pop(520, 1000), 0.30, 0.45, -0.3); add(pop(620, 1250), 0.52, 0.45, 0.3)
for i in range(11): add(pop(700 + i * 60, 1300 + i * 80, 0.08), 1.15 + i * 0.04, 0.12, (i - 5) / 8)
for tw in (2.62, 7.62, 9.62): add(whoosh(0.4), tw - 0.02, 0.75)
for ti in (3.0, 8.0, 10.0): add(impact(), ti, 0.7)
add(pop(450, 900), 3.12, 0.4)
for ts in (3.5, 4.0, 4.5): add(slam(), ts, 0.7)
for tw in (5.6, 13.12): add(whoosh(0.55), tw, 0.8); add(whoosh(0.4, False), tw + 0.32, 0.4)
add(pop(500, 1000), 5.98, 0.4)
for i, ts in enumerate((6.5, 6.75, 7.0)): add(pop(600 + i * 150, 1200 + i * 250), ts, 0.45, (i - 1) * 0.5)
for i, ts in enumerate((8.6, 8.85, 9.1)): add(pop(600 + i * 150, 1200 + i * 250), ts, 0.45, (i - 1) * 0.5)
add(slam(), 10.25, 0.75); add(pop(700, 1400), 10.45, 0.35); add(pop(500, 900), 10.85, 0.4)
for i, ts in enumerate((11.4, 11.85, 12.3)): add(whoosh(0.22), ts - 0.05, 0.35, -0.5 if i % 2 == 0 else 0.5)
add(slam(), 13.62, 0.7); add(pop(500, 1000), 13.85, 0.4)
pent = [72, 74, 76, 79, 81, 84, 86]
for i in range(7): add(marimba(pent[i] + 12, 0.5), 13.9 + i * 0.25, 0.3)
add(whoosh(0.4), 16.1, 0.7); add(impact(), 16.5, 0.9)
add(slam(), 16.62, 0.5)
for i in range(3): add(pop(600 + i * 120, 1200 + i * 200), 17.15 + i * 0.12, 0.35)
add(pop(400, 1000, 0.15), 17.3, 0.5)
add(click(), 18.48, 0.8); add(ding(), 18.5, 0.32)

# ---------------- master
mix = np.stack([L, R], 1)
mix = np.tanh(1.3 * mix / np.max(np.abs(mix))) / np.tanh(1.3) * 0.9      # gentle soft-clip glue
fade = int(0.3 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
mix[:int(0.003 * SR)] *= np.linspace(0, 1, int(0.003 * SR))[:, None]
pcm = (np.clip(mix, -1, 1) * 32000).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
