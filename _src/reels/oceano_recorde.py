#!/usr/bin/env python3
"""Reel narrado: oceano bate recorde há 152 dias seguidos, El Niño acima de 1997 e 2015, calor e proteção (3/11/2026).

Versão 2. Fundo em vídeo (Pexels, uso livre) e gráficos de linha com dados reais do NOAA OISST v2.1,
na série diária do Climate Reanalyzer (Universidade do Maine). Narração: voz "Pedro" (Gemini Charon,
pt-BR) do AnyToSpeech, em sete trechos; cada cena dura exatamente o seu trecho.

Uso: python3 _src/reels/oceano_recorde.py <pasta-de-trabalho>
A pasta precisa ter: sst.json e nino.json (Climate Reanalyzer, json_2clim), v/<id>.mp4 (vídeos Pexels)
e a1.mp3, a2.mp3, n2..n6.mp3 (narração). Saída: <pasta>/oceano-recorde.mp4 e oceano-recorde.jpg.
Teste de um quadro: python3 oceano_recorde.py <pasta> teste <cena> <t> <saida.jpg>
"""
import os, sys, json, math, subprocess, shutil, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calor_votacao as R  # noqa: E402
from calor_votacao import (Image, ImageDraw, W, H, M, INK, RED, RED2, WHITE, LIGHT, GREY,  # noqa: E402
                           fonte, ease, topo, fundo, cena6, quebrar)

R.TAG = "CIÊNCIA · CLIMA"
R.FONTES_FIM = "Fontes: NOAA, Climate Reanalyzer, OMM, Painel El Niño e Ministério da Saúde"
PASTA = sys.argv[1] if len(sys.argv) > 1 else "."
FPS = 30
AUDIOS = ["a1", "a2", "n2", "n3", "n4", "n5", "n6"]
DUR = [8.184, 10.464, 12.504, 9.864, 9.216, 11.928, 13.488, 2.2]
YELLOW = (236, 216, 92); ORANGE = (240, 150, 40); GREEN = (120, 190, 110); BLUE = (110, 150, 205)


# ---------- texto alinhado: a borda esquerda da tinta cai exatamente em x ----------
def escreve(cam, x, y, txt, f, cor, alpha=1.0, ancora="esq"):
    d = ImageDraw.Draw(cam)
    bb = f.getbbox(txt)
    if ancora == "esq":
        xx = x - bb[0]
    elif ancora == "dir":
        xx = x - bb[2]
    else:
        xx = x - (bb[0] + bb[2]) / 2
    d.text((xx, y), txt, font=f, fill=cor + (int(255 * alpha),))
    return y + f.size


def bloco(cam, x, y, txt, f, cor=WHITE, destaque=RED2, alpha=1.0, entre=1.14, maxw=W - 2 * M, dy=0):
    """Parágrafo com quebra; *trecho* em destaque. Borda esquerda alinhada em x. Devolve o y final."""
    d = ImageDraw.Draw(cam)
    a = int(255 * alpha)
    y += dy
    for linha in quebrar(d, txt, f, maxw):
        limpa = linha.replace("*", "")
        xx = x - f.getbbox(limpa)[0]
        dentro = False
        for i, pal in enumerate(linha.split(" ")):
            if pal.startswith("*"):
                dentro = True
            s = pal.strip("*") + (" " if i < len(linha.split(" ")) - 1 else "")
            d.text((xx, y), s, font=f, fill=(destaque if dentro else cor) + (a,))
            xx += d.textlength(s, font=f)
            if pal.endswith("*"):
                dentro = False
        y += int(f.size * entre)
    return y - dy


def entra(t, t0, d=0.4):
    return ease((t - t0) / d)


