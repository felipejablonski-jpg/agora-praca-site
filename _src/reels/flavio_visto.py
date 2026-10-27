#!/usr/bin/env python3
"""Reel: EUA vão dar visto a Flávio Bolsonaro e à família (27/10/2026).

Uso: python3 _src/reels/flavio_visto.py
Gera video/flavio-visto.mp4 e video/flavio-visto.jpg (capa = primeiro quadro).
"""
import os, sys, subprocess
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import *  # noqa: E402,F401

T = tarja("politica", "eleições 2026")
MIDIA = os.path.join(RAIZ, "img", "fotos")
ABR22 = "Foto de arquivo: Marcelo Camargo/Agência Brasil, 2022"
ABR09 = "Foto de arquivo: Marcello Casal Jr/Agência Brasil, 2009"

LISTA = f'''<div class="a" style="left:80px;right:80px;top:520px">
<div class="serif" style="font-size:72px;line-height:1.1">O que ainda <span style="color:{RD}">não</span> foi confirmado</div>
<div style="margin-top:60px;font-size:46px;line-height:1.35;color:#fff">
<div style="display:flex;gap:26px;margin-bottom:40px"><span style="color:{RD};font-weight:800">1</span><span>Onde Flávio está. A chegada aos EUA vem de fontes sem nome</span></div>
<div style="display:flex;gap:26px;margin-bottom:40px"><span style="color:{RD};font-weight:800">2</span><span>Por onde ele saiu. A Argentina nega que ele tenha entrado no país</span></div>
<div style="display:flex;gap:26px"><span style="color:{RD};font-weight:800">3</span><span>Nota oficial da PF, do STF ou do próprio senador</span></div>
</div></div>'''

CENAS = [
    dict(tipo="foto", arquivo="aviao-aeroporto-ponte.jpg", cor=True, mov="in", batidas=5,
         html=topo(T, ABR22) + texto("EUA vão dar visto a Flávio Bolsonaro e à família",
                                      "Confirmou um funcionário do Departamento de Estado à CNN Brasil, sem se identificar", top=700, fs=82)),
    dict(tipo="foto", arquivo="passaporte-brasileiro.jpg", cor=True, mov="dir", batidas=4,
         html=topo(T, ABR22) + numero("11h", "Venceu o prazo para entregar os passaportes à PF",
                                      "Terça-feira (27). Os documentos não foram entregues")),
    dict(tipo="foto", arquivo="justica-estatua-stf.jpg", cor=False, mov="in", batidas=4,
         html=topo(T, ABR09) + texto("Moraes também proibiu Flávio de deixar o país",
                                      "Ele é investigado no STF por suspeita de lavagem de dinheiro", top=760)),
    dict(tipo="fixa", batidas=6, html=topo(T, "Agora Praça, com CNN Brasil, UOL e g1", fundo="preto") + LISTA),
    dict(tipo="fixa", batidas=3, html=topo(T, "Segundo aliado ouvido pelo UOL", fundo="preto")
         + numero("Quarta", "Flávio deve dar entrevista coletiva", "Horário e local não foram divulgados", top=640, fs=200)),
    dict(tipo="fixa", batidas=2, html=assinatura("CNN Brasil, UOL, g1, Gazeta do Povo e Metrópoles")),
]

if __name__ == "__main__":
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "flavio-visto.mp4")
    total = montar(CENAS, saida, MIDIA, tmp=os.path.join("/tmp", "_reel_flavio_visto"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", saida, "-frames:v", "1", "-q:v", "3",
                    os.path.join(pasta, "flavio-visto.jpg")], check=True)
    print(f"ok: {saida} ({total:.1f} s)")
