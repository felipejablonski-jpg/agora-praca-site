#!/usr/bin/env python3
"""Reel: o que está em jogo na eleição de 3/11 nos EUA, com o vídeo de campanha de Jon Ossoff (29/10/2026).

Vídeo do perfil de Jon Ossoff no Threads (gravação de tela, reprodução), sem som, em painel horizontal
sobre fundo desfocado, com o texto entrando por cima em camadas.
Uso: python3 _src/reels/midterms_ossoff.py -> video/midterms-ossoff.mp4 e .jpg
"""
import os, sys, json, subprocess, shutil
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
MOLDES = os.path.join(RAIZ, "identidade", "03-moldes-video")
sys.path.insert(0, MOLDES)
from agora import CSS, topo, assinatura, K, G  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

VIDEO = "/tmp/ossoff.mov"  # cópia de ScreenRecording_10-29-2026_11-18-47_1.mov
TMP = "/tmp/_reel_midterms"
T = "POLÍTICA · ELEIÇÕES NOS EUA"
V = '<span style="color:#FF3B30">{}</span>'
CRED = "Vídeo: perfil de Jon Ossoff no Threads (reprodução)"
# (início no vídeo original, duração)
TRECHOS = [(104.0, 7.0), (34.0, 7.0), (138.0, 7.0), (152.0, 7.0), (2.0, 6.0)]
PAINEL_Y = 650
DUR_ASS = 2.0


def cab():
    h = topo(T, CRED)
    return h[h.index("</div>") + 6:]


def bloco_topo(txt, fs=64):
    return f'<div class="a serif sh" style="left:80px;right:80px;top:330px;font-size:{fs}px;line-height:1.1">{txt}</div>'


def bloco_baixo(txt, rotulo="", sub="", fs=54):
    r = f'<div class="sh" style="font-weight:800;font-size:28px;letter-spacing:.12em;color:#FF3B30">{rotulo}</div>' if rotulo else ""
    s = f'<div class="sh" style="font-size:36px;line-height:1.3;color:{G};margin-top:18px">{sub}</div>' if sub else ""
    return (f'<div class="a" style="left:80px;right:80px;top:1290px">{r}'
            f'<div class="serif sh" style="font-size:{fs}px;line-height:1.14;margin-top:14px">{txt}</div>{s}</div>')


c = [0.0]
for _, d in TRECHOS:
    c.append(c[-1] + d)
TOT = c[-1]

CAMADAS = [
    (cab(), 0.0, TOT),
    (bloco_topo("Terça (3), os EUA elegem o Congresso. O controle das duas Casas está em jogo para " + V.format("Trump")), c[0], c[1]),
    (bloco_baixo("Toda a Câmara, 35 das 100 cadeiras do Senado e 36 governadores", "O QUE SE VOTA"), c[0] + 0.8, c[1]),
    (bloco_topo("No Senado, os republicanos têm 53 cadeiras. Os democratas precisam ganhar " + V.format("mais 4")), c[1], c[2]),
    (bloco_baixo("Com 50 a 50, o vice JD Vance desempata a favor dos republicanos", "A CONTA DO SENADO",
                 "Na Câmara, os republicanos têm 218 de 435, o mínimo para a maioria"), c[1] + 0.8, c[2]),
    (bloco_topo("Na Geórgia, o democrata Jon Ossoff tenta a reeleição contra o republicano Mike Collins, aliado de Trump", 58), c[2], c[3]),
    (bloco_baixo("Ossoff, 48%. Collins, 40%", "PESQUISA UGA PARA O AJC, 7 A 15/10",
                 "1.000 eleitores, margem de 3,1 pontos. Se ninguém passar de 50%, há segundo turno em 1º de dezembro", fs=72), c[2] + 0.8, c[3]),
    (bloco_topo("Ossoff chamou Trump de " + V.format("“crook”") + ", vigarista, e pediu à Geórgia que o “repreenda” nas urnas", 60), c[3], c[4]),
    (bloco_baixo("Collins chama Ossoff de “radical” e diz que ele “nunca teve um emprego na vida”", "NUM DEBATE NA TV, EM OUTUBRO",
                 "São ataques de campanha, dos dois lados"), c[3] + 0.8, c[4]),
    (bloco_topo("A apuração pode levar " + V.format("dias"), 70), c[4], c[5]),
    (bloco_baixo("As primeiras urnas fecham às 20h de Brasília (19h em MT) de terça (3)", "QUANDO SAI O RESULTADO",
                 "Voto pelo correio pode ser contado depois"), c[4] + 0.6, c[5]),
]


