#!/usr/bin/env python3
"""Gráfico da matéria do Global Carbon Budget 2026: variação projetada das emissões fósseis de CO2 em 2026,
por país ou bloco e por combustível. Gera img/carbono/variacao-2026.jpg (1200x900).
Dados: Global Carbon Project, Global Carbon Budget 2026 (10/11/2026).
"""
import os
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(RAIZ, "_src", "fontes")
W, H, M = 1200, 900, 60
INK, RED, GREY, LIGHT, WHITE, LINHA = (20, 20, 20), (255, 71, 61), (150, 145, 137), (232, 228, 220), (255, 255, 255), (90, 90, 90)


def fonte(n, t):
    return ImageFont.truetype(os.path.join(F, {"serif": "libre-caslon-text-latin-700-normal.woff",
                                                "sans": "archivo-latin-600-normal.woff",
                                                "sans-b": "archivo-latin-800-normal.woff"}[n]), t)


PAISES = [("Índia", 4.4), ("China", -0.9), ("Japão", -1.0), ("Estados Unidos", -1.3), ("União Europeia", -1.5),
          ("Resto do mundo", -0.7)]
FUSTIVEIS = [("Carvão", 0.6), ("Gás natural", -0.3), ("Petróleo", -1.9)]


def barras(d, dados, y, x_zero, esc):
    for nome, v in dados:
        d.text((360, y + 20), nome, font=fonte("sans-b", 24), fill=WHITE, anchor="rm")
        x = x_zero + v * esc
        d.rectangle((min(x, x_zero), y, max(x, x_zero), y + 40), fill=RED if v > 0 else GREY)
        txt = f"{v:+.1f}%".replace(".", ",").replace("-", "−")
        if v > 0:
            d.text((x + 12, y + 20), txt, font=fonte("sans-b", 26), fill=WHITE, anchor="lm")
        else:
            d.text((x - 12, y + 20), txt, font=fonte("sans-b", 26), fill=WHITE, anchor="rm")
        y += 54
    return y


def main():
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    d.text((M, 40), "Onde as emissões sobem e onde caem em 2026", font=fonte("serif", 44), fill=WHITE)
    d.text((M, 102), "Variação projetada das emissões de CO2 de combustíveis fósseis, em relação a 2025",
           font=fonte("sans", 24), fill=LIGHT)
    x_zero = 700
    esc = 70
    y = 170
    d.text((M, y), "POR PAÍS OU BLOCO", font=fonte("sans-b", 22), fill=RED)
    y0 = y + 40
    y = barras(d, PAISES, y0, x_zero, esc)
    y += 20
    d.text((M, y), "POR COMBUSTÍVEL", font=fonte("sans-b", 22), fill=RED)
    y1 = y + 40
    y = barras(d, FUSTIVEIS, y1, x_zero, esc)
    d.line((x_zero, y0 - 10, x_zero, y - 10), fill=LINHA, width=2)
    d.text((M, H - 112), "No mundo, as emissões fósseis caem 0,4%, para 38,2 bilhões de toneladas. Com as do uso da terra,",
           font=fonte("sans", 22), fill=LIGHT)
    d.text((M, H - 80), "como o desmatamento, o total de CO2 sobe de 42,8 para 43,3 bilhões de toneladas.", font=fonte("sans", 22), fill=LIGHT)
    d.text((M, H - 44), "Dados: Global Carbon Project, Global Carbon Budget 2026 · Gráfico: Agora Praça",
           font=fonte("sans", 22), fill=GREY)
    os.makedirs(os.path.join(RAIZ, "img", "carbono"), exist_ok=True)
    saida = os.path.join(RAIZ, "img", "carbono", "variacao-2026.jpg")
    im.save(saida, quality=92)
    print("ok", saida)


if __name__ == "__main__":
    main()
