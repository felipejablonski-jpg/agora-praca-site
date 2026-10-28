#!/usr/bin/env python3
"""Reel: Argentina confirma que Flávio Bolsonaro entrou no país (28/10/2026).

Uso: python3 _src/reels/flavio_miami.py
Gera video/flavio-miami.mp4 e video/flavio-miami.jpg (capa = primeiro quadro).
Sem imagem de TV. Fotos de arquivo com crédito.
"""
import os, sys, subprocess
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import *  # noqa: E402,F401

T = tarja("politica", "eleições 2026")
MIDIA = os.path.join(RAIZ, "img", "fotos")
ABR22 = "Foto de arquivo: Marcelo Camargo/Agência Brasil, 2022"

CENAS = [
    dict(tipo="foto", arquivo="flavio-telefone-agencia-senado.jpg", cor=True, mov="in", batidas=5,
         html=topo(T, "Foto de arquivo: Beto Barata/Agência Senado") + texto("A Argentina confirma que Flávio Bolsonaro entrou no país",
                                      "Na terça, o mesmo órgão tinha dito que não havia registro dele", top=720, fs=100)),
    dict(tipo="fixa", batidas=4, html=topo(T, "Comunicado da Direção Nacional de Migrações da Argentina", fundo="preto")
         + numero("22h50", "Hora em que ele entrou, pela ponte Tancredo Neves, em Misiones", "Terça (27), com a mulher e as duas filhas", top=640, fs=230)),
    dict(tipo="fixa", batidas=4, html=topo(T, "Comunicado da Direção Nacional de Migrações da Argentina", fundo="preto")
         + numero("23h30", "Hora em que embarcaram em voo privado com destino declarado a Guayaquil, no Equador", "Segundo o plano de voo", top=620, fs=230)),
    dict(tipo="foto", arquivo="aviao-aeroporto-ponte.jpg", cor=True, mov="out", batidas=5,
         html=topo(T, ABR22 + " · Folha de S.Paulo") + texto("A imprensa diz que ele já está em Miami",
                                      "Os EUA só confirmaram que vão dar vistos. Chegada e asilo seguem sem confirmação oficial", top=700, fs=96)),
    dict(tipo="fixa", batidas=4, html=topo(T, "Segundo aliado ouvido pela CNN Brasil", fundo="preto")
         + numero("Quinta", "Flávio deve falar em Miami, segundo aliado", "Coletiva à tarde, sem horário nem local divulgados", top=640, fs=200)),
    dict(tipo="fixa", batidas=2, html=assinatura("Migrações da Argentina, El Cronista, Ámbito, Folha e CNN Brasil")),
]

if __name__ == "__main__":
    pasta = os.path.join(RAIZ, "video")
    saida = os.path.join(pasta, "flavio-miami.mp4")
    total = montar(CENAS, saida, MIDIA, tmp=os.path.join("/tmp", "_reel_flavio_miami"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.6", "-i", saida, "-frames:v", "1", "-q:v", "3",
                    os.path.join(pasta, "flavio-miami.jpg")], check=True)
    print(f"ok: {saida} ({total:.1f} s)")
