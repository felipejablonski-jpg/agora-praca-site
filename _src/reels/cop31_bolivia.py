#!/usr/bin/env python3
"""Reel narrado: super El Niño abre a COP31 com a Bolívia em emergência (10/11/2026).

Narração: voz "Pedro" (Gemini Charon, pt-BR), AnyToSpeech, em um arquivo só (narracao.mp3).
Vídeos ilustrativos do Pexels em <pasta>/v/<id>.mp4. Fotos em img/fotos/.

Uso: python3 _src/reels/cop31_bolivia.py <pasta>
Teste: python3 _src/reels/cop31_bolivia.py <pasta> teste <cena> <t> <saida.jpg>
"""
import os, sys, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PASTA = sys.argv[1]
import oceano_recorde as V  # noqa: E402
from oceano_recorde import (Image, ImageDraw, W, H, M, INK, RED2, WHITE, LIGHT, GREY,  # noqa: E402
                            fonte, ease, topo, fundo, cena6, escreve, bloco, entra, sombra)
import calor_votacao as R  # noqa: E402

V.PASTA = PASTA
R.TAG = "CIÊNCIA · CLIMA"
R.FONTES_FIM = "Fontes: ONU, OMM, governo da Bolívia e Agência Brasil"
FPS = 30
# cortes nos silêncios da narração (segundos)
CORTES = [0, 9.0, 19.6, 34.5, 43.8, 54.2, 61.3, 68.1]
DUR = [b - a for a, b in zip(CORTES, CORTES[1:])] + [2.2]

V.FUNDOS = {
    0: [(0, "18657861", 0.0, 0.42), (3.9, "20523607", 0.5, 0.2)],
    1: [(0, "7211903", 2.0, 0.5)],
    2: [(0, "4023788", 0.0, 0.55), (10.4, "16905042", 1.0, 0.6)],
    3: [(0, "9789657", 0.0, 0.5)],
    4: [(0, "18991340", 0.0, 0.45), (6.7, "7211903", 12.0, 0.5)],
    6: [(0, "18657861", 5.0, 0.6)],
}


def base_video(k, t, credito, y0=520, y1=1200):
    im = V.fundo_cena(k, t)
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sombra(cam, y0, y1, 0.92)
    ImageDraw.Draw(cam).rectangle((0, y1, W, H), fill=INK + (225,))
    im.alpha_composite(cam)
    topo(im, credito)
    return im, Image.new("RGBA", im.size, (0, 0, 0, 0))


def base_foto(src, t, dur, credito, foco=(0.5, 0.5), alt=1120, z=(1.0, 1.1), caixa=None):
    im = fundo()
    im.alpha_composite(R.foto_kb(src, t, dur, alt, foco=foco, z0=z[0], z1=z[1], caixa=caixa), (0, 0))
    topo(im, credito)
    return im, Image.new("RGBA", im.size, (0, 0, 0, 0))


def s1(t, d):
    im, cam = base_video(0, t, "Vídeos ilustrativos: Pexels · Fonte: governo da Bolívia")
    n = int(round(75 * ease(t / 1.2)))
    escreve(cam, M, 880, f"{n} mil", fonte("serif", 300), RED2)
    escreve(cam, M, 1250, "CABEÇAS DE GADO MORTAS", fonte("sans-b", 58), WHITE)
    escreve(cam, M, 1322, "PELA SECA NA BOLÍVIA", fonte("sans-b", 58), WHITE)
    a = entra(t, 4.3)
    y = bloco(cam, M, 1440, "País vizinho do Brasil decreta *emergência nacional*", fonte("serif", 78), alpha=a,
              dy=int(24 * (1 - a)))
    b = entra(t, 6.9)
    bloco(cam, M, y + 30, "Decreto de 31 de outubro, por causa do El Niño", fonte("sans", 40), LIGHT, alpha=b)
    im.alpha_composite(cam)
    return im


