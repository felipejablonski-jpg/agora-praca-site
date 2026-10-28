#!/usr/bin/env python3
"""Reel: Trump sobre Flávio se dizer presidente, "não vou me envolver" (28/10/2026).

Vídeo em tela cheia o tempo todo, sem som (só a trilha), com o texto entrando por cima
em camadas, sem cortar para tela chapada. Imagens de arquivo (gravação de tela do YouTube).
Uso: python3 _src/reels/trump_flavio.py  ->  video/trump-flavio.mp4 e .jpg
"""
import os, sys, json, subprocess, shutil
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
MOLDES = os.path.join(RAIZ, "identidade", "03-moldes-video")
sys.path.insert(0, MOLDES)
from agora import CSS, topo, tarja, assinatura, K, G  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

A = "/mnt/user-data/attachments/31be2719-c7d8-5b33-91a5-c035937f37a4"
TRUMP = f"{A}/383f6751-ScreenRecording_10-28-2026_18-30-24_1.mov"
FLAVIO = f"{A}/f56fa19c-ScreenRecording_10-28-2026_18-31-42_1.mov"
TMP = "/tmp/_reel_trump_flavio"
T = tarja("politica", "eleições 2026")
V = '<span style="color:#FF3B30">{}</span>'
# (arquivo, início, duração, recorte vertical 9:16 na imagem já girada, crédito)
TRECHOS = [
    (TRUMP, 1.0, 13.0, "crop=658:1170:842:0", "Imagens de arquivo: USA Today, no YouTube (reprodução)"),
    (FLAVIO, 2.0, 15.0, "crop=518:922:1072:19", "Imagens de arquivo: canal de Flávio Bolsonaro no YouTube (reprodução)"),
]
DUR_ASS = 2.0
DESCE = 420  # desce o vídeo para o rosto ficar entre a manchete e o texto de baixo


def cab(cred):
    h = topo(T, cred)
    return h[h.index("</div>") + 6:]  # tira o degradê da faixa de foto, que escurece a tela cheia


def bloco_topo(txt, fs=66):
    return f'<div class="a serif sh" style="left:80px;right:80px;top:330px;font-size:{fs}px;line-height:1.1">{txt}</div>'


def bloco_baixo(txt, rotulo="", sub="", fs=54):
    r = f'<div class="sh" style="font-weight:800;font-size:28px;letter-spacing:.12em;color:#FF3B30">{rotulo}</div>' if rotulo else ""
    s = f'<div class="sh" style="font-size:36px;line-height:1.3;color:{G};margin-top:18px">{sub}</div>' if sub else ""
    return (f'<div class="a" style="left:80px;right:80px;top:1270px">{r}'
            f'<div class="serif sh" style="font-size:{fs}px;line-height:1.14;margin-top:14px">{txt}</div>{s}</div>')


# camadas: (html, início, fim) no tempo do vídeo final
CAMADAS = [
    (cab(TRECHOS[0][4]), 0.0, 13.0),
    (bloco_topo("Perguntado sobre Flávio se dizer presidente, Trump respondeu: " + V.format("“não vou me envolver”")), 0.0, 13.0),
    (bloco_baixo("“Mas sei que demos a ele autorização para entrar no país; veremos o que acontece”", "DONALD TRUMP, NESTA QUARTA (28)"), 3.0, 8.0),
    (bloco_baixo("“Foi uma eleição muito estranha, isso é certo”", "DONALD TRUMP", "Ele não apresentou nenhuma prova de fraude"), 8.0, 13.0),
    (cab(TRECHOS[1][4]), 13.0, 28.0),
    (bloco_topo("Na carta, Flávio se declarou " + V.format("“o verdadeiro presidente eleito do Brasil”")), 13.0, 28.0),
    (bloco_baixo("Horas depois, trocou por " + V.format("“líder do Brasil”") + ". A acusação de fraude, sem prova, continuou", "A SEGUNDA VERSÃO"), 14.5, 20.5),
    (bloco_baixo("Lula foi declarado reeleito pelo TSE, com 51,79% dos votos válidos, e toma posse em 5 de janeiro", "O RESULTADO"), 20.5, 28.0),
]


