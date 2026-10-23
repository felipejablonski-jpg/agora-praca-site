#!/usr/bin/env python3
"""Gera o site estático do Agora Praça a partir de _src/conteudo.py.
Uso: python3 _src/build.py   (rodar na raiz do repositório)"""
import os, sys, html, datetime, shutil

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "_src"))
from conteudo import EDITORIAS, NOTICIAS, VIDEOS, EDICOES, FRASES  # noqa: E402

SITE = "https://agorapraca.com.br"
import hashlib
# versão do CSS no link: muda sempre que o estilo muda, para nenhum navegador usar o antigo do cache
CSS_V = hashlib.md5(open(os.path.join(RAIZ, "_src", "estilo.css"), "rb").read()).hexdigest()[:8]
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
MES_C = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]

e = html.escape


def d(s):
    return datetime.date.fromisoformat(s)


def data_longa(s, dia_semana=True):
    x = d(s)
    t = f"{x.day} de {MESES[x.month-1]} de {x.year}"
    return f"{DIAS[x.weekday()]}, {t}" if dia_semana else t


def data_curta(s):
    x = d(s)
    return f"{x.day} {MES_C[x.month-1]} {x.year}"


NOTICIAS[:] = [n for n in NOTICIAS if not n.get("rascunho")]
NOTICIAS.sort(key=lambda n: (n["data"], n.get("ordem", 0), n.get("atualizado", "")), reverse=True)
POR_SLUG = {n["slug"]: n for n in NOTICIAS}

# Regra: toda matéria tem capa própria do site (16:9), separada da capa do Reel
# e do card do Instagram. Só em caso raro, "sem_capa": "motivo" dispensa a capa.
_sem = [n["slug"] for n in NOTICIAS if not n.get("capa") and not n.get("sem_capa")]
_falta = [n["capa"] for n in NOTICIAS if n.get("capa") and not os.path.exists(os.path.join(RAIZ, n["capa"]))]
if _sem or _falta:
    sys.exit("ERRO: matéria sem capa do site: " + ", ".join(_sem) + (" | arquivo de capa não encontrado: " + ", ".join(_falta) if _falta else "")
             + "\nCrie a capa em _src/capas.py (ou use uma foto 16:9) e preencha \"capa\" e \"capa_credito\".")
EDICOES.sort(key=lambda x: x["data"], reverse=True)
HOJE = max([n.get("atualizado", n["data"]) for n in NOTICIAS] + [x["data"] for x in EDICOES])

LOGO = '''<svg viewBox="0 -8 446 248" role="img" aria-label="Agora Praça"><rect x="40" y="28" width="40" height="9" rx="1.5" fill="#D2232A"/><polygon points="52,37 78,37 106,144 76,144" fill="#D2232A"/><polygon points="50,37 57,37 9,144 1,144" fill="#D2232A"/><rect x="20" y="103" width="49" height="6" fill="#D2232A"/><path d="M75 28 C 77 19, 84 12, 92 8" fill="none" stroke="#D2232A" stroke-width="3.5" stroke-linecap="round"/><circle cx="98" cy="4" r="7.5" fill="#D2232A"/><text x="112" y="144" font-family="Archivo, Arial, sans-serif" font-weight="600" font-size="150" letter-spacing="-3" fill="#141414">gora</text><text x="416" y="222" text-anchor="end" font-family="Archivo, Arial, sans-serif" font-weight="700" font-size="44" letter-spacing="16" fill="#D2232A">PRAÇA</text></svg>'''
ICONE = '''<svg viewBox="-47 -28 200 200" aria-hidden="true"><rect x="-47" y="-28" width="200" height="200" fill="#D2232A"/><rect x="40" y="28" width="40" height="9" rx="1.5" fill="#FFF"/><polygon points="52,37 78,37 106,144 76,144" fill="#FFF"/><polygon points="50,37 57,37 9,144 1,144" fill="#FFF"/><rect x="20" y="103" width="49" height="6" fill="#FFF"/><path d="M75 28 C 77 19, 84 12, 92 8" fill="none" stroke="#FFF" stroke-width="3.5" stroke-linecap="round"/><circle cx="98" cy="4" r="7.5" fill="#FFF"/></svg>'''


