"""Molde único dos Reels do Agora Praça.
Uso: from agora import *; montar(CENAS, 'saida.mp4', pasta_midia)
Cada cena: dict(html=..., tipo='foto'|'video'|'anim'|'fixa', arquivo=..., cor=True|False, mov='in'|'out'|'dir'|'esq', inicio=0, batidas=4)
"""
import os, json, subprocess, shutil
from playwright.sync_api import sync_playwright
AQUI = os.path.dirname(os.path.abspath(__file__))
R = "#D2232A"; RD = "#FF3B30"; K = "#141414"; G = "#C9C5BD"; BAND = 980; FPS = 30; B = 60 / 72
EDITORIAS = {"politica": "POLÍTICA", "servico": "SERVIÇO", "ciencia": "CIÊNCIA"}
CSS = f'''*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1920px;background:transparent;color:#fff;font-family:Archivo;position:relative;overflow:hidden}}
.serif{{font-family:'Libre Caslon Text';font-weight:700}} .a{{position:absolute}} .sh{{text-shadow:0 2px 18px rgba(0,0,0,.7)}}'''
SELO = '''<svg width="{w}" height="{w}" viewBox="-47 -28 200 200"><rect x="-47" y="-28" width="200" height="200" fill="#D2232A"/><rect x="40" y="28" width="40" height="9" rx="1.5" fill="#fff"/><polygon points="52,37 78,37 106,144 76,144" fill="#fff"/><polygon points="50,37 57,37 9,144 1,144" fill="#fff"/><rect x="20" y="103" width="49" height="6" fill="#fff"/><path d="M75 28 C 77 19, 84 12, 92 8" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/><circle cx="98" cy="4" r="7.5" fill="#fff"/></svg>'''
EASE = "function e(x){x=Math.max(0,Math.min(1,x));return 1-Math.pow(1-x,3);}"

def tarja(editoria, subtema=""):
    t = EDITORIAS[editoria]; return f"{t} · {subtema.upper()}" if subtema else t

def topo(tag, credito, fundo="foto"):
    """fundo='foto': degradê sobre imagem na faixa de cima; 'preto': cena gráfica."""
    g = (f'<div class="a" style="left:0;top:0;width:1080px;height:1920px;background:linear-gradient(to bottom,rgba(20,20,20,.7) 0px,rgba(20,20,20,.1) 360px,rgba(20,20,20,0) 470px,rgba(20,20,20,.75) 780px,{K} {BAND}px,{K} 1920px)"></div>'
         if fundo == "foto" else f'<div class="a" style="inset:0;background:{K}"></div>')
    return g + f'''<div class="a sh" style="left:80px;right:80px;top:268px;font-size:25px;font-weight:600;color:rgba(255,255,255,.88)">{credito}</div>
<div class="a" style="left:80px;right:80px;top:190px;display:flex;align-items:center">
<div style="background:{R};font-weight:800;font-size:{28 if len(tag) <= 22 else 22}px;letter-spacing:{".16em" if len(tag) <= 22 else ".09em"};padding:12px 18px;white-space:nowrap">{tag}</div>
<div class="sh" style="margin-left:auto;display:flex;align-items:center;gap:12px;font-weight:800;font-size:26px;letter-spacing:.12em">{SELO.format(w=40)}@AGORAPRACA</div></div>'''

def numero(n, linha, sub="", top=720, fs=230, unidade=""):
    u = f'<span style="font-weight:800;font-size:42px;line-height:1.1;margin-left:20px">{unidade}</span>' if unidade else ""
    return f'''<div class="a" style="left:80px;right:80px;top:{top}px">
<div class="sh" style="display:flex;align-items:baseline"><span class="serif" style="font-size:{fs}px;line-height:.95;color:{RD};letter-spacing:-.03em;white-space:nowrap">{n}</span>{u}</div>
<div class="serif" style="font-size:66px;line-height:1.1;margin-top:26px">{linha}</div>
<div style="font-size:40px;color:{G};margin-top:24px;line-height:1.3">{sub}</div></div>'''

def texto(manchete, sub="", top=770, fs=68):
    return f'''<div class="a" style="left:80px;right:80px;top:{top}px"><div class="serif" style="font-size:{fs}px;line-height:1.1">{manchete}</div>
<div style="font-size:40px;color:{G};margin-top:26px;line-height:1.3">{sub}</div></div>'''

def assinatura(fontes):
    return f'''<div class="a" style="inset:0;background:{K}"></div><div class="a" style="left:0;right:0;top:700px;display:flex;flex-direction:column;align-items:center">{SELO.format(w=170)}
<div class="serif" style="font-size:96px;margin-top:44px">Agora Praça</div>
<div style="font-size:40px;color:{G};margin-top:18px">A praça é de todo mundo.</div>
<div style="font-size:26px;color:#8d8983;margin-top:70px;text-align:center;line-height:1.5;max-width:880px;padding:0 20px">Fontes: {fontes}<br>Reportagem completa em agorapraca.com.br</div></div>'''

