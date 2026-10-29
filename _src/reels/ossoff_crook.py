#!/usr/bin/env python3
"""Reel no formato da China: Jon Ossoff chama Trump de "crook" a seis dias da eleição nos EUA (29/10/2026).

Voz original do discurso (vídeo do perfil de Ossoff no Threads, gravação de tela, reprodução), manchete em cima
e legenda em português acompanhando a fala. Transcrição feita com Whisper (small.en) e conferida trecho a trecho.
Uso: python3 _src/reels/ossoff_crook.py -> video/ossoff-crook.mp4 e .jpg
"""
import os, sys, subprocess, shutil
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
MOLDES = os.path.join(RAIZ, "identidade", "03-moldes-video")
sys.path.insert(0, MOLDES)
from agora import CSS, topo, assinatura, K, G  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

VIDEO = "/tmp/ossoff.mov"  # cópia de ScreenRecording_10-29-2026_11-18-47_1.mov
TMP = "/tmp/_reel_ossoff_crook"
T = "POLÍTICA · ELEIÇÕES NOS EUA"
CRED = "Vídeo: perfil de Jon Ossoff no Threads (reprodução)"
MANCHETE = 'A seis dias da eleição nos EUA, senador democrata chama Trump de <span style="color:#FF3B30">“vigarista”</span>'
QUEM = "Jon Ossoff, senador democrata da Geórgia"
PY = 560  # topo do painel de vídeo

# trechos do discurso: (início, fim no original, x do recorte de 640 px de largura)
TRECHOS = [(149.0, 161.3, 357), (12.2, 19.9, 54), (53.5, 60.5, 264), (72.3, 76.0, 264)]
# legendas no tempo do vídeo final: (início, fim, rótulo, texto). Abre com a frase mais forte.
LEG = [
    (0.2, 5.6, QUEM, "“Em seis dias, a Geórgia vai repreender o presidente <span style=\"color:#FF3B30\">vigarista</span> Donald Trump”"),
    (5.6, 12.3, QUEM, "“com tanta clareza e força que nenhum presidente vai ousar esses abusos de novo por séculos”"),
    (12.5, 20.0, QUEM, "“Vimos nosso governo virar uma ferramenta de vingança pessoal, de poder e de enriquecimento de um homem só”"),
    (20.2, 27.0, QUEM, "“A cada dia, Donald Trump cava mais fundo o buraco moral”"),
    (27.2, 30.7, "Citando Provérbios", "“Quem cava um buraco cai nele”"),
]
CTX_SRC = 96.5  # trecho do discurso que fica de fundo, baixo, na tela de contexto
DUR_CTX = 6.0
DUR_ASS = 2.0


def base_html():
    grad = (f'<div class="a" style="left:0;top:0;width:1080px;height:{PY + 120}px;background:linear-gradient(to bottom,rgba(20,20,20,.92) 0,rgba(20,20,20,.8) {PY}px,rgba(20,20,20,0) {PY + 120}px)"></div>'
            f'<div class="a" style="left:0;bottom:0;width:1080px;height:520px;background:linear-gradient(to top,rgba(20,20,20,.95) 0,rgba(20,20,20,.6) 260px,rgba(20,20,20,0) 520px)"></div>')
    cab = topo(T, CRED)
    cab = cab[cab.index("</div>") + 6:]
    man = f'<div class="a serif sh" style="left:80px;right:80px;top:330px;font-size:62px;line-height:1.12">{MANCHETE}</div>'
    return grad + cab + man


def legenda_html(quem, txt):
    return f'''<div class="a" style="left:50px;right:50px;top:1400px;background:rgba(20,20,20,.8);padding:26px 30px 30px;border-radius:6px">
<div class="sh" style="font-weight:800;font-size:28px;letter-spacing:.1em;color:#FF3B30;text-transform:uppercase">{quem}</div>
<div class="sh" style="font-size:54px;line-height:1.22;font-weight:700;margin-top:16px;color:#fff">{txt}</div></div>'''


def contexto_html():
    cab = topo(T, "Fontes: Atlanta News First e AJC/Universidade da Geórgia")
    cab = cab[cab.index("</div>") + 6:]
    return f'''<div class="a" style="inset:0;background:rgba(20,20,20,.72)"></div>{cab}<div class="a" style="left:80px;right:80px;top:560px">
<div style="font-weight:800;font-size:30px;letter-spacing:.12em;color:#FF3B30">O OUTRO LADO</div>
<div class="serif sh" style="font-size:76px;line-height:1.1;margin-top:20px">Ossoff disputa a vaga com Mike Collins, aliado de Trump</div>
<div class="sh" style="font-size:44px;line-height:1.3;color:#fff;margin-top:44px">No debate, Collins defendeu as políticas de Trump: disse que a fronteira está segura e culpou o Obamacare pela alta dos custos da saúde</div>
<div class="sh" style="font-size:40px;line-height:1.3;color:{G};margin-top:40px">Pesquisa da Universidade da Geórgia (7 a 15/10): Ossoff 48%, Collins 40%. A eleição é terça (3)</div></div>'''


