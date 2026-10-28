#!/usr/bin/env python3
"""Reel: Flávio se declara "verdadeiro presidente eleito" em carta; os números do TSE (28/10/2026).

Uso: python3 _src/reels/flavio_carta.py
Gera video/flavio-carta.mp4 e video/flavio-carta.jpg. Sem imagem de TV. Fotos da Agência Brasil.
Números: 1º turno (TSE, via CartaCapital) e 2º turno (TSE); votos após as 17h (TSE, via CNN Brasil).
"""
import os, sys, subprocess
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import *  # noqa: E402,F401

T = tarja("politica", "eleições 2026")
MIDIA = os.path.join(RAIZ, "img", "fotos")

CENAS = [
    dict(tipo="video", arquivo="../../_src/reels/clips/flavio-stories-2026-10-28.mp4", cor=True, inicio=6.0, batidas=5,
         html=topo(T, "Vídeo: reprodução, stories de Flávio Bolsonaro") + texto("Dos EUA, Flávio diz em carta que é o “verdadeiro presidente eleito”",
                                      "Ele fala em fraude e não apresenta nenhuma prova", top=1010, fs=92)),
    dict(tipo="fixa", batidas=4, html=topo(T, "Tribunal Superior Eleitoral", fundo="preto")
         + numero("+10,4 mi", "Quanto Lula cresceu do primeiro para o segundo turno", "Flávio chama isso de “impossibilidade matemática”", top=620, fs=200)),
    dict(tipo="fixa", batidas=5, html=topo(T, "Tribunal Superior Eleitoral", fundo="preto")
         + numero("9,3 mi", "Votos dos outros dez candidatos no primeiro turno", "E o segundo turno teve 4,8 milhões de votos válidos a mais. A conta fecha", top=620, fs=220)),
    dict(tipo="fixa", batidas=5, html=topo(T, "Dados do TSE, via CNN Brasil", fundo="preto")
         + numero("34.330", "Votos registrados depois das 17h, com o horário estendido pelo STF", "Lula venceu por 4,4 milhões de votos", top=620, fs=220)),
    dict(tipo="foto", arquivo="urnas-lacre-tre-df.jpg", cor=True, mov="out", batidas=5,
         html=topo(T, "Foto: Joédson Alves/Agência Brasil") + texto("Lula foi declarado reeleito pelo TSE e toma posse em 5 de janeiro",
                                      "Flávio diz que vai liderar a oposição dos EUA", top=700, fs=96)),
    dict(tipo="fixa", batidas=2, html=assinatura("Carta de Flávio Bolsonaro, TSE, CartaCapital, CNN Brasil e Metrópoles")),
]

if __name__ == "__main__":
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "flavio-carta.mp4")
    total = montar(CENAS, saida, MIDIA, tmp=os.path.join("/tmp", "_reel_flavio_carta"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", saida, "-frames:v", "1", "-q:v", "3",
                    os.path.join(pasta, "flavio-carta.jpg")], check=True)
    print(f"ok: {saida} ({total:.1f} s)")
