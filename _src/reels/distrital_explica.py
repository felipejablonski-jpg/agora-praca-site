#!/usr/bin/env python3
"""Reel "Agora explica": a fala de Hugo Motta sobre o voto distrital misto, intercalada com explicações (28/10/2026).

Estrutura: trecho da fala, tela que explica, outro trecho, tela que explica, o que falta, assinatura.
Fala: vídeo da Câmara dos Deputados no Instagram (gravação de tela), o mesmo de distrital_motta.py.
Telas explicativas com a trilha da casa; sob a fala, a trilha fica baixa.
Uso: python3 _src/reels/distrital_explica.py  ->  video/distrital-explica.mp4 e .jpg
"""
import os, sys, json, subprocess, shutil
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
MOLDES = os.path.join(RAIZ, "identidade", "03-moldes-video")
sys.path.insert(0, MOLDES)
from agora import CSS, topo, tarja, assinatura, R, RD, K, G  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

GRAV = "/mnt/user-data/uploads/ScreenRecording_10-28-2026_13-59-01_1.mp4"
TMP = "/tmp/_reel_distrital_explica"
CROP = "crop=1170:562:0:778"  # área do vídeo da Câmara, acima da legenda queimada
Y_VIDEO, H_VIDEO = 640, 760
T = tarja("politica", "reforma eleitoral")
CRED_VIDEO = "Vídeo: Câmara dos Deputados, Instagram oficial (reprodução)"
MANCHETE = 'Hugo Motta quer mudar o jeito de eleger deputado e vereador. <span style="color:#FF3B30">A gente traduz:</span>'
QUEM = "Hugo Motta, presidente da Câmara"
V = '<span style="color:#FF3B30">{}</span>'

# trechos da gravação e legendas (início e fim relativos ao trecho)
FALAS = [
    dict(a=2.10, z=17.97, leg=[
        (0.10, 4.80, "Nós caminharemos para fazer, ainda esse ano, uma discussão"),
        (4.80, 10.75, "e possível votação, na Câmara dos Deputados, sobre a mudança"),
        (10.75, 15.87, "do nosso sistema eleitoral, caminhando para o sistema " + V.format("distrital misto."))]),
    dict(a=79.93, z=92.90, leg=[
        (0.00, 3.10, "de podermos buscar a efetivação"),
        (3.10, 8.70, "desse sistema eleitoral no voto distrital misto para o ano de " + V.format("2034")),
        (8.70, 12.97, "e, até lá, construirmos uma " + V.format("transição") + " para esse modelo.")]),
]


def rotulo(txt):
    return f'<div style="font-weight:800;font-size:30px;letter-spacing:.14em;color:{RD}">{txt}</div>'


def assentos(n_verm, n_cinza, tam=58):
    q = "".join(f'<div style="width:{tam}px;height:{tam}px;border-radius:50%;background:{RD}"></div>' for _ in range(n_verm))
    q += "".join(f'<div style="width:{tam}px;height:{tam}px;border-radius:50%;background:#6d6a64"></div>' for _ in range(n_cinza))
    return f'<div style="display:flex;gap:14px;margin-top:26px">{q}</div>'


def legenda_assentos():
    return (f'<div style="display:flex;gap:40px;margin-top:18px;font-size:30px;color:{G}">'
            f'<span><span style="color:{RD}">●</span> mais votado de cada distrito</span>'
            f'<span><span style="color:#8d8983">●</span> lista do partido</span></div>')


# telas explicativas: lista de camadas (html, aparece_em) e duração
TELA1 = dict(dur=9.0, camadas=[
    (topo(T, "O Agora Praça explica", fundo="preto")
     + f'<div class="a serif" style="left:80px;right:80px;top:360px;font-size:84px;line-height:1.05">O que muda no seu voto</div>', 0.0),
    (f'''<div class="a" style="left:80px;right:80px;top:600px">{rotulo("HOJE")}
<div class="serif" style="font-size:120px;line-height:1;margin-top:14px">1 voto</div>
<div style="font-size:40px;line-height:1.3;color:{G};margin-top:18px">Você vota num candidato ou num partido. As vagas do estado são divididas pelo total de votos de cada partido.</div></div>''', 0.6),
    (f'''<div class="a" style="left:80px;right:80px;top:1060px">{rotulo("NO DISTRITAL MISTO")}
<div class="serif" style="font-size:120px;line-height:1;margin-top:14px;color:{RD}">2 votos</div>
<div style="font-size:40px;line-height:1.3;color:#fff;margin-top:18px">Um num candidato da sua região, o distrito. Outro num partido.</div>
{assentos(5, 5)}{legenda_assentos()}</div>''', 3.6),
])

