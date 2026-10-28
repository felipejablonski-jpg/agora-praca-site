#!/usr/bin/env python3
"""Reel no formato print de perfil: China responde à fala de Trump sobre fraude na eleição do Brasil (27/10/2026).

Vídeo completo da coletiva do porta-voz Guo Jiakun, legendado em português a partir da
transcrição oficial do Ministério das Relações Exteriores da China.
Uso: python3 _src/reels/china_brasil.py  ->  video/china-brasil.mp4 e video/china-brasil.jpg
"""
import os, sys, subprocess, shutil
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import CSS, SELO, assinatura  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

CLIPE = os.path.join(RAIZ, "_src", "reels", "clips", "china-guo-jiakun-brasil-2026-10-27.mp4")
TMP = "/tmp/_reel_china_brasil"
Y_VIDEO = 760          # topo do vídeo
H_VIDEO = 608
DUR_ASS = 2.0

CARTAO = ("Trump disse que a eleição do Brasil pareceu fraudada. "
          "A China foi perguntada sobre isso nesta terça e respondeu com uma frase só.")
FONTES = "Fontes: Chancelaria da China e Bloomberg Línea · agorapraca.com.br"
CREDITO = "Vídeo: Ministério das Relações Exteriores da China, via ShanghaiEye (reprodução)"

# (início, fim, quem fala, texto). Tradução da transcrição oficial do Ministério.
LEGENDAS = [
    (2.2, 7.0, "Repórter da AFP", "O presidente dos EUA, Donald Trump, afirmou na segunda-feira"),
    (7.0, 12.3, "Repórter da AFP", "que a eleição do Brasil foi fraudada, depois da vitória do presidente Lula."),
    (12.6, 16.0, "Repórter da AFP", "O Ministério das Relações Exteriores"),
    (16.0, 21.2, "Repórter da AFP", "tem algum comentário sobre o que Trump disse?"),
    (23.6, 27.0, "Guo Jiakun, porta-voz da chancelaria chinesa", "Respeitamos a escolha independente do povo brasileiro."),
]

BASE = f'''<div class="a" style="inset:0;background:#000"></div>
<div class="a" style="left:0;right:0;top:250px;background:#fff;color:#0f1419;padding:44px 56px 40px">
<div style="display:flex;align-items:center;gap:22px"><div style="width:96px;height:96px;border-radius:50%;overflow:hidden">{SELO.format(w=96)}</div>
<div><div style="font-weight:800;font-size:38px">Agora Praça</div><div style="font-size:31px;color:#536471;margin-top:2px">@agorapraca</div></div></div>
<div style="font-size:45px;line-height:1.3;margin-top:28px">{CARTAO}</div>
<div style="font-size:26px;color:#536471;margin-top:22px">{FONTES}</div></div>
<div class="a" style="left:40px;right:40px;top:{Y_VIDEO + H_VIDEO + 16}px;font-size:22px;color:#8d8983">{CREDITO}</div>'''


def legenda_html(quem, txt):
    return f'''<div class="a" style="left:70px;right:70px;top:{Y_VIDEO + H_VIDEO + 110}px">
<div style="font-weight:800;font-size:26px;letter-spacing:.1em;color:#FF3B30;text-transform:uppercase">{quem}</div>
<div style="font-size:52px;line-height:1.25;font-weight:600;margin-top:16px;color:#fff">{txt}</div></div>'''


def png(pg, html, caminho, transparente):
    pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
    pg.wait_for_timeout(250)
    pg.screenshot(path=caminho, omit_background=transparente)


def run(c):
    subprocess.run(c, shell=True, check=True)


def main():
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        png(pg, BASE, f"{TMP}/base.png", False)
        for i, (_, _, quem, txt) in enumerate(LEGENDAS):
            png(pg, legenda_html(quem, txt), f"{TMP}/l{i}.png", True)
        png(pg, assinatura("Ministério das Relações Exteriores da China e Bloomberg Línea"), f"{TMP}/ass.png", False)
        b.close()
    dur = float(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {CLIPE}", shell=True))
    entradas = f"-loop 1 -framerate 30 -i {TMP}/base.png -i {CLIPE} " + " ".join(f"-loop 1 -framerate 30 -i {TMP}/l{i}.png" for i in range(len(LEGENDAS)))
    fc = f"[0:v][1:v]overlay=0:{Y_VIDEO}[v0];"
    for i, (a, z, _, _) in enumerate(LEGENDAS):
        fc += f"[v{i}][{i + 2}:v]overlay=0:0:enable='between(t,{a},{z})'[v{i + 1}];"
    fc += f"[v{len(LEGENDAS)}]format=yuv420p[vo]"
    run(f'ffmpeg -v error -y {entradas} -filter_complex "{fc}" -map "[vo]" -map 1:a -t {dur:.2f} -r 30 -c:v libx264 -crf 18 -c:a aac -b:a 192k -ar 48000 -ac 2 {TMP}/corpo.mp4')
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {TMP}/ass.png -f lavfi -i anullsrc=r=48000:cl=stereo -t {DUR_ASS} -vf "fade=in:st=0:d=0.2,format=yuv420p" -r 30 -c:v libx264 -crf 18 -c:a aac -b:a 192k -shortest {TMP}/ass.mp4')
    open(f"{TMP}/lista.txt", "w").write(f"file '{TMP}/corpo.mp4'\nfile '{TMP}/ass.mp4'\n")
    saida = os.path.join(RAIZ, "video", "china-brasil.mp4")
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/lista.txt -c:v libx264 -crf 18 -r 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart {saida}")
    run(f"ffmpeg -v error -y -ss 0.3 -i {saida} -frames:v 1 -q:v 3 {os.path.join(RAIZ, 'video', 'china-brasil.jpg')}")
    print("ok:", saida)


if __name__ == "__main__":
    main()
