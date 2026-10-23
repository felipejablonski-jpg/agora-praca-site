#!/usr/bin/env python3
"""Carrossel: fundo de perdas e danos reserva US$ 20 milhões ao Nepal (23/10/2026).

Gera img/nepal-fundo/01.jpg ... (1080x1350). Uso: python3 _src/carrosseis/nepal_fundo.py
Precisa de Node com Playwright (NODE_PATH apontando para node_modules com playwright).
"""
import os, sys, json, subprocess, tempfile, html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import telas_pp as T  # noqa: E402

RAIZ = T.RAIZ
e = html.escape
PASTA = os.path.join(RAIZ, "img", "nepal-fundo")
FOTO_A = "file://" + os.path.join(RAIZ, "img", "fotos", "vale-rio-himalaia.jpg")
FOTO_B = "file://" + os.path.join(RAIZ, "img", "fotos", "nota-dolar-detalhe.jpg")

CSS = T.CSS + '''
.ft { position: absolute; left: 0; top: 0; width: 1080px; height: 760px; display: flex; gap: 6px; background: #D2232A; }
.ft div { flex: 1; background-size: cover; background-position: center; }
.ft::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(20,20,20,.55) 0%, rgba(20,20,20,0) 22%, rgba(20,20,20,0) 60%, #141414 100%); }
.sobre { position: relative; z-index: 2; }
.capa2 h1 { font-size: 76px; margin-top: 0; }
.capa2 .bloco { margin-top: auto; position: relative; z-index: 2; }
.capa2 .cred { font-size: 22px; color: #bdb9b1; margin-top: 26px; }
.grade { display: grid; grid-template-columns: repeat(20, 1fr); gap: 6px; margin-top: 40px; }
.grade i { display: block; aspect-ratio: 1; background: #3a3835; }
.grade i.r { background: #FF463C; }
.leg { display: flex; gap: 40px; margin-top: 34px; font-size: 30px; color: #e6e2da; }
.leg b { display: inline-block; width: 26px; height: 26px; margin-right: 12px; vertical-align: -3px; }
.big { font-family: Caslon; font-weight: 700; font-size: 116px; color: #FF463C; line-height: 1; margin-top: 50px; white-space: nowrap; }
'''


def topo(i, n):
    return f'<div class="topo sobre"><span>CLIMA · INTERNACIONAL</span><span>{i}/{n}</span></div>'


def pe(fonte, escuro=True):
    return f'<div class="pe sobre">{T.logo("#D2232A", "#fff" if escuro else "#141414")}<span>{e(fonte)}</span></div>'


def telas():
    n = 6
    t = []
    t.append(f'''<div class="t escuro capa2"><div class="ft"><div style="background-image:url('{FOTO_A}')"></div><div style="background-image:url('{FOTO_B}')"></div></div>
<div class="topo sobre" style="color:#fff">{T.logo("#fff", "#fff", "capa-logo")}<span style="align-self:flex-start;margin-top:14px">@AGORAPRACA</span></div>
<div class="bloco"><span class="tag tag-r" style="margin-top:0">Clima</span><h1 style="margin-top:30px">Fundo da ONU reserva US$ 20 milhões ao Nepal. Reconstruir vai custar US$ 4,78 bilhões</h1>
<div class="cred">Fotos ilustrativas: Pexels</div></div>
<div class="pe sobre" style="margin-top:34px;color:#fff;font-weight:800;letter-spacing:.12em;justify-content:flex-end">ARRASTE PARA O LADO →</div></div>''')
    t.append(f'''<div class="t escuro">{topo(2, n)}<span class="tag tag-r">O desastre</span><h1 style="font-size:70px">Em 26 de agosto, uma avalanche de gelo e rocha virou enxurrada no norte do Nepal</h1>
<ul><li>A lama desceu cerca de 100 km pelo vale dos rios Bhote Koshi e Trishuli</li><li>Mais de 1.400 mortos e mais de 5.000 desaparecidos, segundo a AFP</li><li>Povoados, estradas, pontes e usinas foram destruídos</li></ul>{pe("Fontes: AFP, USGS e Copernicus")}</div>''')
    t.append(f'''<div class="t escuro">{topo(3, n)}<span class="tag tag-r">A decisão</span><h1 style="font-size:70px">Pela primeira vez, o fundo de perdas e danos reservou dinheiro para um país</h1>
<ul><li>O fundo foi criado na conferência do clima da ONU para pagar estragos do clima em países vulneráveis</li><li>O conselho aprovou por unanimidade na quinta-feira (22), numa reunião extraordinária</li><li>US$ 20 milhões é o máximo que o fundo libera por pedido</li></ul>{pe("Fontes: AFP e Climate Home News")}</div>''')
    quad = "".join('<i class="r"></i>' if k == 0 else "<i></i>" for k in range(239))
    t.append(f'''<div class="t escuro">{topo(4, n)}<span class="tag tag-r">A conta</span><h1 style="font-size:64px">Cada quadrado vale US$ 20 milhões. Só um foi reservado</h1>
<div class="grade">{quad}</div>
<div class="leg"><span><b style="background:#FF463C"></b>Reservado pelo fundo</span><span><b style="background:#3a3835"></b>Custo da reconstrução</span></div>
{pe("Estimativa do governo do Nepal, via AFP")}</div>''')
    t.append(f'''<div class="t escuro">{topo(5, n)}<span class="tag tag-r">Ainda não chegou</span><h1 style="font-size:70px">O dinheiro está reservado, mas ainda não foi transferido</h1>
<ul><li>O Nepal precisa apresentar uma proposta de como vai usar o recurso</li><li>Não há prazo para a aprovação. A próxima reunião do conselho é em dezembro</li><li>Alemanha, Tchéquia e Japão disseram que o caso não deve virar regra para os próximos desastres</li></ul>{pe("Fonte: Climate Home News")}</div>''')
    t.append(f'''<div class="t claro">{topo(6, n)}<span class="tag tag-p">Por que importa</span><div class="big">menos de 0,5%</div>
<div class="sub">da reconstrução do Nepal está coberta pelo que o fundo reservou</div><div class="linha"></div>
<div class="det">Os países pobres pediram esse fundo por anos: emitem pouco e pagam caro pelos desastres do clima. Hoje ele tem cerca de US$ 350 milhões para distribuir no mundo todo.</div>
{pe("Fontes: AFP e Climate Home News · agorapraca.com.br", escuro=False)}</div>''')
    return t


def main():
    os.makedirs(PASTA, exist_ok=True)
    tmp = tempfile.mkdtemp()
    arqs = []
    for k, p in enumerate(telas(), 1):
        h = os.path.join(tmp, f"{k:02d}.html")
        open(h, "w", encoding="utf-8").write(f"<!doctype html><meta charset=utf-8><style>{CSS}</style>{p}")
        arqs.append((h, os.path.join(tmp, f"{k:02d}.png"), os.path.join(PASTA, f"{k:02d}.jpg")))
    js = os.path.join(tmp, "s.js")
    open(js, "w").write('''const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({executablePath: process.env.CHROME});
const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
for (const [h, png] of JSON.parse(process.argv[2])) { await p.goto('file://' + h); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250); await p.screenshot({ path: png }); }
await b.close(); })();''')
    env = dict(os.environ, CHROME=os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"))
    subprocess.run(["node", js, json.dumps([[h, png] for h, png, _ in arqs])], check=True, env=env)
    from PIL import Image
    for _, png, jpg in arqs:
        Image.open(png).convert("RGB").save(jpg, quality=90)
        print(jpg)


if __name__ == "__main__":
    main()
