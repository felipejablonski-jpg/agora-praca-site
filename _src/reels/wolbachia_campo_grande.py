#!/usr/bin/env python3
"""Reel: mosquitos com Wolbachia reduzem a dengue em Campo Grande (MS), estudo na Lancet Regional Health - Americas.

Fonte primária: Batista FM et al. Lancet Reg Health Am 2026;54:101327 (publicado em 2/12/2025), doi 10.1016/j.lana.2025.101327.
Uso: python3 _src/reels/wolbachia_campo_grande.py -> video/wolbachia-campo-grande.mp4 e .jpg
"""
import os, sys, subprocess
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import *  # noqa: E402,F401

T = tarja("ciencia", "dengue")
MIDIA = os.path.join(RAIZ, "img", "fotos")
FOTO = "aedes-aegypti-cdc-gathany-2006.jpg"
CRED = "Foto: James Gathany/CDC, 2006 · Domínio público"
FONTE = "Fonte: The Lancet Regional Health (Americas), 2026"

# Gráfico 1: 63,2% de redução (IC 95%: 51,9 a 71,9) nos bairros com Wolbachia estável (60% ou mais).
GRAF1 = f'''<div class="a" style="left:80px;right:80px;top:600px">
<div class="sh" style="display:flex;align-items:baseline"><span id="n" class="serif" style="font-size:300px;line-height:.95;color:{RD};letter-spacing:-.03em">0</span><span class="serif" style="font-size:150px;color:{RD}">%</span></div>
<div class="serif" style="font-size:66px;line-height:1.1;margin-top:26px">menos casos de dengue onde a bactéria se firmou</div>
<div style="position:relative;margin-top:80px;height:70px;background:#2a2a2a">
  <div id="b" style="position:absolute;left:0;top:0;bottom:0;width:0;background:{RD}"></div>
  <div id="ic" style="position:absolute;top:-16px;bottom:-16px;left:51.9%;width:19.9%;border:5px solid #fff;opacity:0"></div>
</div>
<div style="display:flex;justify-content:space-between;margin-top:22px;font-size:30px;font-weight:600;color:{G}"><span>0%</span><span>100%</span></div>
<div id="f" style="margin-top:50px;opacity:0;font-size:40px;color:{G};line-height:1.3">Bairros com 60% ou mais dos mosquitos com a bactéria, contra os mesmos bairros antes da soltura. Margem de erro: 51,9% a 71,9%</div>
</div>
<script>{EASE}
function draw(t){{
  var a=e(t/1.8);
  document.getElementById('n').textContent=(63.2*a).toFixed(1).replace('.',',');
  document.getElementById('b').style.width=(63.2*a)+'%';
  document.getElementById('ic').style.opacity=e((t-2.0)/0.4);
  var f=document.getElementById('f'); f.style.opacity=e((t-2.6)/0.4); f.style.transform='translateY('+(30*(1-e((t-2.6)/0.4)))+'px)';
}}</script>'''

# Gráfico 2: redução por faixa de prevalência da bactéria (1 - IRR), contra a faixa de 0 a 20%.
LINHAS = [("20 a 40%", 0, "sem diferença"), ("40 a 60%", 37, "37%"), ("60 a 80%", 49, "49%"), ("80 a 100%", 57, "57%")]
rows = ""
for i, (rot, v, txt) in enumerate(LINHAS):
    cor = "#8d8983" if v == 0 else RD
    rows += f'''<div style="display:flex;align-items:center;margin-top:46px;opacity:0" id="r{i}">
<div style="width:230px;font-size:38px;font-weight:700">{rot}</div>
<div style="flex:1;position:relative;height:84px;background:#2a2a2a"><div id="w{i}" style="position:absolute;left:0;top:0;bottom:0;width:0;background:{cor}"></div></div>
<div style="width:210px;text-align:right;font-size:{'28' if v == 0 else '58'}px;font-weight:800;color:{'#c9c4bd' if v == 0 else '#fff'}">{txt}</div></div>'''
GRAF2 = f'''<div class="a" style="left:80px;right:80px;top:540px">
<div class="serif" style="font-size:74px;line-height:1.08">Quanto mais mosquitos com a bactéria, menos dengue</div>
<div style="font-size:34px;color:{G};margin-top:22px;line-height:1.3">Queda nos casos, por faixa de mosquitos com Wolbachia no bairro</div>
{rows}
<div id="nt" style="margin-top:56px;opacity:0;font-size:32px;color:{G};line-height:1.35">Comparação com bairros e meses em que só 0 a 20% dos mosquitos tinham a bactéria</div>
</div>
<script>{EASE}
var V=[0,37,49,57];
function draw(t){{
  for(var i=0;i<4;i++){{
    var s=0.5+i*0.7, r=document.getElementById('r'+i);
    r.style.opacity=e((t-s)/0.3);
    document.getElementById('w'+i).style.width=(V[i]/60*100*e((t-s)/0.8))+'%';
  }}
  document.getElementById('nt').style.opacity=e((t-3.6)/0.4);
}}</script>'''

