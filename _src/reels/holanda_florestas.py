#!/usr/bin/env python3
"""Reel: Holanda promete até US$ 500 milhões para o fundo de florestas tropicais (27/10/2026).

Uso: python3 _src/reels/holanda_florestas.py
Gera video/holanda-florestas.mp4 e video/holanda-florestas.jpg (capa = primeiro quadro).
"""
import os, sys, subprocess
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import *  # noqa: E402,F401

T = tarja("ciencia", "florestas")
MIDIA = os.path.join(RAIZ, "img", "fotos")
FOTO = "rio-tejo-acre-floresta.jpg"
ABR = "Foto: Rafa Neddermeyer/Agência Brasil · Rio Tejo, Acre"

# Gráfico: compromissos do fundo (US$ 7,3 bi em setembro + 0,5 bi da Holanda) contra a meta de US$ 10 bi.
BARRA = f'''<div class="a" style="left:80px;right:80px;top:470px">
<div id="n" class="serif" style="font-size:210px;line-height:.95;color:{RD};letter-spacing:-.03em">US$ 0</div>
<div class="serif" style="font-size:62px;line-height:1.1;margin-top:26px">bilhões já prometidos ao fundo</div>
<div style="position:relative;margin-top:90px;height:96px;background:#2a2a2a">
  <div id="b1" style="position:absolute;left:0;top:0;bottom:0;width:0;background:#8d8983"></div>
  <div id="b2" style="position:absolute;top:0;bottom:0;width:0;left:73%;background:{RD}"></div>
  <div style="position:absolute;right:-4px;top:-26px;bottom:-26px;width:8px;background:#fff"></div>
</div>
<div style="display:flex;justify-content:space-between;margin-top:30px;font-size:34px;font-weight:600">
  <span id="h" style="color:{RD};opacity:0">+ US$ 0,5 bi da Holanda</span><span>Meta: US$ 10 bi</span></div>
<div id="f" style="margin-top:110px;opacity:0">
  <div class="serif" style="font-size:66px;line-height:1.1">Faltam US$ 2,2 bi até dezembro</div>
  <div style="font-size:40px;color:{G};margin-top:24px;line-height:1.3">Sem a meta, a Noruega não libera os cerca de US$ 3 bi que prometeu</div></div>
</div>
<script>{EASE}
function draw(t){{
  var a=e(t/1.6), v=7.3*a; if(t>1.9) v=7.3+0.5*e((t-1.9)/0.6);
  document.getElementById('n').textContent='US$ '+v.toFixed(1).replace('.',',');
  document.getElementById('b1').style.width=(73*a)+'%';
  document.getElementById('b2').style.width=(5*e((t-1.9)/0.6))+'%';
  document.getElementById('h').style.opacity=e((t-1.9)/0.4);
  var f=document.getElementById('f'); f.style.opacity=e((t-2.6)/0.4); f.style.transform='translateY('+(30*(1-e((t-2.6)/0.4)))+'px)';
}}</script>'''

CENAS = [
    dict(tipo="foto", arquivo=FOTO, cor=True, mov="in", batidas=5,
         html=topo(T, ABR) + numero("500", "É o teto que a Holanda promete pôr no fundo criado pelo Brasil para manter floresta em pé",
                                    "Pagos em dez anos", top=640, unidade="milhões<br>de dólares")),
    dict(tipo="anim", batidas=5,
         html=topo(T, "Fontes: Carbon Pulse e Exame", fundo="preto") + BARRA),
    dict(tipo="foto", arquivo=FOTO, cor=True, mov="esq", batidas=4,
         html=topo(T, "Foto: Rafa Neddermeyer/Agência Brasil · Fonte: governo da Holanda") + numero("US$ 4", "por hectare de floresta em pé, por ano",
                                                                    "Valor indicado, pago depois que o satélite confirmar que o desmatamento ficou abaixo do limite",
                                                                    top=660)),
    dict(tipo="fixa", batidas=4, html=topo(T, "Fonte: governo da Holanda e Carbon Pulse", fundo="preto")
         + texto("Ainda é promessa", "Depende do Parlamento holandês e de condições que só devem ser fechadas até meados de 2027",
                 top=700, fs=120)),
    dict(tipo="fixa", batidas=2, html=assinatura("Governo da Holanda, Agência Brasil, Carbon Pulse, Reuters e Exame")),
]

if __name__ == "__main__":
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "holanda-florestas.mp4")
    total = montar(CENAS, saida, MIDIA, tmp=os.path.join("/tmp", "_reel_holanda_florestas"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", saida, "-frames:v", "1", "-q:v", "3",
                    os.path.join(pasta, "holanda-florestas.jpg")], check=True)
    print(f"ok: {saida} ({total:.1f} s)")