TELA2 = dict(dur=10.0, camadas=[
    (topo(T, "O Agora Praça explica", fundo="preto")
     + f'<div class="a serif" style="left:80px;right:80px;top:360px;font-size:84px;line-height:1.05">Quando isso valeria</div>'
     + f'<div class="a" style="left:118px;top:560px;width:6px;height:900px;background:#3a3835"></div>', 0.0),
    (f'''<div class="a" style="left:100px;right:80px;top:560px;display:flex;gap:44px">
<div style="width:42px;height:42px;border-radius:50%;background:#8d8983;flex:none;margin-top:14px"></div>
<div><div class="serif" style="font-size:76px;line-height:1">2026</div>
<div style="font-size:38px;line-height:1.3;color:{G};margin-top:10px">A PEC começa a ser discutida na Câmara</div></div></div>''', 0.5),
    (f'''<div class="a" style="left:100px;right:80px;top:850px;display:flex;gap:44px">
<div style="width:42px;height:42px;border-radius:50%;background:{R};flex:none;margin-top:14px"></div>
<div><div class="serif" style="font-size:76px;line-height:1">2030</div>
<div style="font-size:38px;line-height:1.3;color:#fff;margin-top:10px">Eleição de transição: metade das vagas para os mais votados do estado, sem distritos. Metade para as listas dos partidos</div></div></div>''', 2.6),
    (f'''<div class="a" style="left:100px;right:80px;top:1240px;display:flex;gap:44px">
<div style="width:42px;height:42px;border-radius:50%;background:{RD};flex:none;margin-top:14px"></div>
<div><div class="serif" style="font-size:76px;line-height:1;color:{RD}">2034</div>
<div style="font-size:38px;line-height:1.3;color:#fff;margin-top:10px">Distrital misto completo, com o estado dividido em distritos</div></div></div>''', 5.6),
    (f'<div class="a" style="left:80px;right:80px;top:1530px;font-size:30px;color:#8d8983">O modelo de transição ainda está em negociação. Fontes: Câmara dos Deputados, SBT News e Metrópoles</div>', 6.6),
])

TELA3 = dict(dur=7.0, camadas=[
    (topo(T, "O Agora Praça explica", fundo="preto")
     + f'<div class="a serif" style="left:80px;right:80px;top:360px;font-size:84px;line-height:1.05">Para valer, a PEC precisa de</div>', 0.0),
    (f'''<div class="a" style="left:80px;right:80px;top:620px">
<div class="serif" style="font-size:230px;line-height:.95;color:{RD};letter-spacing:-.03em">308</div>
<div class="serif" style="font-size:60px;line-height:1.1;margin-top:20px">dos 513 deputados, em dois turnos</div>
<div class="serif" style="font-size:60px;line-height:1.1;margin-top:30px">e 49 dos 81 senadores</div></div>''', 0.5),
    (f'''<div class="a" style="left:80px;right:80px;top:1240px;font-size:40px;line-height:1.3;color:{G}">PT, PL, PSOL e Novo não estavam na reunião desta quarta. Motta diz que vai procurar os quatro.</div>''', 2.8),
])

DUR_ASS = 2.0
ORDEM = [("fala", 0), ("tela", TELA1), ("fala", 1), ("tela", TELA2), ("tela", TELA3), ("ass", None)]


def base_fala():
    grad = (f'<div class="a" style="left:0;top:0;width:1080px;height:{Y_VIDEO + 40}px;background:linear-gradient(to bottom,rgba(20,20,20,.92) 0px,rgba(20,20,20,.8) {Y_VIDEO - 60}px,rgba(20,20,20,0) {Y_VIDEO + 40}px)"></div>'
            f'<div class="a" style="left:0;bottom:0;width:1080px;height:{1920 - Y_VIDEO - H_VIDEO + 40}px;background:linear-gradient(to top,rgba(20,20,20,.92) 0px,rgba(20,20,20,.8) 400px,rgba(20,20,20,0) {1920 - Y_VIDEO - H_VIDEO + 40}px)"></div>')
    cab = topo(T, CRED_VIDEO, fundo="foto")
    cab = cab[cab.index("</div>") + 6:]
    man = f'<div class="a serif sh" style="left:80px;right:80px;top:336px;font-size:58px;line-height:1.12">{MANCHETE}</div>'
    return grad + cab + man


def legenda_html(txt):
    return f'''<div class="a" style="left:50px;right:50px;top:{Y_VIDEO + H_VIDEO + 36}px;background:rgba(20,20,20,.82);padding:26px 30px 30px;border-radius:6px">
<div class="sh" style="font-weight:800;font-size:28px;letter-spacing:.1em;color:#FF3B30;text-transform:uppercase">{QUEM}</div>
<div class="sh" style="font-size:52px;line-height:1.22;font-weight:700;margin-top:16px;color:#fff">{txt}</div></div>'''


def png(pg, html, caminho, fundo=False):
    bg = f"body{{background:{K}}}" if fundo else ""
    pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}{bg}</style></head><body>{html}</body></html>')
    pg.wait_for_timeout(250)
    pg.screenshot(path=caminho, omit_background=not fundo)


def run(c):
    subprocess.run(c, shell=True, check=True)


AUD = "-c:a aac -b:a 192k -ar 48000 -ac 2"
VID = "-r 30 -c:v libx264 -crf 18 -pix_fmt yuv420p"


