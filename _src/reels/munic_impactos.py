#!/usr/bin/env python3
"""Reel: três em cada quatro cidades tiveram seca, alagamento ou deslizamento em dois anos (Munic 2025, IBGE, 11/11/2026).

Sem narração: cortes na batida de 72 BPM (0,833 s), para a música entrar no Instagram.
Fotos de arquivo da Agência Brasil e de divulgação, em img/fotos/.

Gera video/munic-impactos.mp4 e video/munic-impactos.jpg.
Uso: python3 _src/reels/munic_impactos.py
Teste: python3 _src/reels/munic_impactos.py teste <cena> <t> <saida.jpg>
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_argv = sys.argv
sys.argv = [_argv[0], "."]  # oceano_recorde lê a pasta de trabalho em argv[1]
from oceano_recorde import escreve, bloco, entra, sombra  # noqa: E402
sys.argv = _argv
import calor_votacao as R  # noqa: E402
from calor_votacao import (Image, ImageDraw, W, H, M, INK, RED2, WHITE, LIGHT, GREY,  # noqa: E402
                           fonte, ease, topo, fundo, cena6)

R.TAG = "CIÊNCIA · CLIMA"
R.FONTES_FIM = "Fonte: IBGE, Munic 2025 (divulgada em 11/11/2026)"
B = 60 / 72  # uma batida

F_PONTE = "img/fotos/ponte-lajeado-cheia-rafa-neddermeyer-abr-2024.jpg"
F_SECA = "img/fotos/rio-madeira-seca-fumaca-aspar-2024.jpg"
F_ALAGA = "img/fotos/porto-alegre-alagamento-rafa-neddermeyer-abr-2024.jpg"
F_DESLIZ = "img/fotos/morro-da-oficina-petropolis-tomaz-silva-abr-2022.jpg"
CRED = {
    F_PONTE: "Ponte destruída pela cheia em Lajeado (RS), maio de 2024. Foto: Rafa Neddermeyer/Agência Brasil (arquivo)",
    F_SECA: "Seca e fumaça no rio Madeira (RO), setembro de 2024. Foto: Aspar/Divulgação (arquivo)",
    F_ALAGA: "Alagamento em Porto Alegre (RS), maio de 2024. Foto: Rafa Neddermeyer/Agência Brasil (arquivo)",
    F_DESLIZ: "Deslizamento no Morro da Oficina, Petrópolis (RJ), 2022. Foto: Tomaz Silva/Agência Brasil (arquivo)",
}
_FOTOS = {}


def _foto(src):
    if src not in _FOTOS:
        _FOTOS[src] = Image.open(os.path.join(R.RAIZ, src)).convert("RGB")
    return _FOTOS[src]


def pulso(t):
    """Sem soco de zoom na batida: Felipe pediu só o zoom contínuo (11/11/2026)."""
    return 0.0


def foto_tela(src, t, dur, foco=(0.5, 0.5), z0=1.0, z1=1.14, pan=0.0, escuro=0.0, area=H):
    """Foto ocupando a largura e a altura `area` a partir do topo, com zoom, deslocamento lateral e pulso na batida."""
    im = _foto(src)
    r = W / area
    if im.width / im.height > r:
        nw = int(im.height * r)
        x = int((im.width - nw) * foco[0])
        im = im.crop((x, 0, x + nw, im.height))
    else:
        nh = int(im.width / r)
        y = int((im.height - nh) * foco[1])
        im = im.crop((0, y, im.width, y + nh))
    p = min(1, t / dur)
    z = z0 + (z1 - z0) * p + pulso(t)
    cw, ch = im.width / z, im.height / z
    cx = im.width / 2  # sem deslocamento lateral: só o zoom (pedido do Felipe, 11/11/2026)
    cy = im.height / 2
    im = im.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, area), Image.LANCZOS)
    tela = fundo()
    tela.alpha_composite(im.convert("RGBA"), (0, 0))
    im = tela
    if escuro:
        im.alpha_composite(Image.new("RGBA", (W, H), INK + (int(255 * escuro),)))
    return im


def base(src, t, dur, y0=700, y1=1250, **kw):
    kw.setdefault("area", 1300)
    im = foto_tela(src, t, dur, **kw)
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(cam).rectangle((0, 0, W, 260), fill=INK + (90,))
    sombra(cam, y0, y1, 0.93)
    ImageDraw.Draw(cam).rectangle((0, y1, W, H), fill=INK + (255,))
    im.alpha_composite(cam)
    topo(im, CRED[src])
    return im, Image.new("RGBA", im.size, (0, 0, 0, 0))


def flash(im, t, d=0.1):
    """Sem clarão no corte: Felipe pediu só o zoom (11/11/2026)."""
    return im


def br(v, casas=1):
    txt = f"{v:.{casas}f}".replace(".", ",")
    return txt[:-2] if txt.endswith(",0") else txt


# ---------- cenas ----------
def s1(t, d):
    """Abertura: a ponte destruída e o 3 em 4."""
    im, cam = base(F_PONTE, t, d, 640, 1180, foco=(0.5, 0.5), z0=1.06, z1=1.22, pan=0.4)
    escreve(cam, M, 1020, "3 em 4", fonte("serif", 270), RED2, entra(t, 0.0, 0.25))
    a = entra(t, B * 1, 0.3)
    escreve(cam, M, 1330, "CIDADES DO BRASIL", fonte("sans-b", 64), WHITE, a)
    b = entra(t, B * 2, 0.35)
    y = bloco(cam, M, 1440, "tiveram *seca,* *alagamento* ou *deslizamento* em dois anos", fonte("serif", 74),
              alpha=b, dy=int(24 * (1 - b)))
    c = entra(t, B * 3.5, 0.3)
    escreve(cam, M, y + 30, "IBGE · Munic 2025", fonte("sans-b", 40), LIGHT, c)
    im.alpha_composite(cam)
    return im


def impacto(src, nome, v25, v20, foco, pan):
    def cena(t, d):
        im, cam = base(src, t, d, 700, 1250, foco=foco, z0=1.04, z1=1.16, pan=pan)
        n = v25 * ease(t / (B * 1.1))
        escreve(cam, M, 1060, br(n) + "%", fonte("serif", 250), RED2)
        escreve(cam, M, 1370, nome, fonte("sans-b", 72), WHITE, entra(t, 0.05, 0.25))
        a = entra(t, B * 1, 0.3)
        bloco(cam, M, 1480, f"das cidades · eram *{br(v20)}%* em 2020", fonte("sans-b", 48), LIGHT, alpha=a,
              dy=int(18 * (1 - a)))
        im.alpha_composite(cam)
        return flash(im, t)
    cena.__name__ = "impacto_" + nome.split()[-1].lower()
    return cena


s2 = impacto(F_SECA, "COM SECA", 59.0, 53.4, (0.35, 0.5), -0.5)
s3 = impacto(F_ALAGA, "COM ALAGAMENTO", 49.5, 35.8, (0.45, 0.5), 0.5)
s4 = impacto(F_DESLIZ, "COM DESLIZAMENTO", 25.2, 17.1, (0.5, 0.5), -0.4)

BARRAS = [("Algum impacto", 66.2, 74.3), ("Seca", 53.4, 59.0), ("Alagamento", 35.8, 49.5), ("Deslizamento", 17.1, 25.2)]


def s5(t, d):
    """Gráfico: 2020 contra 2025, com a ponte escurecida ao fundo."""
    im = foto_tela(F_PONTE, t, d, foco=(0.5, 0.5), z0=1.2, z1=1.3, pan=-0.3, escuro=0.78)
    topo(im, "Gráfico: Agora Praça · Dados: IBGE, Munic 2020 e 2025 · Foto ao fundo: Rafa Neddermeyer/Agência Brasil")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(cam)
    a = entra(t, 0, 0.3)
    escreve(cam, M, 330, "Mais cidades atingidas", fonte("serif", 84), WHITE, a)
    escreve(cam, M, 445, "PARCELA DOS MUNICÍPIOS ATINGIDOS", fonte("sans-b", 30), LIGHT, a)
    for cor, txt, x in ((GREY, "2020", M), (RED2, "2025", M + 170)):
        dr.rectangle((x, 518, x + 34, 552), fill=cor + (int(255 * a),))
        escreve(cam, x + 50, 512, txt, fonte("sans-b", 40), WHITE, a)
    x0, x1 = M + 330, W - M - 150
    y = 640
    for i, (nome, v20, v25) in enumerate(BARRAS):
        g = entra(t, B * (0.5 + 0.8 * i), 0.5)
        if g <= 0:
            y += 290
            continue
        escreve(cam, M, y + 20, nome.upper(), fonte("sans-b", 40), WHITE, g)
        for j, (v, cor) in enumerate(((v20, GREY), (v25, RED2))):
            yy = y + 90 + j * 86
            larg = (x1 - (M)) * v / 80 * g
            dr.rectangle((M, yy, M + larg, yy + 70), fill=cor + (255,))
            escreve(cam, int(M + larg + 18), yy + 8, br(v * g) + "%", fonte("sans-b", 46),
                    RED2 if j else WHITE, g)
        y += 290
    im.alpha_composite(cam)
    return flash(im, t)


def s6(t, d):
    """Só 1 em cada 10 cidades tem lei ou plano para se adaptar ao clima."""
    im, cam = base(F_DESLIZ, t, d, 520, 1000, foco=(0.5, 0.4), z0=1.15, z1=1.0, pan=0.3)
    escreve(cam, M, 820, "1 em 10", fonte("serif", 250), RED2, entra(t, 0, 0.25))
    dr = ImageDraw.Draw(cam)
    # dez casas, uma acesa
    lado, gap = 72, 18
    for i in range(10):
        g = entra(t, 0.15 + 0.06 * i, 0.2)
        if g <= 0:
            continue
        x = M + i * (lado + gap)
        yb = 1170
        cor = RED2 if i == 0 else (90, 88, 84)
        al = int(255 * g)
        dr.polygon([(x, yb), (x + lado / 2, yb - 34), (x + lado, yb)], fill=cor + (al,))
        dr.rectangle((x + 8, yb, x + lado - 8, yb + 52), fill=cor + (al,))
    a = entra(t, B * 1.5, 0.35)
    y = bloco(cam, M, 1300, "das cidades tem *lei* *ou* *plano* para se adaptar à mudança do clima", fonte("serif", 70),
              alpha=a, dy=int(22 * (1 - a)))
    b = entra(t, B * 3, 0.3)
    bloco(cam, M, y + 30, "Só 2,7% medem as próprias emissões de gases do efeito estufa", fonte("sans-b", 44),
          LIGHT, alpha=b)
    im.alpha_composite(cam)
    return flash(im, t)


def s7(t, d):
    im, cam = base(F_ALAGA, t, d, 600, 1150, foco=(0.55, 0.5), z0=1.1, z1=1.24, pan=-0.3)
    escreve(cam, M, 1080, "A PERGUNTA QUE FICA", fonte("sans-b", 44), LIGHT, entra(t, 0, 0.25))
    a = entra(t, B * 0.5, 0.3)
    bloco(cam, M, 1170, "A sua cidade está *preparada?*", fonte("serif", 120), alpha=a, dy=int(24 * (1 - a)))
    im.alpha_composite(cam)
    return flash(im, t)


def capa():
    im, cam = base(F_PONTE, 0.0, 1.0, 640, 1180, foco=(0.5, 0.5), z0=1.08, z1=1.08)
    escreve(cam, M, 1000, "IBGE · MUNIC 2025", fonte("sans-b", 54), RED2)
    bloco(cam, M, 1090, "*3* *em* *cada* *4* *cidades* tiveram seca, alagamento ou deslizamento em dois anos",
          fonte("serif", 96))
    im.alpha_composite(cam)
    return im


CENAS = [(s1, 5 * B), (s2, 2 * B), (s3, 2 * B), (s4, 2 * B), (s5, 6 * B), (s6, 4 * B), (s7, 3 * B), (cena6, 2.2)]
NOME = "munic-impactos"

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        if sys.argv[2] == "capa":
            capa().convert("RGB").save(sys.argv[4])
        else:
            fns = {fn.__name__: (fn, d) for fn, d in CENAS}
            fn, d = fns[sys.argv[2]]
            fn(float(sys.argv[3]), d).convert("RGB").save(sys.argv[4])
    else:
        R.render(CENAS, NOME, s1, t_capa=None)
        capa().convert("RGB").save(os.path.join(R.RAIZ, "video", NOME + ".jpg"), quality=88)
