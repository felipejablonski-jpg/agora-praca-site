#!/usr/bin/env python3
"""Reel vertical: Hugo Motta anuncia PEC do voto distrital misto para 2034 (28/10/2026).

Mesmo formato do Reel da China (manchete em cima, vídeo com a fala, legenda grande embaixo).
Fonte do vídeo: post da Câmara dos Deputados no Instagram (28/10), gravação de tela enviada pelo Felipe.
Usa dois trechos do vídeo: slide 2 (anúncio) e slide 3 (2034 e transição).
O recorte do vídeo para acima da legenda queimada da Câmara, para não duplicar com a nossa.
Uso: python3 _src/reels/distrital_motta.py  ->  video/distrital-motta.mp4 e .jpg
"""
import os, sys, subprocess, shutil
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import CSS, topo, tarja, assinatura  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

GRAV = "/mnt/user-data/uploads/ScreenRecording_10-28-2026_13-59-01_1.mp4"
CLIPE = os.path.join(RAIZ, "_src", "reels", "clips", "camara-motta-distrital-2026-10-28.mp4")
TMP = "/tmp/_reel_distrital_motta"
DUR_ASS = 2.0
# trechos da gravação de tela (segundos): já com o carrossel parado em cada slide
TRECHOS = [(2.10, 17.97), (73.30, 92.90)]
# área do vídeo da Câmara na gravação 1170x2532, acima da legenda queimada (que começa em y~1345)
CROP = "crop=1170:562:0:778"
Y_VIDEO, H_VIDEO = 640, 760

CREDITO = "Vídeo: Câmara dos Deputados, Instagram oficial (reprodução)"
T = tarja("politica", "reforma eleitoral")
MANCHETE = 'A Câmara quer mudar o jeito de eleger deputado e vereador. <span style="color:#FF3B30">Hugo Motta explica:</span>'
QUEM = "Hugo Motta, presidente da Câmara"
V = '<span style="color:#FF3B30">{}</span>'
LEGENDAS = [  # (início, fim, texto) no tempo do vídeo final
    (0.10, 4.80, "Nós caminharemos para fazer, ainda esse ano, uma discussão"),
    (4.80, 10.75, "e possível votação, na Câmara dos Deputados, sobre a mudança"),
    (10.75, 15.87, "do nosso sistema eleitoral, caminhando para o sistema " + V.format("distrital misto.")),
    (15.97, 20.77, "A ideia, aqui tratada e decidida na manhã de hoje,"),
    (20.77, 25.57, "ela vai no seguinte sentido: de podermos buscar a efetivação"),
    (25.57, 31.17, "desse sistema eleitoral no voto distrital misto para o ano de " + V.format("2034")),
    (31.17, 35.47, "e, até lá, construirmos uma " + V.format("transição") + " para esse modelo."),
]


def base_html():
    grad = (f'<div class="a" style="left:0;top:0;width:1080px;height:{Y_VIDEO + 40}px;background:linear-gradient(to bottom,rgba(20,20,20,.92) 0px,rgba(20,20,20,.8) {Y_VIDEO - 60}px,rgba(20,20,20,0) {Y_VIDEO + 40}px)"></div>'
            f'<div class="a" style="left:0;bottom:0;width:1080px;height:{1920 - Y_VIDEO - H_VIDEO + 40}px;background:linear-gradient(to top,rgba(20,20,20,.92) 0px,rgba(20,20,20,.8) 400px,rgba(20,20,20,0) {1920 - Y_VIDEO - H_VIDEO + 40}px)"></div>')
    cab = topo(T, CREDITO, fundo="foto")
    cab = cab[cab.index("</div>") + 6:]
    man = f'<div class="a serif sh" style="left:80px;right:80px;top:336px;font-size:58px;line-height:1.12">{MANCHETE}</div>'
    return grad + cab + man


