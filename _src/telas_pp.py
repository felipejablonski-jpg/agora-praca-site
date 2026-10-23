#!/usr/bin/env python3
"""Gera as telas da Primeira Página para o Instagram (1080x1350) em pp/<data>/NN.jpg.

Uso: python3 _src/telas_pp.py _src/telas/2026-10-23.json
O JSON tem: data, dia_longo, capa (lista de manchetes curtas), telas (lista) e agenda.
Tipos de tela: "texto" (fundo escuro, título e tópicos) e "numero" (fundo claro, número grande).
Precisa de Node com Playwright (chromium em /opt/pw-browsers).
"""
import os, sys, json, html, subprocess, tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, "_src", "fontes")
e = html.escape

LOGO = '''<svg viewBox="0 -8 446 248" class="logo"><rect x="40" y="28" width="40" height="9" rx="1.5" fill="{a}"/><polygon points="52,37 78,37 106,144 76,144" fill="{a}"/><polygon points="50,37 57,37 9,144 1,144" fill="{a}"/><rect x="20" y="103" width="49" height="6" fill="{a}"/><path d="M75 28 C 77 19, 84 12, 92 8" fill="none" stroke="{a}" stroke-width="3.5" stroke-linecap="round"/><circle cx="98" cy="4" r="7.5" fill="{a}"/><text x="112" y="144" font-family="Archivo" font-weight="600" font-size="150" letter-spacing="-3" fill="{b}">gora</text><text x="416" y="222" text-anchor="end" font-family="Archivo" font-weight="700" font-size="44" letter-spacing="16" fill="{a}">PRAÇA</text></svg>'''

CSS = f'''
@font-face {{ font-family: Caslon; src: url("file://{F}/libre-caslon-text-latin-700-normal.woff"); font-weight: 700; }}
@font-face {{ font-family: Archivo; src: url("file://{F}/archivo-latin-600-normal.woff"); font-weight: 400 600; }}
@font-face {{ font-family: Archivo; src: url("file://{F}/archivo-latin-800-normal.woff"); font-weight: 700 900; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1080px; height: 1350px; font-family: Archivo; overflow: hidden; }}
.t {{ width: 1080px; height: 1350px; padding: 64px 72px; display: flex; flex-direction: column; position: relative; }}
.escuro {{ background: #141414; color: #fff; }} .claro {{ background: #fff; color: #141414; }} .creme {{ background: #F2EFE9; color: #141414; }} .verm {{ background: #D2232A; color: #fff; }}
.topo {{ display: flex; justify-content: space-between; font-weight: 800; font-size: 22px; letter-spacing: .14em; color: #8a867e; }}
.escuro .topo {{ color: #9b978f; }}
.tag {{ display: inline-block; align-self: flex-start; margin-top: 70px; padding: 10px 18px; font-weight: 800; font-size: 26px; letter-spacing: .12em; text-transform: uppercase; }}
.tag-r {{ background: #D2232A; color: #fff; }} .tag-p {{ background: #141414; color: #fff; }}
h1 {{ font-family: Caslon; font-weight: 700; line-height: 1.08; letter-spacing: -.01em; margin-top: 44px; }}
ul {{ list-style: none; padding: 0; margin-top: 56px; }}
li {{ position: relative; padding-left: 36px; font-size: 36px; line-height: 1.5; color: #e6e2da; margin-bottom: 30px; }}
li::before {{ content: ""; position: absolute; left: 0; top: 18px; width: 13px; height: 13px; background: #D2232A; }}
.num {{ font-family: Caslon; font-weight: 700; color: #D2232A; line-height: .95; margin-top: 60px; letter-spacing: -.02em; }}
.sub {{ font-weight: 700; font-size: 46px; line-height: 1.3; margin-top: 46px; }}
.linha {{ height: 3px; background: #D2232A; margin: 50px 0; }}
.det {{ font-size: 34px; line-height: 1.5; color: #333; }}
.pe {{ margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end; font-size: 22px; color: #6d6a64; }}
.escuro .pe {{ color: #9b978f; }}
.logo {{ width: 120px; }}
.capa-logo {{ width: 210px; }}
.capa h1 {{ font-size: 100px; white-space: nowrap; margin-top: 60px; border-top: 5px solid #fff; padding-top: 34px; }}
.capa .data {{ font-weight: 700; font-size: 28px; margin-top: 18px; padding-bottom: 34px; border-bottom: 2px solid rgba(255,255,255,.55); }}
.capa ol {{ list-style: none; padding: 0; }}
.capa ol li {{ font-family: Caslon; font-size: 38px; line-height: 1.22; color: #fff; padding: 26px 0 26px 56px; margin: 0; border-bottom: 2px solid rgba(255,255,255,.35); }}
.capa ol li::before {{ content: attr(data-n); background: none; width: auto; height: auto; top: 26px; font-weight: 700; }}
.capa .pe {{ color: #fff; font-weight: 800; letter-spacing: .12em; justify-content: flex-end; }}
.ag h1 {{ font-size: 104px; margin-top: 40px; padding-bottom: 30px; border-bottom: 3px solid #141414; }}
.ag .row {{ display: grid; grid-template-columns: 300px 1fr; gap: 30px; padding: 34px 0; border-bottom: 2px solid #141414; }}
.ag .q {{ font-weight: 800; font-size: 22px; letter-spacing: .14em; color: #D2232A; }}
.ag .d {{ font-family: Caslon; font-weight: 700; font-size: 66px; line-height: 1; margin-top: 6px; }}
.ag .tx {{ font-size: 33px; line-height: 1.45; padding-top: 10px; }}
.ag .fim {{ font-weight: 800; font-size: 30px; color: #D2232A; margin-top: 36px; }}
'''


