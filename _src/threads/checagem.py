#!/usr/bin/env python3
"""Card "Circula nas redes": desmente ou confirma o que está circulando, num formato que funciona
sozinho como imagem (WhatsApp, Threads, Instagram), sem depender do link. 1080x1350.

Uso: python3 _src/threads/checagem.py <nome> "<o que circula>" <SELO> "<o que é verdade>" "<fontes>"
- <o que circula>: o boato com as palavras de quem espalha; uma linha por item (\\n).
- <SELO>: FALSO, ENGANOSO, FALTA CONTEXTO ou VERDADEIRO.
- <o que é verdade>: os fatos, em uma ou duas frases. *trecho* sai em destaque.
- <fontes>: entram dentro da imagem, para irem junto quando alguém encaminhar só o print.
Saída: _src/threads/saida/<nome>.jpg
"""
import os, sys, re, html as H
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from card import b64, fontes_css, ICONE, RAIZ  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

CORES = {"FALSO": "#D2232A", "ENGANOSO": "#D2232A", "FALTA CONTEXTO": "#C47A00", "VERDADEIRO": "#1F7A3F"}


def pagina(boato, selo, fato, fontes):
    cor = CORES.get(selo.upper(), "#D2232A")
    itens = [i.strip(" •-") for i in boato.split("\n") if i.strip()]
    intro, lista = (itens[0], itens[1:]) if len(itens) > 1 and itens[0].endswith(":") else ("", itens)
    lis = "".join(f'<li style="margin-top:10px">{H.escape(i)}</li>' for i in lista)
    intro_h = f'<div style="font-size:36px;color:#555">{H.escape(intro)}</div>' if intro else ""
    fato_h = re.sub(r"\*(.+?)\*", rf'<b style="color:{cor}">\1</b>', H.escape(fato))
    tam = 52 if len(fato) < 170 else 46 if len(fato) < 240 else 40
    return f'''<html><head><meta charset="utf-8"><style>{fontes_css()}
*{{box-sizing:border-box;margin:0}} body{{width:1080px;height:1350px;background:#fff;font-family:Archivo;color:#141414;padding:70px 80px;display:flex;flex-direction:column}}
ul{{padding-left:34px}}</style></head><body>
<div style="display:flex;align-items:center;justify-content:space-between">
 <div style="display:flex;align-items:center;gap:20px"><img src="{b64(ICONE, 'image/png')}" style="width:84px;height:84px;border-radius:50%">
 <div><div style="font-weight:800;font-size:32px">Agora Praça</div><div style="font-size:26px;color:#8a8a8a">@agorapraca</div></div></div>
 <div style="background:#141414;color:#fff;font-weight:800;font-size:24px;letter-spacing:.14em;padding:12px 18px">CIRCULA NAS REDES</div>
</div>
<div style="margin-top:48px;background:#f2f1ef;border-left:8px solid #c9c6c1;padding:30px 34px">
 {intro_h}
 <ul style="font-size:38px;line-height:1.22;color:#3a3a3a;margin-top:6px">{lis}</ul>
</div>
<div style="margin-top:40px;display:flex;align-items:center;gap:22px">
 <div style="border:6px solid {cor};color:{cor};font-weight:900;font-size:58px;letter-spacing:.06em;padding:6px 24px;transform:rotate(-3deg)">{H.escape(selo.upper())}</div>
</div>
<div style="margin-top:34px;font-size:{tam}px;line-height:1.28;font-weight:500">{fato_h}</div>
<div style="margin-top:auto;padding-top:30px;border-top:2px solid #ececec;display:flex;justify-content:space-between;align-items:flex-end;gap:30px">
 <div style="font-size:24px;color:#6f6f6f;line-height:1.35">{H.escape(fontes)}</div>
 <div style="font-size:24px;color:#8a8a8a;white-space:nowrap">agorapraca.com.br</div>
</div>
</body></html>'''


def gerar(nome, boato, selo, fato, fontes):
    saida = os.path.join(RAIZ, "_src", "threads", "saida"); os.makedirs(saida, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.set_content(pagina(boato, selo, fato, fontes)); pg.wait_for_timeout(300)
        out = os.path.join(saida, f"{nome}.jpg"); pg.screenshot(path=out, type="jpeg", quality=92); b.close()
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    print(gerar(*a[:5]))