def s2(t, d):
    if t < 3.4:
        im, cam = base_foto("img/fotos/cop31-abertura-correa-do-lago-divulgacao-2026-11-09.jpg", t, 3.4,
                            "Abertura da COP31, em 9/11. Foto: COP30/Divulgação", foco=(0.1, 0.5))
    else:
        im, cam = base_video(1, t - 3.4, "Vídeo ilustrativo: litoral da província de Antália, Turquia (Pexels)",
                             560, 1180)
    escreve(cam, M, 1150, "COP31", fonte("serif", 230), RED2)
    a = entra(t, 1.6)
    y = bloco(cam, M, 1420, "A conferência do clima da ONU começou em *Antália, na Turquia*", fonte("serif", 66),
              alpha=a, dy=int(20 * (1 - a)))
    b = entra(t, 7.2)
    bloco(cam, M, y + 40, "Quase 200 países negociam até 20 de novembro", fonte("sans-b", 44), LIGHT, alpha=b)
    im.alpha_composite(cam)
    return im


def s3(t, d):
    if 4.9 <= t < 10.4:
        im, cam = base_foto("img/elnino/mapa-pacifico-2026.jpg", t - 4.9, 5.5,
                            "Temperatura do mar em 18/10/2026 contra a média. Dados: NOAA · Mapa: Agora Praça",
                            foco=(0.72, 0.5), z=(1.0, 1.15), caixa=(0, 0.295, 1, 0.922))
    else:
        im, cam = base_video(2, t, "Fontes: OMM e NOAA · Vídeos ilustrativos: Pexels")
    if t < 4.9:
        escreve(cam, M, 1130, "O PANO DE FUNDO TEM NOME", fonte("sans-b", 44), LIGHT)
        a = entra(t, 1.3, 0.3)
        bloco(cam, M, 1220, "Super *El Niño*", fonte("serif", 170), alpha=a, dy=int(30 * (1 - a)))
    elif t < 10.4:
        a = entra(t, 4.9, 0.3)
        y = bloco(cam, M, 1190, "O oceano libera calor", fonte("serif", 96), alpha=a, dy=int(24 * (1 - a)))
        b = entra(t, 6.4)
        bloco(cam, M, y + 30, "Temperatura alta *até 2027*", fonte("serif", 96), alpha=b, dy=int(24 * (1 - b)))
    else:
        a = entra(t, 10.4, 0.3)
        escreve(cam, M, 1140, "2026", fonte("serif", 250), RED2, a)
        b = entra(t, 11.8)
        y = bloco(cam, M, 1440, "entre os *4 anos mais quentes* da história", fonte("serif", 80), alpha=b,
                  dy=int(24 * (1 - b)))
        bloco(cam, M, y + 30, "Organização Meteorológica Mundial", fonte("sans", 40), LIGHT, alpha=b)
    im.alpha_composite(cam)
    return im


def s4(t, d):
    im, cam = base_video(3, t, "Fonte: Simon Stiell, secretário de clima da ONU · Vídeo ilustrativo: Pexels", 480, 1060)
    a = entra(t, 0.6, 0.3)
    y = bloco(cam, M, 1040, "ONU cobra *soluções práticas* dos governos", fonte("serif", 88), alpha=a,
              dy=int(24 * (1 - a))) + 50
    fi = fonte("sans-b", 60)
    for txt, t0 in (("Dinheiro para adaptação", 4.4), ("Energia renovável", 6.0), ("Corte de metano", 7.5)):
        b = entra(t, t0)
        if b > 0:
            ImageDraw.Draw(cam).rectangle((M, y + 24, M + 20, y + 44), fill=RED2 + (int(255 * b),))
            escreve(cam, M + 50, y, txt, fi, WHITE, b)
        y += 96
    im.alpha_composite(cam)
    return im


