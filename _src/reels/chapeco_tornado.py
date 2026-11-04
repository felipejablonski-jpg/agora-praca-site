#!/usr/bin/env python3
"""Reel: tornado em Chapecó (SC) danifica o aeroporto (4/11/2026). Vídeo de drone do @dechapeco (reprodução).
Manchete em faixa escura no topo (cobre a marca d'água do perfil de origem, creditado na tela e na legenda) e textos em camadas por cima do vídeo.
Uso: python3 _src/reels/chapeco_tornado.py -> video/chapeco-tornado.mp4 e .jpg
"""
import os, sys, subprocess, shutil
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import CSS, topo, tarja, assinatura  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

TMP = "/tmp/_reel_chapeco_tornado"
CLIPE = os.path.join(AQUI, "clips", "chapeco-tornado-drone-2026-11-04.mp4")
DUR_ASS = 2.0
T = tarja("ciencia", "clima")
CREDITO = "Vídeo: @dechapeco (reprodução)"
MANCHETE = 'Tornado com ventos de até <span style="color:#FF3B30">126 km/h</span> atinge Chapecó (SC) e destrói parte do aeroporto'
R = "#FF3B30"
CAMADAS = [
    (1.5, 13.0, "VENTO", f'Rajada de <span style="color:{R}">126 km/h</span> registrada por uma estação do Inmet. A Defesa Civil confirmou o tornado.'),
    (13.0, 25.0, "AEROPORTO", f'Hangares e saguão destelhados. O aeroporto fica <span style="color:{R}">fechado até sexta (6)</span>, segundo o prefeito.'),
    (25.0, 37.0, "A CIDADE", f'Quase <span style="color:{R}">2,5 mil ocorrências</span>: casas destelhadas, árvores caídas e falta de luz.'),
    (37.0, 46.0, "EMERGÊNCIA", f'Chapecó decretou <span style="color:{R}">situação de emergência</span> por 180 dias.'),
    (46.0, 53.3, "NA REGIÃO", f'Xanxerê também teve tornado, com <span style="color:{R}">mais de 200 casas</span> atingidas.'),
]


def base_html():
    faixa = ('<div class="a" style="left:0;top:0;width:1080px;height:760px;background:linear-gradient(to bottom,rgba(20,20,20,.97) 0px,rgba(20,20,20,.95) 520px,rgba(20,20,20,0) 760px)"></div>'
             '<div class="a" style="left:0;bottom:0;width:1080px;height:700px;background:linear-gradient(to top,rgba(20,20,20,.85) 0px,rgba(20,20,20,.45) 380px,rgba(20,20,20,0) 700px)"></div>')
    cab = topo(T, CREDITO, fundo="foto")
    cab = cab[cab.index("</div>") + 6:]
    man = f'<div class="a serif sh" style="left:80px;right:80px;top:340px;font-size:66px;line-height:1.1">{MANCHETE}</div>'
    return faixa + cab + man


def camada_html(rot, txt):
    return f'''<div class="a" style="left:50px;right:50px;top:1380px;background:rgba(20,20,20,.8);padding:26px 30px 30px;border-radius:6px">
<div class="sh" style="font-weight:800;font-size:28px;letter-spacing:.14em;color:#FF3B30">{rot}</div>
<div class="sh" style="font-size:54px;line-height:1.2;font-weight:700;margin-top:14px;color:#fff">{txt}</div></div>'''


def png(pg, html, caminho):
    pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
    pg.wait_for_timeout(250)
    pg.screenshot(path=caminho, omit_background=True)


def run(c):
    subprocess.run(c, shell=True, check=True)


def main():
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        png(pg, base_html(), f"{TMP}/base.png")
        for i, (_, _, rot, txt) in enumerate(CAMADAS):
            png(pg, camada_html(rot, txt), f"{TMP}/c{i}.png")
        png(pg, assinatura("Defesa Civil de SC, Prefeitura de Chapecó, Inmet, CNN Brasil e ND Mais. Vídeo: @dechapeco"), f"{TMP}/ass.png")
        b.close()
    dur = float(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {CLIPE}", shell=True))
    entradas = f"-i {CLIPE} -loop 1 -framerate 30 -i {TMP}/base.png " + " ".join(f"-loop 1 -framerate 30 -i {TMP}/c{i}.png" for i in range(len(CAMADAS)))
    fc = "[0:v]eq=contrast=1.03:saturation=0.95[bg];[bg][1:v]overlay=0:0[v0];"
    for i, (a, z, _, _) in enumerate(CAMADAS):
        fc += f"[{i + 2}:v]format=rgba,fade=in:st={a}:d=0.25:alpha=1[f{i}];[v{i}][f{i}]overlay=0:0:enable='between(t,{a},{z})'[v{i + 1}];"
    fc += f"[v{len(CAMADAS)}]format=yuv420p[vo]"
    run(f'ffmpeg -v error -y {entradas} -filter_complex "{fc}" -map "[vo]" -map 0:a -t {dur:.2f} -r 30 -c:v libx264 -crf 19 -c:a aac -b:a 192k -ar 48000 -ac 2 {TMP}/corpo.mp4')
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {TMP}/ass.png -f lavfi -i anullsrc=r=48000:cl=stereo -t {DUR_ASS} -vf "fade=in:st=0:d=0.2,format=yuv420p" -r 30 -c:v libx264 -crf 18 -c:a aac -b:a 192k -shortest {TMP}/ass.mp4')
    open(f"{TMP}/lista.txt", "w").write(f"file '{TMP}/corpo.mp4'\nfile '{TMP}/ass.mp4'\n")
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "chapeco-tornado.mp4")
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/lista.txt -c:v libx264 -crf 21 -r 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart {saida}")
    run(f"ffmpeg -v error -y -ss 0.3 -i {saida} -frames:v 1 -q:v 3 {os.path.join(pasta, 'chapeco-tornado.jpg')}")
    print("ok:", saida)


if __name__ == "__main__":
    main()
