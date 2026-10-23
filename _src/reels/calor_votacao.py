#!/usr/bin/env python3
"""Reel: calor e alerta de tempestade no domingo de votação (23/10/2026).

Gera video/calor-votacao.mp4 (1080x1920, 30 fps, ~18 s, áudio mudo) e a capa video/calor-votacao.jpg.
Uso: python3 _src/reels/calor_votacao.py <mt-municipios.geojson>
"""
import os, sys, json, math, subprocess, tempfile, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(RAIZ, "_src", "fontes")
W, H, FPS = 1080, 1920, 30
M = 80
INK = (20, 20, 20); RED = (210, 35, 42); RED2 = (255, 70, 60); WHITE = (255, 255, 255)
LIGHT = (225, 221, 213); GREY = (150, 146, 138)


def fonte(n, t):
    return ImageFont.truetype(os.path.join(F, {"serif": "libre-caslon-text-latin-700-normal.woff",
                                               "sans": "archivo-latin-600-normal.woff",
                                               "sans-b": "archivo-latin-800-normal.woff"}[n]), t)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def quebrar(d, txt, f, maxw):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if d.textlength(t.replace("*", ""), font=f) <= maxw:
            atual = t
        else:
            linhas.append(atual); atual = p
    if atual:
        linhas.append(atual)
    return linhas


def texto_rico(im, xy, txt, f, maxw, cor=WHITE, destaque=RED2, entre=1.12, alpha=1.0, dy=0):
    """Escreve com quebra de linha; palavras entre *asteriscos* saem na cor de destaque. Devolve o y final."""
    if alpha <= 0:
        d = ImageDraw.Draw(im)
        return xy[1] + len(quebrar(d, txt, f, maxw)) * int(f.size * entre)
    camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    x0, y = xy[0], xy[1] + dy
    a = int(255 * alpha)
    for linha in quebrar(d, txt, f, maxw):
        x, dentro = x0, False
        for i, pal in enumerate(linha.split()):
            ini, fim = pal.startswith("*"), pal.endswith("*")
            if ini: dentro = True
            limpa = pal.strip("*") + (" " if i < len(linha.split()) - 1 else "")
            c = destaque if dentro else cor
            d.text((x, y), limpa, font=f, fill=c + (a,))
            x += d.textlength(limpa, font=f)
            if fim: dentro = False
        y += int(f.size * entre)
    im.alpha_composite(camada)
    return y - dy


def topo(im, fonte_txt, alpha=1.0):
    d = ImageDraw.Draw(im)
    f = fonte("sans-b", 28)
    tag = "SERVIÇO · ELEIÇÕES 2026"
    tw = d.textlength(tag, font=f) + 2 * 3 * len(tag) // 4
    x = M
    d.rectangle((x, 110, x + tw + 36, 160), fill=RED)
    xx = x + 18
    for ch in tag:
        d.text((xx, 117), ch, font=f, fill=WHITE); xx += d.textlength(ch, font=f) + 1.5
    # marca à direita
    fm = fonte("serif", 34); fa = fonte("sans-b", 28)
    handle = "@AGORAPRACA"
    hw = d.textlength(handle, font=fa)
    xr = W - M - hw
    d.text((xr, 120), handle, font=fa, fill=WHITE)
    d.rectangle((xr - 50, 113, xr - 14, 157), fill=RED)
    d.text((xr - 32, 135), "Á", font=fm, fill=WHITE, anchor="mm")
    if fonte_txt:
        ff = fonte("sans", 25)
        cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(cam)
        dc.rectangle((M - 10, 176, M + d.textlength(fonte_txt, font=ff) + 10, 214), fill=(20, 20, 20, 170))
        im.alpha_composite(cam)
        d = ImageDraw.Draw(im)
        d.text((M, 182), fonte_txt, font=ff, fill=(225, 221, 213))