def png(pg, html, caminho, fundo=False):
    bg = f"body{{background:{K}}}" if fundo else ""
    pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}{bg}</style></head><body>{html}</body></html>')
    pg.wait_for_timeout(250)
    pg.screenshot(path=caminho, omit_background=not fundo)


def run(cmd):
    subprocess.run(cmd, shell=True, check=True)


VID = "-r 30 -c:v libx264 -crf 18 -pix_fmt yuv420p"


def main():
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    grad = (f'<div class="a" style="left:0;top:0;width:1080px;height:{PAINEL_Y}px;background:linear-gradient(to bottom,rgba(20,20,20,.85) 0,rgba(20,20,20,.6) {PAINEL_Y}px)"></div>'
            f'<div class="a" style="left:0;top:{PAINEL_Y + 594}px;width:1080px;bottom:0;background:rgba(20,20,20,.7)"></div>')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        png(pg, grad, f"{TMP}/grad.png")
        for i, (h, _, _) in enumerate(CAMADAS):
            png(pg, h, f"{TMP}/c{i}.png")
        png(pg, assinatura("Al Jazeera, AJC/Universidade da Geórgia, Atlanta News First, RTP e perfil de Jon Ossoff"), f"{TMP}/ass.png", fundo=True)
        b.close()
    partes = []
    for i, (ini, d) in enumerate(TRECHOS):
        out = f"{TMP}/v{i}.mp4"
        run(f'ffmpeg -v error -y -ss {ini} -t {d} -i "{VIDEO}" -an -filter_complex '
            f'"[0:v]fps=30,eq=contrast=1.04:saturation=0.95,split[a][b];'
            f'[a]scale=-2:1920,crop=1080:1920,boxblur=30:2,eq=brightness=-0.25[f];'
            f'[b]scale=1080:594:flags=lanczos,setsar=1[p];[f][p]overlay=0:{PAINEL_Y},setsar=1" {VID} {out}')
        partes.append(out)
    open(f"{TMP}/l.txt", "w").write("".join(f"file '{x}'\n" for x in partes))
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/l.txt -c copy {TMP}/base.mp4")
    ent = f"-i {TMP}/base.mp4 -loop 1 -framerate 30 -t {TOT} -i {TMP}/grad.png " + " ".join(
        f"-loop 1 -framerate 30 -t {TOT} -i {TMP}/c{i}.png" for i in range(len(CAMADAS)))
    fc = "[0:v][1:v]overlay=0:0[v0];"
    for i, (_, a, z) in enumerate(CAMADAS):
        fo = max(a, z - 0.3)
        fc += (f"[{i + 2}:v]format=rgba,fade=in:st={a}:d=0.4:alpha=1,fade=out:st={fo}:d=0.3:alpha=1[o{i}];"
               f"[v{i}][o{i}]overlay=0:0:enable='between(t,{a},{z})'[v{i + 1}];")
    fc += f"[v{len(CAMADAS)}]format=yuv420p[vo]"
    run(f'ffmpeg -v error -y {ent} -filter_complex "{fc}" -map "[vo]" -t {TOT} {VID} {TMP}/corpo.mp4')
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {TMP}/ass.png -t {DUR_ASS} -vf "fade=in:st=0:d=0.2,format=yuv420p" {VID} {TMP}/ass.mp4')
    open(f"{TMP}/l2.txt", "w").write(f"file '{TMP}/corpo.mp4'\nfile '{TMP}/ass.mp4'\n")
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/l2.txt -c copy {TMP}/mudo.mp4")
    total = TOT + DUR_ASS
    run(f"python3 {MOLDES}/trilha.py {TMP}/trilha.wav {total:.3f} '{json.dumps(c[1:])}'")
    saida = os.path.join(RAIZ, "video", "midterms-ossoff.mp4")
    run(f'ffmpeg -v error -y -i {TMP}/mudo.mp4 -i {TMP}/trilha.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af "volume=-3dB,loudnorm=I=-18:TP=-1.5" -t {total:.2f} -movflags +faststart {saida}')
    run(f"ffmpeg -v error -y -ss 3 -i {saida} -frames:v 1 -q:v 3 {os.path.join(RAIZ, 'video', 'midterms-ossoff.jpg')}")
    print(f"ok: {saida} ({total:.1f} s)")


if __name__ == "__main__":
    main()
