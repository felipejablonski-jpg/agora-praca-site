#!/usr/bin/env python3
"""Reel: TSE dá 24 horas para Meta e X explicarem tratamento de Lula e Flávio (23/10/2026).

Gera video/tse-meta-x.mp4 e video/tse-meta-x.jpg. Uso: python3 _src/reels/tse_meta_x.py [teste <saida.jpg>]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calor_votacao as R  # noqa: E402
from calor_votacao import (Image, ImageDraw, W, M, INK, RED, RED2, WHITE, LIGHT, GREY,  # noqa: E402
                           fonte, ease, texto_rico, topo, foto_kb, degradar, fundo, cena6)

R.TAG = "POLÍTICA · ELEIÇÕES 2026"
R.FONTES_FIM = "Fontes: Agência Brasil, Estadão e Gazeta do Povo"
NB = " "


def lista(im, y, itens, t, t0=0.5, passo=0.55, tam=46):
    for i, it in enumerate(itens):
        b = ease((t - t0 - i * passo) / 0.4)
        camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(camada).rectangle((M, y + 22 + int(20 * (1 - b)), M + 18, y + 40 + int(20 * (1 - b))),
                                         fill=RED2 + (int(255 * b),))
        im.alpha_composite(camada)
        y = texto_rico(im, (M + 46, y), it, fonte("sans", tam), W - 2 * M - 46, alpha=b, dy=int(20 * (1 - b)), entre=1.3) + 36
    return y


def cena1(t, dur):
    im = fundo()
    meia = 520
    dupla = Image.new("RGBA", (W, 1060), INK + (255,))
    dupla.alpha_composite(foto_kb("img/fotos/predio-tse.jpg", t, dur, meia, caixa=(0.25, 0, 1, 1), foco=(0.5, 0.3),
                                  z0=1.0, z1=1.08, degrade=False), (0, 0))
    dupla.alpha_composite(foto_kb("img/fotos/celular-apps-meta.jpg", t, dur, 1060 - meia, foco=(0.5, 0.4),
                                  z0=1.08, z1=1.0, degrade=False), (0, meia))
    ImageDraw.Draw(dupla).rectangle((0, meia - 3, W, meia + 3), fill=RED)
    im.alpha_composite(degradar(dupla), (0, 0))
    topo(im, "Fotos: Marcelo Camargo e Marcello Casal Jr/Agência Brasil")
    a = ease((t - 0.1) / 0.35)
    y = texto_rico(im, (M, 930), f"TSE dá *24{NB}horas* para Meta e X se explicarem", fonte("serif", 96), W - 2 * M,
                   alpha=a, dy=int(40 * (1 - a)))
    b = ease((t - 0.6) / 0.4)
    texto_rico(im, (M, y + 30), "A campanha de Lula acusa as redes de favorecer Flávio", fonte("sans", 44), W - 2 * M,
               cor=LIGHT, alpha=b, dy=int(30 * (1 - b)))
    return im


def cena2(t, dur):
    im = fundo()
    topo(im, "Fontes: Agência Brasil e Estadão")
    a = ease(t / 0.4)
    y = texto_rico(im, (M, 380), "O que o TSE *quer saber*", fonte("serif", 100), W - 2 * M, alpha=a, dy=int(30 * (1 - a))) + 50
    lista(im, y, ["Como os algoritmos distribuem posts e anúncios políticos",
                  "Se a tradução automática da Meta mudou o sentido de comentários",
                  "Como o Grok, a IA do X, responde sobre os candidatos"], t)
    return im


def cena3(t, dur):
    im = fundo()
    topo(im, "Fonte: Estadão")
    d = ImageDraw.Draw(im)
    a = ease(t / 0.35)
    f = fonte("sans-b", 34)
    x = M
    for ch in "MULTA POR DIA, PARA CADA EMPRESA":
        d.text((x, 560 + int(20 * (1 - a))), ch, font=f, fill=GREY + (int(255 * a),)); x += d.textlength(ch, font=f) + 2
    n = int(round(500 * ease(t / 1.0)))
    d.text((M - 8, 620), f"R$ {n} mil", font=fonte("serif", 168), fill=RED2)
    b = ease((t - 1.1) / 0.45)
    texto_rico(im, (M, 900), "se Meta ou X não responderem sem justificativa", fonte("serif", 72), W - 2 * M, alpha=b,
               dy=int(30 * (1 - b)))
    return im


def cena4(t, dur):
    im = fundo()
    im.alpha_composite(foto_kb("img/fotos/celular-apps-meta.jpg", t, dur, 1060, foco=(0.5, 0.5), z0=1.1, z1=1.22), (0, 0))
    topo(im, "Fonte: Agência Brasil · Foto: Marcello Casal Jr/Agência Brasil")
    a = ease((t - 0.1) / 0.4)
    y = texto_rico(im, (M, 930), "Vídeo que criticava Flávio foi *derrubado* do Instagram", fonte("serif", 88), W - 2 * M,
                   alpha=a, dy=int(40 * (1 - a)))
    b = ease((t - 0.8) / 0.45)
    texto_rico(im, (M, y + 30), "O ministro mandou a Meta fazer revisão humana do vídeo, apresentado pelo MC Cabelinho",
               fonte("sans", 42), W - 2 * M, cor=LIGHT, alpha=b, dy=int(30 * (1 - b)))
    return im


def cena5(t, dur):
    im = fundo()
    topo(im, "Fontes: Agência Brasil, Estadão e Gazeta do Povo")
    a = ease(t / 0.4)
    y = texto_rico(im, (M, 330), "*Ainda não há* conclusão", fonte("serif", 100), W - 2 * M, alpha=a, dy=int(30 * (1 - a))) + 50
    lista(im, y, ["O ministro disse que abrir a investigação não comprova as acusações",
                  "A ação pede a cassação da chapa de Flávio, que tem 5 dias para se defender",
                  "A Meta nega favorecer qualquer candidato"], t, tam=44)
    return im


CENAS = [(cena1, 3.5), (cena2, 4.0), (cena3, 3.0), (cena4, 3.6), (cena5, 4.0), (cena6, 2.2)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        quadros = [f(d - 0.05, d).convert("RGB").resize((360, 640)) for f, d in CENAS]
        o = Image.new("RGB", (360 * len(quadros), 640))
        for i, q in enumerate(quadros):
            o.paste(q, (i * 360, 0))
        o.save(sys.argv[2])
    else:
        R.render(CENAS, "tse-meta-x", cena1)
