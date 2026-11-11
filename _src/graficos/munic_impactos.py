#!/usr/bin/env python3
"""Gráfico da matéria da Munic 2025 (IBGE): municípios com seca, alagamento e deslizamento, 2020 x 2025.

Gera img/munic/impactos-2020-2025.jpg (1200x800). Uso: python3 _src/graficos/munic_impactos.py
Dados: Munic 2025 do IBGE, divulgada em 11/11/2026, via Agência Brasil.
"""
import os
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(RAIZ, "_src", "fontes")
W, H, M = 1200, 800, 60
INK, RED, GREY, LIGHT, WHITE, LINHA = (20, 20, 20), (255, 71, 61), (150, 145, 137), (232, 228, 220), (255, 255, 255), (70, 70, 70)


def fonte(n, t):
    return ImageFont.truetype(os.path.join(F, {"serif": "libre-caslon-text-latin-700-normal.woff",
                                                "sans": "archivo-latin-600-normal.woff",
                                                "sans-b": "archivo-latin-800-normal.woff"}[n]), t)


DADOS = [("Algum impacto", 66.2, 74.3), ("Seca", 53.4, 59.0), ("Alagamento", 35.8, 49.5), ("Deslizamento", 17.1, 25.2)]


def br(v):
    return f"{v:.1f}".replace(".", ",") + "%"


def main():
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    d.text((M, 46), "Mais cidades atingidas", font=fonte("serif", 58), fill=WHITE)
    d.text((M, 122), "Municípios que declararam o impacto nos dois anos antes da pesquisa", font=fonte("sans", 25), fill=LIGHT)
    # legenda
    y = 172
    for cor, txt, x in ((GREY, "2020", M), (RED, "2025", M + 130)):
        d.rectangle((x, y + 4, x + 24, y + 28), fill=cor)
        d.text((x + 36, y), txt, font=fonte("sans-b", 26), fill=WHITE)
    x0, x1, y0, y1 = M + 60, W - M, 250, 690
    for v in (0, 25, 50, 75):
        yy = y1 - (y1 - y0) * v / 80
        d.line((x0, yy, x1, yy), fill=LINHA, width=2)
        d.text((M, yy - 16), f"{v}%", font=fonte("sans", 24), fill=GREY)
    grupo = (x1 - x0) / len(DADOS)
    bw = 92
    for i, (nome, a, b) in enumerate(DADOS):
        cx = x0 + grupo * (i + 0.5)
        for v, cor, dx in ((a, GREY, -bw - 6), (b, RED, 6)):
            top = y1 - (y1 - y0) * v / 80
            d.rectangle((cx + dx, top, cx + dx + bw, y1), fill=cor)
            f = fonte("sans-b", 28)
            t = br(v)
            d.text((cx + dx + bw / 2 - d.textlength(t, font=f) / 2, top - 40), t, font=f, fill=RED if cor == RED else WHITE)
        f = fonte("sans-b", 28)
        d.text((cx - d.textlength(nome, font=f) / 2, y1 + 18), nome, font=f, fill=WHITE)
    d.text((M, H - 50), "Dados: Munic 2025 e Munic 2020, IBGE (declarado pelas prefeituras) · Gráfico: Agora Praça",
           font=fonte("sans", 22), fill=GREY)
    saida = os.path.join(RAIZ, "img", "munic", "impactos-2020-2025.jpg")
    im.save(saida, quality=92)
    print("ok", saida)


if __name__ == "__main__":
    main()