def url_noticia(n):
    return f"/noticias/{n['slug']}/"


def url_edicao(x):
    return f"/primeira-pagina/{x['data']}/"


def cabeca(titulo, desc, caminho, imagem="/og.png", tipo="website", completo=False):
    t = "Agora Praça" if titulo is None else f"{titulo} | Agora Praça"
    nav = "".join(f'<a href="/{k}/">{e(v["nome"])}</a>' for k, v in EDITORIAS.items())
    nav += '<a href="/primeira-pagina/">Primeira Página</a><a href="/em-uma-linha/">Em uma linha</a><a href="/sobre/">Quem somos</a>'
    if completo:
        topo = f'''<div class="brand"><a href="/" aria-label="Agora Praça, página inicial">{LOGO}</a><p>A praça é de todo mundo. Do lado do interesse público, com fato checado.</p></div>'''
    else:
        topo = f'''<div class="brand brand-sm"><a href="/" aria-label="Agora Praça, página inicial">{LOGO}</a></div>'''
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(t)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{caminho}">
<meta property="og:type" content="{tipo}">
<meta property="og:site_name" content="Agora Praça">
<meta property="og:title" content="{e(titulo or 'Agora Praça')}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{caminho}">
<meta property="og:image" content="{SITE}{imagem}">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#141414">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="/estilo.css?v={CSS_V}">
</head>
<body>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="mast"><div class="wrap">
<div class="dateline"><strong>Primavera do Leste (MT)</strong><span>Atualizado em {data_longa(HOJE)}</span></div>
{topo}
<nav class="nav" aria-label="Seções">{nav}</nav>
</div></header>
<main id="conteudo">
'''


RODAPE = f'''</main>
<footer><div class="wrap">
<div class="foot-brand">{ICONE}<div><strong>Agora Praça</strong><span>Jornalismo digital independente. Redação em Primavera do Leste (MT).</span></div></div>
<nav class="foot-nav" aria-label="Institucional"><a href="/sobre/#principios">Princípios</a><a href="/sobre/#correcoes">Correções</a><a href="/sobre/#expediente">Expediente</a><a href="https://www.instagram.com/agorapraca/" rel="noopener">Instagram @agorapraca</a></nav>
</div></footer>
</body>
</html>
'''


def chapeu(n):
    ed = EDITORIAS[n["editoria"]]
    return f'<span class="kicker kicker-{ed["cor"]}">{e(ed["nome"])}</span>'


def imagem_lista(n):
    ed = EDITORIAS[n["editoria"]]
    if n.get("capa"):
        return f'<img src="/{n["capa"]}" alt="" loading="lazy" width="1200" height="675">'
    if n.get("sem_thumb"):
        return f'<div class="tipo tipo-{ed["cor"]}"><span>{e(n.get("chapeu") or ed["nome"])}</span></div>'
    if n.get("thumb"):
        return f'<img src="/{n["thumb"]}" alt="" loading="lazy" width="960" height="540">'
    if n.get("foto"):
        return f'<img src="/{n["foto"]}" alt="" loading="lazy" width="1200" height="675">'
    if n.get("carrossel"):
        return f'<img src="/{n["carrossel"][0]}" alt="" loading="lazy" class="img-vid">'
    if n.get("card"):
        return f'<img src="/{n["card"]}" alt="" loading="lazy" class="img-vid">'
    if n.get("video"):
        return f'<img src="/video/{n["video"]}.jpg" alt="" loading="lazy" class="img-vid">'
    return f'<div class="tipo tipo-{ed["cor"]}"><span>{e(n.get("chapeu") or ed["nome"])}</span></div>'


def item(n, grande=False):
    cls = "item item-g" if grande else "item"
    fina = f'<p class="fina">{e(n["linha_fina"])}</p>' if grande else ""
    return f'''<article class="{cls}"><a href="{url_noticia(n)}"><div class="thumb">{imagem_lista(n)}</div>