def png(pg, html, caminho, fundo=False):
    bg = f"body{{background:{K}}}" if fundo else ""
    pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}{bg}</style></head><body>{html}</body></html>')
    pg.wait_for_timeout(250)
    pg.screenshot(path=caminho, omit_background=not fundo)


def run(c):
    subprocess.run(c, shell=True, check=True)


VID = "-r 30 -c:v libx264 -crf 18 -pix_fmt yuv420p"


def main():
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    grad = ('<div class="a" style="left:0;top:0;width:1080px;height:720px;background:linear-gradient(to bottom,rgba(20,20,20,.9) 0,rgba(20,20,20,.75) 470px,rgba(20,20,20,0) 720px)"></div>'
            '<div class="a" style="left:0;bottom:0;width:1080px;height:820px;background:linear-gradient(to top,rgba(20,20,20,.95) 0,rgba(20,20,20,.8) 560px,rgba(20,20,20,0) 820px)"></div>')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        png(pg, grad, f"{TMP}/grad.png")
        for i, (h, _, _) in enumerate(CAMADAS):
            png(pg, h, f"{TMP}/c{i}.png")
        png(pg, assinatura("Donald Trump a jornalistas, CNN Brasil, Metrópoles e TSE"), f"{TMP}/ass.png", fundo=True)
        b.close()
    partes = []
    for i, (arq, ini, d, crop, _) in enumerate(TRECHOS):
        out = f"{TMP}/v{i}.mp4"
        run(f'ffmpeg -v error -y -ss {ini} -t {d} -i "{arq}" -an -filter_complex "[0:v]fps=30,{crop},scale=1080:1920:flags=lanczos,eq=contrast=1.05:saturation=0.95,setsar=1,split[a][b];[a]boxblur=30:2,eq=brightness=-0.22[f];[f][b]overlay=0:{DESCE}" {VID} {out}')
        partes.append(out)
    open(f"{TMP}/l.txt", "w").write("".join(f"file '{x}'\n" for x in partes))
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/l.txt -c copy {TMP}/base.mp4")
    total_v = sum(t[2] for t in TRECHOS)
    ent = f"-i {TMP}/base.mp4 -loop 1 -framerate 30 -t {total_v} -i {TMP}/grad.png " + " ".join(
        f"-loop 1 -framerate 30 -t {total_v} -i {TMP}/c{i}.png" for i in range(len(CAMADAS)))
    fc = "[0:v][1:v]overlay=0:0[v0];"
    for i, (_, a, z) in enumerate(CAMADAS):
        fo = max(a, z - 0.3)
        fc += (f"[{i + 2}:v]format=rgba,fade=in:st={a}:d=0.4:alpha=1,fade=out:st={fo}:d=0.3:alpha=1[o{i}];"
               f"[v{i}][o{i}]overlay=0:0:enable='between(t,{a},{z})'[v{i + 1}];")
    fc += f"[v{len(CAMADAS)}]format=yuv420p[vo]"
    run(f'ffmpeg -v error -y {ent} -filter_complex "{fc}" -map "[vo]" -t {total_v} {VID} {TMP}/corpo.mp4')
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {TMP}/ass.png -t {DUR_ASS} -vf "fade=in:st=0:d=0.2,format=yuv420p" {VID} {TMP}/ass.mp4')
    open(f"{TMP}/l2.txt", "w").write(f"file '{TMP}/corpo.mp4'\nfile '{TMP}/ass.mp4'\n")
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/l2.txt -c copy {TMP}/mudo.mp4")
    total = total_v + DUR_ASS
    cortes = [3.0, 8.0, 13.0, 14.5, 20.5, total_v]
    run(f"python3 {MOLDES}/trilha.py {TMP}/trilha.wav {total:.3f} '{json.dumps(cortes)}'")
    saida = os.path.join(RAIZ, "video", "trump-flavio.mp4")
    run(f'ffmpeg -v error -y -i {TMP}/mudo.mp4 -i {TMP}/trilha.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af "volume=-3dB,loudnorm=I=-18:TP=-1.5" -t {total:.2f} -movflags +faststart {saida}')
    run(f"ffmpeg -v error -y -ss 4 -i {saida} -frames:v 1 -q:v 3 {os.path.join(RAIZ, 'video', 'trump-flavio.jpg')}")
    print(f"ok: {saida} ({total:.1f} s)")


if __name__ == "__main__":
    main()
