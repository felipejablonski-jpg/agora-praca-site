#!/usr/bin/env python3
"""Reel: desemprego de 5,2% no 3º trimestre de 2026 e recorde de pessoas ocupadas (Pnad Contínua, IBGE, 30/10/2026).

Uso: python3 _src/reels/desemprego_52.py -> video/desemprego-52.mp4 e .jpg
"""
import os, sys, subprocess
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import *  # noqa: E402,F401

T = tarja("servico", "emprego")
FOTOS = os.path.join(RAIZ, "img", "fotos")
MIDIA = "/tmp/_midia_desemprego"  # fotos da casa + vídeos ilustrativos do Pexels, baixados na hora
PEXELS = {"multidao.mp4": "855564/855564-hd_1920_1080_24fps", "desfocada.mp4": "852107/852107-hd_1920_1080_30fps",
          "aerea.mp4": "2088290/2088290-hd_1920_1080_30fps"}
PX = "Vídeo ilustrativo: Pexels · Fonte: IBGE"


def preparar():
    os.makedirs(MIDIA, exist_ok=True)
    for f in os.listdir(FOTOS):
        if f.endswith(".jpg") and not os.path.exists(os.path.join(MIDIA, f)):
            os.symlink(os.path.join(FOTOS, f), os.path.join(MIDIA, f))
    for nome, cam in PEXELS.items():
        dest = os.path.join(MIDIA, nome)
        if not os.path.exists(dest):
            subprocess.run(["curl", "-s", "-L", "-o", dest, f"https://videos.pexels.com/video-files/{cam}.mp4"], check=True)
FR = "Foto de arquivo: Fernando Frazão/Agência Brasil · Fonte: IBGE"
TR = "Foto de arquivo: Tânia Rêgo/Agência Brasil · Fonte: IBGE"
MC = "Foto de arquivo: Marcelo Camargo/Agência Brasil · Fonte: IBGE"

CENAS = [
    dict(tipo="video", arquivo="multidao.mp4", inicio=2, batidas=5,
         html=topo(T, PX) + numero("103,6", "milhões de pessoas trabalhando no Brasil, o maior número da série do IBGE",
                                   "De julho a setembro de 2026. A série começa em 2012", top=640)),
    dict(tipo="video", arquivo="desfocada.mp4", inicio=4, batidas=5,
         html=topo(T, PX) + numero("5,2%", "de desemprego, o menor para um terceiro trimestre desde 2012",
                                   "Eram 5,6% um ano antes. Ainda são 5,6 milhões de pessoas procurando trabalho", top=640)),
    dict(tipo="foto", arquivo="carteira-trabalho-digital-marcelo-camargo-abr.jpg", cor=True, mov="dir", batidas=5,
         html=topo(T, MC) + numero("37,5%", "de quem trabalha está na informalidade",
                                   "São 38,8 milhões de pessoas, quase quatro em cada dez", top=640)),
    dict(tipo="video", arquivo="aerea.mp4", inicio=5, batidas=5,
         html=topo(T, PX) + numero("R$ 3.790", "é o rendimento médio de quem trabalha",
                                   "Estável no trimestre e 3,6% acima de um ano antes, já descontada a inflação", top=640, fs=190)),
    dict(tipo="fixa", batidas=2, html=assinatura("IBGE, Pnad Contínua, via Agência Brasil. Vídeos ilustrativos: Pexels")),
]

if __name__ == "__main__":
    preparar()
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "desemprego-52.mp4")
    total = montar(CENAS, saida, MIDIA, tmp=os.path.join("/tmp", "_reel_desemprego"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", saida, "-frames:v", "1", "-q:v", "3",
                    os.path.join(pasta, "desemprego-52.jpg")], check=True)
    print(f"ok: {saida} ({total:.1f} s)")