def legenda_html(txt):
    return f'''<div class="a" style="left:50px;right:50px;top:{Y_VIDEO + H_VIDEO + 36}px;background:rgba(20,20,20,.82);padding:26px 30px 30px;border-radius:6px">
<div class="sh" style="font-weight:800;font-size:28px;letter-spacing:.1em;color:#FF3B30;text-transform:uppercase">{QUEM}</div>
<div class="sh" style="font-size:52px;line-height:1.22;font-weight:700;margin-top:16px;color:#fff">{txt}</div></div>'''


def png(pg, html, caminho):
    pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
    pg.wait_for_timeout(250)
    pg.screenshot(path=caminho, omit_background=True)


def run(c):
    subprocess.run(c, shell=True, check=True)


def clipe():
    """Corta os dois trechos da gravação, recorta a área do vídeo e junta (com 0,1 s de fade no áudio)."""
    if os.path.exists(CLIPE):
        return
    os.makedirs(os.path.dirname(CLIPE), exist_ok=True)
    partes = []
    for i, (a, z) in enumerate(TRECHOS):
        d = z - a
        p = f"{TMP}/t{i}.mp4"
        run(f'ffmpeg -v error -y -ss {a} -i {GRAV} -t {d:.2f} -vf "{CROP},setsar=1,fps=30" '
            f'-af "afade=in:d=0.08,afade=out:st={d - 0.1:.2f}:d=0.1" -c:v libx264 -crf 14 -c:a aac -b:a 192k -ar 48000 -ac 2 {p}')
        partes.append(p)
    open(f"{TMP}/tl.txt", "w").write("".join(f"file '{p}'\n" for p in partes))
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/tl.txt -c copy {CLIPE}")


def main():
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    clipe()
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        png(pg, base_html(), f"{TMP}/base.png")
        for i, (_, _, txt) in enumerate(LEGENDAS):
            png(pg, legenda_html(txt), f"{TMP}/l{i}.png")
        png(pg, assinatura("Câmara dos Deputados, Congresso em Foco, SBT News e Metrópoles"), f"{TMP}/ass.png")
        b.close()
    dur = float(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {CLIPE}", shell=True))
    # vídeo 1170x562: amplia para altura 760 e corta o centro em 1080
    vf = f"scale=-2:{H_VIDEO}:flags=lanczos,crop=1080:{H_VIDEO},eq=contrast=1.03,setsar=1"
    entradas = f"-i {CLIPE} -loop 1 -framerate 30 -i {TMP}/base.png " + " ".join(f"-loop 1 -framerate 30 -i {TMP}/l{i}.png" for i in range(len(LEGENDAS)))
    fc = (f"[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=30:2,eq=brightness=-0.2[fundo];"
          f"[b]{vf}[vid];[fundo][vid]overlay=0:{Y_VIDEO}:shortest=1[bg];[bg][1:v]overlay=0:0[v0];")
    for i, (a, z, _) in enumerate(LEGENDAS):
        fc += f"[v{i}][{i + 2}:v]overlay=0:0:enable='between(t,{a},{z})'[v{i + 1}];"
    fc += f"[v{len(LEGENDAS)}]format=yuv420p[vo]"
    run(f'ffmpeg -v error -y {entradas} -filter_complex "{fc}" -map "[vo]" -map 0:a -t {dur:.2f} -r 30 -c:v libx264 -crf 18 -c:a aac -b:a 192k -ar 48000 -ac 2 {TMP}/corpo.mp4')
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {TMP}/ass.png -f lavfi -i anullsrc=r=48000:cl=stereo -t {DUR_ASS} -vf "fade=in:st=0:d=0.2,format=yuv420p" -r 30 -c:v libx264 -crf 18 -c:a aac -b:a 192k -shortest {TMP}/ass.mp4')
    open(f"{TMP}/lista.txt", "w").write(f"file '{TMP}/corpo.mp4'\nfile '{TMP}/ass.mp4'\n")
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "distrital-motta.mp4")
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/lista.txt -c:v libx264 -crf 18 -r 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart {saida}")
    run(f"ffmpeg -v error -y -ss 26 -i {saida} -frames:v 1 -q:v 3 {os.path.join(pasta, 'distrital-motta.jpg')}")
    print("ok:", saida)


if __name__ == "__main__":
    main()