def sombra(cam, y0, y1, forte=0.85):
    """Degradê escuro para leitura sobre o vídeo, de y0 (transparente) a y1 (escuro)."""
    d = ImageDraw.Draw(cam)
    passo = 1 if y1 > y0 else -1
    n = abs(y1 - y0)
    for i, y in enumerate(range(y0, y1, passo)):
        d.line((0, y, W, y), fill=INK + (int(255 * forte * (i / n) ** 1.3),))


# ---------- dados ----------
def carregar():
    base = {}
    for nome in ("sst", "nino"):
        d = {x["name"]: x["data"] for x in json.load(open(os.path.join(PASTA, nome + ".json")))}
        y = list(d["2026"])
        for i, v in enumerate(d.get("Preliminary", [])):
            if v is not None:
                y[i] = v
        d["2026"] = y
        base[nome] = d
    return base


DADOS = None


def serie(nome, ano, clim):
    d = DADOS[nome]
    c = d[clim]
    out = []
    for i, v in enumerate(d[ano]):
        out.append(None if v is None or i >= len(c) or c[i] is None else v - c[i])
    return out


# ---------- gráfico de linhas ----------
class Grafico:
    def __init__(self, caixa, ymin):
        self.x0, self.y0, self.x1, self.y1 = caixa
        self.ymin = ymin

    def px(self, i, v, ymax):
        x = self.x0 + (self.x1 - self.x0) * i / 365
        y = self.y1 - (self.y1 - self.y0) * (v - self.ymin) / (ymax - self.ymin)
        return x, y

    def eixo(self, cam, ymax, passo, fmt, alpha=1.0):
        d = ImageDraw.Draw(cam)
        f = fonte("sans", 28)
        v = math.ceil(self.ymin / passo) * passo
        while v <= ymax + 1e-6:
            _, y = self.px(0, v, ymax)
            d.line((self.x0, y, self.x1, y), fill=(255, 255, 255, int(38 * alpha)), width=2)
            escreve(cam, self.x1 + 14, y - 16, fmt(v), f, GREY, alpha)
            v += passo
        for k, mes in enumerate(["JAN", "MAR", "MAI", "JUL", "SET", "NOV"]):
            dia = [0, 59, 120, 181, 243, 304][k]
            x, _ = self.px(dia, self.ymin, ymax)
            escreve(cam, x, self.y1 + 18, mes, fonte("sans-b", 26), GREY, alpha)

    def linha(self, cam, s, ymax, cor, larg, ate=366, alpha=1.0):
        pts = [self.px(i, v, ymax) for i, v in enumerate(s[:int(ate)]) if v is not None]
        if len(pts) > 1:
            ImageDraw.Draw(cam).line(pts, fill=cor + (int(255 * alpha),), width=larg, joint="curve")
        return pts[-1] if pts else None


def ponto(cam, xy, cor, r=11):
    d = ImageDraw.Draw(cam)
    x, y = xy
    d.ellipse((x - r - 6, y - r - 6, x + r + 6, y + r + 6), fill=cor + (70,))
    d.ellipse((x - r, y - r, x + r, y + r), fill=cor + (255,))


# ---------- fundos em vídeo ----------
# cena -> lista de (início na cena, id do vídeo, segundo inicial no vídeo, foco horizontal 0..1)
FUNDOS = {
    0: [(0, "34620659", 2.0, 0.5)],
    3: [(0, "4023788", 0.0, 0.55)],
    4: [(0, "37533724", 6.0, 0.5), (2.2, "33660410", 3.0, 0.5), (4.5, "35675329", 1.0, 0.5),
        (6.3, "26051251", 0.0, 0.45)],
    5: [(0, "26051251", 4.0, 0.6)],
    6: [(0, "4023788", 6.0, 0.35)],
}
_CACHE = {}