<div class="item-txt">{chapeu(n)}<h3>{e(n["titulo"])}</h3>{fina}<time datetime="{n["data"]}">{data_curta(n["data"])}</time></div></a></article>'''


def paragrafos(lista):
    out = []
    for p in lista:
        if p.startswith("## "):
            out.append(f"<h2>{e(p[3:])}</h2>")
        elif p.startswith("!fig "):
            src, leg = (p[5:].split("|", 1) + [""])[:2]
            out.append(f'<figure class="hero"><img src="/{e(src.strip())}" alt="{e(leg.strip())}" loading="lazy"><figcaption>{e(leg.strip())}</figcaption></figure>')
        else:
            out.append(f"<p>{e(p)}</p>")
    return "\n".join(out)


def video_tag(v):
    return f'''<figure class="reel"><video controls playsinline preload="none" poster="/video/{v}.jpg" width="1080" height="1920"><source src="/video/{v}.mp4" type="video/mp4"></video><figcaption>Vídeo publicado no Instagram do Agora Praça</figcaption></figure>'''


def escrever(caminho, conteudo):
    p = os.path.join(RAIZ, caminho.strip("/"), "index.html") if not caminho.endswith(".html") else os.path.join(RAIZ, caminho.strip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(conteudo)


def pagina_noticia(n):
    ed = EDITORIAS[n["editoria"]]
    topo, og, extra = "", "/og.png", ""
    if n.get("capa"):
        topo = f'<figure class="hero"><img src="/{n["capa"]}" alt="{e(n.get("alt", ""))}" width="1200" height="675"><figcaption>{e(n.get("capa_credito", ""))}</figcaption></figure>'
        og = "/" + n["capa"]
        if n.get("foto") and n["foto"] != n["capa"] and n.get("foto_retrato"):
            extra += f'<figure class="cardimg"><img src="/{n["foto"]}" alt="{e(n.get("alt", ""))}" loading="lazy"><figcaption>{e(n.get("credito", ""))}</figcaption></figure>'
    elif n.get("foto"):
        topo = f'<figure class="hero"><img src="/{n["foto"]}" alt="" width="1200" height="675"><figcaption>{e(n["credito"])}</figcaption></figure>'
        og = "/" + n["foto"]
    # O que foi publicado no Instagram entra no corpo da matéria, nunca como capa.
    if n.get("video"):
        extra += video_tag(n["video"])
    if n.get("card"):
        extra += f'<figure class="cardimg"><img src="/{n["card"]}" alt="Card publicado no Instagram com o resumo desta notícia" loading="lazy" width="1080" height="1350"><figcaption>Card publicado no Instagram em {data_curta(n["data"])}</figcaption></figure>'
    if n.get("carrossel"):
        imgs = "".join(f'<img src="/{c}" alt="Tela {i+1} do carrossel publicado no Instagram" loading="lazy" width="1080" height="1350">' for i, c in enumerate(n["carrossel"]))
        extra += f'<figure class="carrossel"><div class="car-trilho">{imgs}</div><figcaption>Carrossel publicado no Instagram. Deslize para ver as {len(n["carrossel"])} telas.</figcaption></figure>'
    pv = ""
    if n.get("para_voce"):
        r, t = n["para_voce"]
        pv = f'<aside class="pv pv-{ed["cor"]}"><b>{e(r)}</b><p>{e(t)}</p></aside>'
    fontes = "".join(
        f'<li><a href="{e(u)}" rel="noopener">{e(nm)}</a></li>' if u else f"<li>{e(nm)}</li>" for nm, u in n["fontes"]
    )
    atual = f' · Atualizado em {data_curta(n["atualizado"])}' if n.get("atualizado") else ""
    rel = [x for x in NOTICIAS if x["slug"] != n["slug"] and x["editoria"] == n["editoria"]][:3]
    if len(rel) < 3:
        rel += [x for x in NOTICIAS if x["slug"] != n["slug"] and x not in rel][: 3 - len(rel)]
    url = SITE + url_noticia(n)
    corpo = f'''<article class="materia"><div class="wrap estreita">
