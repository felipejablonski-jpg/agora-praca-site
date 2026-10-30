#!/usr/bin/env python3
"""Reel: desemprego de 5,2% no 3º trimestre de 2026 e recorde de pessoas ocupadas (Pnad Contínua, IBGE, 30/10/2026).

Uso: python3 _src/reels/desemprego_52.py -> video/desemprego-52.mp4 e .jpg
"""
import os, sys, subprocess
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import *  # noqa: E402,F401

T = tarja("servico", "emprego")
MIDIA = os.path.join(RAIZ, "img", "fotos")
FR = "Foto de arquivo: Fernando Frazão/Agência Brasil · Fonte: IBGE"
TR = "Foto de arquivo: Tânia Rêgo/Agência Brasil · Fonte: IBGE"
MC = "Foto de arquivo: Marcelo Camargo/Agência Brasil · Fonte: IBGE"

CENAS = [
    dict(tipo="foto", arquivo="multidao-rua-fernando-frazao-abr.jpg", cor=True, mov="in", batidas=5,
         html=topo(T, FR) + numero("103,6", "milhões de pessoas trabalhando no Brasil, o maior número da série do IBGE",
                                   "De julho a setembro de 2026. A série começa em 2012", top=640)),
    dict(tipo="foto", arquivo="multidao-calcadao-tania-rego-abr.jpg", cor=True, mov="esq", batidas=5,
         html=topo(T, TR) + numero("5,2%", "de desemprego, o menor para um terceiro trimestre desde 2012",
                                   "Eram 5,6% um ano antes. Ainda são 5,6 milhões de pessoas procurando trabalho", top=640)),
    dict(tipo="foto", arquivo="carteira-trabalho-digital-marcelo-camargo-abr.jpg", cor=True, mov="dir", batidas=5,
         html=topo(T, MC) + numero("37,5%", "de quem trabalha está na informalidade",
                                   "São 38,8 milhões de pessoas, quase quatro em cada dez", top=640)),
    dict(tipo="foto", arquivo="fila-onibus-tania-rego-abr.jpg", cor=True, mov="in", batidas=5,
         html=topo(T, TR) + numero("R$ 3.790", "é o rendimento médio de quem trabalha",
                                   "Estável no trimestre e 3,6% acima de um ano antes, já descontada a inflação", top=640, fs=190)),
    dict(tipo="fixa", batidas=2, html=assinatura("IBGE, Pnad Contínua, via Agência Brasil")),
]

if __name__ == "__main__":
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "desemprego-52.mp4")
    total = montar(CENAS, saida, MIDIA, tmp=os.path.join("/tmp", "_reel_desemprego"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", saida, "-frames:v", "1", "-q:v", "3",
                    os.path.join(pasta, "desemprego-52.jpg")], check=True)
    print(f"ok: {saida} ({total:.1f} s)")
