# Original score + sound design for Smar Home ad A (120 BPM, 20 s), synthesized with numpy.
# Cues follow the timeline in ad.html.  Output: out/music-a.wav (48 kHz stereo)
import numpy as np, wave

SR = 48000
DUR = 29.5
N = int(SR * DUR)
BEAT = 0.5          # 120 BPM
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

def t_(d): return np.arange(int(d * SR)) / SR

def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    sig = sig[: N - i]
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l * 1.414
    R[i:i + len(sig)] += sig * gain * r * 1.414

def spectral(sig, lo, hi, slope=None):
    """band-shape a signal in the frequency domain"""
    S = np.fft.rfft(sig); f = np.fft.rfftfreq(len(sig), 1 / SR)
    m = ((f >= lo) & (f <= hi)).astype(float)
    if slope: m *= (np.maximum(f, 1) / lo) ** slope
    return np.fft.irfft(S * m, len(sig))

def env(n, a, d, sustain=0.0, curve=4.0):
    e = np.ones(n)
    na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    rest = n - na
    if rest > 0:
        x = np.linspace(0, 1, rest)
        e[na:] = sustain + (1 - sustain) * np.exp(-curve * x * (len(x) / SR) / max(d, 1e-3))
    return e

def midi(n): return 440 * 2 ** ((n - 69) / 12)

# ---------------------------------------------------------------- instruments
def kick(gain=1.0):
    t = t_(0.45)
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 7.5)
    click = spectral(rng.standard_normal(len(t)), 2000, 8000) * np.exp(-t * 300) * .4
    return np.tanh((s + click) * 1.6) * gain

def impact():
    t = t_(2.2)
    f = 38 + 90 * np.exp(-t * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    noise = spectral(rng.standard_normal(len(t)), 80, 6000, slope=-0.6) * np.exp(-t * 6) * .5
    return np.tanh((boom * 1.2 + noise) * 1.3)

def clap():
    t = t_(0.3); n = rng.standard_normal(len(t))
    e = np.zeros(len(t))
    for o in (0, .011, .022): i = int(o * SR); e[i:] += np.exp(-(t[: len(t) - i]) * (60 if o < .02 else 18))
    return spectral(n * e, 900, 7000) * .55

def hat(open_=False):
    t = t_(0.25 if open_ else 0.06); n = rng.standard_normal(len(t))
    return spectral(n, 7000, 16000) * np.exp(-t * (14 if open_ else 70)) * .35

def shaker():
    t = t_(0.09); n = rng.standard_normal(len(t))
    return spectral(n, 5000, 12000) * np.sin(np.pi * t / t[-1]) ** 2 * .18

def sub(note, dur):
    t = t_(dur); f = midi(note)
    s = np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)
    e = env(len(t), .005, dur * .9, sustain=.75, curve=1.5); e[-int(.02 * SR):] *= np.linspace(1, 0, int(.02 * SR))
    return np.tanh(s * e * 1.3) * .5

def pluck(note, dur=0.5, bright=1.0):
    """FM 'marimba / steel' pluck"""
    t = t_(dur); f = midi(note)
    idx = 2.2 * bright * np.exp(-t * 18)
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 3.5 * t))
    return s * env(len(t), .002, .18, curve=5) * .28

def pad(notes, dur):
    t = t_(dur); s = np.zeros(len(t))
    for n in notes:
        for det in (-.12, 0, .12):
            f = midi(n + det)
            s += np.sign(np.sin(2 * np.pi * f * t + rng.random() * 6)) * .5 + np.sin(2 * np.pi * f * t)
    s = spectral(s, 60, 2200) / (len(notes) * 3)
    e = np.minimum(1, t / .35) * np.minimum(1, (dur - t) / .4)
    return s * e * .16

def whoosh(dur=0.5, up=True):
    t = t_(dur); n = rng.standard_normal(len(t))
    out = np.zeros(len(t)); seg = int(.02 * SR)
    for i in range(0, len(t), seg):   # moving band-pass sweep
        p = i / len(t); c = (400 + 5000 * (p if up else 1 - p))
        out[i:i + seg] = spectral(n[i:i + seg] if len(n[i:i + seg]) > 8 else n[i:i + seg], c * .6, c * 1.6)
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** (1.5 if up else .8)
    return out * e * .5

def riser(dur):
    t = t_(dur); n = rng.standard_normal(len(t))
    out = np.zeros(len(t)); seg = int(.03 * SR)
    for i in range(0, len(t), seg):
        p = i / len(t); c = 300 + 7000 * p ** 2
        out[i:i + seg] = spectral(n[i:i + seg], c * .7, c * 1.4)
    tone = np.sin(2 * np.pi * np.cumsum(200 + 600 * (t / dur) ** 2) / SR) * .15
    return (out * .5 + tone) * (t / dur) ** 2

def ui_click():
    t = t_(0.06)
    s = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 120) + spectral(rng.standard_normal(len(t)), 3000, 9000) * np.exp(-t * 200) * .5
    return s * .5

def pop(freq=900):
    t = t_(0.12); f = freq * (1 + 1.2 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30) * .35

def tick():
    t = t_(0.04); return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 150) * .25