def quadro_video(vid, seg, foco):
    pasta = os.path.join(PASTA, "q", f"{vid}_{seg:.2f}_{foco}")
    if pasta not in _CACHE:
        if not os.path.isdir(pasta):
            os.makedirs(pasta)
            src = os.path.join(PASTA, "v", vid + ".mp4")
            vf = (f"scale=-2:1920:flags=lanczos,crop=1080:1920:(iw-1080)*{foco}:0,fps={FPS},"
                  "eq=saturation=1.08:contrast=1.04")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-ss", str(seg), "-i", src,
                            "-t", "16", "-vf", vf, "-q:v", "3", os.path.join(pasta, "%04d.jpg")], check=True)
        _CACHE[pasta] = sorted(os.listdir(pasta))
    return pasta, _CACHE[pasta]


def fundo_cena(k, t):
    if k not in FUNDOS:
        return fundo()
    ini, vid, seg, foco = [f for f in FUNDOS[k] if f[0] <= t][-1]
    pasta, lista = quadro_video(vid, seg, foco)
    i = min(int((t - ini) * FPS), len(lista) - 1)
    return Image.open(os.path.join(pasta, lista[i])).convert("RGBA")


# ---------- cenas ----------
def s1(t, dur):
    """Gancho: 152 dias seguidos de recorde."""
    im = fundo_cena(0, t)
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sombra(cam, 560, 1500, 0.9)
    ImageDraw.Draw(cam).rectangle((0, 1500, W, H), fill=INK + (230,))
    im.alpha_composite(cam)
    topo(im, "Vídeo ilustrativo: Pexels · Dados: NOAA OISST, via Climate Reanalyzer")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    n = int(round(152 * ease(t / 1.3)))
    escreve(cam, M, 760, str(n), fonte("serif", 420), RED2)
    escreve(cam, M, 1250, "DIAS SEGUIDOS DE RECORDE", fonte("sans-b", 54), WHITE)
    a = entra(t, 0.9)
    y = bloco(cam, M, 1350, "de calor no oceano do planeta", fonte("serif", 84), alpha=a, dy=int(24 * (1 - a)))
    b = entra(t, 5.3)
    bloco(cam, M, y + 40, "Todos os dias desde 3 de junho, segundo dados da NOAA até 1º de novembro",
          fonte("sans", 40), LIGHT, alpha=b, dy=int(20 * (1 - b)))
    im.alpha_composite(cam)
    return im


