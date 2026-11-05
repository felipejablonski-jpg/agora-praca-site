#!/usr/bin/env python3
"""Reel: Santiago Peña renuncia à Presidência do Paraguai (5/11/2026), no formato do Reel da China.
Voz original (espanhol), manchete em cima, legenda traduzida nos trechos. O vídeo de origem é quadrado e pequeno
(290x294, das redes de Peña), então entra inteiro no meio da tela sobre fundo desfocado, sem recorte 9:16.
Uso: python3 _src/reels/pena_renuncia.py <video_origem> -> video/pena-renuncia.mp4 e .jpg
"""
import os, sys, subprocess, shutil
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import CSS, topo, tarja, assinatura  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

TMP = "/tmp/_reel_pena"
ORIGEM = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "clips", "pena-renuncia-2026-11-05.mov")
DUR_ASS = 2.0
T = tarja("politica", "Paraguai")
CREDITO = "Vídeo: redes sociais de Santiago Peña"
MANCHETE = 'Santiago Peña renuncia à Presidência do Paraguai em meio à crise do banco Ueno. <span style="color:#FF3B30">Ouça:</span>'
QUEM = "Santiago Peña, presidente do Paraguai"
# trechos do vídeo original (segundos)
TRECHOS = [(23.0, 36.3), (50.3, 59.9), (65.7, 73.6), (120.95, 127.9)]
# legendas com o tempo do vídeo original
LEG = [
    (23.15, 27.59, "Tomei a decisão de apresentar minha renúncia à Presidência da República."),
    (28.13, 32.61, "Faço isso pensando na estabilidade do nosso país, na paz social"),
    (32.65, 36.20, "e na necessidade de preservar nossas instituições democráticas."),
    (50.43, 55.23, "Também quero pedir desculpas ao povo se em algum momento eu falhei."),
    (55.69, 59.85, "Nunca foi minha intenção trair a confiança que depositaram em mim."),
    (65.79, 70.29, "Mas hoje minha prioridade é uma só: a tranquilidade dos paraguaios"),
    (70.35, 73.55, "que confiaram suas economias ao nosso sistema financeiro."),
    (121.07, 124.59, "Nenhum cargo é mais importante que a estabilidade da República."),
    (124.99, 127.85, "Nenhuma pessoa está acima do Paraguai."),
]


def rel(t):
    acc = 0.0
    for a, b in TRECHOS:
        if a <= t <= b + 0.01:
            return acc + (t - a)
        acc += b - a
    raise ValueError(t)


def base_html():
    grad = ('<div class="a" style="left:0;top:0;width:1080px;height:700px;background:linear-gradient(to bottom,rgba(20,20,20,.95) 0px,rgba(20,20,20,.85) 460px,rgba(20,20,20,0) 700px)"></div>')
    cab = topo(T, CREDITO, fundo="foto")
    cab = cab[cab.index("</div>") + 6:]
    man = f'<div class="a serif sh" style="left:80px;right:80px;top:330px;font-size:58px;line-height:1.1">{MANCHETE}</div>'
    return grad + cab + man


def legenda_html(txt):
    return f'''<div class="a" style="left:50px;right:50px;top:1430px;background:rgba(20,20,20,.8);padding:26px 30px 30px;border-radius:6px">
<div class="sh" style="font-weight:800;font-size:28px;letter-spacing:.1em;color:#FF3B30;text-transform:uppercase">{QUEM}</div>
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
        for i, (_, _, txt) in enumerate(LEG):
            png(pg, legenda_html(txt), f"{TMP}/l{i}.png")
        png(pg, assinatura("La Nación (Paraguai), Emol, BioBioChile e Excélsior. Vídeo: redes sociais de Santiago Peña"), f"{TMP}/ass.png")
        b.close()
    # 1) junta os trechos
    n = len(TRECHOS)
    fc = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];" for i, (a, b) in enumerate(TRECHOS))
    fc += "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"
    run(f'ffmpeg -v error -y -i "{ORIGEM}" -filter_complex "{fc}" -map "[v]" -map "[a]" -r 30 -c:v libx264 -crf 14 -c:a aac -b:a 192k {TMP}/trechos.mp4')
    dur = sum(b - a for a, b in TRECHOS)
    # 2) fundo desfocado + vídeo quadrado ampliado no meio + manchete + legendas
    entradas = f"-i {TMP}/trechos.mp4 -loop 1 -framerate 30 -i {TMP}/base.png " + " ".join(f"-loop 1 -framerate 30 -i {TMP}/l{i}.png" for i in range(len(LEG)))
    fc = ("[0:v]split[s1][s2];[s1]scale=1920:1920,crop=1080:1920,boxblur=40:3,eq=brightness=-0.22[fundo];"
          "[s2]scale=1080:1094:flags=lanczos,unsharp=5:5:0.7[vid];[fundo][vid]overlay=0:650[bg];[bg][1:v]overlay=0:0[w0];")
    for i, (a, z, _) in enumerate(LEG):
        fc += f"[w{i}][{i + 2}:v]overlay=0:0:enable='between(t,{rel(a):.2f},{rel(z):.2f})'[w{i + 1}];"
    fc += f"[w{len(LEG)}]format=yuv420p[vo]"
    run(f'ffmpeg -v error -y {entradas} -filter_complex "{fc}" -map "[vo]" -map 0:a -af loudnorm=I=-16:TP=-1.5 -t {dur:.2f} -r 30 -c:v libx264 -crf 20 -c:a aac -b:a 192k -ar 48000 -ac 2 {TMP}/corpo.mp4')
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {TMP}/ass.png -f lavfi -i anullsrc=r=48000:cl=stereo -t {DUR_ASS} -vf "fade=in:st=0:d=0.2,format=yuv420p" -r 30 -c:v libx264 -crf 18 -c:a aac -b:a 192k -shortest {TMP}/ass.mp4')
    open(f"{TMP}/lista.txt", "w").write(f"file '{TMP}/corpo.mp4'\nfile '{TMP}/ass.mp4'\n")
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "pena-renuncia.mp4")
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/lista.txt -c:v libx264 -crf 21 -r 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart {saida}")
    run(f"ffmpeg -v error -y -ss 0.3 -i {saida} -frames:v 1 -q:v 3 {os.path.join(pasta, 'pena-renuncia.jpg')}")
    print("ok:", saida, round(dur, 2))


if __name__ == "__main__":
    main()