def chime(notes, dur=1.6):
    t = t_(dur); s = np.zeros(len(t))
    for i, n in enumerate(notes):
        f = midi(n); d = int(i * .045 * SR)
        x = np.sin(2 * np.pi * f * t + 1.2 * np.exp(-t * 6) * np.sin(2 * np.pi * f * 2 * t)) * np.exp(-t * 2.2)
        s[d:] += x[: len(t) - d]
    return s * .14

# ---------------------------------------------------------------- arrangement (voice-led ad, 29.5 s)
CH = [(41, [57, 60, 64, 65, 69]), (43, [55, 59, 62, 64, 67]), (40, [55, 59, 62, 64, 67]), (45, [57, 60, 64, 67, 72])]
def chord_at(t): return CH[int(t // 2) % 4]
def groove(a, b, kick_on=True):
    t = a
    while t < b - 1e-6:
        bi = int(round((t - a) / BEAT))
        if kick_on: add(kick(), t, .7)
        if kick_on and bi % 2 == 1: add(clap(), t, .3, .1)
        add(hat(), t + BEAT / 2, .35, .3)
        for q in (0.125, 0.375): add(shaker(), t + q, .35, -.35)
        t += BEAT
add(pad([53, 57, 60, 64], 3.3), 0.0, 2.2)
for i in range(7): add(tick(), .15 + 2.3 * (1 - (1 - i / 6) ** 2) * 1.0, 1.2, -.3 + i * .1)        # calendar days
add(chime([72, 76, 79]), 2.55, .7)                                                              # ring on day 7
add(riser(.6), 2.7, .45); add(whoosh(.45, True), 2.9, .7); add(impact(), 3.3, .5)                 # zoom through the 7
groove(3.3, 15.1); groove(17.0, 25.4); groove(25.4, 29.0, kick_on=False)
for bar in range(15):
    t0 = bar * 2.0; root, notes = chord_at(t0)
    if t0 + 2 <= 3.3 or t0 >= 29.0: continue
    for st in np.arange(max(t0, 3.3), min(t0 + 2, 29.0), BEAT):
        if 15.1 <= st < 17.0: continue
        add(sub(root - 12 + (7 if abs((st - t0) - 1.5) < 1e-6 else 0), BEAT * .45), st + .25, .6)
    if not (15.1 <= t0 < 17.0): add(pad(notes[:4], 2.05), max(t0, 3.3), .8)
for st in np.arange(5.5, 29.0, 0.25):
    if 15.1 <= st < 17.0: continue
    root, notes = chord_at(st); i = int(round(st / .25)) % 8
    add(pluck(notes[[0, 2, 1, 3, 2, 4, 3, 1][i] % 5] + 12, .45, .8), st, .45, (-.4 if i % 2 else .4))
for i in range(6): add(pop(600 + i * 80), 5.65 + i * .07, .5)                                    # cards fly in
add(whoosh(.6, True), 7.2, .4)                                                                  # to the 13 m²
add(whoosh(2.0, True), 9.2, .5); add(whoosh(.8, False), 13.95, .45)                            # scroll + return
add(ui_click(), 14.85, 1.2); add(pop(1600), 14.86, .6)                                         # pick the card
add(whoosh(.35, True), 14.95, .5)
# 15.1-17.0: your falling-module video brings its own sound (left quiet)
add(impact(), 17.0, .4); add(chime([72, 76, 79, 84]), 18.25, .5)                               # shield + check
for at in (18.74, 19.6, 20.24): add(pop(1300), at, .6)                                          # chips
tc_ = np.arange(int(.09 * SR)) / SR
shutter = (spectral(rng.standard_normal(len(tc_)), 1800, 9000) * np.exp(-tc_ * 70) + spectral(rng.standard_normal(len(tc_)), 300, 1500) * np.exp(-tc_ * 50) * .6) * .8
for at in [21.34, 21.77, 22.2, 22.68, 23.16, 23.77, 24.38, 24.635, 24.89, 25.145]: add(shutter, at, 1.0)   # photo cuts
add(whoosh(.4, True), 25.3, .5); add(pop(900), 25.44, .4); add(pop(1100), 26.3, .4)
add(chime([77, 81, 84, 89]), 26.9, .5); add(ui_click(), 28.5, 1.1); add(chime([84, 91]), 28.52, .5)

# ---------------------------------------------------------------- mix
mixL, mixR = L.copy(), R.copy()
# small room reverb via FFT convolution
ir_t = t_(1.4); ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 4.2); ir[0] = 0
def conv(x, h):
    n = len(x) + len(h); nf = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nf) * np.fft.rfft(h, nf), nf)[: len(x)]
mixL += conv(L, ir) * .05; mixR += conv(R, np.roll(ir, 37)) * .05
# glue: soft clip + normalise to -1 dBFS peak, gentle RMS target
st = np.stack([mixL, mixR])
st = np.tanh(st / np.max(np.abs(st)) * 1.2)
st = st / np.sqrt(np.mean(st ** 2)) * 10 ** (-19 / 20)
st = st / max(1, np.max(np.abs(st)) / 10 ** (-1 / 20))
fade = int(.3 * SR); st[:, -fade:] *= np.linspace(1, 0, fade)
st[:, :int(.004 * SR)] *= np.linspace(0, 1, int(.004 * SR))
pcm = (st.T * 32767).astype(np.int16)
with wave.open('audio/musique.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', pcm.shape, 'rms dBFS', 20 * np.log10(np.sqrt(np.mean(st ** 2))))