def png(pg, html, caminho, fundo=False):
    bg = f"body{{background:{K}}}" if fundo else ""
    pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}{bg}</style></head><body>{html}</body></html>')
    pg.wait_for_timeout(250)
    pg.screenshot(path=caminho, omit_background=not fundo)


def run(c):
    subprocess.run(c, shell=True, check=True)


VID = "-r 30 -c:v libx264 -crf 18 -pix_fmt yuv420p"
AUD = "-c:a aac -b:a 192k -ar 48000 -ac 2"


def main():
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        png(pg, base_html(), f"{TMP}/base.png")
        for i, (_, _, q, t) in enumerate(LEG):
            png(pg, legenda_html(q, t), f"{TMP}/l{i}.png")
        png(pg, contexto_html(), f"{TMP}/ctx.png")
        png(pg, assinatura("Discurso de Jon Ossoff (perfil no Threads), AJC/Universidade da Geórgia e Atlanta News First"), f"{TMP}/ass.png", fundo=True)
        b.close()
    partes = []
    for i, (a, z, x) in enumerate(TRECHOS):
        out = f"{TMP}/t{i}.mp4"
        run(f'ffmpeg -v error -y -ss {a} -t {z - a:.2f} -i "{VIDEO}" -filter_complex '
            f'"[0:v]fps=30,crop=640:642:{x}:0,eq=contrast=1.04,split[a][b];'
            f'[a]scale=-2:1920,crop=1080:1920,boxblur=30:2,eq=brightness=-0.25[f];'
            f'[b]scale=1080:1083:flags=lanczos,setsar=1[p];[f][p]overlay=0:{PY},setsar=1[v];'
            f'[0:a]afade=in:st=0:d=0.08,afade=out:st={z - a - 0.12:.2f}:d=0.12[au]" '
            f'-map "[v]" -map "[au]" {VID} {AUD} {out}')
        partes.append(out)
    open(f"{TMP}/l.txt", "w").write("".join(f"file '{x}'\n" for x in partes))
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/l.txt -c copy {TMP}/base.mp4")
    tot = sum(z - a for a, z, _ in TRECHOS)
    ent = f"-i {TMP}/base.mp4 -loop 1 -framerate 30 -t {tot} -i {TMP}/base.png " + " ".join(
        f"-loop 1 -framerate 30 -t {tot} -i {TMP}/l{i}.png" for i in range(len(LEG)))
    fc = "[0:v][1:v]overlay=0:0[v0];"
    for i, (a, z, _, _) in enumerate(LEG):
        fc += (f"[{i + 2}:v]format=rgba,fade=in:st={a}:d=0.2:alpha=1[o{i}];"
               f"[v{i}][o{i}]overlay=0:0:enable='between(t,{a},{z})'[v{i + 1}];")
    fc += f"[v{len(LEG)}]format=yuv420p[vo]"
    run(f'ffmpeg -v error -y {ent} -filter_complex "{fc}" -map "[vo]" -map 0:a -af "loudnorm=I=-16:TP=-1.5" -t {tot:.2f} {VID} {AUD} {TMP}/corpo.mp4')
    # contexto: plateia desfocada com o discurso baixo de fundo, como ambiente, sumindo antes da assinatura
    run(f'ffmpeg -v error -y -ss {CTX_SRC} -t {DUR_CTX} -i "{VIDEO}" -loop 1 -framerate 30 -t {DUR_CTX} -i {TMP}/ctx.png -filter_complex '
        f'"[0:v]fps=30,scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.2,setsar=1[f];[f][1:v]overlay=0:0,fade=in:st=0:d=0.3,format=yuv420p[v];'
        f'[0:a]volume=0.13,afade=in:st=0:d=0.4,afade=out:st={DUR_CTX - 1.6}:d=1.6[au]" '
        f'-map "[v]" -map "[au]" -t {DUR_CTX} {VID} {AUD} {TMP}/ctx.mp4')
    run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {TMP}/ass.png -f lavfi -i anullsrc=r=48000:cl=stereo -t {DUR_ASS} '
        f'-vf "fade=in:st=0:d=0.2,format=yuv420p" {VID} {AUD} {TMP}/ass.mp4')
    open(f"{TMP}/l2.txt", "w").write("".join(f"file '{TMP}/{n}.mp4'\n" for n in ("corpo", "ctx", "ass")))
    saida = os.path.join(RAIZ, "video", "ossoff-crook.mp4")
    run(f'ffmpeg -v error -y -f concat -safe 0 -i {TMP}/l2.txt -c:v copy {AUD} -movflags +faststart {saida}')
    run(f"ffmpeg -v error -y -ss 2 -i {saida} -frames:v 1 -q:v 3 {os.path.join(RAIZ, 'video', 'ossoff-crook.jpg')}")
    print(f"ok: {saida} ({tot + DUR_CTX + DUR_ASS:.1f} s)")


if __name__ == "__main__":
    main()
