#!/usr/bin/env python3
"""Carrossel 1080x1350: a carta de Flávio Bolsonaro, página por página, com a checagem (28/10/2026).

As páginas são prints da carta divulgada por Flávio (reprodução). Trechos marcados em vermelho.
Uso: python3 _src/carrosseis/flavio_carta.py [pasta_saida]  ->  01.jpg ... 06.jpg
"""
import os, sys, base64
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "identidade", "03-moldes-video"))
from agora import SELO, R, RD, K, G  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

MIDIA = os.path.join(RAIZ, "_src", "carrosseis", "midia")
PW, PH = 1166, 1842  # tamanho das páginas em midia/
TOTAL = 6


def b64(nome):
    return "data:image/png;base64," + base64.b64encode(open(os.path.join(MIDIA, nome), "rb").read()).decode()


CSS = f'''*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1350px;background:{K};color:#fff;font-family:Archivo;position:relative;overflow:hidden}}
.serif{{font-family:'Libre Caslon Text';font-weight:700}} .a{{position:absolute}}
.pag{{position:absolute;background:#fff;box-shadow:0 30px 80px rgba(0,0,0,.65);overflow:hidden}}
.pag img{{width:100%;display:block}}
.mk{{position:absolute;background:rgba(255,59,48,.38);mix-blend-mode:multiply;border-bottom:4px solid {RD}}}
.tag{{background:{R};font-weight:800;font-size:24px;letter-spacing:.14em;padding:10px 16px;display:inline-block}}
.num{{position:absolute;right:60px;bottom:44px;font-weight:800;font-size:26px;color:{G}}}
.fato{{font-weight:800;font-size:24px;letter-spacing:.14em;color:{RD}}}'''


def cabeca(tag):
    return f'''<div class="a" style="left:60px;right:60px;top:52px;display:flex;align-items:center">
<span class="tag">{tag}</span>
<div style="margin-left:auto;display:flex;align-items:center;gap:12px;font-weight:800;font-size:24px;letter-spacing:.12em">{SELO.format(w=38)}@AGORAPRACA</div></div>'''


def pagina(nome, x, y, h, rot=0, marcas=()):
    """Página inteira com altura h; marcas = [(x0, y0, x1, y1)] em pixels da página original."""
    k = h / PH
    w = PW * k
    mk = "".join(f'<div class="mk" style="left:{a * k:.0f}px;top:{b * k:.0f}px;width:{(c - a) * k:.0f}px;height:{(d - b) * k:.0f}px"></div>'
                 for a, b, c, d in marcas)
    return f'<div class="pag" style="left:{x}px;top:{y}px;width:{w:.0f}px;height:{h}px;transform:rotate({rot}deg)"><img src="{b64(nome)}">{mk}</div>'


def cartao(citacao, fato, top=760):
    return f'''<div class="a" style="left:300px;right:40px;top:{top}px;background:rgba(20,20,20,.96);border-left:8px solid {RD};padding:34px 36px 38px;box-shadow:0 20px 60px rgba(0,0,0,.6)">
<div class="serif" style="font-size:44px;line-height:1.16">“{citacao}”</div>
<div class="fato" style="margin-top:28px">O FATO</div>
<div style="font-size:31px;line-height:1.32;margin-top:10px;color:#eee">{fato}</div></div>'''


def num(i):
    return f'<div class="num">{i}/{TOTAL}</div>'