def foto_kb(src, t, dur, area_h, foco=(0.5, 0.5), z0=1.0, z1=1.1):
    """Foto preenchendo a largura e area_h de altura, com zoom lento; base com degradê para o fundo."""
    im = Image.open(os.path.join(RAIZ, src)).convert("RGB")
    r = W / area_h
    if im.width / im.height > r:
        nw = int(im.height * r); x = int((im.width - nw) * foco[0]); im = im.crop((x, 0, x + nw, im.height))
    else:
        nh = int(im.width / r); y = int((im.height - nh) * foco[1]); im = im.crop((0, y, im.width, y + nh))
    z = z0 + (z1 - z0) * (t / dur)
    cw, ch = im.width / z, im.height / z
    cx, cy = im.width / 2, im.height / 2
    im = im.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, area_h), Image.LANCZOS)
    im = im.convert("RGBA")
    grad = Image.new("L", (1, area_h))
    for y in range(area_h):
        p = y / area_h
        grad.putpixel((0, y), int(255 * max(0, min(1, (p - 0.55) / 0.45)) ** 1.4) if p > 0.55 else int(190 * (1 - p / 0.25)) if p < 0.25 else 0)
    sombra = Image.new("RGBA", (W, area_h), INK + (255,))
    sombra.putalpha(grad.resize((W, area_h)))
    im.alpha_composite(sombra)
    return im


def fundo():
    return Image.new("RGBA", (W, H), INK + (255,))


# ---------- mapa ----------

