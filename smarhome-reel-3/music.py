# Original score + sound design for Smar Home ad A (120 BPM, 20 s), synthesized with numpy.
# Cues follow the timeline in ad.html.  Output: out/music-a.wav (48 kHz stereo)
import numpy as np, wave

SR = 48000
DUR = 20.0
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

# ---------------------------------------------------------------- arrangement (Smar Home 3D, voice-over friendly)
# warm tropical house, 120 BPM: Fmaj7 | G6 | Em7 | Am7
CH = [(41, [57, 60, 64, 65, 69]), (43, [55, 59, 62, 64, 67]), (40, [55, 59, 62, 64, 67]), (45, [57, 60, 64, 67, 72])]
def chord_at(t): return CH[int(t // 2) % 4]
def groove(a, b, full=True):
    t = a
    while t < b - 1e-6:
        bi = int(round((t - a) / BEAT))
        add(kick(), t, .8 if full else .55)
        if full and bi % 2 == 1: add(clap(), t, .4, .1)
        add(hat(), t + BEAT / 2, .4, .3)
        for q in (0.125, 0.375): add(shaker(), t + q, .45, -.35)
        t += BEAT
# intro: pad + soft plucks, riser into the build
add(pad([53, 57, 60, 64], 3.0), 0.0, 2.6)
for st in np.arange(0.0, 3.0, 0.25):
    root, notes = chord_at(st); i = int(round(st / .25)) % 8
    add(pluck(notes[[0, 2, 1, 3, 2, 4, 3, 1][i] % 5] + 12, .5, .6), st, 1.3, (-.4 if i % 2 else .4))
add(riser(1.0), 2.0, .4); add(whoosh(.5, True), 2.55, .5)
groove(3.0, 10.8); groove(10.8, 13.8, full=False); groove(13.8, 17.0)
for bar in range(10):
    t0 = bar * 2.0; root, notes = chord_at(t0)
    if t0 + 2 <= 3.0 or t0 >= 17.0: continue
    for st in np.arange(max(t0, 3.0), min(t0 + 2, 17.0), BEAT):
        last = abs((st - t0) - 1.5) < 1e-6
        add(sub(root - 12 + (7 if last else 0), BEAT * .45), st + .25, .75)
    add(pad(notes[:4], 2.05), max(t0, 3.0), .7)
for st in np.arange(7.0, 17.0, 0.25):
    root, notes = chord_at(st); i = int(round(st / .25)) % 8
    add(pluck(notes[[0, 2, 1, 3, 2, 4, 3, 1][i] % 5] + 12, .45, 1.1 if i % 4 == 0 else .7), st, .55, (-.4 if i % 2 else .4))
# --- sound design synced to the 3D
add(whoosh(.9, False), 3.3, .55)                     # second module falls
add(impact(), 4.15, .55)                              # lands (bounce)
for i in range(18): add(pop(600 + i * 40), 4.2 + i * .045, .25, -.6 + i / 15)   # deck planks
for at in (4.1, 4.6, 5.1): add(pop(1400), at, .35)   # tags
for at in (7.0, 8.85, 13.8, 17.0): add(whoosh(.35, False), at - .05, .6); add(impact(), at, .35)   # cuts + flashes
add(whoosh(.7, True), 6.95, .45); add(whoosh(.7, True), 8.8, .45)                 # gold titles rise
for at in (7.5, 7.72, 7.94, 9.35, 9.57, 9.79): add(pop(1100), at, .4)             # size tags
add(whoosh(.6, True), 10.75, .5)                                                  # padlock spins in
tc_ = np.arange(int(.12 * SR)) / SR
clack = (spectral(rng.standard_normal(len(tc_)), 1500, 9000) * np.exp(-tc_ * 60) + np.sin(2 * np.pi * 900 * tc_) * np.exp(-tc_ * 40) * .6) * .9
add(clack, 11.95, 1.0); add(chime([72, 76, 79]), 11.97, .7)                        # shackle snaps shut
for i in range(7): add(pop(700 + i * 90), 14.15 + i * .3, .6, -.5 + i / 6); add(pluck(72 + [0, 2, 4, 7, 9, 12, 14][i], .5, .8), 14.15 + i * .3, .6)
add(impact(), 17.0, .7); add(pad([41, 53, 57, 60, 64, 69], 3.0), 17.0, 2.4); add(chime([77, 81, 84, 89]), 17.4, .6)
for st in np.arange(17.5, 19.75, 0.25):
    i = int(round(st / .25)) % 8; add(pluck([65, 69, 72, 76, 77, 76, 72, 69][i], .6, .6), st, 1.2, (-.5 if i % 2 else .5))
for st in np.arange(17.5, 19.7, BEAT): add(hat(), st + .25, .6, .3); add(shaker(), st + .125, .7, -.35); add(kick(), st, .35)
add(ui_click(), 19.0, 1.1); add(pop(1800), 19.0, .5); add(chime([84, 91]), 19.02, .5)

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
with wave.open('out/music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', pcm.shape, 'rms dBFS', 20 * np.log10(np.sqrt(np.mean(st ** 2))))