def seg_fala(i, k, f, base):
    d = f["z"] - f["a"]
    out = f"{TMP}/s{i}.mp4"
    ent = f"-ss {f['a']} -t {d:.2f} -i {GRAV} -loop 1 -framerate 30 -i {base} " + " ".join(f"-loop 1 -framerate 30 -i {TMP}/f{k}l{j}.png" for j in range(len(f["leg"])))
    vf = f"{CROP},scale=-2:{H_VIDEO}:flags=lanczos,crop=1080:{H_VIDEO},eq=contrast=1.03,setsar=1"
    fc = (f"[0:v]fps=30,{CROP},setsar=1,split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=30:2,eq=brightness=-0.2[fundo];"
          f"[b]scale=-2:{H_VIDEO}:flags=lanczos,crop=1080:{H_VIDEO},eq=contrast=1.03[vid];[fundo][vid]overlay=0:{Y_VIDEO}[bg];[bg][1:v]overlay=0:0[v0];")
    for j, (a, z, _) in enumerate(f["leg"]):
        fc += f"[v{j}][{j + 2}:v]overlay=0:0:enable='between(t,{a},{z})'[v{j + 1}];"
    fc += f"[v{len(f['leg'])}]fade=in:st=0:d=0.15,format=yuv420p[vo];[0:a]afade=in:d=0.08,afade=out:st={d - 0.1:.2f}:d=0.1[ao]"
    run(f'ffmpeg -v error -y {ent} -filter_complex "{fc}" -map "[vo]" -map "[ao]" -t {d:.2f} {VID} {AUD} {out}')
    return out, d


def seg_tela(i, tela):
    out = f"{TMP}/s{i}.mp4"
    n = len(tela["camadas"])
    ent = f"-f lavfi -i color=c=0x141414:s=1080x1920:r=30:d={tela['dur']} -f lavfi -i anullsrc=r=48000:cl=stereo " + " ".join(
        f"-loop 1 -framerate 30 -t {tela['dur']} -i {TMP}/t{i}c{j}.png" for j in range(n))
    fc = "[0:v]null[v0];"
    for j, (_, t0) in enumerate(tela["camadas"]):
        fc += f"[{j + 2}:v]format=rgba,fade=in:st={t0}:d=0.35:alpha=1[c{j}];[v{j}][c{j}]overlay=0:0[v{j + 1}];"
    fc += f"[v{n}]format=yuv420p[vo]"
    run(f'ffmpeg -v error -y {ent} -filter_complex "{fc}" -map "[vo]" -map 1:a -t {tela["dur"]} {VID} {AUD} {out}')
    return out, tela["dur"]


def main():
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        png(pg, base_fala(), f"{TMP}/base.png")
        for i, f in enumerate(FALAS):
            for j, (_, _, txt) in enumerate(f["leg"]):
                png(pg, legenda_html(txt), f"{TMP}/f{i}l{j}.png")
        for i, (tipo, x) in enumerate(ORDEM):
            if tipo == "tela":
                for j, (html, _) in enumerate(x["camadas"]):
                    png(pg, html, f"{TMP}/t{i}c{j}.png")
        png(pg, assinatura("Câmara dos Deputados, Congresso em Foco, SBT News e Metrópoles"), f"{TMP}/ass.png", fundo=True)
        b.close()
    partes, falas_t, acum, cortes = [], [], 0.0, []
    for i, (tipo, x) in enumerate(ORDEM):
        if tipo == "fala":
            out, d = seg_fala(i, x, FALAS[x], f"{TMP}/base.png"); falas_t.append((acum, acum + d))
        elif tipo == "tela":
            out, d = seg_tela(i, x)
        else:
            out, d = f"{TMP}/s{i}.mp4", DUR_ASS
            run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {TMP}/ass.png -f lavfi -i anullsrc=r=48000:cl=stereo -t {d} -vf "fade=in:st=0:d=0.2,format=yuv420p" {VID} {AUD} {out}')
        partes.append(out); acum += d; cortes.append(round(acum, 3))
    total = acum
    open(f"{TMP}/lista.txt", "w").write("".join(f"file '{x}'\n" for x in partes))
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {TMP}/lista.txt -c:v copy {AUD} {TMP}/corpo.mp4")
    run(f"python3 {MOLDES}/trilha.py {TMP}/trilha.wav {total:.3f} '{json.dumps(cortes[:-1])}'")
    baixa = "+".join(f"between(t,{a:.2f},{z:.2f})" for a, z in falas_t)
    vol = f"volume='if({baixa},0.12,0.7)':eval=frame"
    saida = os.path.join(RAIZ, "video", "distrital-explica.mp4")
    run(f'ffmpeg -v error -y -i {TMP}/corpo.mp4 -i {TMP}/trilha.wav -filter_complex "[1:a]{vol}[tr];[0:a][tr]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[a]" '
        f'-map 0:v -map "[a]" -c:v copy {AUD} -movflags +faststart {saida}')
    run(f"ffmpeg -v error -y -ss 20 -i {saida} -frames:v 1 -q:v 3 {os.path.join(RAIZ, 'video', 'distrital-explica.jpg')}")
    print(f"ok: {saida} ({total:.1f} s)")


if __name__ == "__main__":
    main()
