#!/usr/bin/env python3
"""Reel: jovem de 18 anos esfaqueada no pescoço em Umarizal (RN); polícia investiga motivação política (31/10/2026).

Sem fotos da vítima (arquivo pessoal de pessoa privada): vídeos ilustrativos do Pexels.
Uso: python3 _src/reels/umarizal_clara.py -> video/umarizal-clara.mp4 e .jpg
"""
import os, sys, subprocess
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import *  # noqa: E402,F401

T = "BRASIL · VIOLÊNCIA"
MIDIA = "/tmp/_midia_clara"
PEXELS = {"sirene.mp4": "7714430/7714430-hd_1920_1080_30fps", "viatura.mp4": "7714379/7714379-hd_1920_1080_30fps",
          "hospital.mp4": "5203510/5203510-hd_1920_1080_30fps"}
PX = "Vídeo ilustrativo: Pexels"
FT = "Fontes: Correio, O Antagonista e O Globo"


def preparar():
    os.makedirs(MIDIA, exist_ok=True)
    for nome, cam in PEXELS.items():
        dest = os.path.join(MIDIA, nome)
        if not os.path.exists(dest):
            subprocess.run(["curl", "-s", "-L", "-o", dest, f"https://videos.pexels.com/video-files/{cam}.mp4"], check=True)


CENAS = [
    dict(tipo="video", arquivo="sirene.mp4", inicio=1, batidas=5,
         html=topo(T, PX) + texto("Jovem de 18 anos é esfaqueada no pescoço no Rio Grande do Norte",
                                  "A polícia investiga se o ataque teve motivação política", top=700, fs=80)),
    dict(tipo="video", arquivo="viatura.mp4", inicio=1, batidas=5,
         html=topo(T, PX) + texto("O suspeito é o namorado dela, também de 18 anos",
                                  "Ele foi preso em flagrante na madrugada de 26 de outubro, em Umarizal (RN), e ficou em silêncio", top=700, fs=80)),
    dict(tipo="fixa", batidas=6,
         html=topo(T, FT, fundo="preto") + texto("Segundo a advogada da vítima, o ataque veio depois que Clara comemorou a vitória de Lula",
                                                  "A motivação política ainda não está confirmada. A defesa dele não se manifestou", top=640, fs=78)),
    dict(tipo="video", arquivo="hospital.mp4", inicio=0, batidas=4,
         html=topo(T, PX) + texto("Clara passou por cirurgia na traqueia e saiu da UTI na sexta (30)",
                                  "Ela ainda não consegue falar", top=700, fs=80)),
    dict(tipo="fixa", batidas=5,
         html=topo(T, "Serviço", fundo="preto") + texto("Violência contra a mulher tem canal de denúncia",
                                                         "Ligue 180, a Central de Atendimento à Mulher, gratuita e 24 horas. Em emergência, ligue 190", top=640, fs=88)),
    dict(tipo="fixa", batidas=2, html=assinatura("Correio, O Antagonista e O Globo. Vídeos ilustrativos: Pexels")),
]

if __name__ == "__main__":
    preparar()
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "umarizal-clara.mp4")
    total = montar(CENAS, saida, MIDIA, tmp=os.path.join("/tmp", "_reel_umarizal"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", saida, "-frames:v", "1", "-q:v", "3",
                    os.path.join(pasta, "umarizal-clara.jpg")], check=True)
    print(f"ok: {saida} ({total:.1f} s)")