def _run(c): subprocess.run(c, shell=True, check=True)

def montar(cenas, saida, midia, tmp=None):
    tmp = tmp or os.path.join(os.path.dirname(os.path.abspath(saida)), "_tmp_" + os.path.splitext(os.path.basename(saida))[0])
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    AR = 1080 / BAND
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for i, c in enumerate(cenas):
            dur = c["batidas"] * B
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{c["html"]}</body></html>'); pg.wait_for_timeout(300)
            if c["tipo"] == "anim":
                fd = os.path.join(tmp, f"fr{i}"); os.makedirs(fd)
                for k in range(int(round(dur * FPS))):
                    pg.evaluate(f"draw({k / FPS})"); pg.screenshot(path=os.path.join(fd, f"{k:04d}.png"))
            else:
                pg.screenshot(path=os.path.join(tmp, f"ov{i}.png"), omit_background=True)
        b.close()
    partes, cortes, acum = [], [], 0.0
    for i, c in enumerate(cenas):
        dur = c["batidas"] * B; n = int(round(dur * FPS)); out = os.path.join(tmp, f"sv{i}.mp4"); partes.append(out); ov = os.path.join(tmp, f"ov{i}.png")
        grade = "eq=saturation=0.85:contrast=1.06" if c.get("cor", True) else "hue=s=0,eq=contrast=1.12:brightness=-0.02"
        if c["tipo"] == "anim":
            _run(f'ffmpeg -v error -y -framerate 30 -i {tmp}/fr{i}/%04d.png -vf format=yuv420p -t {dur} -c:v libx264 -crf 18 -r 30 {out}')
        elif c["tipo"] == "fixa":
            _run(f'ffmpeg -v error -y -loop 1 -framerate 30 -i {ov} -vf "scale=1080:1920,fade=in:st=0:d=0.2,format=yuv420p" -t {dur} -c:v libx264 -crf 18 -r 30 {out}')
        elif c["tipo"] == "video":
            vf = f"fps=30,crop='ih*{AR:.4f}':ih,scale=1080:{BAND},{grade},pad=1080:1920:0:0:color=0x141414,setsar=1"
            _run(f'ffmpeg -v error -y -ss {c.get("inicio", 0)} -i {midia}/{c["arquivo"]} -loop 1 -framerate 30 -i {ov} -filter_complex "[0:v]{vf}[bg];[1:v]format=rgba,fade=in:st=0:d=0.2:alpha=1[o];[bg][o]overlay=0:0,format=yuv420p" -t {dur} -an -c:v libx264 -crf 18 -r 30 {out}')
        else:  # foto
            mv = c.get("mov", "in")
            z = {"in": f"1.0+0.10*on/{n}", "out": f"1.10-0.10*on/{n}", "dir": "1.15", "esq": "1.15"}[mv]
            x = {"in": "iw/2-(iw/zoom/2)", "out": "iw/2-(iw/zoom/2)", "dir": f"(iw-iw/zoom)*on/{n}", "esq": f"(iw-iw/zoom)*(1-on/{n})"}[mv]
            vf = (f"crop='min(iw,ih*{AR:.4f})':'min(ih,iw/{AR:.4f})',scale=3240:-2,zoompan=z='{z}':x='{x}':y='ih/2-(ih/zoom/2)':d={n}:s=1080x{BAND}:fps=30,{grade},pad=1080:1920:0:0:color=0x141414,setsar=1")
            _run(f'ffmpeg -v error -y -loop 1 -i {midia}/{c["arquivo"]} -loop 1 -framerate 30 -i {ov} -filter_complex "[0:v]{vf}[bg];[1:v]format=rgba,fade=in:st=0:d=0.25:alpha=1[o];[bg][o]overlay=0:0,format=yuv420p" -t {dur} -c:v libx264 -crf 18 -r 30 {out}')
        acum += dur; cortes.append(round(acum, 3))
    total = cortes[-1]; cortes = cortes[:-1]
    open(os.path.join(tmp, "partes.txt"), "w").write("".join(f"file '{x}'\n" for x in partes))
    _run(f"python3 {AQUI}/trilha.py {tmp}/fx.wav {total:.3f} '{json.dumps(cortes)}'")
    _run(f'ffmpeg -v error -y -f concat -safe 0 -i {tmp}/partes.txt -i {tmp}/fx.wav -map 0:v -map 1:a -c:v libx264 -crf 18 -r 30 -pix_fmt yuv420p -c:a aac -b:a 192k -af "volume=-3dB,loudnorm=I=-18:TP=-1.5" -t {total:.3f} -movflags +faststart {saida}')
    return total