class Mapa:
    ALERTA = ["Poconé", "Barão de Melgaço", "Itiquira", "Alto Taquari", "Alto Araguaia"]

    def __init__(self, geo, caixa):
        d = json.load(open(geo, encoding="utf-8"))
        self.mun = {}
        xs, ys = [], []
        for ft in d["features"]:
            g = ft["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            anel = [p[0] for p in polys]
            self.mun[ft["properties"]["name"]] = anel
            for a in anel:
                for lon, lat in a:
                    xs.append(lon); ys.append(lat)
        k = math.cos(math.radians(-13))
        self.lon0, self.lat1 = min(xs), max(ys)
        sw = (max(xs) - min(xs)) * k; sh = max(ys) - min(ys)
        x0, y0, x1, y1 = caixa
        self.s = min((x1 - x0) / sw, (y1 - y0) / sh)
        self.ox = x0 + ((x1 - x0) - sw * self.s) / 2
        self.oy = y0 + ((y1 - y0) - sh * self.s) / 2
        self.k = k
        self.SS = 2
        self.base = self._desenhar({})

    def p(self, lon, lat, ss=1):
        return ((self.ox + (lon - self.lon0) * self.k * self.s) * ss, (self.oy + (self.lat1 - lat) * self.s) * ss)

    def centro(self, nome):
        a = max(self.mun[nome], key=len)
        return self.p(sum(c[0] for c in a) / len(a), sum(c[1] for c in a) / len(a))

    def _desenhar(self, cores):
        ss = self.SS
        im = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for nome, aneis in self.mun.items():
            for a in aneis:
                pts = [self.p(lon, lat, ss) for lon, lat in a]
                d.polygon(pts, fill=cores.get(nome, (52, 50, 47)), outline=(30, 30, 30))
        return im.resize((W, H), Image.LANCZOS)

    def quadro(self, prog):
        """prog: quantos municípios em alerta já acenderam (float)."""
        cores = {}
        for i, n in enumerate(self.ALERTA):
            a = ease(prog - i)
            if a > 0:
                c0 = (52, 50, 47)
                cores[n] = tuple(int(c0[j] + (RED[j] - c0[j]) * a) for j in range(3))
        return self._desenhar(cores) if cores else self.base.copy()


def rotulo(d, xy, txt, sub=None, ancora="l", cor=WHITE, alpha=255):
    f = fonte("sans-b", 30); fs = fonte("sans", 24)
    x, y = xy
    if ancora == "r":
        x -= d.textlength(txt, font=f)
    d.text((x, y), txt, font=f, fill=cor + (alpha,))
    if sub:
        xs = xy[0] - (d.textlength(sub, font=fs) if ancora == "r" else 0)
        d.text((xs, y + 36), sub, font=fs, fill=LIGHT + (alpha,))


# ---------- cenas ----------

def cena1(t, dur):
    im = fundo()
    im.alpha_composite(foto_kb("img/fotos/sol-forte-horizonte.jpg", t, dur, 1060, foco=(0.5, 0.5), z0=1.0, z1=1.12), (0, 0))
    topo(im, "Foto ilustrativa: Pexels")
    a = ease(t / 0.45)
    y = texto_rico(im, (M, 930), "Domingo de votação vai ser *quente* em Mato Grosso", fonte("serif", 96), W - 2 * M,
                   alpha=a, dy=int(40 * (1 - a)))
    b = ease((t - 0.7) / 0.45)
    texto_rico(im, (M, y + 34), "E tem alerta de tempestade no sul do estado", fonte("sans", 44), W - 2 * M, cor=LIGHT,
               alpha=b, dy=int(30 * (1 - b)))
    return im


def cena2(t, dur):
    im = fundo()
    topo(im, "Fontes: Climatempo (Primavera) e Inmet, via Cenário MT (Cuiabá)")
    d = ImageDraw.Draw(im)
    a = ease(t / 0.35)
    f = fonte("sans-b", 34)
    x = M
    for ch in "PRIMAVERA DO LESTE · MÁXIMA PREVISTA":
        d.text((x, 520 + int(20 * (1 - a))), ch, font=f, fill=GREY + (int(255 * a),)); x += d.textlength(ch, font=f) + 2
    n = int(round(36 * ease(t / 1.1)))
    fn = fonte("serif", 380)
    d.text((M - 10, 560), f"{n}°C", font=fn, fill=RED2)
    b = ease((t - 1.1) / 0.45)
    y = texto_rico(im, (M, 1040), "e até *39°C* em Cuiabá", fonte("serif", 88), W - 2 * M, alpha=b, dy=int(30 * (1 - b)))
    c = ease((t - 1.6) / 0.45)
    texto_rico(im, (M, y + 30), "Em Primavera, sol entre nuvens e sem chuva prevista", fonte("sans", 42), W - 2 * M,
               cor=LIGHT, alpha=c, dy=int(30 * (1 - c)))
    return im


def cena3(t, dur):
    im = fundo()
    im.alpha_composite(foto_kb("img/fotos/chuva-fim-de-tarde-campo.jpg", t, dur, 1060, foco=(0.42, 0.3), z0=1.04, z1=1.14), (0, 0))
    topo(im, "Fonte: Inmet, via Cenário MT · Foto ilustrativa: Pexels")
    a = ease(t / 0.45)
    y = texto_rico(im, (M, 930), "*Alerta amarelo* de tempestade no sul do estado", fonte("serif", 96), W - 2 * M,
                   alpha=a, dy=int(40 * (1 - a)))
    b = ease((t - 0.7) / 0.45)
    texto_rico(im, (M, y + 34), "Rajadas de até 60 km/h e até 50 mm de chuva no domingo", fonte("sans", 44), W - 2 * M,
               cor=LIGHT, alpha=b, dy=int(30 * (1 - b)))
    return im


MAPA = None


def cena4(t, dur):
    im = fundo()
    topo(im, "Fonte: Inmet, via Cenário MT · Mapa: Agora Praça (malha IBGE)")
    a = ease(t / 0.4)
    texto_rico(im, (M, 270), "*5 cidades* em alerta no domingo", fonte("serif", 84), W - 2 * M, alpha=a, dy=int(30 * (1 - a)))
    prog = max(0, (t - 0.4) / 0.32)
    im.alpha_composite(MAPA.quadro(prog))
    camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    # Primavera do Leste
    px, py = MAPA.centro("Primavera do Leste")
    ap = int(255 * ease((t - 0.2) / 0.4))
    d.ellipse((px - 14, py - 14, px + 14, py + 14), fill=WHITE + (ap,), outline=INK + (ap,), width=4)
    d.line((px, py, px - 60, py - 110), fill=WHITE + (ap,), width=3)
    rotulo(d, (px - 66, py - 186), "PRIMAVERA DO LESTE", "sem alerta, até 36°C", ancora="r", alpha=ap)
    # rótulos das cidades em alerta
    grupos = [("Poconé", "POCONÉ E BARÃO", "DE MELGAÇO", 1.0, (-40, 200), "l"),
              ("Itiquira", "ITIQUIRA", None, 2.6, (0, 120), "c"),
              ("Alto Araguaia", "ALTO ARAGUAIA E", "ALTO TAQUARI", 4.4, (10, 250), "r")]
    for nome, l1, l2, quando, (dx, dy), anc in grupos:
        al = int(255 * ease(prog - quando))
        if al <= 0:
            continue
        cx, cy = MAPA.centro(nome)
        ex, ey = cx + dx, cy + dy
        d.line((cx, cy, ex, ey), fill=WHITE + (al,), width=3)
        d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=WHITE + (al,))
        f = fonte("sans-b", 30)
        larg = max(d.textlength(l1, font=f), d.textlength(l2 or "", font=f))
        xt = {"l": ex - larg / 2, "c": ex - larg / 2, "r": min(ex - larg / 2, W - M - larg)}[anc]
        d.text((xt, ey + 8), l1, font=f, fill=WHITE + (al,))
        if l2:
            d.text((xt, ey + 44), l2, font=f, fill=WHITE + (al,))
    im.alpha_composite(camada)
    return im


