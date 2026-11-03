#!/usr/bin/env python3
"""Reel vertical em tela cheia: vice-presidente do Flamengo fala no STF sobre o fim das bets (3/11/2026).

Clipe: fala de Flávio Willeman na audiência pública do STF, recortada da transmissão da TV Justiça.
Mesmo formato do Reel da China (china_brasil_reel.py): voz original, manchete em cima, legenda nos trechos.
Uso: python3 _src/reels/flamengo_willeman_stf.py -> video/flamengo-stf-bets.mp4 e .jpg
"""
import os, sys, subprocess, shutil
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import CSS, topo, tarja, assinatura  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

TMP = "/tmp/_reel_flamengo_stf"
CLIPE = os.path.join(AQUI, "clips", "flamengo-willeman-stf-2026-11-03.mp4")
DUR_ASS = 2.0
DESCE = 560
T = tarja("politica", "bets")
CREDITO = "Vídeo: TV Justiça/STF (reprodução)"
MANCHETE = 'Com o fim das bets, o Flamengo diz que pode perder R$ 430 milhões por ano. <span style="color:#FF3B30">No STF, o clube falou assim:</span>'
QUEM = "Flávio Willeman, vice-presidente do Flamengo"
LEGENDAS = [
    (0.0, 7.76, QUEM, "O Flamengo contraiu obrigações financeiras com atletas e com empregados com base nesses contratos."),
    (7.76, 18.64, QUEM, "O Flamengo acreditou que o Brasil, após amplo debate no Congresso Nacional, regulou as apostas neste país"),
    (18.64, 23.53, QUEM, "e, portanto, confiou que essa atividade econômica teria perenidade"),
    (23.53, 33.55, QUEM, "que possibilitasse às instituições desportivas celebrar contratos e contrair obrigações"),
    (33.55, 37.11, QUEM, "com base nessa legislação."),
    (37.11, 44.41, QUEM, "O Flamengo possui mais de <span style=\"color:#FF3B30\">1.200 empregados</span> que poderão ser comprometidos"),
    (44.41, 54.02, QUEM, "com a queda de aproximadamente <span style=\"color:#FF3B30\">R$ 430 milhões</span> de receitas anuais com o futebol e com esportes olímpicos."),
    (54.02, 61.14, QUEM, "Senhor ministro, o Flamengo é o segundo maior fornecedor de atleta olímpico"),
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
        png(pg, assinatura("TV Justiça/STF, Metrópoles e Poder360"), f"{TMP}/ass.png")
        b.close()
    dur = float(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {CLIPE}", shell=True))
    # clipe 1080x608 (16:9): recorta 9:16 em volta do orador e amplia para 1080x1920
    vf = "crop=342:608:555:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,eq=contrast=1.04,setsar=1"
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
    saida = os.path.join(pasta, "flamengo-stf-bets.mp4")
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/lista.txt -c:v libx264 -crf 18 -r 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart {saida}")
    run(f"ffmpeg -v error -y -ss 0.3 -i {saida} -frames:v 1 -q:v 3 {os.path.join(pasta, 'flamengo-stf-bets.jpg')}")
    print("ok:", saida)


if __name__ == "__main__":
    main()