def s2(t, dur):
    """Linhas: cada ano desde 1982; 2026 em vermelho estoura o gráfico."""
    im = fundo()
    topo(im, "Dados: NOAA OISST v2.1, via Climate Reanalyzer · Gráfico: Agora Praça")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    y = bloco(cam, M, 260, "Temperatura do mar no planeta, *ano a ano*", fonte("serif", 72))
    bloco(cam, M, y + 10, "Diferença para a média de 1982 a 2010, em °C (oceano entre 60°S e 60°N)",
          fonte("sans", 34), LIGHT)
    g = Grafico((M, 700, W - M - 110, 1560), -0.4)
    # quanto de cada coisa já entrou
    anos = [str(a) for a in range(1982, 2023)]
    n_anos = len(anos) * ease(t / 2.6)
    p23 = entra(t, 2.6, 0.9); p26 = ease((t - 3.4) / 3.6)
    visiveis = [serie("sst", a, "1982-2010") for a in anos[:int(math.ceil(n_anos))]]
    if p23 > 0:
        visiveis += [serie("sst", a, "1982-2010") for a in ("2023", "2024", "2025")]
    s26 = serie("sst", "2026", "1982-2010")
    ult = max(i for i, v in enumerate(s26) if v is not None)
    ate26 = (ult + 1) * p26
    mx = max([v for s in visiveis for v in s if v is not None] + [0.4])
    if ate26 > 1:
        mx = max(mx, max(v for v in s26[:int(ate26)] if v is not None))
    ymax = mx + 0.12
    g.eixo(cam, ymax, 0.2, lambda v: f"{v:+.1f}".replace(".", ",").replace("+0,0", "0").replace("-0,0", "0"))
    for i, a in enumerate(anos[:int(math.ceil(n_anos))]):
        al = min(1.0, n_anos - i)
        tom = 0.35 + 0.65 * i / len(anos)
        cor = tuple(int(BLUE[j] * tom + 40 * (1 - tom)) for j in range(3))
        g.linha(cam, serie("sst", a, "1982-2010"), ymax, cor, 2, alpha=0.75 * al)
    if p23 > 0:
        for a, cor in (("2023", YELLOW), ("2024", ORANGE), ("2025", GREEN)):
            g.linha(cam, serie("sst", a, "1982-2010"), ymax, cor, 4, ate=366 * p23)
    fim = None
    if ate26 > 1:
        fim = g.linha(cam, s26, ymax, RED2, 8, ate=ate26)
        ponto(cam, fim, RED2)
    # legenda alinhada à esquerda
    fl = fonte("sans-b", 30)
    x = M
    for rot, cor, t0 in (("1982 a 2022", BLUE, 0), ("2023", YELLOW, 2.6), ("2024", ORANGE, 2.6),
                         ("2025", GREEN, 2.6), ("2026", RED2, 3.4)):
        al = entra(t, t0)
        if al <= 0:
            continue
        ImageDraw.Draw(cam).rectangle((x, 1672, x + 34, 1680), fill=cor + (int(255 * al),))
        escreve(cam, x + 46, 1660, rot, fl, WHITE, al)
        x += 46 + int(fl.getlength(rot)) + 40
    c = entra(t, 7.0, 0.5)
    if c > 0 and fim:
        v = s26[ult]
        escreve(cam, M, 1740, "O gráfico precisou crescer para caber 2026", fonte("sans-b", 40), RED2, c)
        escreve(cam, int(fim[0]) - 24, int(fim[1]) - 92, f"+{v:.2f}".replace(".", ",") + "°C",
                fonte("sans-b", 44), WHITE, c, ancora="dir")
    im.alpha_composite(cam)
    return im


def s3(t, dur):
    """El Niño: 2026 contra 1997 e 2015."""
    im = fundo()
    topo(im, "Dados: NOAA OISST v2.1, via Climate Reanalyzer · Gráfico: Agora Praça")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    y = bloco(cam, M, 260, "El Niño: a água do Pacífico central *acima do normal*", fonte("serif", 72))
    bloco(cam, M, y + 10, "Região Niño 3.4, diferença para a média de 1991 a 2020, em °C", fonte("sans", 34), LIGHT)
    g = Grafico((M, 760, W - M - 110, 1560), -1.0)
    s97 = serie("nino", "1997", "1991-2020"); s15 = serie("nino", "2015", "1991-2020")
    s26 = serie("nino", "2026", "1991-2020")
    ult = max(i for i, v in enumerate(s26) if v is not None)
    pv = ease(t / 1.6); p26 = ease((t - 1.4) / 3.2)
    ate26 = (ult + 1) * p26
    mx = max(v for v in s97 + s15 if v is not None)
    if ate26 > 1:
        mx = max(mx, max(v for v in s26[:int(ate26)] if v is not None))
    ymax = max(3.0, mx + 0.25)
    g.eixo(cam, ymax, 1.0, lambda v: f"{v:+.0f}".replace("+0", "0").replace("-0", "0"))
    # linha do recorde anterior (pico de 2015)
    pico15 = max(v for v in s15 if v is not None)
    _, yr = g.px(0, pico15, ymax)
    ImageDraw.Draw(cam).line((g.x0, yr, g.x1, yr), fill=YELLOW + (int(150 * pv),), width=2)
    destaque97 = 1 + 0.6 * max(0, 1 - abs(t - 9.8) / 0.8)
    destaque15 = 1 + 0.6 * max(0, 1 - abs(t - 11.6) / 0.8)
    e97 = g.linha(cam, s97, ymax, (150, 146, 138), int(4 * destaque97), ate=366 * pv)
    e15 = g.linha(cam, s15, ymax, YELLOW, int(4 * destaque15), ate=366 * pv)
    fim = None
    if ate26 > 1:
        fim = g.linha(cam, s26, ymax, RED2, 8, ate=ate26)
        ponto(cam, fim, RED2)
    fl = fonte("sans-b", 34)
    if pv > 0.95:
        escreve(cam, int(e97[0]) - 10, int(e97[1]) + 10, "1997", fl, LIGHT, 1, ancora="dir")
        escreve(cam, int(e15[0]) - 10, int(e15[1]) - 52, "2015", fl, YELLOW, 1, ancora="dir")
    c = entra(t, 4.6)
    if c > 0 and fim:
        v = s26[ult]
        escreve(cam, int(fim[0]) - 24, int(fim[1]) - 92, f"2026: +{v:.1f}".replace(".", ",") + "°C",
                fonte("sans-b", 46), RED2, c, ancora="dir")
        escreve(cam, M, 1700, "Mais quente que os El Niños de 1997 e 2015", fonte("sans-b", 40), WHITE, entra(t, 6.6))
        escreve(cam, M, 1756, "na mesma época do ano", fonte("sans-b", 40), WHITE, entra(t, 6.6))
    im.alpha_composite(cam)
    return im


