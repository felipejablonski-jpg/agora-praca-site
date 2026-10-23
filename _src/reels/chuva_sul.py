#!/usr/bin/env python3
"""Reel: risco alto de inundação no Sul no sábado e chuva até 200 mm em Chapecó (23/10/2026).

Gera video/chuva-sul.mp4 e video/chuva-sul.jpg. Uso: python3 _src/reels/chuva_sul.py [teste <saida.jpg>]
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calor_votacao as R  # noqa: E402
from calor_votacao import (Image, ImageDraw, W, H, M, INK, RED, RED2, WHITE, LIGHT, GREY,  # noqa: E402
                           fonte, ease, texto_rico, topo, foto_kb, degradar, fundo, cena6)

R.TAG = "SERVIÇO · CLIMA"
R.FONTES_FIM = "Fontes: Cemaden, Inmet e Defesa Civil de Chapecó"
NB = " "

CIDADES = [("Chapecó", -27.10, -52.62, "d", 0), ("Ijuí", -28.39, -53.91, "e", 0), ("Passo Fundo", -28.26, -52.41, "d", 0),
           ("Cascavel", -24.96, -53.46, "e", 0), ("Guarapuava", -25.39, -51.46, "e", 30), ("Ponta Grossa", -25.09, -50.16, "d", -34),
           ("Curitiba", -25.43, -49.27, "d", 26)]


class MapaSul:
    def __init__(self, caixa):
        d = json.load(open(os.path.join(R.RAIZ, "_src", "reels", "geo", "sul-sp-ms.json"), encoding="utf-8"))
        self.ufs = {}
        for ft in d["features"]:
            g = ft["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            self.ufs[ft["properties"]["sigla"]] = [p[0] for p in polys]
        self.lon0, self.lon1, self.lat0, self.lat1 = -57.8, -48.0, -33.8, -24.2
        self.k = math.cos(math.radians(-28))
        x0, y0, x1, y1 = caixa
        sw = (self.lon1 - self.lon0) * self.k; sh = self.lat1 - self.lat0
        self.s = min((x1 - x0) / sw, (y1 - y0) / sh)
        self.ox = x0 + ((x1 - x0) - sw * self.s) / 2
        self.oy = y0 + ((y1 - y0) - sh * self.s) / 2
        ss = 2
        im = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        for uf, aneis in self.ufs.items():
            cor = (58, 56, 52) if uf in ("PR", "SC", "RS") else (36, 35, 33)
            for a in aneis:
                dr.polygon([self.p(lon, lat, ss) for lon, lat in a], fill=cor, outline=(20, 20, 20))
        base = im.resize((W, H), Image.LANCZOS)
        mascara = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mascara).rectangle((0, y0 - 40, W, y1 + 20), fill=255)
        a = base.getchannel("A")
        base.putalpha(Image.composite(a, Image.new("L", (W, H), 0), mascara))
        self.base = base

    def p(self, lon, lat, ss=1):
        return ((self.ox + (lon - self.lon0) * self.k * self.s) * ss, (self.oy + (self.lat1 - lat) * self.s) * ss)


MAPA = None


def cena1(t, dur):
    im = fundo()
    meia = 520
    dupla = Image.new("RGBA", (W, 1060), INK + (255,))
    dupla.alpha_composite(foto_kb("img/fotos/temporal-rio-grande-rs.jpg", t, dur, meia, foco=(0.4, 0.5),
                                  z0=1.0, z1=1.08, degrade=False), (0, 0))
    dupla.alpha_composite(foto_kb("img/fotos/chuva-rodovia-meio-oeste-sc.jpg", t, dur, 1060 - meia, foco=(0.5, 0.5),
                                  z0=1.08, z1=1.0, degrade=False), (0, meia))
    ImageDraw.Draw(dupla).rectangle((0, meia - 3, W, meia + 3), fill=RED)
    im.alpha_composite(degradar(dupla), (0, 0))
    topo(im, "Fotos: Prefeitura do Rio Grande/Divulgação e Julio Cavalheiro/Secom SC (arquivo)")
    a = ease((t - 0.1) / 0.35)
    y = texto_rico(im, (M, 930), f"Sul em alerta: até *200{NB}mm* de chuva em Chapecó", fonte("serif", 92), W - 2 * M,
                   alpha=a, dy=int(40 * (1 - a)))
    b = ease((t - 0.6) / 0.4)
    texto_rico(im, (M, y + 30), "O Cemaden vê risco alto de inundação no sábado em SC, no RS e no PR", fonte("sans", 44),
               W - 2 * M, cor=LIGHT, alpha=b, dy=int(30 * (1 - b)))
    return im


def cena2(t, dur):
    im = fundo()
    topo(im, "Fonte: Defesa Civil de Chapecó")
    d = ImageDraw.Draw(im)
    a = ease(t / 0.35)
    f = fonte("sans-b", 34)
    x = M
    for ch in "CHAPECÓ · SEXTA E SÁBADO":
        d.text((x, 520 + int(20 * (1 - a))), ch, font=f, fill=GREY + (int(255 * a),)); x += d.textlength(ch, font=f) + 2
    n = int(round(200 * ease(t / 1.1)))
    d.text((M - 10, 580), f"{n} mm", font=fonte("serif", 220), fill=RED2)
    b = ease((t - 1.1) / 0.45)
    y = texto_rico(im, (M, 960), "de chuva acumulada, com picos de mais de *20 mm* em uma hora", fonte("serif", 76), W - 2 * M,
                   alpha=b, dy=int(30 * (1 - b)))
    return im


def cena3(t, dur):
    im = fundo()
    topo(im, "Fontes: Cemaden e Inmet · Mapa: Agora Praça")
    im.alpha_composite(MAPA.base)
    a = ease(t / 0.4)
    texto_rico(im, (M, 250), "Risco *alto* de inundação no sábado", fonte("serif", 84), W - 2 * M, alpha=a, dy=int(30 * (1 - a)))
    camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    f = fonte("sans-b", 30)
    for i, (nome, lat, lon, lado, ddy) in enumerate(CIDADES):
        al = int(255 * ease((t - 0.4 - i * 0.18) / 0.3))
        if al <= 0:
            continue
        x, y = MAPA.p(lon, lat)
        r = 16
        d.ellipse((x - r, y - r, x + r, y + r), fill=RED2 + (al,), outline=WHITE + (al,), width=3)
        tx = x + 26 if lado == "d" else x - 26 - d.textlength(nome.upper(), font=f)
        d.text((tx, y - 18 + ddy), nome.upper(), font=f, fill=WHITE + (al,))
    im.alpha_composite(camada)
    b = ease((t - 1.9) / 0.45)
    texto_rico(im, (M, 1500), "Inmet: alerta *vermelho* no Oeste catarinense no sábado, das 6h às 21h (Brasília)", fonte("sans", 42),
               W - 2 * M, cor=LIGHT, alpha=b, dy=int(20 * (1 - b)))
    return im


def cena4(t, dur):
    im = fundo()
    im.alpha_composite(foto_kb("img/fotos/chuva-guarda-chuva-rio.jpg", t, dur, 1060, foco=(0.55, 0.5), z0=1.0, z1=1.1), (0, 0))
    topo(im, "Fonte: Cemaden · Foto: Fernando Frazão/Agência Brasil (arquivo)")
    a = ease((t - 0.1) / 0.4)
    y = texto_rico(im, (M, 930), "O domingo de votação também tem *risco*", fonte("serif", 92), W - 2 * M, alpha=a,
                   dy=int(40 * (1 - a)))
    b = ease((t - 0.8) / 0.45)
    texto_rico(im, (M, y + 30), "A cheia do rio Uruguai continua, e há risco de alagamento e deslizamento em São Paulo",
               fonte("sans", 42), W - 2 * M, cor=LIGHT, alpha=b, dy=int(30 * (1 - b)))
    return im


def cena5(t, dur):
    im = fundo()
    topo(im, "Fonte: Defesa Civil de Chapecó")
    a = ease(t / 0.4)
    y = texto_rico(im, (M, 380), "Se a chuva *apertar*", fonte("serif", 104), W - 2 * M, alpha=a, dy=int(30 * (1 - a))) + 50
    itens = ["Não atravesse rua alagada, nem a pé nem de carro",
             "Fique longe de córrego e rio que sobe rápido",
             "Emergência: Defesa Civil 199, Bombeiros 193"]
    for i, it in enumerate(itens):
        b = ease((t - 0.5 - i * 0.55) / 0.4)
        camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(camada).rectangle((M, y + 22 + int(20 * (1 - b)), M + 18, y + 40 + int(20 * (1 - b))),
                                         fill=RED2 + (int(255 * b),))
        im.alpha_composite(camada)
        y = texto_rico(im, (M + 46, y), it, fonte("sans", 48), W - 2 * M - 46, alpha=b, dy=int(20 * (1 - b)), entre=1.3) + 40
    return im


CENAS = [(cena1, 3.5), (cena2, 3.2), (cena3, 4.2), (cena4, 3.5), (cena5, 3.4), (cena6, 2.2)]

if __name__ == "__main__":
    MAPA = MapaSul((M, 470, W - M, 1450))
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        quadros = [f(d - 0.05, d).convert("RGB").resize((360, 640)) for f, d in CENAS]
        o = Image.new("RGB", (360 * len(quadros), 640))
        for i, q in enumerate(quadros):
            o.paste(q, (i * 360, 0))
        o.save(sys.argv[2])
    else:
        R.render(CENAS, "chuva-sul", cena1, t_capa=3.0)