<div class="chap"><a href="/{n["editoria"]}/">{chapeu(n)}</a>{f'<span class="sub">{e(n["chapeu"])}</span>' if n.get("chapeu") else ""}</div>
<h1>{e(n["titulo"])}</h1>
<p class="linha-fina">{e(n["linha_fina"])}</p>
<div class="assina"><strong>Da Redação</strong><span><time datetime="{n["data"]}">{data_longa(n["data"])}</time>{atual}</span></div>
</div>
<div class="wrap media">{topo}</div>
<div class="wrap estreita corpo">
{pv}
{paragrafos(n["texto"])}
{extra}
{f'<p class="obs">{e(n["credito_extra"])}</p>' if n.get("credito_extra") else ""}
<section class="fontes"><h2>Fontes</h2><ul>{fontes}</ul><p class="obs">Viu um erro? Escreva para <a href="mailto:contato@agorapraca.com.br">contato@agorapraca.com.br</a>. Toda correção fica registrada na página de <a href="/sobre/#correcoes">correções</a>.</p></section>
<div class="share"><a class="btn" href="https://www.instagram.com/agorapraca/" rel="noopener">Seguir no Instagram</a></div>
</div>
</article>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>Leia também</h2></div><div class="grade">{"".join(item(x) for x in rel)}</div></div></section>
'''
    escrever(url_noticia(n), cabeca(n["titulo"], n["linha_fina"], url_noticia(n), og, "article") + corpo + RODAPE)


def lista_pp(x):
    out = []
    for i, (t, s) in enumerate(x["itens"]):
        txt = f'<a href="{url_noticia(POR_SLUG[s])}">{e(t)}</a>' if s else e(t)
        out.append(f'<li><span class="n">{i+1}</span><span>{txt}</span></li>')
    return "".join(out)


def bloco_pp(x, curto=False):
    itens = lista_pp(x)
    return f'''<div class="pp"><div class="pp-head"><span class="pp-tit">Primeira Página</span><span class="pp-data">{data_longa(x["data"])}</span></div>
<ol class="pp-lista">{itens}</ol>
<a class="pp-mais" href="{url_edicao(x)}">Ver a edição completa →</a></div>'''


def pagina_edicao(x):
    telas = "".join(f'<img src="/{x["pasta"]}/{i:02d}.jpg" alt="Tela {i} da Primeira Página" loading="lazy" width="1080" height="1350">' for i in range(1, x["telas"] + 1))
    insta = f'<details class="pp-insta"><summary>Ver como saiu no Instagram</summary><div class="telas">{telas}</div></details>'
    m = x.get("materia")
    if m:
        idx = "".join(f'<li><span class="n">{i+1}</span><span><a href="#s{i+1}">{e(sec["titulo"])}</a></span></li>' for i, sec in enumerate(m["secoes"]))
        secs = ""
        for i, sec in enumerate(m["secoes"]):
            ps = "".join(f"<p>{e(t)}</p>" for t in sec["texto"])
            mais = f'<p class="pp-link"><a href="{url_noticia(POR_SLUG[sec["slug"]])}">Leia a matéria completa →</a></p>' if sec.get("slug") else ""
            fts = " · ".join(f'<a href="{e(u)}" rel="noopener">{e(nm)}</a>' for nm, u in sec.get("fontes", []))
            fts = f'<p class="obs">Fontes: {fts}</p>' if fts else ""
            secs += f'<section class="pp-sec" id="s{i+1}"><span class="kicker kicker-red">{e(sec["chapeu"])}</span><h2>{e(sec["titulo"])}</h2>{ps}{mais}{fts}</section>'
        ag = ""
        if m.get("agenda"):
            rows = "".join(f'<li><b>{e(d)}</b><span>{e(t)}</span></li>' for d, t in m["agenda"])
            ag = f'<section class="pp-sec" id="agenda"><span class="kicker kicker-red">Agenda</span><h2>A semana</h2><ul class="pp-agenda">{rows}</ul></section>'
        corpo = f'''<div class="wrap estreita materia">
