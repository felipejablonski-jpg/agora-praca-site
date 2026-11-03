#!/usr/bin/env python3
"""Reel narrado, versão 3: a linha do calor do oceano sobe desde o primeiro quadro (3/11/2026).

Metade do Reel é a linha de 2026 subindo, com a temperatura subindo junto; depois o El Niño, o pico,
o efeito no Brasil e a volta da linha. Dados: NOAA OISST v2.1 via Climate Reanalyzer. Vídeos: Pexels.
Narração: voz "Pedro" (Gemini Charon, pt-BR), AnyToSpeech, em seis trechos (v1..v6.mp3).

Uso: python3 _src/reels/oceano_recorde_v3.py <pasta>
A pasta precisa ter sst.json, nino.json, v1..v6.mp3 e v/<id>.mp4. Saída: <pasta>/oceano-recorde-v3.mp4 e .jpg
Teste: python3 oceano_recorde_v3.py <pasta> teste <cena> <t> <saida.jpg>
"""
import os, sys, math, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PASTA = sys.argv[1]
sys.argv = [sys.argv[0], PASTA] + sys.argv[2:]
import oceano_recorde as V  # noqa: E402  (reaproveita escrita alinhada, gráfico e fundos em vídeo)
from oceano_recorde import (Image, ImageDraw, W, H, M, INK, RED2, WHITE, LIGHT, GREY,  # noqa: E402
                            fonte, ease, topo, fundo, cena6, escreve, bloco, entra, sombra, Grafico, ponto,
                            serie, YELLOW, ORANGE, GREEN, BLUE)
import calor_votacao as R  # noqa: E402

V.PASTA = PASTA
R.TAG = "CIÊNCIA · CLIMA"
R.FONTES_FIM = "Fontes: NOAA (OISST), Climate Reanalyzer, OMM e Painel El Niño"
FPS = 30
AUDIOS = ["v1", "v2", "v3", "v4", "v5", "v6"]


def dur(a):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                          os.path.join(PASTA, a + ".mp3")]))


