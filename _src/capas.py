#!/usr/bin/env python3
"""Gera as capas do site (1200x675, 16:9) em img/capa/<slug>.jpg.

Regra da redação: toda matéria do site tem capa própria, feita para o site.
A capa não é a capa do Reel nem o card do Instagram colado: é foto recortada
em 16:9 sem texto por cima, ou arte de dados desenhada para 16:9, com todo o
texto dentro da imagem e legível na miniatura do celular.

Uso: python3 _src/capas.py [slug ...]   (rodar na raiz do repositório)
Sem argumentos, gera todas as capas definidas em CAPAS.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(RAIZ, "_src", "fontes")
W, H = 1200, 675
M = 72  # margem

INK = (20, 20, 20)
RED = (255, 59, 48)      # vermelho sobre fundo escuro
ORANGE = (240, 106, 52)  # laranja sobre fundo escuro
GREY = (138, 134, 126)
LIGHT = (232, 228, 220)
WHITE = (255, 255, 255)


def fonte(nome, tam):
    arq = {"serif": "libre-caslon-text-latin-700-normal.woff",
           "sans": "archivo-latin-600-normal.woff",
           "sans-b": "archivo-latin-800-normal.woff"}[nome]
    return ImageFont.truetype(os.path.join(FONTES, arq), tam)


def largura(d, txt, f):
    return d.textlength(txt, font=f)


def caber(d, txt, nome, tam, maxw):
    """Diminui a fonte até o texto caber na largura."""
    while tam > 12 and largura(d, txt, fonte(nome, tam)) > maxw:
        tam -= 2
    return fonte(nome, tam)


def quebrar(d, txt, f, maxw):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if largura(d, t, f) <= maxw:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def chapeu(d, txt, cor):
    f = fonte("sans-b", 22)
    x = M
    for ch in txt.upper():
        d.text((x, M - 6), ch, font=f, fill=cor)
        x += largura(d, ch, f) + 3


def rodape(d, txt):
    f = fonte("sans", 30)
    linhas = quebrar(d, txt, f, W - 2 * M)
    y = H - M - len(linhas) * 38 + 6
    for l in linhas:
        d.text((M, y), l, font=f, fill=LIGHT)
        y += 38


def base(txt_chapeu, cor):
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    chapeu(d, txt_chapeu, cor)
    return im, d


# ---------- capas de foto ----------

def foto(src, foco=(0.5, 0.5), caixa=None):
    """Recorta a foto em 16:9. caixa=(x0, y0, x1, y1) em fração da imagem, opcional."""
    im = Image.open(os.path.join(RAIZ, src)).convert("RGB")
    if caixa:
        x0, y0, x1, y1 = caixa
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    r = W / H
    if im.width / im.height > r:
        nw = int(im.height * r)
        x = int((im.width - nw) * foco[0])
        im = im.crop((x, 0, x + nw, im.height))
    else:
        nh = int(im.width / r)
        y = int((im.height - nh) * foco[1])
        im = im.crop((0, y, im.width, y + nh))
    return im.resize((W, H), Image.LANCZOS)


def foto_retrato(src):
    """Foto vertical inteira no centro, com o fundo preenchido pela própria foto desfocada."""
    im = Image.open(os.path.join(RAIZ, src)).convert("RGB")
    fundo = foto(src).filter(ImageFilter.GaussianBlur(28))
    fundo = Image.blend(fundo, Image.new("RGB", (W, H), INK), 0.45)
    nh = H
    nw = int(im.width * nh / im.height)
    fundo.paste(im.resize((nw, nh), Image.LANCZOS), ((W - nw) // 2, 0))
    return fundo


def foto_dupla(a, b, caixa_a=None, caixa_b=None):
    """Duas fotos lado a lado, metade da capa para cada uma."""
    def metade(src, caixa):
        im = Image.open(os.path.join(RAIZ, src)).convert("RGB")
        if caixa:
            x0, y0, x1, y1 = caixa
            im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
        r = (W // 2) / H
        if im.width / im.height > r:
            nw = int(im.height * r); x = (im.width - nw) // 2; im = im.crop((x, 0, x + nw, im.height))
        else:
            nh = int(im.width / r); im = im.crop((0, 0, im.width, nh))
        return im.resize((W // 2, H), Image.LANCZOS)
    out = Image.new("RGB", (W, H), WHITE)
    out.paste(metade(a, caixa_a), (0, 0))
    out.paste(metade(b, caixa_b), (W // 2 + 3, 0))
    return out


# ---------- capas de arte (dados) ----------
# Regra: arte NÃO é capa. Estas funções ficam para gráficos dentro da matéria.

def arte_troca(txt_chapeu, cor, antes, depois, legenda):
    """Número antigo riscado e número novo em destaque."""
    im, d = base(txt_chapeu, cor)
    fa = fonte("serif", 150)
    fd = fonte("serif", 300)
    ya = 130
    d.text((M, ya), antes, font=fa, fill=GREY)
    bb = d.textbbox((M, ya), antes, font=fa)
    meio = (bb[1] + bb[3]) // 2
    d.line((M - 8, meio + 14, bb[2] + 8, meio - 14), fill=RED, width=12)
    d.text((M, 250), depois, font=fd, fill=cor)
    bx = d.textbbox((M, 250), depois, font=fd)
    f = fonte("sans", 34)
    linhas = quebrar(d, legenda, f, W - bx[2] - 60 - M)
    y = bx[3] - len(linhas) * 44
    for l in linhas:
        d.text((bx[2] + 60, y), l, font=f, fill=LIGHT)
        y += 44
    return im


def arte_barras(txt_chapeu, cor, a, b, destaque, legenda):
    im, d = base(txt_chapeu, cor)
    (la, va), (lb, vb) = a, b
    topo, chao = 150, 530
    alt = chao - topo
    ha = int(alt * va / vb)
    bw = 220
    xa, xb = M + 40, M + 40 + bw + 80
    d.rectangle((xa, chao - ha, xa + bw, chao), fill=(96, 93, 88))
    barra = Image.new("RGB", (bw, alt), cor)
    db = ImageDraw.Draw(barra)
    for k in range(-alt, bw, 26):  # listras, só dentro da barra
        db.line((k, alt, k + alt, 0), fill=(178, 50, 20) if cor == ORANGE else (176, 28, 34), width=9)
    im.paste(barra, (xb, topo))
    fv = fonte("serif", 46)
    for x, v, c, y in ((xa, va, LIGHT, chao - ha), (xb, vb, cor, topo)):
        t = f"{v:,}".replace(",", ".")
        d.text((x + (bw - largura(d, t, fv)) / 2, y - 62), t, font=fv, fill=c)
    fl = fonte("sans-b", 26)
    for x, t in ((xa, la), (xb, lb)):
        d.text((x + (bw - largura(d, t, fl)) / 2, chao + 14), t, font=fl, fill=LIGHT)
    d.line((M, chao, xb + bw + 40, chao), fill=GREY, width=2)
    xr = xb + bw + 90
    fdst = fonte("serif", 150)
    d.text((xr, 160), destaque, font=fdst, fill=cor)
    f = fonte("sans", 34)
    y = 360
    for l in quebrar(d, legenda, f, W - xr - M):
        d.text((xr, y), l, font=f, fill=LIGHT)
        y += 44
    return im


def arte_numero(txt_chapeu, cor, numero, legenda, acima=None, seta=None):
    """Um número ou palavra em destaque, com frase acima (opcional) e legenda logo abaixo.
    seta=(a, b) desenha "a → b" com a seta feita à mão (a fonte não tem o caractere)."""
    im, d = base(txt_chapeu, cor)
    maxw = W - 2 * M
    blocos = []  # (altura, função de desenho)
    if acima:
        fa = caber(d, acima, "serif", 60, maxw)
        for l in quebrar(d, acima, fa, maxw):
            blocos.append((int(fa.size * 1.2), lambda y, l=l, fa=fa: d.text((M, y), l, font=fa, fill=WHITE)))
    tam = 250 if not acima else 200
    if seta:
        a, b = seta
        fn = fonte("serif", tam)
        while tam > 40 and largura(d, a, fn) + largura(d, b, fn) + tam * 1.1 > maxw:
            tam -= 4
            fn = fonte("serif", tam)
        def desenha(y, a=a, b=b, fn=fn, tam=tam):
            d.text((M, y), a, font=fn, fill=cor)
            x0 = M + largura(d, a, fn) + tam * 0.18
            x1 = x0 + tam * 0.72
            bb = d.textbbox((M, y), a, font=fn)
            ym = (bb[1] + bb[3]) / 2
            esp = max(6, tam // 16)
            d.line((x0, ym, x1 - esp * 2, ym), fill=cor, width=esp)
            d.polygon([(x1, ym), (x1 - tam * 0.26, ym - tam * 0.2), (x1 - tam * 0.26, ym + tam * 0.2)], fill=cor)
            d.text((x1 + tam * 0.18, y), b, font=fn, fill=cor)
        blocos.append((int(tam * 1.05), desenha))
    else:
        fn = caber(d, numero, "serif", tam, maxw)
        blocos.append((int(fn.size * 1.05), lambda y, fn=fn: d.text((M, y - fn.size * 0.1), numero, font=fn, fill=cor)))
    fl = fonte("sans", 34)
    blocos.append((14, lambda y: None))
    for l in quebrar(d, legenda, fl, maxw):
        blocos.append((44, lambda y, l=l: d.text((M, y), l, font=fl, fill=LIGHT)))
    total = sum(h for h, _ in blocos)
    y = M + 40 + max(0, (H - M - (M + 40) - total) // 2)
    for h, fdes in blocos:
        fdes(y)
        y += h
    return im


def foto_conter(src, caixa):
    """Mostra o recorte inteiro (mapas e artes), sem cortar nada; as laterais
    são preenchidas pela própria imagem desfocada e escurecida."""
    im = Image.open(os.path.join(RAIZ, src)).convert("RGB")
    x0, y0, x1, y1 = caixa
    im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    # fundo liso na cor da borda direita do recorte (fundo do mapa)
    borda = im.crop((im.width - 4, 0, im.width, im.height)).resize((1, 1), Image.BOX).getpixel((0, 0))
    fundo = Image.new("RGB", (W, H), borda)
    nh = H
    nw = int(im.width * nh / im.height)
    if nw > W:
        nw, nh = W, int(im.height * W / im.width)
    fundo.paste(im.resize((nw, nh), Image.LANCZOS), ((W - nw) // 2, (H - nh) // 2))
    return fundo


# ---------- definição das capas ----------
# credito: o que aparece embaixo da capa na página da matéria.

CAPAS = {
    "domingo-de-votacao-calor-alerta-tempestade-mt": (
        lambda: foto("img/fotos/chuva-fim-de-tarde-campo.jpg", foco=(0.5, 0.3)),
        "Chuva chega no fim de tarde sobre área rural. Foto ilustrativa: Pexels"),
    "justica-eleitoral-corrige-343-secoes-mudanca-local": (
        lambda: foto("img/fotos/urnas-preparacao-sp.jpg", foco=(0.35, 0.5)),
        "Urnas na preparação para a eleição em São Paulo. Foto: Paulo Pinto / Agência Brasil"),
    "calor-europa-50-mil-mortes-2026": (
        lambda: foto("img/fotos/fonte-bratislava-verao.jpg", foco=(0.5, 0.6)),
        "Crianças se refrescam em uma fonte no verão. Foto ilustrativa: Pexels"),
    "ondas-de-calor-gigantes-20-vezes-mais-frequentes": (
        lambda: foto("img/fotos/sol-cidade-laranja.jpg", foco=(0.4, 0.5)),
        "Sol sobre cidade encoberta pela névoa seca. Foto ilustrativa: Pexels"),
    "bolsa-familia-antecipa-pagamento-quarta-21": (
        lambda: foto("img/fotos/notas-real.jpg"),
        "Notas de real. Foto ilustrativa: Pexels"),
    "debate-band-lula-flavio-segundo-turno": (
        lambda: foto_dupla("img/fotos/lula-ceilandia.jpg", "img/fotos/flavio-paulista.jpg",
                           (0.15, 0.25, 0.75, 1), (0.25, 0, 0.75, 0.75)),
        "Lula em ato na Ceilândia (DF), em 9/10 (Bruno Peres/Agência Brasil), e Flávio em ato na Avenida Paulista, em 18/10 (Rafa Neddermeyer/Agência Brasil)"),
    "pode-levar-cola-para-votar": (
        lambda: foto("img/fotos/urna-treinamento-tre-sp.jpg", foco=(0.3, 0.5)),
        "Demonstração da urna no TRE-SP. Foto: Paulo Pinto / Agência Brasil"),
    "senado-aprova-teto-mei-perdao-dividas": (
        lambda: foto("img/fotos/senado-sessao-mei.jpg", foco=(0.4, 0.5)),
        "Sessão do Senado que votou o projeto do MEI, em 15 de outubro. Foto: Lula Marques / Agência Brasil"),
    "locais-de-votacao-segundo-turno": (
        lambda: foto("img/fotos/urnas-lacre-tre-df.jpg", foco=(0.55, 0.5)),
        "Lacração de urnas no TRE-DF. Foto: Joédson Alves / Agência Brasil"),
    "ebola-oitava-provincia-congo": (
        lambda: foto("img/fotos/traje-protecao.jpg", caixa=(0.3, 0, 1, 0.9), foco=(0.5, 0.2)),
        "Traje de proteção usado por profissionais de saúde. Foto ilustrativa: Pexels"),
    "romenia-abate-drones-otan-mar-negro": (
        lambda: foto("img/fotos/f16-ceu.jpg", foco=(0.45, 0.5)),
        "Caça F-16, modelo usado pela Força Aérea da Romênia. Foto ilustrativa: Pexels"),
    "amazonia-emite-mais-co2-do-que-absorve-estudo-inpe-nature": (
        lambda: foto("img/amazonia/satelite-fogo-2024-09-08.jpg"),
        "Imagem de satélite: NASA Worldview, 8 de setembro de 2024"),
    "el-nino-recorde-onu-pacifico-3-8-graus": (
        lambda: foto("img/fotos/oceano-ondas.jpg"),
        "Ondas em mar aberto. Foto ilustrativa: Pexels"),
    "analise-debate-band-flavio-atras-de-lula-marcal": (
        lambda: foto_dupla("img/fotos/lula-ceilandia.jpg", "img/fotos/flavio-paulista.jpg",
                           (0.15, 0.25, 0.75, 1), (0.25, 0, 0.75, 0.75)),
        "Lula em ato na Ceilândia (DF), em 9/10 (Bruno Peres/Agência Brasil), e Flávio em ato na Avenida Paulista, em 18/10 (Rafa Neddermeyer/Agência Brasil)"),
    "missil-inflavel-ataque-nuclear-ato-pro-flavio": (
        lambda: foto_retrato("img/missil.jpg"),
        "Foto: reprodução / redes sociais (autoria não identificada)"),
}


def gerar(slugs=None):
    os.makedirs(os.path.join(RAIZ, "img", "capa"), exist_ok=True)
    for s, (fn, _) in CAPAS.items():
        if slugs and s not in slugs:
            continue
        fn().save(os.path.join(RAIZ, "img", "capa", f"{s}.jpg"), quality=88, optimize=True)
        print("capa:", s)


if __name__ == "__main__":
    gerar(sys.argv[1:] or None)