CRED_LAB = "Foto: Flávio Carvalho/WMP Brasil/Fiocruz (divulgação)"

# Ilustração: a bactéria se espalha pela população de mosquitos (valor final real: 86,4% em 2024).
import random
random.seed(7)
ORDEM = list(range(120)); random.shuffle(ORDEM)
PTS = "".join(f'<div id="p{k}" style="position:absolute;left:{(k % 12) * 72}px;top:{(k // 12) * 72}px;width:50px;height:50px;border-radius:50%;background:#3a3a3a"></div>' for k in range(120))
SPREAD = f'''<div class="a" style="left:80px;right:80px;top:470px">
<div class="serif" style="font-size:72px;line-height:1.08">Ela passa da mãe para os filhotes</div>
<div style="position:relative;width:940px;height:720px;margin-top:60px">{PTS}</div>
<div style="display:flex;align-items:baseline;margin-top:30px"><span id="n" class="serif" style="font-size:120px;color:{RD};line-height:1">0</span><span class="serif" style="font-size:70px;color:{RD}">%</span>
<span style="font-size:36px;color:{G};margin-left:24px;line-height:1.25">dos mosquitos testados em 2024 tinham a bactéria</span></div>
<div style="font-size:26px;color:#8d8983;margin-top:22px">Ilustração: Agora Praça. Cada bolinha representa 1 em 120 mosquitos</div>
</div>
<script>{EASE}
var ORD={ORDEM};
function draw(t){{
  var a=e((t-0.3)/3.6), m=Math.round(120*0.864*a);
  for(var k=0;k<120;k++){{ document.getElementById('p'+ORD[k]).style.background = k<m ? '{RD}' : '#3a3a3a'; }}
  document.getElementById('n').textContent=(86.4*a).toFixed(1).replace('.',',');
}}</script>'''

CENAS = [
    dict(tipo="foto", arquivo=FOTO, cor=True, mov="in", batidas=5,
         html=topo(T, CRED) + numero("100", "milhões de mosquitos foram soltos de propósito em Campo Grande",
                                     "Mais de 100 milhões, de dezembro de 2020 a dezembro de 2023", top=640, unidade="")),
    dict(tipo="foto", arquivo="wolbachia-lab-triagem-placa-wmp-fiocruz.jpg", cor=True, mov="dir", batidas=4,
         html=topo(T, CRED_LAB) + texto("Eles carregam uma bactéria que atrapalha o vírus da dengue",
                                        "A Wolbachia faz o mosquito transmitir menos o vírus", top=720, fs=76)),
    dict(tipo="anim", batidas=6, html=topo(T, FONTE, fundo="preto") + SPREAD),
    dict(tipo="foto", arquivo="wolbachia-lab-mosquitos-tela-wmp-fiocruz.jpg", cor=True, mov="in", batidas=5,
         html=topo(T, CRED_LAB) + texto("Criados em laboratório e soltos de carro",
                                        "Em tubos com 100 a 150 mosquitos, em seis áreas da cidade, uma de cada vez. Cerca de 880 mil moradores, 73 bairros",
                                        top=720, fs=80)),
    dict(tipo="anim", batidas=7, html=topo(T, FONTE, fundo="preto") + GRAF1),
    dict(tipo="anim", batidas=8, html=topo(T, FONTE, fundo="preto") + GRAF2),
    dict(tipo="foto", arquivo="wolbachia-lab-microscopio-wmp-fiocruz.jpg", cor=True, mov="esq", batidas=7,
         html=topo(T, CRED_LAB) + texto("O que o estudo deixa em aberto",
                                        "Onde a bactéria ficou instável, a queda foi de 9,2%, dentro da margem de erro. O estudo observou a cidade, sem sortear grupos. A pandemia pode ter afetado os registros de 2020 e 2021",
                                        top=700, fs=84)),
    dict(tipo="fixa", batidas=2, html=assinatura("The Lancet Regional Health (Americas), Batista et al., 2026, Fiocruz e CDC")),
]

if __name__ == "__main__":
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "wolbachia-campo-grande.mp4")
    total = montar(CENAS, saida, MIDIA, tmp=os.path.join("/tmp", "_reel_wolbachia"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", saida, "-frames:v", "1", "-q:v", "3",
                    os.path.join(pasta, "wolbachia-campo-grande.jpg")], check=True)
    print(f"ok: {saida} ({total:.1f} s)")