def pausas(a):
    """Fins de frase do trecho (meio de cada silêncio), para sincronizar o texto com a voz."""
    out = subprocess.run(["ffmpeg", "-i", os.path.join(PASTA, a + ".mp3"), "-af", "silencedetect=n=-38dB:d=0.22",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    ini = [float(l.split("silence_start: ")[1]) for l in out.splitlines() if "silence_start" in l]
    fim = [float(l.split("silence_end: ")[1].split(" ")[0]) for l in out.splitlines() if "silence_end" in l]
    return [(a + b) / 2 for a, b in zip(ini, fim)]


V.FUNDOS = {
    3: [(0, "4023788", 0.0, 0.55)],
    4: [(0, "37533724", 6.0, 0.5), (2.2, "33660410", 3.0, 0.5), (4.5, "35675329", 1.0, 0.5),
        (6.3, "37533724", 20.0, 0.3)],
}
SST = NINO = None
ULT = 0
INICIO_REC = 153  # 3 de junho (índice do dia no ano)
MESES = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
INI_MES = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def data_dia(i):
    m = max(k for k in range(12) if INI_MES[k] <= i)
    return f"{i - INI_MES[m] + 1} {MESES[m]}"


def num(v, casas=2):
    return f"{v:+.{casas}f}".replace(".", ",") + "°C"


def contador_topo(cam, valor, legenda, dia_txt, cor=RED2):
    """Temperatura grande no alto, subindo junto com a linha."""
    escreve(cam, M, 250, legenda, fonte("sans-b", 34), LIGHT)
    escreve(cam, M, 300, num(valor), fonte("serif", 190), cor)
    if dia_txt:
        escreve(cam, W - M, 330, dia_txt, fonte("sans-b", 44), WHITE, ancora="dir")
        escreve(cam, W - M, 386, "2026", fonte("sans-b", 34), GREY, ancora="dir")


def recordes(i):
    return max(0, min(i, ULT) - INICIO_REC + 1)


# ---------- 1. só a linha de 2026 subindo ----------
def s1(t, d):
    im = fundo()
    topo(im, "Dados: NOAA OISST v2.1, via Climate Reanalyzer · Gráfico: Agora Praça")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    p = ease(t / (d * 0.86)) if t < d * 0.86 else 1.0
    p = min(1.0, t / (d * 0.86)) if t < d * 0.86 else 1.0   # avanço constante dos dias
    ate = 1 + ULT * p
    i = int(ate) - 1
    vis = [v for v in SST[:int(ate)] if v is not None]
    ymin = 0.45
    ymax = max(0.72, max(vis) + 0.05)  # o eixo só cresce para cima, quando a linha encosta no topo
    g = Grafico((M, 620, W - M - 110, 1500), ymin)
    g.eixo(cam, ymax, 0.1, lambda v: f"{v:+.1f}".replace(".", ","))
    fim = g.linha(cam, SST, ymax, RED2, 9, ate=ate)
    if fim:
        ponto(cam, fim, RED2, 13)
    contador_topo(cam, SST[i], "ACIMA DA MÉDIA DE 1982 A 2010", data_dia(i))
    n = recordes(i)
    if n > 0:
        al = entra(t, 0, 0.01)
        fr = fonte("sans-b", 40)
        lr = int(fr.getbbox("RECORDE")[2] - fr.getbbox("RECORDE")[0])
        ImageDraw.Draw(cam).rectangle((M, 1588, M + lr + 44, 1652), fill=RED2 + (255,))
        escreve(cam, M + 22, 1596, "RECORDE", fr, WHITE)
        escreve(cam, M + lr + 74, 1594, f"{n} dias seguidos", fonte("sans-b", 44), WHITE, al)
    im.alpha_composite(cam)
    return im


# ---------- 2. todos os anos entram atrás ----------
def s2(t, d):
    im = fundo()
    topo(im, "Dados: NOAA OISST v2.1, via Climate Reanalyzer · Gráfico: Agora Praça")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    anos = [str(a) for a in range(1982, 2023)]
    pa = ease(t / (d * 0.45))
    pc = entra(t, d * 0.35, 0.8)
    vis = [SST[k] for k in range(ULT + 1)]
    ymin_alvo = -0.45
    ymin = min(vis) - 0.06 + (ymin_alvo - (min(vis) - 0.06)) * ease(t / 1.2)
    ymax = max(vis) + 0.06
    g = Grafico((M, 620, W - M - 110, 1500), ymin)
    g.eixo(cam, ymax, 0.2, lambda v: f"{v:+.1f}".replace(".", ",").replace("+0,0", "0").replace("-0,0", "0"))
    n = len(anos) * pa
    for k, a in enumerate(anos[:int(math.ceil(n))]):
        al = min(1.0, n - k)
        tom = 0.35 + 0.65 * k / len(anos)
        cor = tuple(int(BLUE[j] * tom + 40 * (1 - tom)) for j in range(3))
        g.linha(cam, serie("sst", a, "1982-2010"), ymax, cor, 2, alpha=0.75 * al)
    for a, cor in (("2023", YELLOW), ("2024", ORANGE), ("2025", GREEN)):
        if pc > 0:
            g.linha(cam, serie("sst", a, "1982-2010"), ymax, cor, 4, alpha=pc)
    fim = g.linha(cam, SST, ymax, RED2, 9)
    ponto(cam, fim, RED2, 13)
    contador_topo(cam, SST[ULT], "ACIMA DA MÉDIA DE 1982 A 2010", data_dia(ULT))
    fl = fonte("sans-b", 30)
    x = M
    for rot, cor, al in (("1982 a 2022", BLUE, entra(t, 0)), ("2023", YELLOW, pc), ("2024", ORANGE, pc),
                         ("2025", GREEN, pc), ("2026", RED2, 1.0)):
        if al > 0:
            ImageDraw.Draw(cam).rectangle((x, 1592, x + 34, 1600), fill=cor + (int(255 * al),))
            escreve(cam, x + 46, 1580, rot, fl, WHITE, al)
        x += 46 + int(fl.getlength(rot)) + 40
    c = entra(t, d * 0.6)
    bloco(cam, M, 1660, "Nenhum ano chegou *tão alto* nesta época", fonte("serif", 62), alpha=c)
    im.alpha_composite(cam)
    return im


# ---------- 3. El Niño: a linha do Pacífico sobe ----------
P3 = []


def s3(t, d):
    im = fundo()
    topo(im, "Dados: NOAA OISST v2.1, via Climate Reanalyzer · Gráfico: Agora Praça")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    s97 = serie("nino", "1997", "1991-2020"); s15 = serie("nino", "2015", "1991-2020")
    ult = max(k for k, v in enumerate(NINO) if v is not None)
    meio = [x for x in P3 if 0.3 < x < d - 0.3]
    t97, t15, tpico = (meio[-3], meio[-2], meio[-1]) if len(meio) >= 3 else (d * 0.55, d * 0.7, d * 0.85)
    p = min(1.0, t / max(1.0, t97 - 0.3))
    ate = 1 + ult * p
    i = int(ate) - 1
    vis = [v for v in NINO[:int(ate)] if v is not None]
    a97 = entra(t, t97 - 0.1, 0.6); a15 = entra(t, t15 - 0.1, 0.6)
    mx = max(vis + ([max(v for v in s97 if v is not None)] if a97 > 0 else []) +
             ([max(v for v in s15 if v is not None)] if a15 > 0 else []))
    ymin = min(-1.0, min(vis) - 0.2)
    ymax = max(mx + 0.3, ymin + 1.5)
    g = Grafico((M, 620, W - M - 110, 1500), ymin)
    g.eixo(cam, ymax, 1.0, lambda v: f"{v:+.0f}".replace("+0", "0").replace("-0", "0"))
    fl = fonte("sans-b", 36)
    if a97 > 0:
        e = g.linha(cam, s97, ymax, (170, 166, 158), 4, ate=366 * a97, alpha=a97)
        if a97 > 0.95:
            escreve(cam, int(e[0]) - 12, int(e[1]) + 12, "1997", fl, LIGHT, ancora="dir")
    if a15 > 0:
        e = g.linha(cam, s15, ymax, YELLOW, 4, ate=366 * a15, alpha=a15)
        if a15 > 0.95:
            escreve(cam, int(e[0]) - 12, int(e[1]) - 56, "2015", fl, YELLOW, ancora="dir")
    fim = g.linha(cam, NINO, ymax, RED2, 9, ate=ate)
    if fim:
        ponto(cam, fim, RED2, 13)
    contador_topo(cam, NINO[i], "EL NIÑO · PACÍFICO CENTRAL, ACIMA DO NORMAL", data_dia(i))
    c = entra(t, tpico)
    bloco(cam, M, 1600, "E ele ainda *não chegou no pico*", fonte("serif", 66), alpha=c)
    escreve(cam, M, 1760, "Região Niño 3.4, diferença para a média de 1991 a 2020", fonte("sans", 30), GREY)
    im.alpha_composite(cam)
    return im


# ---------- 4. pico e 2027 (vídeo) ----------
def s4(t, d):
    im = V.fundo_cena(3, t)
    V.texto_sobre_video(im, None, "Fontes: OMM e NOAA · Vídeo ilustrativo: Pexels")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    a = entra(t, 0, 0.3)
    y = bloco(cam, M, 1150, "Pico previsto: *dezembro*", fonte("serif", 100), alpha=a, dy=int(24 * (1 - a)))
    b = entra(t, 2.2)
    y = bloco(cam, M, y + 24, "Depois, o calor passa do mar para o ar", fonte("sans", 48), LIGHT, alpha=b, dy=int(20 * (1 - b)))
    c = entra(t, 5.4)
    bloco(cam, M, y + 70, "*2027* pode ser o ano mais quente já registrado", fonte("serif", 92), alpha=c, dy=int(30 * (1 - c)))
    im.alpha_composite(cam)
    return im


# ---------- 5. o que vem para o Brasil (vídeos) ----------
REGIOES = [(0.0, "NORTE E NORDESTE", "Seca e fogo", (240, 106, 52)),
           (4.5, "SUL", "Chuva demais", (90, 160, 230)),
           (6.3, "QUASE TODO O PAÍS", "Calor acima do normal", RED2)]


def s5(t, d):
    im = V.fundo_cena(4, t)
    V.texto_sobre_video(im, None, "Fonte: Painel El Niño (Inmet e mais seis órgãos federais) · Vídeos ilustrativos: Pexels")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    bloco(cam, M, 960, "A previsão para o Brasil", fonte("sans-b", 44), LIGHT)
    t0, reg, txt, cor = [r for r in REGIOES if r[0] <= t][-1]
    a = entra(t, t0, 0.3)
    dy = int(24 * (1 - a))
    ImageDraw.Draw(cam).rectangle((M, 1100 + dy, M + 120, 1112 + dy), fill=cor + (int(255 * a),))
    escreve(cam, M, 1140 + dy, reg, fonte("sans-b", 50), cor, a)
    bloco(cam, M, 1220, txt, fonte("serif", 116), alpha=a, dy=dy)
    im.alpha_composite(cam)
    return im


# ---------- 6. a linha volta ----------
def s6(t, d):
    im = s2(d, d)  # gráfico completo
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(cam).rectangle((0, 1560, W, H), fill=INK + (255,))
    im.alpha_composite(cam)
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    escreve(cam, M, 1590, str(recordes(ULT)), fonte("serif", 150), RED2)
    escreve(cam, M + 270, 1622, "DIAS SEGUIDOS", fonte("sans-b", 44), WHITE)
    escreve(cam, M + 270, 1676, "DE RECORDE", fonte("sans-b", 44), WHITE)
    c = entra(t, 2.0)
    bloco(cam, M, 1790, "E a linha *continua subindo*", fonte("serif", 58), alpha=c)
    im.alpha_composite(cam)
    return im


CENAS = [s1, s2, s3, s4, s5, s6, cena6]


def preparar():
    global SST, NINO, ULT, P3
    V.DADOS = V.carregar()
    SST = serie("sst", "2026", "1982-2010")
    NINO = serie("nino", "2026", "1991-2020")
    ULT = max(k for k, v in enumerate(SST) if v is not None)
    P3 = pausas("v3")
    return [dur(a) for a in AUDIOS] + [2.2]


def render(DUR):
    tmp = os.path.join(PASTA, "quadros3"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    k = 0
    for fn, d in zip(CENAS, DUR):
        for i in range(int(round(d * FPS))):
            q = fn(i / FPS, d).convert("RGB")
            q.save(os.path.join(tmp, f"{k:05d}.jpg"), quality=93)
            if fn is s1 and i == int(d * 0.75 * FPS):
                q.save(os.path.join(PASTA, "oceano-recorde-v3.jpg"), quality=90)
            k += 1
    lista = os.path.join(PASTA, "lista3.txt")
    with open(lista, "w") as f:
        for a in AUDIOS:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PASTA, a + ".mp3"), "-ar", "48000", "-ac", "2",
                            os.path.join(PASTA, a + ".wav")], check=True)
            f.write(f"file '{os.path.join(PASTA, a + '.wav')}'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista,
                    "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=10:release=200,"
                           "loudnorm=I=-15:TP=-1.5:LRA=9,apad",
                    "-ar", "48000", "-t", f"{k / FPS:.3f}", os.path.join(PASTA, "narracao3.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.jpg"),
                    "-i", os.path.join(PASTA, "narracao3.wav"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                    "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                    os.path.join(PASTA, "oceano-recorde-v3.mp4")], check=True)
    print("ok", k, "quadros")


if __name__ == "__main__":
    DUR = preparar()
    print("duracoes", [round(x, 2) for x in DUR], "pausas v3", [round(x, 2) for x in P3])
    if len(sys.argv) > 2 and sys.argv[2] == "teste":
        fn = {f.__name__: f for f in CENAS}[sys.argv[3]]
        fn(float(sys.argv[4]), DUR[CENAS.index(fn)]).convert("RGB").save(sys.argv[5])
    else:
        render(DUR)