TELAS = [
    # 1. capa
    cabeca("ELEIÇÕES 2026")
    + pagina("flavio-carta-p3.png", 560, 150, 760, 7)
    + pagina("flavio-carta-p2.png", 400, 135, 760, 2)
    + pagina("flavio-carta-p1.png", 200, 150, 780, -4)
    + f'''<div class="a" style="left:0;right:0;bottom:0;height:820px;background:linear-gradient(to top,{K} 0,{K} 580px,rgba(20,20,20,0) 820px)"></div>
<div class="a" style="left:60px;right:60px;top:790px">
<div style="font-weight:800;font-size:26px;letter-spacing:.14em;color:{RD}">A CARTA DE FLÁVIO</div>
<div class="serif" style="font-size:62px;line-height:1.1;margin-top:18px">Dos EUA, Flávio se declarou “o verdadeiro presidente eleito do Brasil”</div>
<div style="font-size:32px;line-height:1.3;color:#fff;margin-top:22px;border-left:6px solid {RD};padding-left:18px">Horas depois, trocou “presidente eleito” por “líder do Brasil” e manteve a acusação de fraude</div>
<div style="font-size:30px;color:{G};margin-top:22px">A primeira versão e o que os números dizem &nbsp;→</div></div>''' + num(1),
    # 2. página 1
    cabeca("A CARTA · PÁGINA 1 DE 3")
    + pagina("flavio-carta-p1.png", 50, 130, 1100, -2, [(760, 352, 1112, 386), (66, 391, 140, 425), (222, 716, 1112, 750)])
    + cartao("Lula acrescentasse mais de 10 milhões de votos do primeiro para o segundo turno",
             "O número existe: Lula cresceu 10,4 milhões. E a conta fecha. Os outros dez candidatos tiveram 9,3 milhões de votos no primeiro turno, e o segundo turno teve 4,8 milhões de votos válidos a mais.", top=700) + num(2),
    # 3. página 2
    cabeca("A CARTA · PÁGINA 2 DE 3")
    + pagina("flavio-carta-p2.png", 50, 130, 1100, -2, [(272, 388, 670, 422)])
    + cartao("Não fugi do Brasil, eu saí pelo Brasil",
             "Quando saiu, pela Argentina, na noite de terça (27), Flávio estava proibido pelo STF de deixar o país. Agora diz que vai liderar a oposição dos Estados Unidos.", top=760) + num(3),
    # 4. página 3
    cabeca("A CARTA · PÁGINA 3 DE 3")
    + pagina("flavio-carta-p3.png", 50, 130, 1100, -2, [(560, 142, 1112, 176), (66, 180, 140, 214)])
    + cartao("Para impedir que Lula consolide um regime ditatorial no Brasil",
             "Lula foi declarado reeleito pelo TSE, com 51,79% dos votos válidos, e toma posse em 5 de janeiro. Flávio não apresenta prova de fraude.", top=700) + num(4),
    # 5. horário estendido
    cabeca("A CARTA E O HORÁRIO")
    + f'''<div class="a" style="left:60px;right:60px;top:200px">
<div class="serif" style="font-size:52px;line-height:1.14">A carta também ataca a decisão do STF que estendeu a votação até as 19h</div>
<div class="serif" style="font-size:210px;line-height:1;color:{RD};margin-top:70px;letter-spacing:-.03em">34.330</div>
<div class="serif" style="font-size:48px;line-height:1.15;margin-top:20px">votos registrados depois das 17h, no segundo turno</div>
<div style="font-size:34px;line-height:1.35;color:{G};margin-top:30px">Lula venceu por 4,4 milhões de votos. Mesmo que todos esses votos fossem dele, a vantagem passaria de 4,39 milhões.</div>
<div style="font-size:24px;color:#8d8983;margin-top:40px">Dados do TSE, via CNN Brasil</div></div>''' + num(5),
    # 6. fecho
    f'''<div class="a" style="left:0;right:0;top:330px;display:flex;flex-direction:column;align-items:center;text-align:center;padding:0 90px">{SELO.format(w=150)}
<div class="serif" style="font-size:80px;margin-top:40px">Agora Praça</div>
<div style="font-size:36px;color:{G};margin-top:14px">A praça é de todo mundo.</div>
<div class="serif" style="font-size:46px;line-height:1.2;margin-top:80px">A matéria completa, com todas as fontes, está no link da bio</div>
<div style="font-size:24px;color:#8d8983;margin-top:50px;line-height:1.5">Fontes: carta de Flávio Bolsonaro (reprodução), TSE, CartaCapital, CNN Brasil e Metrópoles</div></div>''' + num(6),
]


def main():
    saida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "_src", "carrosseis", "saida", "flavio-carta")
    os.makedirs(saida, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, html in enumerate(TELAS, 1):
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
            pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(saida, f"{i:02d}.jpg"), type="jpeg", quality=92)
        b.close()
    print("ok:", saida)


if __name__ == "__main__":
    main()