def texto_sobre_video(im, linhas, credito):
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sombra(cam, 520, 1300, 0.92)
    ImageDraw.Draw(cam).rectangle((0, 1300, W, H), fill=INK + (235,))
    im.alpha_composite(cam)
    topo(im, credito)


def s4(t, dur):
    im = fundo_cena(3, t)
    texto_sobre_video(im, None, "Fontes: OMM e NOAA · Vídeo ilustrativo: Pexels")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    a = entra(t, 0, 0.3)
    y = bloco(cam, M, 900, "Pico previsto: *dezembro*", fonte("serif", 100), alpha=a, dy=int(24 * (1 - a)))
    b = entra(t, 2.2)
    y = bloco(cam, M, y + 24, "Depois, o calor passa do mar para o ar", fonte("sans", 48), LIGHT, alpha=b, dy=int(20 * (1 - b)))
    c = entra(t, 5.4)
    bloco(cam, M, y + 70, "*2027* pode ser o ano mais quente já registrado", fonte("serif", 92), alpha=c, dy=int(30 * (1 - c)))
    im.alpha_composite(cam)
    return im


REGIOES = [(0.0, "NORTE E NORDESTE", "Seca e fogo", (240, 106, 52)),
           (4.5, "SUL", "Temporais e cheias", (90, 160, 230)),
           (6.3, "QUASE TODO O PAÍS", "Calor acima do normal", RED2)]


def s5(t, dur):
    im = fundo_cena(4, t)
    texto_sobre_video(im, None, "Fonte: Painel El Niño (Inmet e mais seis órgãos federais) · Vídeos ilustrativos: Pexels")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    bloco(cam, M, 960, "O que a previsão indica para o Brasil", fonte("sans-b", 44), LIGHT)
    t0, reg, txt, cor = [r for r in REGIOES if r[0] <= t][-1]
    a = entra(t, t0, 0.3)
    dy = int(24 * (1 - a))
    ImageDraw.Draw(cam).rectangle((M, 1100 + dy, M + 120, 1112 + dy), fill=cor + (int(255 * a),))
    escreve(cam, M, 1140 + dy, reg, fonte("sans-b", 50), cor, a)
    bloco(cam, M, 1220, txt, fonte("serif", 116), alpha=a, dy=dy)
    im.alpha_composite(cam)
    return im


