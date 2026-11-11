#!/usr/bin/env python3
"""Reel narrado: ondas de calor do futuro podem durar seis meses (Nature Communications, 5/11/2026).

Narração: voz "Pedro" (Gemini Charon, AnyToSpeech), tirada de gravação de tela do Felipe.
Vídeos ilustrativos do Pexels (quadros extraídos em <pasta>/fr/<chave>/%05d.jpg, 1080x1920, 30 fps)
e fotos de arquivo da Agência Brasil. Só zoom contínuo nas fotos: sem pulso, sem clarão.

Gera video/ondas-calor.mp4 e video/ondas-calor.jpg.
Uso: python3 _src/reels/ondas_calor.py <pasta_dos_quadros> <audio.wav>
Teste: python3 _src/reels/ondas_calor.py <pasta> teste <cena> <t> <saida.jpg>
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PASTA = sys.argv[1]
import munic_impactos as P  # noqa: E402
from munic_impactos import (base, escreve, bloco, entra, sombra, R, Image, ImageDraw,  # noqa: E402
                            W, H, M, INK, RED2, WHITE, LIGHT, GREY, fonte, ease, topo, cena6, br)

R.TAG = "CIÊNCIA NA PRAÇA"
R.FONTES_FIM = "Fonte: Aglas-Leitner et al., Nature Communications (5/11/2026)"

F_FRAZAO = "img/fotos/calor-rio-fernando-frazao-abr-fev-2025.jpg"
F_ANHANG = "img/fotos/calor-anhangabau-paulo-pinto-abr-nov-2023.jpg"
F_TANIA = "img/fotos/calor-rio-tania-rego-abr-fev-2024.jpg"
P.CRED.update({
    F_FRAZAO: "Onda de calor no Rio de Janeiro (RJ), fevereiro de 2025. Foto: Fernando Frazão/Agência Brasil (arquivo)",
    F_ANHANG: "Calor no Vale do Anhangabaú, São Paulo (SP), novembro de 2023. Foto: Paulo Pinto/Agência Brasil (arquivo)",
    F_TANIA: "Calor no centro do Rio de Janeiro (RJ), fevereiro de 2024. Foto: Tânia Rêgo/Agência Brasil (arquivo)",
})
VCRED = {
    "ceu": "Imagem ilustrativa. Vídeo: Dmitry Marchenkov/Pexels",
    "nuvens": "Imagem ilustrativa. Vídeo: Dmitry Marchenkov/Pexels",
    "estrada": "Imagem ilustrativa. Vídeo: Grbr Snts/Pexels",
    "praia": "Imagem ilustrativa. Vídeo: Roman Odintsov/Pexels",
    "cidade": "Imagem ilustrativa. Vídeo: Aero Drone/Pexels",
}

INICIO = 3.5  # segundo da gravação em que o vídeo começa (a fala começa em 3,76 s)
# cortes, em segundos do vídeo, dentro dos silêncios da narração
CORTES = [0, 5.95, 14.45, 18.5, 24.6, 30.5, 36.45, 42.75, 51.5]


def video_base(k, t, y0=820, y1=1380, forte=0.92):
    pasta = os.path.join(PASTA, "fr", k)
    n = len(os.listdir(pasta))
    i = min(n, int(t * 30) + 1)
    im = Image.open(os.path.join(pasta, f"{i:05d}.jpg")).convert("RGBA")
    cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(cam).rectangle((0, 0, W, 260), fill=INK + (90,))
    sombra(cam, y0, y1, forte)
    ImageDraw.Draw(cam).rectangle((0, y1, W, H), fill=INK + (int(255 * forte),))
    im.alpha_composite(cam)
    topo(im, VCRED[k])
    return im, Image.new("RGBA", im.size, (0, 0, 0, 0))


def s1(t, d):
    im, cam = video_base("praia", t)
    escreve(cam, M, 960, "NATURE COMMUNICATIONS", fonte("sans-b", 44), RED2, entra(t, 0, 0.3))
    y = bloco(cam, M, 1040, "Ondas de calor do futuro podem durar *seis* *meses*", fonte("serif", 104), alpha=entra(t, 0.1, 0.3))
    a = entra(t, 2.4, 0.4)
    bloco(cam, M, y + 30, "e deixar os recordes de hoje para trás", fonte("sans-b", 50), LIGHT, alpha=a, dy=int(18 * (1 - a)))
    im.alpha_composite(cam)
    return im


def s2(t, d):
    im, cam = video_base("nuvens", t)
    n = int(round(22 * ease((t - 0.3) / 1.2)))
    escreve(cam, M, 900, str(n), fonte("serif", 260), RED2)
    escreve(cam, M, 1210, "ONDAS DE CALOR", fonte("sans-b", 64), WHITE, entra(t, 0.3, 0.3))
    a = entra(t, 1.8, 0.35)
    y = bloco(cam, M, 1310, "de 2010 a 2023, comparadas com projeções até *2100*", fonte("serif", 70), alpha=a, dy=int(20 * (1 - a)))
    b = entra(t, 4.0, 0.35)
    escreve(cam, M, y + 40, "Nature Communications · 5/11/2026", fonte("sans-b", 40), LIGHT, b)
    im.alpha_composite(cam)
    return im


def s3(t, d):
    im, cam = video_base("estrada", t)
    escreve(cam, M, 990, "6 meses", fonte("serif", 200), RED2, entra(t, 0.2, 0.3))
    escreve(cam, M, 1270, "SEGUIDOS DE CALOR", fonte("sans-b", 66), WHITE, entra(t, 0.4, 0.3))
    a = entra(t, 1.6, 0.35)
    bloco(cam, M, 1380, "o limite do que o estudo consegue medir", fonte("serif", 64), LIGHT, alpha=a, dy=int(18 * (1 - a)))
    im.alpha_composite(cam)
    return im


REGIOES = ["Europa", "Nordeste da Sibéria", "Norte da África e Oriente Médio", "Noroeste da América do Norte", "América do Sul"]


def s4(t, d):
    im, cam = base(F_FRAZAO, t, d, 380, 780, foco=(0.5, 0.5), z0=1.0, z1=1.12)
    a = entra(t, 0, 0.3)
    y = bloco(cam, M, 680, "Regiões que chegam perto dos *6* *meses* mesmo com corte forte de emissões", fonte("serif", 64), alpha=a)
    y += 40
    for i, nome in enumerate(REGIOES):
        g = entra(t, 0.5 + 0.35 * i, 0.3)
        if g <= 0:
            continue
        sul = nome == "América do Sul"
        if sul and t >= 3.9:
            f = fonte("sans-b", 64)
            dr = ImageDraw.Draw(cam)
            larg = dr.textlength(nome.upper(), font=f)
            dr.rectangle((M - 14, y - 10, M + larg + 14, y + 80), fill=RED2 + (255,))
            escreve(cam, M, y, nome.upper(), f, WHITE)
            y += 100
        else:
            escreve(cam, M, y, nome.upper(), fonte("sans-b", 46), WHITE if not sul else LIGHT, g)
            y += 72
    im.alpha_composite(cam)
    return im


def s5(t, d):
    im, cam = video_base("ceu", t, 300, 700, 0.9)
    dr = ImageDraw.Draw(cam)
    a = entra(t, 0, 0.3)
    escreve(cam, M, 380, "AMÉRICA DO SUL", fonte("sans-b", 46), RED2, a)
    escreve(cam, M, 450, "Duração da onda de calor", fonte("serif", 74), WHITE, a)
    x0, x1 = M, W - M
    esc = (x1 - x0) / 180
    # 2022: 7 dias
    g = entra(t, 0.5, 0.4)
    if g > 0:
        escreve(cam, M, 700, "RECORDE DE 2022", fonte("sans-b", 40), LIGHT, g)
        dr.rectangle((x0, 770, x0 + 7 * esc * g, 870), fill=GREY + (255,))
        escreve(cam, int(x0 + 7 * esc + 24), 772, "7 dias", fonte("serif", 84), WHITE, g)
    # futuro: até 180 dias
    g2 = entra(t, 3.6, 1.2)
    if g2 > 0:
        escreve(cam, M, 1010, "NO FUTURO, ATÉ", fonte("sans-b", 40), LIGHT, min(1, g2 * 3))
        dr.rectangle((x0, 1080, x0 + 180 * esc * g2, 1180), fill=RED2 + (255,))
        n = int(round(180 * g2))
        escreve(cam, M, 1210, f"{n} dias", fonte("serif", 120), RED2, min(1, g2 * 3))
        escreve(cam, M, 1370, "o teto de seis meses da análise", fonte("sans-b", 40), LIGHT, entra(t, 4.6, 0.3))
    im.alpha_composite(cam)
    return im


def s6(t, d):
    im, cam = video_base("cidade", t)
    escreve(cam, M, 930, "5x", fonte("serif", 280), RED2, entra(t, 0.2, 0.3))
    escreve(cam, M, 1260, "MAIS CALOR ACUMULADO", fonte("sans-b", 64), WHITE, entra(t, 0.5, 0.3))
    a = entra(t, 2.4, 0.35)
    y = bloco(cam, M, 1370, "que os recordes de hoje, em parte das ondas projetadas", fonte("serif", 62), alpha=a, dy=int(18 * (1 - a)))
    b = entra(t, 3.6, 0.3)
    bloco(cam, M, y + 30, "Cenário de emissões altas: de 1 em 10 a 1 em 5 ondas, na maioria das regiões", fonte("sans-b", 36), LIGHT, alpha=b)
    im.alpha_composite(cam)
    return im


def s7(t, d):
    im, cam = base(F_ANHANG, t, d, 640, 1150, foco=(0.5, 0.5), z0=1.0, z1=1.12)
    troca = 4.2
    if t < troca:
        a = entra(t, 0.2, 0.3) * (1 - entra(t, troca - 0.25, 0.25))
        escreve(cam, M, 1020, "1 vez", fonte("serif", 230), RED2, a)
        escreve(cam, M, 1300, "A CADA 55 ANOS", fonte("sans-b", 70), WHITE, a)
        bloco(cam, M, 1410, "era o ritmo de um calor assim, de 1951 a 2005", fonte("serif", 60), LIGHT, alpha=a * entra(t, 1.0, 0.3))
    else:
        a = entra(t, troca, 0.3)
        escreve(cam, M, 1020, "Todo ano", fonte("serif", 200), RED2, a)
        escreve(cam, M, 1280, "ATÉ O FIM DO SÉCULO", fonte("sans-b", 70), WHITE, a)
        bloco(cam, M, 1390, "na maior parte dos modelos, de 2060 a 2099", fonte("serif", 60), LIGHT, alpha=entra(t, troca + 0.6, 0.3))
    im.alpha_composite(cam)
    return im


def s8(t, d):
    im, cam = base(F_TANIA, t, d, 640, 1150, foco=(0.5, 0.5), z0=1.0, z1=1.14)
    troca = 4.6
    if t < troca:
        a = entra(t, 0.2, 0.3) * (1 - entra(t, troca - 0.25, 0.25))
        y = bloco(cam, M, 1080, "O estudo mede o *calor*", fonte("serif", 96), alpha=a)
        bloco(cam, M, y + 30, "Mortes e prejuízos ficam fora da conta", fonte("sans-b", 50), LIGHT, alpha=a * entra(t, 1.6, 0.3))
    else:
        a = entra(t, troca, 0.3)
        y = bloco(cam, M, 1080, "Cortar emissões ajuda.", fonte("serif", 90), alpha=a)
        b = entra(t, troca + 0.9, 0.3)
        bloco(cam, M, y + 10, "*E* *vai* *ser* *preciso* *se* *adaptar.*", fonte("serif", 90), alpha=b)
    im.alpha_composite(cam)
    return im


def capa():
    im, cam = video_base("praia", 1.0)
    escreve(cam, M, 960, "NATURE COMMUNICATIONS", fonte("sans-b", 44), RED2)
    y = bloco(cam, M, 1040, "Ondas de calor do futuro podem durar *seis* *meses*", fonte("serif", 104))
    bloco(cam, M, y + 30, "e deixar os recordes de hoje para trás", fonte("sans-b", 50), LIGHT)
    im.alpha_composite(cam)
    return im


FUNCS = [s1, s2, s3, s4, s5, s6, s7, s8]
CENAS = [(fn, b - a) for fn, (a, b) in zip(FUNCS, zip(CORTES, CORTES[1:]))] + [(cena6, 2.2)]
NOME = "ondas-calor"

if __name__ == "__main__":
    if sys.argv[2] == "teste":
        if sys.argv[3] == "capa":
            capa().convert("RGB").save(sys.argv[5])
            sys.exit()
        fns = {fn.__name__: (fn, d) for fn, d in CENAS}
        fn, d = fns[sys.argv[3]]
        fn(float(sys.argv[4]), d).convert("RGB").save(sys.argv[5])
        sys.exit()
    audio = sys.argv[2]
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
