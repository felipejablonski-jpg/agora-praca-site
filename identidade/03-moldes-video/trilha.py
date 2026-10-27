import sys, json
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
DUR = float(sys.argv[2]); CUTS = json.loads(sys.argv[3])  # cortes entre cenas; o último é a assinatura
N = int(SR * DUR)
rng = np.random.default_rng(11)
t = np.arange(N) / SR
L = np.zeros(N); Rt = np.zeros(N)


def add(x, start, gain=1.0, pan=0.0):
    i = int(start * SR); j = min(N, i + len(x))
    if j <= i: return
    seg = x[: j - i] * gain
    L[i:j] += seg * np.sqrt((1 - pan) / 2) * 1.414
    Rt[i:j] += seg * np.sqrt((1 + pan) / 2) * 1.414


def env_adsr(n, a, r):
    e = np.ones(n); na = int(a * SR); nr = int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e

# 1) Fundo: acorde grave em lá menor, com batimento lento e ruído marrom filtrado
pad = np.zeros(N)
for f, g in [(55.0, .55), (55.35, .35), (82.41, .32), (82.0, .2), (130.81, .10), (110.0, .14)]:
    pad += g * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28))
lfo = 0.75 + 0.25 * np.sin(2 * np.pi * 0.11 * t)
brown = np.cumsum(rng.normal(0, 1, N)); brown -= signal.savgol_filter(brown, 48001, 1)
brown = signal.sosfilt(signal.butter(2, [40, 260], 'band', fs=SR, output='sos'), brown)
brown /= np.abs(brown).max()
xs = [0, .5] + CUTS + [min(DUR - .2, CUTS[-1] + .9), DUR]
ys = [0, .55] + [.6 + .15 * i / max(1, len(CUTS) - 1) for i in range(len(CUTS))] + [.4, 0]
intens = np.interp(t, xs, ys)
bed = (pad * lfo * 0.16 + brown * 0.06) * intens
L += bed; Rt += bed * 0.97

# 2) Impacto grave: varredura senoidal + transiente abafado
def impact(depth=1.0, length=2.2):
    n = int(length * SR); tt = np.arange(n) / SR
    f = 38 + 70 * np.exp(-tt * 9)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-tt * (2.2 / depth))
    nz = signal.sosfilt(signal.butter(2, 900, 'low', fs=SR, output='sos'), rng.normal(0, 1, n)) * np.exp(-tt * 28)
    return (body * 0.9 + nz * 0.35) * env_adsr(n, 0.004, 0.2)

# 3) Sopro (zoom): ruído com filtro passa-banda que varre
def whoosh(length, f0=250, f1=2200, f2=500, peak=0.6):
    n = int(length * SR); x = rng.normal(0, 1, n); out = np.zeros(n); blk = 1024
    zi = None
    for k in range(0, n, blk):
        u = k / n
        fc = f0 + (f1 - f0) * (u / peak) if u < peak else f1 + (f2 - f1) * ((u - peak) / (1 - peak))
        sos = signal.butter(2, [fc * 0.6, fc * 1.5], 'band', fs=SR, output='sos')
        if zi is None: zi = np.zeros((sos.shape[0], 2))
        out[k:k + blk], zi = signal.sosfilt(sos, x[k:k + blk], zi=zi)
    e = np.where(np.linspace(0, 1, n) < peak, (np.linspace(0, 1, n) / peak) ** 2, ((1 - np.linspace(0, 1, n)) / (1 - peak)) ** 1.5)
    return out / np.abs(out).max() * e

# 4) Pulso tonal grave para cada província
def pulse(f=98.0, length=0.9, bright=0.25):
    n = int(length * SR); tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * tt) + bright * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 9)
    return x * np.exp(-tt * 5.5) * env_adsr(n, 0.006, 0.1)

# 5) Tique seco para o contador
def tick():
    n = int(0.012 * SR); x = rng.normal(0, 1, n) * np.exp(-np.arange(n) / SR * 600)
    return signal.sosfilt(signal.butter(2, 1800, 'high', fs=SR, output='sos'), x)


add(impact(1.2, 2.2), 0.02, 0.6)
add(pulse(73.4, 1.2, 0.3), 0.3, 0.18)
for s0 in CUTS[:-1]:
    add(whoosh(0.7), s0-0.55, 0.09); add(impact(0.8, 1.6), s0, 0.42)
add(whoosh(0.9), CUTS[-1]-0.55, 0.07); add(impact(1.0, 2.0), CUTS[-1], 0.45)
irn = int(2.4 * SR); ir = rng.normal(0, 1, irn) * np.exp(-np.arange(irn) / SR * 2.6)
ir = signal.sosfilt(signal.butter(2, 3500, 'low', fs=SR, output='sos'), ir); ir /= np.sqrt((ir ** 2).sum())
wetL = signal.fftconvolve(L, ir)[:N]; wetR = signal.fftconvolve(Rt, ir[::-1].copy() * 0 + np.roll(ir, 37))[:N]
outL = L * 0.82 + wetL * 0.28; outR = Rt * 0.82 + wetR * 0.28
fade = np.ones(N); nf = int(1.2 * SR); fade[-nf:] = np.linspace(1, 0, nf) ** 2
st = np.stack([outL * fade, outR * fade], 1)
st = signal.sosfilt(signal.butter(2, 28, 'high', fs=SR, output='sos'), st, axis=0)
st /= np.abs(st).max() / 0.89
wavfile.write(sys.argv[1], SR, (st * 32767).astype(np.int16))
print('ok')
