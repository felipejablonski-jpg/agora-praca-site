#!/usr/bin/env python3
"""Reel narrado: oceano em recorde, El Niño acima de 1997 e 2015 e como se proteger do calor (3/11/2026).

Narração: voz "Pedro" (Gemini Charon, pt-BR) do AnyToSpeech, em seis trechos. Cada cena dura exatamente o
trecho de narração correspondente (DUR), e a assinatura fecha sem narração.
Gera video/oceano-recorde-mudo.mp4 (só imagem) e video/oceano-recorde.jpg (capa).
A mixagem com a narração sai em video/oceano-recorde.mp4.
Uso: python3 _src/reels/oceano_recorde.py [teste <cena> <t> <saida.jpg>]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calor_votacao as R  # noqa: E402
from calor_votacao import (Image, ImageDraw, W, H, M, INK, RED, RED2, WHITE, LIGHT, GREY,  # noqa: E402
                           fonte, ease, texto_rico, topo, foto_kb, degradar, fundo, cena6)

R.TAG = "CIÊNCIA · CLIMA"
R.FONTES_FIM = "Fontes: Copernicus, NOAA, OMM, Painel El Niño e Ministério da Saúde"

# duração de cada trecho da narração (s), medida com ffprobe
DUR = [12.528, 12.504, 9.864, 9.216, 11.928, 13.488]
ORANGE = (240, 106, 52)
BLUE = (90, 160, 230)


def entra(t, t0, d=0.45):
    return ease((t - t0) / d)


def escurecer(im, a):
    cam = Image.new("RGBA", im.size, INK + (int(255 * a),))
    im.alpha_composite(cam)


def num_br(x, casas=2):
    return f"{x:.{casas}f}".replace(".", ",")


# ---------- 1. o oceano em recorde ----------
def c1(t, dur):
    im = fundo()
    if t < 3.6:
        im.alpha_composite(foto_kb("img/fotos/oceano-ondas.jpg", t, 3.6, H, z0=1.0, z1=1.08), (0, 0))
        topo(im, "Foto ilustrativa: Pexels")
        a = entra(t, 0, 0.35)
        texto_rico(im, (M, 1080), "O oceano do planeta nunca esteve *tão quente*", fonte("serif", 104), W - 2 * M,
                   alpha=a, dy=int(40 * (1 - a)))
        return im
    t2 = t - 3.6
    im.alpha_composite(foto_kb("img/fotos/oceano-ondas.jpg", t, dur, 760, z0=1.08, z1=1.14), (0, 0))
    topo(im, "Fonte: Copernicus (C3S), oceano entre 60°S e 60°N")
    d = ImageDraw.Draw(im)
    a = entra(t2, 0, 0.35)
    f = fonte("sans-b", 34)
    x = M
    for ch in "SUPERFÍCIE DO MAR · MÉDIA DE SETEMBRO":
        d.text((x, 720 + int(20 * (1 - a))), ch, font=f, fill=GREY + (int(255 * a),)); x += d.textlength(ch, font=f) + 2
    v = 20.0 + 1.05 * ease((t2 - 1.6) / 1.4)
    d.text((M - 8, 760), num_br(v) + "°C", font=fonte("serif", 260), fill=RED2)
    b = entra(t2, 5.6)
    y = texto_rico(im, (M, 1100), "*Recorde* para o mês", fonte("serif", 96), W - 2 * M, alpha=b, dy=int(30 * (1 - b)))
    # comparação com o recorde anterior
    c = entra(t2, 6.4, 0.6)
    if c > 0:
        cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(cam)
        y0 = y + 70
        full = W - 2 * M
        for i, (rot, val, cor) in enumerate([("Setembro de 2023 (recorde anterior)", 20.92, GREY),
                                              ("Setembro de 2026", 21.05, RED2)]):
            yy = y0 + i * 150
            al = int(255 * c)
            dc.text((M, yy), rot, font=fonte("sans", 36), fill=LIGHT + (al,))
            frac = (val - 20.0) / 1.2 * ease((t2 - 6.4 - i * 0.3) / 0.8)
            dc.rectangle((M, yy + 52, M + int(full * 0.82 * frac), yy + 100), fill=cor + (al,))
            dc.text((M + int(full * 0.82 * frac) + 18, yy + 52), num_br(val) + "°C", font=fonte("sans-b", 40),
                    fill=WHITE + (al,))
        im.alpha_composite(cam)
    return im


# ---------- 2. o El Niño estoura o gráfico ----------
BARRAS = [("1997", 2.2, GREY, 0.5), ("2015", 2.4, GREY, 1.3), ("2026", 3.6, RED2, 2.6)]


def c2(t, dur):
    im = fundo()
    topo(im, "Dados: NOAA OISST v2.1, base 1971 a 2000 · Cálculo: Agora Praça")
    a = entra(t, 0, 0.35)
    y = texto_rico(im, (M, 270), "Pacífico central: quanto a água estava *acima do normal*", fonte("serif", 74),
                   W - 2 * M, alpha=a, dy=int(30 * (1 - a)))
    b = entra(t, 0.4)
    texto_rico(im, (M, y + 20), "No mesmo dia do ano, 18 de outubro, nos três maiores El Niños das últimas décadas",
               fonte("sans", 36), W - 2 * M, cor=LIGHT, alpha=b)
    # altura de cada barra no tempo
    alturas = [val * ease((t - t0) / (1.0 if nome != "2026" else 2.0)) for nome, val, _, t0 in BARRAS]
    # o eixo começa em 3 °C e cresce quando a barra de 2026 passa do topo
    topo_eixo = min(4.0, max(3.0, alturas[2] + 0.4))
    base_y, alto_y = 1620, 760
    esc = (base_y - alto_y) / topo_eixo
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(cam)
    fg = fonte("sans", 30)
    for g in range(0, 5):
        if g > topo_eixo + 0.01:
            continue
        yy = base_y - g * esc
        d.line((M + 90, yy, W - M, yy), fill=(70, 68, 64, 255), width=2)
        d.text((M, yy - 18), f"+{g}°C" if g else "0", font=fg, fill=GREY + (255,))
    larg = 190
    xs = [M + 170, M + 170 + 280, M + 170 + 560]
    for (nome, val, cor, t0), h, x in zip(BARRAS, alturas, xs):
        if h <= 0:
            continue
        top = base_y - h * esc
        d.rectangle((x, top, x + larg, base_y), fill=cor + (255,))
        d.text((x + larg / 2, base_y + 46), nome, font=fonte("sans-b", 44), fill=WHITE + (255,), anchor="mm")
        d.text((x + larg / 2, top - 44), "+" + num_br(h, 1) + "°C", font=fonte("sans-b", 48),
               fill=(RED2 if nome == "2026" else WHITE) + (255,), anchor="mm")
    # aviso de que o gráfico precisou crescer
    c = entra(t, 4.6, 0.5)
    if c > 0:
        al = int(255 * c)
        d.text((M, 1740), "O gráfico precisou de mais espaço", font=fonte("sans-b", 44), fill=RED2 + (al,))
    im.alpha_composite(cam)
    return im


# ---------- 3. pico em dezembro, recorde em 2027 ----------
def c3(t, dur):
    im = fundo()
    im.alpha_composite(foto_kb("img/fotos/sol-forte-horizonte.jpg", t, dur, H, foco=(0.2, 0.5), z0=1.02, z1=1.12), (0, 0))
    escurecer(im, 0.25)
    topo(im, "Fontes: OMM e NOAA · Foto ilustrativa: Pexels")
    a = entra(t, 0, 0.35)
    y = texto_rico(im, (M, 760), "Pico previsto: *dezembro*", fonte("serif", 100), W - 2 * M, alpha=a, dy=int(30 * (1 - a)))
    b = entra(t, 2.2)
    y = texto_rico(im, (M, y + 30), "Depois, o calor passa do oceano para o ar", fonte("sans", 48), W - 2 * M,
                   cor=LIGHT, alpha=b, dy=int(30 * (1 - b)))
    c = entra(t, 5.4)
    texto_rico(im, (M, y + 80), "*2027* pode ser o ano mais quente já registrado", fonte("serif", 96), W - 2 * M,
               alpha=c, dy=int(40 * (1 - c)))
    return im


# ---------- 4. o que vem para o Brasil ----------
LINHAS = [("NORTE E NORDESTE", "seca e risco de fogo", ORANGE, 0.0),
          ("SUL", "chuva acima da média e cheias", BLUE, 4.6),
          ("QUASE TODO O PAÍS", "calor acima do normal", RED2, 6.4)]


def c4(t, dur):
    im = fundo()
    im.alpha_composite(foto_kb("img/fotos/sol-cidade-laranja.jpg", t, dur, 700, foco=(0.5, 0.3), z0=1.0, z1=1.08), (0, 0))
    topo(im, "Fonte: Painel El Niño (Inmet e mais seis órgãos federais) · Foto ilustrativa: Pexels")
    a = entra(t, 0, 0.35)
    y = texto_rico(im, (M, 560), "O que a previsão diz para o Brasil", fonte("serif", 84), W - 2 * M, alpha=a,
                   dy=int(30 * (1 - a))) + 50
    for reg, txt, cor, t0 in LINHAS:
        b = entra(t, t0 + 0.2)
        if b > 0:
            cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dc = ImageDraw.Draw(cam)
            dy = int(24 * (1 - b))
            dc.rectangle((M, y + dy, M + 16, y + 190 + dy), fill=cor + (int(255 * b),))
            im.alpha_composite(cam)
            texto_rico(im, (M + 48, y + 8), reg, fonte("sans-b", 40), W - 2 * M - 48, cor=cor, alpha=b, dy=dy)
            texto_rico(im, (M + 48, y + 64), txt, fonte("serif", 66), W - 2 * M - 48, alpha=b, dy=dy)
        y += 280
    return im


# ---------- 5. onda de calor mata ----------
def c5(t, dur):
    im = fundo()
    im.alpha_composite(foto_kb("img/fotos/fonte-bratislava-verao.jpg", t, dur, 900, foco=(0.55, 0.6), z0=1.0, z1=1.08), (0, 0))
    topo(im, "Foto ilustrativa: Pexels")
    a = entra(t, 0, 0.35)
    y = texto_rico(im, (M, 760), "Onda de calor *mata*", fonte("serif", 120), W - 2 * M, alpha=a, dy=int(40 * (1 - a))) + 30
    for txt, t0 in [("Idosos", 2.3), ("Crianças", 3.9), ("Quem trabalha no sol", 4.9)]:
        b = entra(t, t0)
        y2 = texto_rico(im, (M + 46, y), txt, fonte("sans-b", 54), W - 2 * M - 46, alpha=b, dy=int(20 * (1 - b)))
        if b > 0:
            cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(cam).rectangle((M, y + 22, M + 20, y + 42), fill=RED2 + (int(255 * b),))
            im.alpha_composite(cam)
        y = y2 + 14
    c = entra(t, 6.7, 0.5)
    if c > 0:
        cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(cam).rectangle((M - 20, y + 30, W - M + 20, y + 330), fill=(48, 46, 43, int(255 * c)))
        im.alpha_composite(cam)
        yy = texto_rico(im, (M + 10, y + 60), "*Calor com umidade* é o mais perigoso", fonte("serif", 58), W - 2 * M - 20, alpha=c)
        texto_rico(im, (M + 10, yy + 14), "O suor não consegue resfriar o corpo", fonte("sans", 44), W - 2 * M - 20,
                   cor=LIGHT, alpha=entra(t, 9.1))
    return im


# ---------- 6. como se proteger ----------
ITENS = [("Beba água mesmo sem sede", 0.0), ("Evite o sol das 10h às 16h", 2.3),
         ("Fique de olho em quem mora sozinho", 5.1),
         ("Tontura, náusea, dor de cabeça e fraqueza no calor: *procure atendimento*", 7.2)]


def c6(t, dur):
    im = fundo()
    im.alpha_composite(foto_kb("img/fotos/fila-onibus-tania-rego-abr.jpg", t, dur, 620, foco=(0.5, 0.35), z0=1.0, z1=1.08), (0, 0))
    topo(im, "Fonte: Ministério da Saúde · Foto: Tânia Rêgo/Agência Brasil")
    a = entra(t, 0, 0.3)
    y = texto_rico(im, (M, 560), "Para se proteger", fonte("serif", 100), W - 2 * M, alpha=a, dy=int(30 * (1 - a))) + 40
    for txt, t0 in ITENS:
        b = entra(t, t0 + 0.15, 0.4)
        if b > 0:
            cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(cam).rectangle((M, y + 24 + int(20 * (1 - b)), M + 20, y + 44 + int(20 * (1 - b))),
                                          fill=RED2 + (int(255 * b),))
            im.alpha_composite(cam)
        y = texto_rico(im, (M + 50, y), txt, fonte("sans", 52), W - 2 * M - 50, alpha=b, dy=int(20 * (1 - b)), entre=1.25) + 40
    return im


CENAS = [(c1, DUR[0]), (c2, DUR[1]), (c3, DUR[2]), (c4, DUR[3]), (c5, DUR[4]), (c6, DUR[5]), (cena6, 2.2)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        fn = {f.__name__: f for f, _ in CENAS}[sys.argv[2]]
        dur = dict((f.__name__, d) for f, d in CENAS)[sys.argv[2]]
        fn(float(sys.argv[3]), dur).convert("RGB").save(sys.argv[4])
    else:
        R.render(CENAS, "oceano-recorde-mudo", c1, t_capa=2.8)
        os.replace(os.path.join(R.RAIZ, "video", "oceano-recorde-mudo.jpg"), os.path.join(R.RAIZ, "video", "oceano-recorde.jpg"))
