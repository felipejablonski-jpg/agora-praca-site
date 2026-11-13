#!/usr/bin/env python3
"""Reel narrado: mundo tem menos de quatro anos de emissões antes de estourar 1,5°C (Global Carbon Budget 2026).

Narração: voz "Pedro" (Gemini Charon, AnyToSpeech), tirada de gravação de tela do Felipe.
Fotos de arquivo da Agência Brasil e da COP31 (divulgação), uma por cena, sem repetir. Só zoom contínuo.

Gera video/orcamento-carbono.mp4 e video/orcamento-carbono.jpg.
Uso: python3 _src/reels/orcamento_carbono.py <audio.wav>
Teste: python3 _src/reels/orcamento_carbono.py teste <cena> <t> <saida.jpg>
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import munic_impactos as P  # noqa: E402
from munic_impactos import (base, escreve, bloco, entra, R, ImageDraw,  # noqa: E402
                            W, M, RED2, WHITE, LIGHT, GREY, fonte, ease, cena6, br)

R.TAG = "CIÊNCIA · CLIMA"
R.FONTES_FIM = "Fonte: Global Carbon Project, Global Carbon Budget 2026 (10/11/2026)"

F_QUEIMA = "img/fotos/acre-queimada-pasto-rafa-neddermeyer-abr-out-2026.jpg"
F_COP = "img/fotos/cop31-abertura-correa-do-lago-divulgacao-2026-11-09.jpg"
F_BOMBA = "img/fotos/combustivel-bomba-tomaz-silva-abr-2019.jpg"
F_SP = "img/fotos/sao-paulo-poluicao-paulo-pinto-abr-2024.jpg"
F_FUMACA = "img/fotos/acre-fumaca-floresta-rafa-neddermeyer-abr-out-2026.jpg"
F_TEJO = "img/fotos/rio-tejo-acre-floresta.jpg"
P.CRED.update({
    F_QUEIMA: "Queimada em área desmatada no Acre, outubro de 2026. Foto: Rafa Neddermeyer/Agência Brasil",
    F_COP: "Abertura da COP31, em Antália (Turquia), 9/11/2026. Foto: COP30/Divulgação",
    F_BOMBA: "Abastecimento em posto de combustível, 2019. Foto: Tomaz Silva/Agência Brasil (arquivo)",
    F_SP: "Poluição do ar em São Paulo (SP), setembro de 2024. Foto: Paulo Pinto/Agência Brasil (arquivo)",
    F_FUMACA: "Fumaça sobre a floresta no Acre, outubro de 2026. Foto: Rafa Neddermeyer/Agência Brasil",
    F_TEJO: "Rio Tejo e floresta amazônica no Acre, outubro de 2026. Foto: Rafa Neddermeyer/Agência Brasil",
})

INICIO = 8.34  # ajustar com a gravação: segundo em que a fala começa, menos uns décimos
# cortes, em segundos do vídeo, dentro dos silêncios entre os parágrafos da narração (ajustar com silencedetect)
CORTES = [0, 7.51, 21.51, 33.46, 42.26, 47.86, 54.0]


def s1(t, d):
    im, cam = base(F_QUEIMA, t, d, 620, 1160, foco=(0.62, 0.5), z0=1.0, z1=1.12)
    a = entra(t, 0, 0.3)
    escreve(cam, M, 930, "MENOS DE", fonte("sans-b", 70), WHITE, a)
    escreve(cam, M, 1010, "4 anos", fonte("serif", 250), RED2, a)
    b = entra(t, 2.2, 0.35)
    bloco(cam, M, 1300, "de emissões até o planeta estourar o limite de *1,5°C*", fonte("serif", 66), alpha=b, dy=int(18 * (1 - b)))
    im.alpha_composite(cam)
    return im


def s2(t, d):
    im, cam = base(F_COP, t, d, 380, 780, foco=(0.12, 0.5), z0=1.0, z1=1.1)
    dr = ImageDraw.Draw(cam)
    a = entra(t, 0, 0.3)
    escreve(cam, M, 560, "GLOBAL CARBON BUDGET 2026", fonte("sans-b", 42), RED2, a)
    escreve(cam, M, 620, "apresentado na COP31, na Turquia", fonte("serif", 54), WHITE, a)
    # o que resta: 150 bilhões de toneladas, contado em anos de 43,3
    g = entra(t, 6.1, 0.4)
    if g > 0:
        n = int(round(150 * ease((t - 6.1) / 1.0)))
        escreve(cam, M, 790, "RESTAM", fonte("sans-b", 44), LIGHT, g)
        escreve(cam, M, 850, f"{n} bilhões", fonte("serif", 150), WHITE, g)
        escreve(cam, M, 1030, "DE TONELADAS DE CO2", fonte("sans-b", 46), WHITE, g)
    x0, x1 = M, W - M
    esc = (x1 - x0) / 150
    g2 = entra(t, 9.8, 0.3)
    if g2 > 0:
        y = 1160
        dr.rectangle((x0, y, x1, y + 90), outline=GREY + (int(255 * g2),), width=4)
        ano = 43.3
        for i in range(4):
            gi = entra(t, 10.2 + 0.6 * i, 0.45)
            if gi <= 0:
                continue
            ini = i * ano
            fim = min(150, ini + ano * gi)
            if ini >= 150:
                break
            cor = RED2 if i % 2 == 0 else (200, 52, 45)
            if (fim - ini) * esc > 6:
                dr.rectangle((x0 + ini * esc + 2, y + 4, x0 + fim * esc - 2, y + 86), fill=cor + (255,))
            if gi > 0.6 and ini + ano <= 150:
                escreve(cam, int(x0 + ini * esc + 20), y + 18, f"ano {i + 1}", fonte("sans-b", 40), WHITE, 1)
        b = entra(t, 10.3, 0.3)
        escreve(cam, M, y + 120, "Em 2026, o mundo deve emitir 43,3 bilhões", fonte("sans-b", 40), LIGHT, b)
    im.alpha_composite(cam)
    return im


def s3(t, d):
    im, cam = base(F_BOMBA, t, d, 560, 1100, foco=(0.6, 0.5), z0=1.0, z1=1.12)
    a = entra(t, 0, 0.3)
    escreve(cam, M, 820, "EMISSÕES DE COMBUSTÍVEIS FÓSSEIS", fonte("sans-b", 42), WHITE, a)
    n = entra(t, 2.0, 0.35)
    escreve(cam, M, 880, "−0,4%", fonte("serif", 230), RED2, n)
    escreve(cam, M, 1140, "EM 2026", fonte("sans-b", 50), LIGHT, n)
    b = entra(t, 7.5, 0.35)
    y = bloco(cam, M, 1260, "Petróleo: *−1,9%*", fonte("serif", 84), alpha=b, dy=int(18 * (1 - b)))
    c = entra(t, 8.3, 0.35)
    bloco(cam, M, y + 20, "choque de energia da guerra com o Irã", fonte("sans-b", 46), LIGHT, alpha=c)
    im.alpha_composite(cam)
    return im


def s4(t, d):
    im, cam = base(F_SP, t, d, 440, 900, foco=(0.55, 0.5), z0=1.02, z1=1.14)
    dr = ImageDraw.Draw(cam)
    troca = 4.5
    if t < troca:
        a = entra(t, 1.8, 0.3) * (1 - entra(t, troca - 0.25, 0.25))
        y = bloco(cam, M, 900, "Queda puxada por *guerra* *não* *dura*", fonte("serif", 100), alpha=a)
        bloco(cam, M, y + 30, "avisam os cientistas do Global Carbon Project", fonte("sans-b", 44), LIGHT, alpha=a * entra(t, 0.8, 0.3))
    else:
        a = entra(t, troca, 0.3)
        escreve(cam, M, 820, "TOTAL DE CO2, COM O DESMATAMENTO", fonte("sans-b", 40), WHITE, a)
        x0, x1 = M, W - M
        esc = (x1 - x0 - 260) / 43.3
        for i, (rot, v, cor) in enumerate([("2025", 42.8, GREY), ("2026", 43.3, RED2)]):
            g = entra(t, troca + 0.3 + 0.6 * i, 0.5)
            if g <= 0:
                continue
            y = 900 + i * 170
            escreve(cam, M, y, rot, fonte("sans-b", 40), LIGHT, g)
            dr.rectangle((x0, y + 55, x0 + v * esc * g, y + 145), fill=cor + (255,))
            escreve(cam, int(x0 + v * esc * g + 20), y + 62, br(v) + " bi", fonte("serif", 64), WHITE, g)
        b = entra(t, troca + 1.8, 0.3)
        escreve(cam, M, 1270, "O TOTAL AINDA SOBE", fonte("sans-b", 64), RED2, b)
    im.alpha_composite(cam)
    return im


def s5(t, d):
    im, cam = base(F_FUMACA, t, d, 620, 1160, foco=(0.5, 0.5), z0=1.0, z1=1.12)
    a = entra(t, 0, 0.3)
    escreve(cam, M, 900, "BRASIL", fonte("sans-b", 60), RED2, a)
    b = entra(t, 1.9, 0.35)
    bloco(cam, M, 990, "Replanta floresta, mas *desmata* *mais* do que replanta", fonte("serif", 84), alpha=b, dy=int(18 * (1 - b)))
    im.alpha_composite(cam)
    return im


def s6(t, d):
    im, cam = base(F_TEJO, t, d, 620, 1160, foco=(0.4, 0.5), z0=1.0, z1=1.1)
    a = entra(t, 0.4, 0.3)
    escreve(cam, M, 930, "MENOS DE", fonte("sans-b", 70), WHITE, a)
    escreve(cam, M, 1010, "4 anos", fonte("serif", 250), RED2, a)
    b = entra(t, 2.1, 0.35)
    bloco(cam, M, 1300, "A COP31 negocia até *20* *de* *novembro*", fonte("serif", 66), alpha=b, dy=int(18 * (1 - b)))
    im.alpha_composite(cam)
    return im


def capa():
    im, cam = base(F_QUEIMA, 0.0, 1, 620, 1160, foco=(0.62, 0.5), z0=1.0, z1=1.12)
    escreve(cam, M, 930, "MENOS DE", fonte("sans-b", 70), WHITE)
    escreve(cam, M, 1010, "4 anos", fonte("serif", 250), RED2)
    bloco(cam, M, 1300, "de emissões até o planeta estourar o limite de *1,5°C*", fonte("serif", 66))
    im.alpha_composite(cam)
    return im


FUNCS = [s1, s2, s3, s4, s5, s6]
NOME = "orcamento-carbono"


def cenas():
    return [(fn, b - a) for fn, (a, b) in zip(FUNCS, zip(CORTES, CORTES[1:]))] + [(cena6, 2.2)]


if __name__ == "__main__":
    if sys.argv[1] == "teste":
        if sys.argv[2] == "capa":
            capa().convert("RGB").save(sys.argv[4])
            sys.exit()
        fns = {fn.__name__: (fn, d) for fn, d in cenas()}
        fn, d = fns[sys.argv[2]]
        fn(float(sys.argv[3]), d).convert("RGB").save(sys.argv[4])
        sys.exit()
    audio = sys.argv[1]
    CENAS = cenas()
    R.render(CENAS, NOME + "-mudo", s1)
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