<div class="chap"><span class="kicker kicker-red">Primeira Página</span><span class="sub">Edição das 7h</span></div>
<h1>O resumo de {data_longa(x["data"])}</h1>
<p class="linha-fina">{e(m["abertura"])}</p>
<h2 class="h2-telas">Nesta edição</h2>
<ol class="pp-lista pp-lista-g">{idx}</ol>
{secs}{ag}
{insta}
</div>'''
    else:
        itens = lista_pp(x)
        corpo = f'''<div class="wrap estreita materia">
<div class="chap"><span class="kicker kicker-red">Primeira Página</span><span class="sub">Edição das 7h</span></div>
<h1>O resumo de {data_longa(x["data"])}</h1>
<p class="linha-fina">Toda manhã, o que você precisa saber para começar o dia, em poucos minutos.</p>
<ol class="pp-lista pp-lista-g">{itens}</ol>
<p class="obs">{e(x["fonte"])}</p>
{insta}
</div>'''
    escrever(url_edicao(x), cabeca(f"Primeira Página de {data_curta(x['data'])}", x["itens"][0][0], url_edicao(x), f"/{x['pasta']}/01.jpg") + corpo + RODAPE)


def pagina_home():
    lead, lados = NOTICIAS[0], NOTICIAS[1:3]
    resto = NOTICIAS[3:]
    comvid = [n for n in NOTICIAS if n.get("video")][:3]
    vids = "".join(
        f'<a class="vid" href="{url_noticia(n)}"><img src="/video/{n["video"]}.jpg" alt="" loading="lazy"><span>{e(VIDEOS.get(n["video"], n["titulo"]))}</span></a>'
        for n in comvid
    )
    eds = ""
    for k, v in EDITORIAS.items():
        ns = [n for n in NOTICIAS if n["editoria"] == k][:4]
        lis = "".join(f'<li><a href="{url_noticia(n)}">{e(n["titulo"])}</a></li>' for n in ns)
        eds += f'<div class="edcol"><a href="/{k}/" class="bar bar-{v["cor"]}">{e(v["nome"])}</a><ul>{lis}</ul><a class="mais" href="/{k}/">Tudo de {e(v["nome"])} →</a></div>'
    corpo = f'''<section class="topo"><div class="wrap topo-g">
<div class="topo-lead">{item(lead, grande=True)}</div>
<div class="topo-lado">{"".join(item(n) for n in lados)}</div>
<div class="topo-pp">{bloco_pp(EDICOES[0])}</div>
</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>Últimas</h2></div><div class="grade">{"".join(item(n) for n in resto)}</div></div></section>
<section class="sec sec-escura"><div class="wrap"><div class="sec-head"><h2>Vídeos</h2><span>Explicado em menos de um minuto</span></div><div class="vids">{vids}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>Editorias</h2></div><div class="eds">{eds}</div></div></section>
<section class="sec"><div class="wrap manifesto"><span class="kicker kicker-red">Quem somos</span><h2>É hora de voltar para a praça</h2><p>O Agora Praça nasce para devolver o debate público às pessoas, com informação confiável e fácil de entender. Cada fato passa por checagem antes de chegar até você.</p><a class="btn" href="/sobre/">Conheça nossos princípios</a></div></section>
'''
    escrever("/", cabeca(None, "A praça é de todo mundo. Do lado do interesse público, com fato checado.", "/", completo=True) + corpo + RODAPE)


def pagina_editoria(k):
    v = EDITORIAS[k]
    ns = [n for n in NOTICIAS if n["editoria"] == k]
    corpo = f'''<section class="sec"><div class="wrap"><div class="sec-head"><h1 class="h1-sec">{e(v["nome"])}</h1><span>{e(v["desc"])}</span></div>
