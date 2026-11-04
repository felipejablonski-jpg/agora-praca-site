#!/usr/bin/env python3
"""Reel vertical em tela cheia: Trump fala do salão de baile da Casa Branca um dia depois das midterms (4/11/2026).

Clipe: fala de Flávio Willeman na audiência pública do STF, recortada da transmissão da TV Justiça.
Mesmo formato do Reel da China (china_brasil_reel.py): voz original, manchete em cima, legenda nos trechos.
Uso: python3 _src/reels/flamengo_willeman_stf.py -> video/trump-salao-casa-branca.mp4 e .jpg
"""
import os, sys, subprocess, shutil
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import CSS, topo, tarja, assinatura  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

TMP = "/tmp/_reel_trump_salao"
CLIPE = os.path.join(AQUI, "clips", "trump-salao-casa-branca-2026-11-04.mp4")
DUR_ASS = 2.0
DESCE = 560
T = tarja("politica", "EUA")
CREDITO = "Vídeo: Casa Branca, via transmissão da Fox News (reprodução)"
MANCHETE = 'Um dia depois de os democratas vencerem no Congresso, Trump falou do salão de baile da Casa Branca. <span style="color:#FF3B30">Ouça:</span>'
QUEM = "Donald Trump, presidente dos EUA"
LEGENDAS = [
    (0.17, 2.93, QUEM, "E o teto tem mais de 15 metros de altura."),
    (2.97, 7.10, QUEM, "É como um prédio de cinco andares. Não acho que exista outro salão de baile..."),
    (7.23, 10.83, QUEM, "Duvido que exista um salão de baile no país com teto de 15 metros."),
    (10.83, 14.07, QUEM, "E vai dar para fazer jantares para quantas pessoas vocês quiserem."),
    (14.07, 18.25, QUEM, "O rei Charles esteve aqui, e nós ficamos muito limitados."),
    (18.28, 22.90, QUEM, "Nós perguntamos: \"Podemos ter umas 350 pessoas nossas?\""),
    (23.30, 26.80, QUEM, "Disseram: \"Não cabem 350. Cabem umas 98.\""),
    (27.28, 29.90, QUEM, "Então ter 350 é um pouco difícil."),
    (29.99, 32.90, QUEM, "Mas recebemos o presidente Xi, da China..."),
]


def base_html():
    grad = (f'<div class="a" style="left:0;top:0;width:1080px;height:820px;background:linear-gradient(to bottom,rgba(20,20,20,.9) 0px,rgba(20,20,20,.72) 480px,rgba(20,20,20,0) 820px)"></div>'
            f'<div class="a" style="left:0;bottom:0;width:1080px;height:760px;background:linear-gradient(to top,rgba(20,20,20,.92) 0px,rgba(20,20,20,.6) 420px,rgba(20,20,20,0) 760px)"></div>')
    cab = topo(T, CREDITO, fundo="foto")
    cab = cab[cab.index("</div>") + 6:]
    man = f'<div class="a serif sh" style="left:80px;right:80px;top:340px;font-size:62px;line-height:1.12">{MANCHETE}</div>'
    return grad + cab + man


def legenda_html(quem, txt):
    return f'''<div class="a" style="left:50px;right:50px;top:1400px;background:rgba(20,20,20,.78);padding:26px 30px 30px;border-radius:6px">
<div class="sh" style="font-weight:800;font-size:28px;letter-spacing:.1em;color:#FF3B30;text-transform:uppercase">{quem}</div>
<div class="sh" style="font-size:54px;line-height:1.22;font-weight:700;margin-top:16px;color:#fff">{txt}</div></div>'''


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
        for i, (_, _, quem, txt) in enumerate(LEGENDAS):
            png(pg, legenda_html(quem, txt), f"{TMP}/l{i}.png")
        png(pg, assinatura("Casa Branca, Fox News, TV Brasil e Associated Press"), f"{TMP}/ass.png")
        b.close()
    dur = float(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {CLIPE}", shell=True))
    # clipe 1080x608 (16:9): recorta 9:16 em volta do orador e amplia para 1080x1920
    vf = "crop=362:644:389:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,eq=contrast=1.04,setsar=1"
    entradas = f"-i {CLIPE} -loop 1 -framerate 30 -i {TMP}/base.png " + " ".join(f"-loop 1 -framerate 30 -i {TMP}/l{i}.png" for i in range(len(LEGENDAS)))
    fc = (f"[0:v]{vf},split[a][b];[a]boxblur=30:2,eq=brightness=-0.18[fundo];"
          f"[fundo][b]overlay=0:{DESCE}:shortest=1[bg];[bg][1:v]overlay=0:0[v0];")
    for i, (a, z, _, _) in enumerate(LEGENDAS):
        fc += f"[v{i}][{i + 2}:v]overlay=0:0:enable='between(t,{a},{z})'[v{i + 1}];"
    fc += f"[v{len(LEGENDAS)}]format=yuv420p[vo]"
    run(f'ffmpeg -v error -y {entradas} -filter_complex "{fc}" -map "[vo]" -map 0:a -t {dur:.2f} -r 30 -c:v libx264 -crf 18 -c:a aac -b:a 192k -ar 48000 -ac 2 {TMP}/corpo.mp4')
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {TMP}/ass.png -f lavfi -i anullsrc=r=48000:cl=stereo -t {DUR_ASS} -vf "fade=in:st=0:d=0.2,format=yuv420p" -r 30 -c:v libx264 -crf 18 -c:a aac -b:a 192k -shortest {TMP}/ass.mp4')
    open(f"{TMP}/lista.txt", "w").write(f"file '{TMP}/corpo.mp4'\nfile '{TMP}/ass.mp4'\n")
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "trump-salao-casa-branca.mp4")
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/lista.txt -c:v libx264 -crf 18 -r 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart {saida}")
    run(f"ffmpeg -v error -y -ss 0.3 -i {saida} -frames:v 1 -q:v 3 {os.path.join(pasta, 'trump-salao-casa-branca.jpg')}")
    print("ok:", saida)


if __name__ == "__main__":
    main()
