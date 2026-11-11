#!/usr/bin/env python3
"""Reel narrado da Munic 2025 (IBGE, 11/11/2026): versão com a voz "Pedro" (Gemini Charon, AnyToSpeech).

A narração veio de uma gravação de tela do Felipe tocando o mp3. As cenas cortam nos silêncios da fala.
Gera video/munic-impactos.mp4 e video/munic-impactos.jpg (substitui a versão muda).

Uso: python3 _src/reels/munic_impactos_narrado.py <audio.wav>
Teste: python3 _src/reels/munic_impactos_narrado.py teste <cena> <t> <saida.jpg>
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import munic_impactos as P  # noqa: E402
from munic_impactos import (base, foto_tela, flash, br, escreve, bloco, entra, R, Image, ImageDraw,  # noqa: E402
                            W, M, INK, RED2, WHITE, LIGHT, GREY, fonte, ease, topo, cena6, capa, s1, s6, s7,
                            F_PONTE, F_SECA, F_ALAGA, F_DESLIZ)

F_PREF = "img/fotos/porto-alegre-prefeitura-alagada-gilvan-rocha-abr-2024.jpg"
F_BUSCA = "img/fotos/morro-da-oficina-buscas-tania-rego-abr-2022.jpg"
F_SP = "img/fotos/sao-paulo-poluicao-paulo-pinto-abr-2024.jpg"
P.CRED.update({
    F_PREF: "Prefeitura e Mercado Público alagados em Porto Alegre (RS), maio de 2024. Foto: Gilvan Rocha/Agência Brasil (arquivo)",
    F_BUSCA: "Buscas no Morro da Oficina, Petrópolis (RJ), fevereiro de 2022. Foto: Tânia Rêgo/Agência Brasil (arquivo)",
    F_SP: "Poluição do ar em São Paulo (SP), setembro de 2024. Foto: Paulo Pinto/Agência Brasil (arquivo)",
})

INICIO = 1.6  # segundo da gravação em que o vídeo começa (a fala começa em 1,77 s)
# cortes, em segundos do vídeo, sempre dentro de um silêncio da narração
CORTES = [0, 7.2, 13.6, 19.1, 23.75, 26.3, 29.3, 35.2, 38.9, 42.6]


def s_ibge(t, d):
    im, cam = base(F_PREF, t, d, 600, 1150, foco=(0.5, 0.5), z0=1.18, z1=1.05, pan=0.4)
    n = int(round(5571 * ease((t - 0.2) / 1.6)))
    escreve(cam, M, 1000, f"{n:,}".replace(",", "."), fonte("serif", 250), RED2)
    escreve(cam, M, 1310, "MUNICÍPIOS", fonte("sans-b", 72), WHITE, entra(t, 0.3, 0.3))
    a = entra(t, 2.6, 0.35)
    y = bloco(cam, M, 1420, "O IBGE ouviu as *prefeituras* de todo o país", fonte("serif", 74), alpha=a,
              dy=int(22 * (1 - a)))
    b = entra(t, 4.2, 0.3)
    escreve(cam, M, y + 30, "Munic 2025, divulgada nesta quarta (11)", fonte("sans-b", 40), LIGHT, b)
    im.alpha_composite(cam)
    return flash(im, t)


def s_comparacao(t, d):
    """Em 2020, 66,2%; agora, 74,3%. A barra de 2025 entra quando a voz diz 'agora'."""
    im = foto_tela(F_ALAGA, t, d, foco=(0.5, 0.5), z0=1.1, z1=1.2, pan=-0.3, escuro=0.8)
    topo(im, "Gráfico: Agora Praça · Dados: IBGE, Munic 2020 e 2025 · Foto ao fundo: Rafa Neddermeyer/Agência Brasil")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(cam)
    a = entra(t, 0, 0.3)
    escreve(cam, M, 360, "Cidades com algum", fonte("serif", 84), WHITE, a)
    escreve(cam, M, 460, "impacto ambiental", fonte("serif", 84), WHITE, a)
    escreve(cam, M, 580, "EM DOIS ANOS, SEGUNDO AS PREFEITURAS", fonte("sans-b", 34), LIGHT, a)
    base_y, topo_y = 1640, 760
    larg = 330
    for ano, v, cor, t0, x in (("2020", 66.2, GREY, 0.25, M + 20), ("2025", 74.3, RED2, 2.75, W - M - 20 - larg)):
        g = entra(t, t0, 0.7)
        if g <= 0:
            continue
        h = (base_y - topo_y) * v / 80 * g
        dr.rectangle((x, base_y - h, x + larg, base_y), fill=cor + (255,))
        f = fonte("serif", 120)
        txt = br(v * g) + "%"
        escreve(cam, int(x + larg / 2), int(base_y - h - 150), txt, f, RED2 if ano == "2025" else WHITE, 1.0, "meio")
        escreve(cam, int(x + larg / 2), base_y + 30, ano, fonte("sans-b", 64), WHITE, 1.0, "meio")
    im.alpha_composite(cam)
    return flash(im, t)


def impacto(src, nome, v25, v20, foco, pan, t_num):
    def cena(t, d):
        im, cam = base(src, t, d, 700, 1250, foco=foco, z0=1.04, z1=1.16, pan=pan)
        n = v25 * ease((t - t_num) / 0.9)
        if t >= t_num - 0.05:
            escreve(cam, M, 1060, br(n) + "%", fonte("serif", 250), RED2)
        escreve(cam, M, 1370, nome, fonte("sans-b", 72), WHITE, entra(t, 0.05, 0.25))
        a = entra(t, t_num + 0.9, 0.3)
        bloco(cam, M, 1480, f"das cidades · eram *{br(v20)}%* em 2020", fonte("sans-b", 48), LIGHT, alpha=a,
              dy=int(18 * (1 - a)))
        im.alpha_composite(cam)
        return flash(im, t)
    cena.__name__ = "impacto_" + nome.split()[-1].lower()
    return cena


s_seca = impacto(F_SECA, "COM SECA", 59.0, 53.4, (0.35, 0.5), -0.5, 2.2)
s_alaga = impacto(F_ALAGA, "COM ALAGAMENTO", 49.5, 35.8, (0.45, 0.5), 0.5, 0.25)
s_desliz = impacto(F_BUSCA, "COM DESLIZAMENTO", 25.2, 17.1, (0.08, 0.5), 0.2, 0.25)


def s_adapta(t, d):
    """Só 1 em 10 tem lei ou plano. Reaproveita a cena muda sem a linha das emissões, que ganhou cena própria."""
    im, cam = base(F_DESLIZ, t, d, 520, 1000, foco=(0.5, 0.4), z0=1.15, z1=1.0, pan=0.3)
    escreve(cam, M, 820, "1 em 10", fonte("serif", 250), RED2, entra(t, 0.3, 0.25))
    dr = ImageDraw.Draw(cam)
    lado, gap = 72, 18
    for i in range(10):
        g = entra(t, 0.5 + 0.06 * i, 0.2)
        if g <= 0:
            continue
        x = M + i * (lado + gap)
        yb = 1170
        cor = RED2 if i == 0 else (90, 88, 84)
        al = int(255 * g)
        dr.polygon([(x, yb), (x + lado / 2, yb - 34), (x + lado, yb)], fill=cor + (al,))
        dr.rectangle((x + 8, yb, x + lado - 8, yb + 52), fill=cor + (al,))
    a = entra(t, 1.6, 0.35)
    bloco(cam, M, 1300, "das cidades tem *lei* *ou* *plano* para se adaptar à mudança do clima", fonte("serif", 70),
          alpha=a, dy=int(22 * (1 - a)))
    im.alpha_composite(cam)
    return flash(im, t)


def s_emissoes(t, d):
    im, cam = base(F_SP, t, d, 560, 1100, foco=(0.55, 0.5), z0=1.05, z1=1.18, pan=-0.4)
    n = 2.7 * ease((t - 0.3) / 0.9)
    escreve(cam, M, 960, br(n) + "%", fonte("serif", 250), RED2)
    a = entra(t, 0.6, 0.3)
    y = bloco(cam, M, 1270, "das cidades medem quanto *gás* *do* *efeito* *estufa* emitem", fonte("serif", 72),
              alpha=a, dy=int(22 * (1 - a)))
    b = entra(t, 2.0, 0.3)
    bloco(cam, M, y + 30, "São 151 dos 5.571 municípios", fonte("sans-b", 44), LIGHT, alpha=b)
    im.alpha_composite(cam)
    return flash(im, t)


def s_pergunta(t, d):
    im, cam = base(F_PONTE, t, d, 600, 1150, foco=(0.7, 0.5), z0=1.3, z1=1.12, pan=0.3)
    escreve(cam, M, 1080, "A PERGUNTA QUE FICA", fonte("sans-b", 44), LIGHT, entra(t, 0.25, 0.25))
    a = entra(t, 1.4, 0.3)
    bloco(cam, M, 1170, "A sua cidade está *preparada?*", fonte("serif", 120), alpha=a, dy=int(24 * (1 - a)))
    im.alpha_composite(cam)
    return flash(im, t)


def s_abre(t, d):
    """Abertura: a mesma da versão muda, com o texto no ritmo da fala."""
    return s1(t * 0.75, d)


FUNCS = [s_abre, s_ibge, s_comparacao, s_seca, s_alaga, s_desliz, s_adapta, s_emissoes, s_pergunta]
CENAS = [(fn, b - a) for fn, (a, b) in zip(FUNCS, zip(CORTES, CORTES[1:]))] + [(cena6, 2.2)]
NOME = "munic-impactos"

if __name__ == "__main__":
    if sys.argv[1] == "teste":
        fns = {fn.__name__: (fn, d) for fn, d in CENAS}
        fn, d = fns[sys.argv[2]]
        fn(float(sys.argv[3]), d).convert("RGB").save(sys.argv[4])
        sys.exit()
    audio = sys.argv[1]
    R.render(CENAS, NOME + "-mudo", s_abre)
    total = sum(d for _, d in CENAS)
    out = os.path.join(R.RAIZ, "video", NOME + ".mp4")
    mudo = os.path.join(R.RAIZ, "video", NOME + "-mudo.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mudo, "-ss", str(INICIO), "-i", audio,
                    "-filter_complex", "[1:a]highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=10:release=200,"
                    "loudnorm=I=-15:TP=-1.5:LRA=9,apad[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True)
    os.remove(mudo)
    os.remove(os.path.join(R.RAIZ, "video", NOME + "-mudo.jpg"))
    capa().convert("RGB").save(os.path.join(R.RAIZ, "video", NOME + ".jpg"), quality=88)
    print("ok", out, f"{total:.2f} s")