def cena5(t, dur):
    im = fundo()
    im.alpha_composite(foto_kb("img/fotos/urnas-lacre-tre-df.jpg", t, dur, 760, foco=(0.55, 0.5), z0=1.0, z1=1.08), (0, 0))
    topo(im, "Foto: Joédson Alves / Agência Brasil")
    a = ease(t / 0.4)
    y = texto_rico(im, (M, 700), "Para votar *no calor*", fonte("serif", 96), W - 2 * M, alpha=a, dy=int(30 * (1 - a))) + 40
    itens = ["Urnas abertas das 7h às 16h, no horário de MT. Vá cedo",
             "Leve água e evite o sol das 10h às 16h",
             "Chegou na fila antes das 16h? Ainda vota"]
    for i, it in enumerate(itens):
        b = ease((t - 0.5 - i * 0.55) / 0.4)
        camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(camada)
        d.rectangle((M, y + 22 + int(20 * (1 - b)), M + 18, y + 40 + int(20 * (1 - b))), fill=RED2 + (int(255 * b),))
        im.alpha_composite(camada)
        y = texto_rico(im, (M + 46, y), it, fonte("sans", 46), W - 2 * M - 46, cor=WHITE, alpha=b, dy=int(20 * (1 - b)), entre=1.3) + 34
    return im


def cena6(t, dur):
    im = fundo()
    d = ImageDraw.Draw(im)
    a = ease(t / 0.5)
    al = int(255 * a)
    camada = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    cx, cy = W // 2, 760
    d.rectangle((cx - 70, cy - 70, cx + 70, cy + 70), fill=RED + (al,))
    d.text((cx, cy + 6), "Á", font=fonte("serif", 130), fill=WHITE + (al,), anchor="mm")
    d.text((cx, cy + 160), "Agora Praça", font=fonte("serif", 92), fill=WHITE + (al,), anchor="mm")
    d.text((cx, cy + 240), "A praça é de todo mundo.", font=fonte("sans", 40), fill=LIGHT + (al,), anchor="mm")
    b = int(255 * ease((t - 0.5) / 0.5))
    fs = fonte("sans", 28)
    d.text((cx, cy + 380), "Fontes: Inmet, Climatempo, Cenário MT e TSE", font=fs, fill=GREY + (b,), anchor="mm")
    d.text((cx, cy + 424), "Reportagem completa em agorapraca.com.br", font=fs, fill=GREY + (b,), anchor="mm")
    im.alpha_composite(camada)
    return im


CENAS = [(cena1, 3.0), (cena2, 3.2), (cena3, 3.0), (cena4, 3.6), (cena5, 3.4), (cena6, 2.2)]


def main(geo):
    global MAPA
    MAPA = Mapa(geo, (M + 20, 440, W - M - 20, 1560))
    tmp = tempfile.mkdtemp()
    k = 0
    capa = None
    for fn, dur in CENAS:
        nf = int(round(dur * FPS))
        for i in range(nf):
            t = i / FPS
            im = fn(t, dur).convert("RGB")
            im.save(os.path.join(tmp, f"{k:05d}.png"))
            if fn is cena2 and i == nf - 1:
                capa = im.copy()
            k += 1
    out = os.path.join(RAIZ, "video", "calor-votacao.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.png"),
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart",
                    "-c:a", "aac", "-b:a", "96k", out], check=True)
    capa.save(os.path.join(RAIZ, "video", "calor-votacao.jpg"), quality=88)
    shutil.rmtree(tmp)
    print(out, k, "frames")


if __name__ == "__main__":
    main(sys.argv[1])
