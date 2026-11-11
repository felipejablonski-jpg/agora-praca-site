#!/usr/bin/env python3
"""Gráfico da matéria das ondas de calor (Nature Communications, 5/11/2026): duração das nove ondas de referência
contra o teto de seis meses da análise. Gera img/calor/duracao-ondas-referencia.jpg (1200x900).
Dados: Aglas-Leitner et al. (2026), tabela das ondas de referência (Berkeley Earth).
"""
import os
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(RAIZ, "_src", "fontes")
W, H, M = 1200, 900, 60
INK, RED, GREY, LIGHT, WHITE, LINHA = (20, 20, 20), (255, 71, 61), (150, 145, 137), (232, 228, 220), (255, 255, 255), (70, 70, 70)


def fonte(n, t):
    return ImageFont.truetype(os.path.join(F, {"serif": "libre-caslon-text-latin-700-normal.woff",
                                                "sans": "archivo-latin-600-normal.woff",
                                                "sans-b": "archivo-latin-800-normal.woff"}[n]), t)


DADOS = [("Norte da África e Oriente Médio, 2023", 133), ("China, 2022", 38), ("Europa, 2018", 34),
         ("Austrália, 2019-2020", 21), ("Índia e Paquistão, 2019", 21), ("Nordeste da Sibéria, 2020", 18),
         ("Sul da África, 2015-2016", 12), ("Noroeste da América do Norte, 2021", 10), ("América do Sul, 2022", 7)]
TETO = 180


def main():
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    d.text((M, 40), "Os recordes recentes e o teto de seis meses", font=fonte("serif", 46), fill=WHITE)
    d.text((M, 104), "Duração, em dias, das ondas de calor usadas como referência no estudo", font=fonte("sans", 25), fill=LIGHT)
    x0, x1 = 560, W - M - 20
    y = 190
    esc = (x1 - x0) / 190
    xt = x0 + TETO * esc
    d.line((xt, 170, xt, 800), fill=RED, width=4)
    d.text((xt - 12, 148), "180 dias", font=fonte("sans-b", 24), fill=RED, anchor="rs")
    for nome, v in DADOS:
        f = fonte("sans-b", 23)
        d.text((x0 - 16, y + 24), nome, font=f, fill=WHITE, anchor="rm")
        d.rectangle((x0, y, x0 + v * esc, y + 46), fill=RED if "América do Sul" in nome else GREY)
        d.text((x0 + v * esc + 12, y + 24), str(v), font=fonte("sans-b", 26), fill=WHITE, anchor="lm")
        y += 68
    d.text((M, H - 78), "A linha vermelha é o máximo que a análise alcança: os seis meses mais quentes de cada região.",
           font=fonte("sans", 22), fill=LIGHT)
    d.text((M, H - 44), "Dados: Aglas-Leitner et al., Nature Communications (2026) · Gráfico: Agora Praça",
           font=fonte("sans", 22), fill=GREY)
    saida = os.path.join(RAIZ, "img", "calor", "duracao-ondas-referencia.jpg")
    im.save(saida, quality=92)
    print("ok", saida)


if __name__ == "__main__":
    main()