def s5(t, d):
    if t < 1.7:
        im, cam = base_foto("img/fotos/nota-dolar-detalhe.jpg", t, 1.7, "Foto ilustrativa: Pexels", z=(1.0, 1.06))
    elif t < 6.7:
        im, cam = base_video(4, t - 1.7, "Vídeo ilustrativo: rebanho em área seca (Pexels)")
    else:
        im, cam = base_video(4, t, "Vídeo ilustrativo: litoral da província de Antália, Turquia (Pexels)")
    escreve(cam, M, 1130, "O MAIOR NÓ", fonte("sans-b", 44), LIGHT)
    a = entra(t, 0.3, 0.3)
    y = bloco(cam, M, 1200, "*Dinheiro*", fonte("serif", 190), alpha=a, dy=int(30 * (1 - a)))
    if t < 6.7:
        b = entra(t, 2.0)
        bloco(cam, M, y + 20, "Países mais atingidos pedem acesso mais rápido a recursos", fonte("serif", 62),
              alpha=b, dy=int(20 * (1 - b)))
    else:
        c = entra(t, 6.7, 0.3)
        bloco(cam, M, y + 20, "Pouca gente espera *grandes acordos* em Antália", fonte("serif", 70), alpha=c,
              dy=int(20 * (1 - c)))
    im.alpha_composite(cam)
    return im


def s6(t, d):
    im, cam = base_foto("img/fotos/lula-planalto-valter-campanato-abr-2026-11.jpg", t, d,
                        "Foto: Valter Campanato/Agência Brasil", foco=(0.5, 0.5))
    a = entra(t, 0.2, 0.3)
    y = bloco(cam, M, 1170, "Lula na *Cúpula de Líderes*", fonte("serif", 96), alpha=a, dy=int(24 * (1 - a)))
    b = entra(t, 1.6)
    escreve(cam, M, y + 30, "11 E 12 DE NOVEMBRO", fonte("sans-b", 54), RED2, b)
    c = entra(t, 3.3)
    bloco(cam, M, y + 130, "Primeira viagem internacional depois da reeleição", fonte("sans", 48), LIGHT, alpha=c)
    im.alpha_composite(cam)
    return im


def s7(t, d):
    im, cam = base_video(6, t, "Vídeo ilustrativo: Pexels", 420, 1000)
    escreve(cam, M, 1010, "A PERGUNTA QUE FICA", fonte("sans-b", 44), LIGHT)
    a = entra(t, 1.0, 0.3)
    y = bloco(cam, M, 1090, "O mundo paga a conta do clima *agora*", fonte("serif", 104), alpha=a,
              dy=int(24 * (1 - a)))
    b = entra(t, 4.3, 0.3)
    bloco(cam, M, y + 30, "ou depois, *com juros?*", fonte("serif", 104), alpha=b, dy=int(24 * (1 - b)))
    im.alpha_composite(cam)
    return im


def capa():
    im, cam = base_video(0, 5.2, "Vídeo ilustrativo: Pexels", 560, 1100)
    escreve(cam, M, 1000, "COP31", fonte("sans-b", 54), RED2)
    bloco(cam, M, 1090, "Super El Niño abre a COP31 com a *Bolívia em emergência*", fonte("serif", 112))
    im.alpha_composite(cam)
    return im


CENAS = [s1, s2, s3, s4, s5, s6, s7, cena6]
NOME = "cop31-bolivia"


def render():
    tmp = os.path.join(PASTA, "quadros"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    k = 0
    for fn, dur in zip(CENAS, DUR):
        for i in range(int(round(dur * FPS))):
            fn(i / FPS, dur).convert("RGB").save(os.path.join(tmp, f"{k:05d}.jpg"), quality=92)
            k += 1
    capa().convert("RGB").save(os.path.join(PASTA, NOME + ".jpg"), quality=90)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PASTA, "narracao.mp3"),
                    "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=10:release=200,"
                           "loudnorm=I=-15:TP=-1.5:LRA=9,apad",
                    "-ar", "48000", "-ac", "2", "-t", f"{k / FPS:.3f}", os.path.join(PASTA, "narracao.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.jpg"),
                    "-i", os.path.join(PASTA, "narracao.wav"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                    "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                    os.path.join(PASTA, NOME + ".mp4")], check=True)
    print("ok", k, "quadros")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "teste":
        if sys.argv[3] == "capa":
            capa().convert("RGB").save(sys.argv[5])
        else:
            fn = {f.__name__: f for f in CENAS}[sys.argv[3]]
            fn(float(sys.argv[4]), DUR[CENAS.index(fn)]).convert("RGB").save(sys.argv[5])
    else:
        render()
