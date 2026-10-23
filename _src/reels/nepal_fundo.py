#!/usr/bin/env python3
"""Reel: fundo de perdas e danos reserva US$ 20 milhões ao Nepal (23/10/2026).

Gera video/nepal-fundo.mp4 e video/nepal-fundo.jpg. Usa as funções do Reel calor_votacao.
Uso: python3 _src/reels/nepal_fundo.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calor_votacao as R  # noqa: E402
from calor_votacao import (Image, ImageDraw, W, M, INK, RED, RED2, WHITE, LIGHT, GREY,  # noqa: E402
                           fonte, ease, texto_rico, topo, foto_kb, degradar, fundo, cena6)

R.TAG = "CLIMA · INTERNACIONAL"
R.FONTES_FIM = "Fontes: AFP, Climate Home News e USGS"


def cena1(t, dur):
    im = fundo()
    meia = 520
    dupla = Image.new("RGBA", (W, 1060), INK + (255,))
    dupla.alpha_composite(foto_kb("img/fotos/vale-rio-himalaia.jpg", t, dur, meia, caixa=(0, 0.3, 1, 0.9),
                                  foco=(0.5, 0.6), z0=1.0, z1=1.08, degrade=False), (0, 0))
    dupla.alpha_composite(foto_kb("img/fotos/nota-dolar-detalhe.jpg", t, dur, 1060 - meia, foco=(0.5, 0.3),
                                  z0=1.08, z1=1.0, degrade=False), (0, meia))
    ImageDraw.Draw(dupla).rectangle((0, meia - 3, W, meia + 3), fill=RED)
    im.alpha_composite(degradar(dupla), (0, 0))
    topo(im, "Fotos ilustrativas: Pexels")
    a = ease(t / 0.45)
    y = texto_rico(im, (M, 930), "ONU reserva *US$\u00a020\u00a0milhões* para o Nepal", fonte("serif", 96), W - 2 * M,
                   alpha=a, dy=int(40 * (1 - a)))
    b = ease((t - 0.7) / 0.45)
    texto_rico(im, (M, y + 34), "É a primeira vez que o fundo do clima separa dinheiro para um país", fonte("sans", 44),
               W - 2 * M, cor=LIGHT, alpha=b, dy=int(30 * (1 - b)))
    return im


def cena2(t, dur):
    im = fundo()
    topo(im, "Fonte: AFP")
    d = ImageDraw.Draw(im)
    a = ease(t / 0.35)
    f = fonte("sans-b", 34)
    x = M
    for ch in "MORTOS NA ENCHENTE DE AGOSTO":
        d.text((x, 520 + int(20 * (1 - a))), ch, font=f, fill=GREY + (int(255 * a),)); x += d.textlength(ch, font=f) + 2
    n = int(round(1400 * ease(t / 1.2)))
    d.text((M - 10, 560), "+" + f"{n:,}".replace(",", "."), font=fonte("serif", 300), fill=RED2)
    b = ease((t - 1.2) / 0.45)
    y = texto_rico(im, (M, 960), "e mais de *5.000* desaparecidos", fonte("serif", 88), W - 2 * M, alpha=b, dy=int(30 * (1 - b)))
    c = ease((t - 1.7) / 0.45)
    texto_rico(im, (M, y + 30), "Povoados, estradas, pontes e usinas foram destruídos", fonte("sans", 42), W - 2 * M,
               cor=LIGHT, alpha=c, dy=int(30 * (1 - c)))
    return im


def cena3(t, dur):
    im = fundo()
    im.alpha_composite(foto_kb("img/fotos/vale-rio-himalaia.jpg", t, dur, 1060, caixa=(0, 0.25, 1, 1), foco=(0.5, 0.6),
                               z0=1.0, z1=1.12), (0, 0))
    topo(im, "Fonte: USGS · Foto ilustrativa: Pexels")
    a = ease(t / 0.45)
    y = texto_rico(im, (M, 930), "Uma avalanche de gelo e rocha virou *enxurrada*", fonte("serif", 96), W - 2 * M,
                   alpha=a, dy=int(40 * (1 - a)))
    b = ease((t - 0.7) / 0.45)
    texto_rico(im, (M, y + 34), "A lama desceu cerca de 100 km pelo vale, em 26 de agosto", fonte("sans", 44), W - 2 * M,
               cor=LIGHT, alpha=b, dy=int(30 * (1 - b)))
    return im


def cena4(t, dur):
    im = fundo()
    topo(im, "Estimativa do governo do Nepal, via AFP")
    a = ease(t / 0.4)
    y = texto_rico(im, (M, 270), "Reconstruir custa *US$\u00a04,78\u00a0bilhões*", fonte("serif", 84), W - 2 * M, alpha=a,
                   dy=int(30 * (1 - a)))
    cols, total = 16, 239
    gap = 10
    lado = (W - 2 * M - gap * (cols - 1)) / cols
    y0 = y + 50
    prog = max(0.0, (t - 0.5) / 1.6) * total
    camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    for k in range(total):
        if k == 0:
            al = int(255 * ease((t - 0.3) / 0.3)); cor = RED2
        else:
            al = int(255 * max(0, min(1, prog - k))); cor = (64, 62, 58)
        if al <= 0:
            continue
        r, c = divmod(k, cols)
        x = M + c * (lado + gap); yy = y0 + r * (lado + gap)
        d.rectangle((x, yy, x + lado, yy + lado), fill=cor + (al,))
    im.alpha_composite(camada)
    yfim = y0 + 15 * (lado + gap) + 30
    b = ease((t - 2.2) / 0.45)
    texto_rico(im, (M, yfim), "Cada quadrado vale US$ 20 milhões. O fundo reservou *um*", fonte("sans", 44), W - 2 * M,
               cor=LIGHT, alpha=b, dy=int(20 * (1 - b)))
    return im


def cena5(t, dur):
    im = fundo()
    topo(im, "Fonte: Climate Home News")
    a = ease(t / 0.4)
    y = texto_rico(im, (M, 420), "O dinheiro *ainda não saiu*", fonte("serif", 104), W - 2 * M, alpha=a,
                   dy=int(30 * (1 - a))) + 50
    itens = ["O Nepal precisa apresentar uma proposta de uso",
             "Não há prazo para a aprovação",
             "Países ricos dizem que o caso não deve virar regra"]
    for i, it in enumerate(itens):
        b = ease((t - 0.5 - i * 0.55) / 0.4)
        camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(camada).rectangle((M, y + 22 + int(20 * (1 - b)), M + 18, y + 40 + int(20 * (1 - b))),
                                         fill=RED2 + (int(255 * b),))
        im.alpha_composite(camada)
        y = texto_rico(im, (M + 46, y), it, fonte("sans", 48), W - 2 * M - 46, alpha=b, dy=int(20 * (1 - b)), entre=1.3) + 40
    return im


CENAS = [(cena1, 3.0), (cena2, 3.2), (cena3, 3.0), (cena4, 3.8), (cena5, 3.2), (cena6, 2.2)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        quadros = [f(d - 0.05, d).convert("RGB").resize((360, 640)) for f, d in CENAS]
        o = Image.new("RGB", (360 * len(quadros), 640))
        for i, q in enumerate(quadros):
            o.paste(q, (i * 360, 0))
        o.save(sys.argv[2])
    else:
        R.render(CENAS, "nepal-fundo", cena1)