def logo(a="#D2232A", b="#141414", cls="logo"):
    return LOGO.format(a=a, b=b).replace('class="logo"', f'class="{cls}"')


def tela_capa(c, n):
    itens = "".join(f'<li data-n="{i+1}">{e(t)}</li>' for i, t in enumerate(c["capa"]))
    return f'''<div class="t verm capa"><div class="topo" style="color:#fff">{logo("#fff", "#fff", "capa-logo")}<span style="align-self:flex-start;margin-top:14px">@AGORAPRACA</span></div>
<h1>Primeira Página</h1><div class="data">{e(c["dia_longo"])}</div><ol>{itens}</ol>
<div class="pe">ARRASTE PARA O LADO →</div></div>'''


def tela(c, t, i, n):
    topo = f'<div class="topo"><span>PRIMEIRA PÁGINA · {e(c["data_curta"])}</span><span>{i}/{n}</span></div>'
    if t["tipo"] == "texto":
        tam = t.get("tam", 66)
        lis = "".join(f"<li>{e(x)}</li>" for x in t["topicos"])
        return f'''<div class="t escuro">{topo}<span class="tag tag-r">{e(t["tag"])}</span><h1 style="font-size:{tam}px">{e(t["titulo"])}</h1><ul>{lis}</ul>
<div class="pe">{logo("#D2232A", "#fff")}<span>{e(t["fonte"])}</span></div></div>'''
    tam = t.get("tam", 240)
    return f'''<div class="t claro">{topo}<span class="tag tag-p">{e(t["tag"])}</span><div class="num" style="font-size:{tam}px">{e(t["numero"])}</div>
<div class="sub">{e(t["frase"])}</div><div class="linha"></div><div class="det">{e(t["detalhe"])}</div>
<div class="pe">{logo()}<span>{e(t["fonte"])}</span></div></div>'''


def tela_agenda(c, i, n):
    topo = f'<div class="topo"><span>PRIMEIRA PÁGINA · {e(c["data_curta"])}</span><span>{i}/{n}</span></div>'
    rows = "".join(f'<div class="row"><div><div class="q">{e(q)}</div><div class="d">{e(d)}</div></div><div class="tx">{e(tx)}</div></div>' for q, d, tx in c["agenda"])
    return f'''<div class="t creme ag">{topo}<h1>{e(c.get("agenda_titulo", "Os próximos dias"))}</h1>{rows}<div class="fim">Amanhã cedo tem Primeira Página de novo.</div>
<div class="pe">{logo()}<span>{e(c["agenda_fonte"])}</span></div></div>'''


def main(arq):
    c = json.load(open(arq, encoding="utf-8"))
    n = len(c["telas"]) + 2
    paginas = [tela_capa(c, n)] + [tela(c, t, i + 2, n) for i, t in enumerate(c["telas"])] + [tela_agenda(c, n, n)]
    pasta = os.path.join(RAIZ, "pp", c["data"])
    os.makedirs(pasta, exist_ok=True)
    tmp = tempfile.mkdtemp()
    arquivos = []
    for k, p in enumerate(paginas, 1):
        h = os.path.join(tmp, f"{k:02d}.html")
        open(h, "w", encoding="utf-8").write(f"<!doctype html><meta charset=utf-8><style>{CSS}</style>{p}")
        arquivos.append((h, os.path.join(tmp, f"{k:02d}.png"), os.path.join(pasta, f"{k:02d}.jpg")))
    js = os.path.join(tmp, "s.js")
    open(js, "w").write('''const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({executablePath: process.env.CHROME});
const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
for (const [h, png] of JSON.parse(process.argv[2])) { await p.goto('file://' + h); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150); await p.screenshot({ path: png }); }
await b.close(); })();''')
    env = dict(os.environ, CHROME=os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"),
               NODE_PATH=os.environ.get("NODE_PATH", ""))
    subprocess.run(["node", js, json.dumps([[h, png] for h, png, _ in arquivos])], check=True, env=env)
    from PIL import Image
    for _, png, jpg in arquivos:
        Image.open(png).convert("RGB").save(jpg, quality=90)
        print(jpg)


if __name__ == "__main__":
    main(sys.argv[1])