<div class="grade">{"".join(item(n) for n in ns) or '<p>Ainda não há publicações nesta editoria.</p>'}</div></div></section>'''
    escrever(f"/{k}/", cabeca(v["nome"], v["desc"], f"/{k}/") + corpo + RODAPE)


def pagina_pp_indice():
    blocos = "".join(f'<div class="pp-idx">{bloco_pp(x)}</div>' for x in EDICOES)
    corpo = f'''<section class="sec"><div class="wrap"><div class="sec-head"><h1 class="h1-sec">Primeira Página</h1><span>O resumo do dia, toda manhã às 7h</span></div><div class="pps">{blocos}</div></div></section>'''
    escrever("/primeira-pagina/", cabeca("Primeira Página", "O resumo do dia, toda manhã às 7h.", "/primeira-pagina/") + corpo + RODAPE)


def pagina_sobre():
    corpo = open(os.path.join(RAIZ, "_src", "sobre.html"), encoding="utf-8").read()
    escrever("/sobre/", cabeca("Quem somos", "Manifesto, princípios editoriais, correções e expediente do Agora Praça.", "/sobre/") + corpo + RODAPE)


def pagina_frases():
    itens = ""
    for f in sorted(FRASES, key=lambda x: x["data"], reverse=True):
        fontes = " · ".join(f'<a href="{e(u)}" rel="noopener">{e(nm)}</a>' if u else e(nm) for nm, u in f["fontes"])
        itens += f'''<article class="frase" id="{f["slug"]}"><img src="/{f["img"]}" alt="{e(f["frase"])}" loading="lazy" width="1080" height="1350">
<div class="frase-txt"><time datetime="{f["data"]}">{data_curta(f["data"])}</time><h2>{e(f["frase"])}</h2><p>{e(f["explica"])}</p><p class="obs">Fontes: {fontes}</p></div></article>'''
    corpo = f'''<section class="sec"><div class="wrap"><div class="sec-head"><h1 class="h1-sec">Em uma linha</h1><span>Uma frase para guardar, e de onde ela vem</span></div><div class="frases">{itens}</div></div></section>'''
    escrever("/em-uma-linha/", cabeca("Em uma linha", "Frases curtas sobre seus direitos e o poder público, cada uma com a explicação e a fonte.", "/em-uma-linha/") + corpo + RODAPE)


def pagina_404():
    corpo = '''<section class="sec"><div class="wrap estreita"><h1 class="h1-sec">Página não encontrada</h1><p>O endereço pode ter mudado. Volte para a <a href="/">página inicial</a>.</p></div></section>'''
    p = os.path.join(RAIZ, "404.html")
    open(p, "w", encoding="utf-8").write(cabeca("Página não encontrada", "Página não encontrada.", "/404") + corpo + RODAPE)


def sitemap():
    urls = ["/", "/sobre/", "/primeira-pagina/", "/em-uma-linha/"] + [f"/{k}/" for k in EDITORIAS] + [url_noticia(n) for n in NOTICIAS] + [url_edicao(x) for x in EDICOES]
    xs = "".join(f"<url><loc>{SITE}{u}</loc></url>" for u in urls)
    open(os.path.join(RAIZ, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{xs}</urlset>\n')
    open(os.path.join(RAIZ, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    for n in NOTICIAS:
        pagina_noticia(n)
    for x in EDICOES:
        pagina_edicao(x)
    for k in EDITORIAS:
        pagina_editoria(k)
    pagina_home()
    pagina_pp_indice()
    pagina_sobre()
    pagina_frases()
    pagina_404()
    sitemap()
    shutil.copy(os.path.join(RAIZ, "_src", "estilo.css"), os.path.join(RAIZ, "estilo.css"))
    print("ok:", len(NOTICIAS), "notícias,", len(EDICOES), "edições")
