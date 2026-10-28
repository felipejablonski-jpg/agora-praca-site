#!/usr/bin/env python3
"""Card do Threads no estilo post de rede social, na marca do Agora Praça (1080x1350).

Uso: python3 _src/threads/card.py <nome> "<texto>" [foto] [crédito]
Saída: _src/threads/saida/<nome>.jpg. Texto com *trecho* sai em vermelho.
"""
import os, sys, re, base64
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from playwright.sync_api import sync_playwright

FONTES = os.path.join(RAIZ, "identidade", "03-moldes-video", "fontes")
ICONE = os.path.join(RAIZ, "identidade", "01-marca", "agora-praca-icone-1080.png")


def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()


def fontes_css():
    css = ""
    for f in sorted(os.listdir(FONTES)):
        if "italic" in f.lower():
            continue
        fam = "Libre Caslon Text" if "caslon" in f.lower() else "Archivo"
        css += f"@font-face{{font-family:'{fam}';font-weight:100 900;src:url({b64(os.path.join(FONTES, f), 'font/ttf')})}}"
    return css


def html(texto, foto=None, credito=""):
    texto = re.sub(r"\*(.+?)\*", r'<span style="color:#FF3B30">\1</span>', texto).replace("\n", "<br>")
    tam = 58 if len(texto) < 140 else 50 if len(texto) < 220 else 44
    if foto:
        tam = min(tam, 46)
    img = ""
    if foto:
        mime = "image/png" if foto.endswith("png") else "image/jpeg"
        img = (f'<div style="margin-top:34px;border-radius:22px;overflow:hidden;height:520px;background:#222">'
               f'<img src="{b64(foto, mime)}" style="width:100%;height:100%;object-fit:cover;object-position:center 30%"></div>'
               f'<div style="font-size:22px;color:#8d8983;margin-top:12px">{credito}</div>')
    return f'''<html><head><meta charset="utf-8"><style>{fontes_css()}
*{{box-sizing:border-box;margin:0}} body{{width:1080px;height:1350px;background:#141414;font-family:Archivo;color:#fff;display:flex;align-items:center;justify-content:center}}
.c{{width:960px;background:#1f1f1f;border:1px solid #2e2e2e;border-radius:34px;padding:52px 56px 44px}}</style></head><body><div class="c">
<div style="display:flex;align-items:center;gap:22px">
<img src="{b64(ICONE, 'image/png')}" style="width:96px;height:96px;border-radius:50%">
<div><div style="font-weight:800;font-size:36px">Agora Praça</div><div style="font-size:30px;color:#8d8983;margin-top:2px">@agorapraca</div></div></div>
<div style="font-family:'Libre Caslon Text';font-weight:700;font-size:{tam}px;line-height:1.2;margin-top:38px">{texto}</div>
{img}
<div style="display:flex;justify-content:space-between;margin-top:36px;padding-top:26px;border-top:1px solid #2e2e2e;font-size:26px;color:#8d8983">
<span>agorapraca.com.br</span><span style="color:#FF3B30;font-weight:800;letter-spacing:.08em">MATÉRIA COMPLETA NO SITE</span></div>
</div></body></html>'''


def gerar(nome, texto, foto=None, credito=""):
    saida = os.path.join(RAIZ, "_src", "threads", "saida"); os.makedirs(saida, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.set_content(html(texto, foto, credito)); pg.wait_for_timeout(300)
        out = os.path.join(saida, f"{nome}.jpg"); pg.screenshot(path=out, type="jpeg", quality=92); b.close()
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    print(gerar(a[0], a[1], a[2] if len(a) > 2 else None, a[3] if len(a) > 3 else ""))