def s6(t, dur):
    im = fundo_cena(5, t)
    texto_sobre_video(im, None, "Fonte: Ministério da Saúde · Vídeo ilustrativo: Pexels (Nova Délhi, Índia, 2024)")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    a = entra(t, 0, 0.3)
    y = bloco(cam, M, 820, "Onda de calor *mata*", fonte("serif", 130), alpha=a, dy=int(30 * (1 - a))) + 20
    fi = fonte("sans-b", 54)
    for txt, t0 in (("Idosos", 2.3), ("Crianças", 3.9), ("Quem trabalha no sol", 4.9)):
        b = entra(t, t0)
        if b > 0:
            ImageDraw.Draw(cam).rectangle((M, y + 20, M + 18, y + 38), fill=RED2 + (int(255 * b),))
            escreve(cam, M + 44, y, txt, fi, WHITE, b)
        y += 74
    c = entra(t, 6.7, 0.4)
    if c > 0:
        y += 30
        bloco(cam, M, y, "*Calor com umidade* é o mais perigoso:", fonte("serif", 60), alpha=c)
        bloco(cam, M, y + 150, "o suor não consegue resfriar o corpo", fonte("sans", 46), LIGHT, alpha=entra(t, 9.1))
    im.alpha_composite(cam)
    return im


ITENS = [("Beba água mesmo sem sede", 0.0), ("Evite o sol das 10h às 16h", 2.3),
         ("Fique de olho em quem mora sozinho", 5.1),
         ("Tontura, náusea, dor de cabeça ou fraqueza: *procure atendimento*", 7.2)]


def s7(t, dur):
    im = fundo_cena(6, t)
    texto_sobre_video(im, None, "Fonte: Ministério da Saúde · Vídeo ilustrativo: Pexels")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    a = entra(t, 0, 0.3)
    y = bloco(cam, M, 760, "Para se proteger", fonte("serif", 110), alpha=a, dy=int(24 * (1 - a))) + 30
    fi = fonte("sans", 52)
    for txt, t0 in ITENS:
        b = entra(t, t0 + 0.15)
        if b > 0:
            ImageDraw.Draw(cam).rectangle((M, y + 22, M + 18, y + 40), fill=RED2 + (int(255 * b),))
        y = bloco(cam, M + 44, y, txt, fi, alpha=b, maxw=W - 2 * M - 44, entre=1.22) + 34
    im.alpha_composite(cam)
    return im


CENAS = [s1, s2, s3, s4, s5, s6, s7, cena6]


def render():
    tmp = os.path.join(PASTA, "quadros"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    k = 0
    for fn, dur in zip(CENAS, DUR):
        for i in range(int(round(dur * FPS))):
            fn(i / FPS, dur).convert("RGB").save(os.path.join(tmp, f"{k:05d}.jpg"), quality=93)
            if fn is s1 and i == int(2.0 * FPS):
                fn(i / FPS, dur).convert("RGB").save(os.path.join(PASTA, "oceano-recorde.jpg"), quality=90)
            k += 1
    # narração: trechos em sequência + silêncio na assinatura, com tratamento de voz
    lista = os.path.join(PASTA, "lista_audio.txt")
    with open(lista, "w") as f:
        for a in AUDIOS:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PASTA, a + ".mp3"), "-ar", "48000", "-ac", "2",
                            os.path.join(PASTA, a + ".wav")], check=True)
            f.write(f"file '{os.path.join(PASTA, a + '.wav')}'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista,
                    "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=10:release=200,"
                           "loudnorm=I=-15:TP=-1.5:LRA=9,apad",
                    "-ar", "48000", "-t", f"{k / FPS:.3f}", os.path.join(PASTA, "narracao.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.jpg"),
                    "-i", os.path.join(PASTA, "narracao.wav"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19",
                    "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                    os.path.join(PASTA, "oceano-recorde.mp4")], check=True)
    print("ok", k, "quadros")


if __name__ == "__main__":
    DADOS = carregar()
    if len(sys.argv) > 2 and sys.argv[2] == "teste":
        fn = {f.__name__: f for f in CENAS}[sys.argv[3]]
        fn(float(sys.argv[4]), DUR[CENAS.index(fn)]).convert("RGB").save(sys.argv[5])
    else:
        render()
