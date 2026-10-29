#!/usr/bin/env python3
"""Mini doc "4 dias, 3 versões": a saída de Flávio Bolsonaro, de domingo (25) a quinta (29/10/2026).

Sem narração: texto na tela, carimbos, gráficos e mapa por cima de fotos e vídeos.
Cada quadro é desenhado no Chromium (Playwright) e enviado direto ao ffmpeg.
Fatos: os mesmos das matérias publicadas no site (fontes na assinatura e no README da pasta).
Uso: python3 _src/doc/flavio_4dias.py  ->  video/doc-flavio-4-dias.mp4 e .jpg
"""
import os, sys, json, subprocess, shutil
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
MOLDES = os.path.join(RAIZ, "identidade", "03-moldes-video")
sys.path.insert(0, MOLDES)
from agora import SELO, R, RD, K, G  # noqa: E402

FOTOS = os.path.join(RAIZ, "img", "fotos")
MIDIA = os.path.join(RAIZ, "_src", "carrosseis", "midia")
A = "/mnt/user-data/attachments/31be2719-c7d8-5b33-91a5-c035937f37a4"
TMP = "/tmp/_doc_flavio"
MAPA = os.path.join(AQUI, "mapa-rota.json")
FPS = 30
TOTAL = 85.0
ASS = 82.5  # início da assinatura

# trechos de vídeo: nome -> (arquivo, início, duração, filtro até 1080x1920)
VIDEOS = {
    "stories": (os.path.join(RAIZ, "_src/reels/clips/flavio-stories-2026-10-28.mp4"), 6.0, 3.7, "scale=-2:1920,crop=1080:1920"),
    "stories2": (os.path.join(RAIZ, "_src/reels/clips/flavio-stories-2026-10-28.mp4"), 9.0, 7.6, "scale=-2:1920,crop=1080:1920"),
    "flavio": (f"{A}/f56fa19c-ScreenRecording_10-28-2026_18-31-42_1.mov", 2.0, 6.6, "crop=518:922:1072:19,scale=1080:1920"),
    "trump1": (f"{A}/383f6751-ScreenRecording_10-28-2026_18-30-24_1.mov", 1.0, 4.1, "crop=658:1170:842:0,scale=1080:1920"),
    "trump2": (f"{A}/383f6751-ScreenRecording_10-28-2026_18-30-24_1.mov", 7.5, 3.6, "crop=658:1170:842:0,scale=1080:1920"),
    "bregman": (f"{A}/5c05dd39-ScreenRecording_10-28-2026_20-51-24_1.mov", 0.5, 3.6, "crop=658:1170:756:0,scale=1080:1920"),
}

ABR22 = "Foto de arquivo: Marcelo Camargo/Agência Brasil, 2022"

# ---------- cenas ----------
# bg: ("foto", arquivo, escala0, escala1, foco_x, foco_y, escurecer, pb) | ("video", nome, escurecer) | ("preto",) | ("bandeira",)
CENAS = [
    dict(t0=0.0, t1=3.6, dia=-1, bg=("video", "stories", .3), cred="Vídeo: stories de Flávio Bolsonaro, 28/10 (reprodução)"),
    dict(t0=3.6, t1=6.0, dia=-1, bg=("foto", "flavio-senado-lula-marques-abr-2025.jpg", 1.0, 1.08, .72, .4, .8, False), cred="Foto de arquivo: Lula Marques/Agência Brasil, 2025"),
    dict(t0=6.0, t1=11.0, dia=0, bg=("foto", "urnas-preparacao-sp.jpg", 1.05, 1.2, .4, .5, .6, False), cred="Foto: Paulo Pinto/Agência Brasil"),
    dict(t0=11.0, t1=16.0, dia=0, bg=("foto", "justica-estatua-stf.jpg", 1.2, 1.05, .5, .35, .55, True), cred="Foto de arquivo: Marcello Casal Jr/Agência Brasil, 2009"),
    dict(t0=16.0, t1=22.5, dia=1, bg=("video", "flavio", .35), cred="Imagem de arquivo: canal de Flávio no YouTube (reprodução). A fala é do vídeo de segunda"),
    dict(t0=22.5, t1=26.5, dia=1, bg=("video", "trump1", .35), cred="Imagem de arquivo: USA Today, no YouTube (reprodução)"),
    dict(t0=26.5, t1=30.0, dia=2, bg=("foto", "flavio-senado-lula-marques-abr-2025.jpg", 1.05, 1.18, .72, .4, .45, False), cred="Foto de arquivo: Lula Marques/Agência Brasil, 2025"),
    dict(t0=30.0, t1=35.0, dia=2, bg=("foto", "flavio-telefone-agencia-senado.jpg", 1.15, 1.02, .62, .4, .5, True), cred="Foto de arquivo: Beto Barata/Agência Senado"),
    dict(t0=35.0, t1=48.0, dia=2, bg=("preto",), cred="Mapa: Agora Praça · Migrações (Argentina) e Folha de S.Paulo · horários de Brasília"),
    dict(t0=48.0, t1=52.0, dia=3, bg=("foto", "aviao-aeroporto-ponte.jpg", 1.08, 1.22, .3, .5, .55, False), cred=ABR22),
    dict(t0=52.0, t1=59.5, dia=3, bg=("video", "stories2", .72), cred="Vídeo: stories de Flávio Bolsonaro, 28/10 (reprodução) · carta: reprodução"),
    dict(t0=59.5, t1=64.0, dia=3, bg=("foto", "urna-treinamento-tre-sp.jpg", 1.05, 1.16, .3, .5, .74, False), cred="Foto: Paulo Pinto/Agência Brasil · dados do TSE"),
    dict(t0=64.0, t1=67.5, dia=3, bg=("foto", "urnas-lacre-tre-df.jpg", 1.05, 1.18, .5, .5, .72, False), cred="Foto: Joédson Alves/Agência Brasil · dados do TSE, via CNN Brasil"),
    dict(t0=67.5, t1=71.0, dia=3, bg=("video", "trump2", .35), cred="Imagem de arquivo: USA Today, no YouTube (reprodução)"),
    dict(t0=71.0, t1=74.5, dia=3, bg=("video", "bregman", .35), cred="Arquivo de 14/10, sobre outro tema: canal do PTS no YouTube (reprodução)"),
    dict(t0=74.5, t1=82.5, dia=4, bg=("bandeira",), cred="Ilustração: Agora Praça"),
    dict(t0=82.5, t1=85.0, dia=-2, bg=("preto",), cred=""),
]
CORTES = [c["t0"] for c in CENAS[1:]]
MAPA_T0 = 35.0
QUEDAS = [37.2, 46.0, 56.6]  # carimbos das versões que caíram
TROCA = 55.4  # "verdadeiro presidente eleito" vira "líder"

# ---------- elementos de texto: (início, fim, html, tipo) ----------
V = '<span style="color:#FF3B30">{}</span>'


def cab(chapeu, txt, fs=74, top=360):
    return (f'<div style="position:absolute;left:80px;right:110px;top:{top}px">'
            f'<div class="chip">{chapeu}</div><div class="serif sh" style="font-size:{fs}px;line-height:1.08;margin-top:22px">{txt}</div></div>')


def baixo(txt, rotulo="", sub="", fs=58, top=1240):
    r = f'<div class="rot">{rotulo}</div>' if rotulo else ""
    s = f'<div class="sub sh">{sub}</div>' if sub else ""
    return (f'<div style="position:absolute;left:80px;right:110px;top:{top}px">{r}'
            f'<div class="serif sh" style="font-size:{fs}px;line-height:1.13;margin-top:12px">{txt}</div>{s}</div>')


def carimbo(txt, top=820, rot=-9, fs=86, sub=""):
    s = f'<div style="font-size:30px;letter-spacing:.14em;margin-top:6px">{sub}</div>' if sub else ""
    return (f'<div class="stamp" style="top:{top}px;--r:{rot}deg"><div style="font-size:{fs}px;line-height:1">{txt}</div>{s}</div>')


ITENS = [
    # gancho: o personagem e o arco inteiro numa frase
    (0.15, 3.6, baixo("Domingo, Flávio Bolsonaro perdeu a eleição.", fs=70, top=1050), "up"),
    (1.5, 3.6, baixo("Quarta, já estava em Miami " + V.format("se dizendo presidente."), fs=70, top=1340), "up"),
    (3.7, 6.0, '<div style="position:absolute;left:80px;right:80px;top:700px"><div class="serif sh" style="font-size:150px;line-height:1">4 dias,</div>'
     f'<div class="serif sh" style="font-size:150px;line-height:1;color:{RD}">3 versões</div>'
     '<div class="sub sh" style="font-size:44px;margin-top:40px">Como ele saiu do Brasil proibido pela Justiça, dia a dia</div></div>', "up"),
    # domingo
    (6.1, 11.0, cab("DOMINGO, 25", "O TSE declara Lula reeleito"), "up"),
    (6.3, 11.0, '<div id="barras" class="g"></div>', "fade"),
    (11.1, 16.0, cab("DOMINGO, 25, À NOITE", "Moraes proíbe Flávio de deixar o país", fs=78), "up"),
    (11.6, 16.0, '<div class="papel" id="papel"><div class="p-t">STF · DECISÃO DE ALEXANDRE DE MORAES</div>'
     '<div class="p-l">Entregar os passaportes comum e diplomático à Polícia Federal</div>'
     '<div class="p-l">Não deixar o país</div><div class="p-l">Investigação sobre suspeita de lavagem de dinheiro</div></div>', "left"),
    (13.4, 16.0, carimbo("24 H", top=1380, rot=-12, fs=150, sub="PRAZO PARA OS PASSAPORTES"), "stamp"),
    # segunda
    (16.1, 22.5, cab("SEGUNDA, 26", "Flávio grava um vídeo", fs=70), "up"),
    (16.6, 19.6, baixo("“Fui intimado a entregar os meus passaportes e também estou proibido de deixar o país”", "FLÁVIO BOLSONARO, EM VÍDEO", fs=56), "up"),
    (19.6, 22.5, baixo("No mesmo vídeo, diz que " + V.format("nunca pensou em deixar o Brasil"), "GUARDE ESTA FRASE", fs=62), "up"),
    (22.6, 26.5, cab("SEGUNDA, 26", "Trump fala da eleição brasileira", fs=70), "up"),
    (22.9, 26.5, baixo("A eleição “pareceu mais uma eleição fraudada”", "DONALD TRUMP, A JORNALISTAS", fs=62), "up"),
    (24.2, 26.5, carimbo("SEM PROVA", top=780, rot=8, fs=110), "stamp"),
    # terça
    (26.6, 30.0, cab("TERÇA, 27", "Vence o prazo", fs=80), "up"),
    (26.8, 30.0, '<div id="relogio" class="g"></div>', "fade"),
    (28.0, 30.0, baixo("11h: os passaportes não são entregues à Polícia Federal", fs=60, top=1290), "up"),
    (30.1, 35.0, cab("TERÇA, 27", "O que se dizia durante o dia", fs=70), "up"),
    (30.6, 35.0, '<div class="aspas" style="top:700px"><div class="rot">ROGÉRIO MARINHO, ALIADO, DE MANHÃ</div><div class="serif" style="font-size:96px;margin-top:10px">“Não saiu”</div></div>', "left"),
    (32.3, 35.0, '<div class="aspas" style="top:1060px"><div class="rot">GOVERNO DA ARGENTINA, AO G1</div><div class="serif" style="font-size:60px;margin-top:10px;line-height:1.12">“Não há registro de entrada de Flávio no país”</div></div>', "left"),
    (35.0, 48.0, '<div id="mapa" class="g"></div>', "fade"),
    (35.1, 48.0, cab("TERÇA, 27, À NOITE", "A rota", fs=74), "up"),
    (37.2, 39.6, carimbo("VERSÃO 1<br>CAIU", top=820, rot=-8, fs=96, sub="ELE TINHA DITO QUE NUNCA PENSOU EM SAIR"), "stamp"),
    (46.0, 48.0, carimbo("VERSÃO 2<br>CAIU", top=980, rot=7, fs=96, sub="DE MADRUGADA, A ARGENTINA CONFIRMA A ENTRADA"), "stamp"),
    # quarta
    (48.1, 52.0, cab("QUARTA, 28", "Entra nos EUA com uma autorização temporária", fs=70), "up"),
    (48.6, 52.0, '<div class="visto" id="visto"><div style="font-size:30px;letter-spacing:.2em">ENTRADA NOS EUA · 28/10/2026</div>'
     '<div class="serif" style="font-size:84px;margin:14px 0 6px">PAROLE</div><div style="font-size:34px">autorização humanitária temporária</div>'
     '<div style="font-size:44px;font-weight:800;margin-top:18px">VÁLIDA ATÉ 27/10/2027</div></div>', "stamp2"),
    (49.4, 52.0, baixo("Segundo registros da alfândega americana obtidos pelo Metrópoles", fs=46, top=1430), "up"),
    (52.1, 59.5, cab("QUARTA, 28, À TARDE", "Ele divulga uma carta", fs=70), "up"),
    (52.3, 59.5, '<div id="carta" class="g"></div>', "fade"),
    (52.8, 59.5, '<div style="position:absolute;left:80px;right:110px;top:1270px"><div class="serif sh" style="font-size:66px;line-height:1.12">'
     'Se declara “o <span id="troca"><span id="velho" style="color:#FF3B30">verdadeiro presidente eleito</span></span> do Brasil”</div>'
     '<div class="sub sh" id="depois" style="opacity:0">Horas depois, troca por “líder do Brasil”. A acusação de fraude, sem prova, continua</div></div>', "up"),
    (56.6, 59.5, carimbo("VERSÃO 3<br>CAIU", top=520, rot=-7, fs=96), "stamp"),
    (59.6, 64.0, cab("A CARTA DIZ", "Que os 10 milhões de votos que Lula ganhou no 2º turno são uma “impossibilidade matemática”", fs=58), "up"),
    (59.8, 64.0, '<div id="soma" class="g"></div>', "fade"),
    (62.4, 64.0, carimbo("A CONTA FECHA", top=1530, rot=-5, fs=74), "stamp"),
    (64.1, 67.5, cab("A CARTA TAMBÉM", "Ataca a decisão do STF que estendeu a votação até as 19h", fs=62), "up"),
    (64.3, 67.5, '<div style="position:absolute;left:80px;right:110px;top:1000px"><div class="serif sh" style="font-size:220px;line-height:.9;color:#FF3B30"><span id="c34">0</span> mil</div>'
     '<div class="serif sh" style="font-size:56px;line-height:1.12;margin-top:24px">votos depois das 17h, segundo o TSE</div>'
     '<div class="sub sh">Lula venceu por 4,4 milhões</div></div>', "up"),
    (65.8, 67.5, carimbo("NÃO MUDA", top=1530, rot=6, fs=80), "stamp"),
    (67.6, 71.0, cab("QUARTA, 28", "Trump é perguntado sobre Flávio", fs=70), "up"),
    (67.8, 71.0, baixo("“Não vou me envolver”", "DONALD TRUMP", "“Mas sei que demos a ele autorização para entrar no país”", fs=80), "up"),
    (71.1, 74.5, cab("QUARTA, 28", "Na Argentina, a oposição cobra Milei", fs=70), "up"),
    (71.3, 74.5, baixo("Deputados falam em “absoluta cumplicidade” do governo na passagem de Flávio", "", "É acusação deles, sem prova divulgada", fs=56), "up"),
    # quinta
    (74.6, 82.5, cab("QUINTA, 29", "O que ainda não se sabe", fs=88), "up"),
    (75.5, 82.5, '<div class="perg" style="top:700px"><span>1</span>Ele vai pedir asilo?</div>', "left"),
    (76.8, 82.5, '<div class="perg" style="top:860px"><span>2</span>Quem pagou o voo?</div>', "left"),
    (78.1, 82.5, '<div class="perg" style="top:1020px"><span>3</span>O governo argentino ajudou?</div>', "left"),
    (79.7, 82.5, baixo("Uma certeza: Lula toma posse em " + V.format("5 de janeiro"), "", "Aliados anunciam uma entrevista de Flávio em Miami", fs=64, top=1260), "up"),
    (82.5, 85.0, f'<div style="position:absolute;inset:0;background:{K}"></div><div style="position:absolute;left:0;right:0;top:660px;display:flex;flex-direction:column;align-items:center">{SELO.format(w=170)}'
     '<div class="serif" style="font-size:96px;margin-top:44px">Agora Praça</div><div style="font-size:40px;color:#C9C5BD;margin-top:18px">A praça é de todo mundo.</div>'
     '<div style="font-size:26px;color:#8d8983;margin-top:70px;text-align:center;line-height:1.5;padding:0 90px">Fontes: TSE, CNN Brasil, Metrópoles, Folha de S.Paulo, g1, Exame,<br>Migrações (Argentina), Ámbito e Infobae<br>Reportagens completas em agorapraca.com.br</div></div>', "fade"),
]

CSS = f'''*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:{K};color:#fff;font-family:Archivo}}
.serif{{font-family:'Libre Caslon Text';font-weight:700}} .sh{{text-shadow:0 2px 20px rgba(0,0,0,.75)}}
#bg{{position:absolute;inset:0;overflow:hidden}} #bg img{{position:absolute;left:0;top:0;transform-origin:0 0}}
#esc{{position:absolute;inset:0}} .it{{position:absolute;inset:0;will-change:transform,opacity}} .g{{position:absolute;inset:0}}
.chip{{display:inline-block;font-weight:800;font-size:30px;letter-spacing:.16em;color:{RD}}}
.rot{{font-weight:800;font-size:28px;letter-spacing:.13em;color:{RD}}}
.sub{{font-size:40px;line-height:1.3;color:{G};margin-top:22px}}
.stamp{{position:absolute;left:50%;transform:translateX(-50%) rotate(var(--r));border:9px solid {RD};color:{RD};padding:18px 34px;
  font-weight:800;text-align:center;letter-spacing:.04em;background:rgba(20,20,20,.35);border-radius:10px;white-space:nowrap;
  box-shadow:0 0 0 4px rgba(255,59,48,.25) inset;mix-blend-mode:normal}}
.papel{{position:absolute;left:110px;right:110px;top:760px;background:#F2EFE9;color:{K};padding:44px 50px;box-shadow:0 30px 80px rgba(0,0,0,.6);transform:rotate(-2deg)}}
.p-t{{font-weight:800;font-size:26px;letter-spacing:.14em;color:#8a867e;margin-bottom:24px}}
.p-l{{font-family:'Libre Caslon Text';font-weight:700;font-size:44px;line-height:1.2;padding:18px 0;border-top:2px solid #d9d4ca}}
.aspas{{position:absolute;left:80px;right:110px;background:rgba(20,20,20,.82);border-left:10px solid {RD};padding:30px 40px}}
.visto{{position:absolute;left:150px;right:150px;top:780px;border:8px solid #6fa8ff;color:#9cc3ff;border-radius:18px;padding:34px;text-align:center;
  background:rgba(10,20,40,.55);transform:rotate(-6deg)}}
.perg{{position:absolute;left:80px;right:110px;font-family:'Libre Caslon Text';font-weight:700;font-size:70px;line-height:1.1;display:flex;align-items:center;gap:30px}}
.perg span{{font-family:Archivo;font-weight:800;font-size:44px;width:84px;height:84px;flex:none;border:5px solid {RD};color:{RD};border-radius:50%;display:flex;align-items:center;justify-content:center}}
#hud{{position:absolute;left:0;right:0;top:0;height:330px}}
'''

HTML = '''<!doctype html><html><head><meta charset="utf-8"><style>__CSS__</style></head><body>
<div id="bg"></div><div id="esc"></div><div id="itens"></div><div id="hud"></div>
<script>
const CENAS=__CENAS__, ITENS=__ITENS__, MAPA=__MAPA__, FPS=__FPS__, ASS=__ASS__;
const R="#D2232A", RD="#FF3B30", G="#C9C5BD";
const cl=(x)=>Math.max(0,Math.min(1,x)), ease=(x)=>1-Math.pow(1-cl(x),3), lerp=(a,b,x)=>a+(b-a)*x;
const DIAS=["DOM 25","SEG 26","TER 27","QUA 28","QUI 29"];
const bg=document.getElementById('bg'), esc=document.getElementById('esc'), itensEl=document.getElementById('itens'), hud=document.getElementById('hud');
// itens
const nodes=ITENS.map(([a,b,html,tipo])=>{const d=document.createElement('div');d.className='it';d.innerHTML=html;d.style.opacity=0;itensEl.appendChild(d);return {a,b,tipo,d};});
// hud
hud.innerHTML=`<div style="position:absolute;left:80px;right:110px;top:150px;display:flex;align-items:center">
<div style="background:${R};font-weight:800;font-size:26px;letter-spacing:.16em;padding:11px 16px">POLÍTICA · ELEIÇÕES 2026</div>
<div style="margin-left:auto;display:flex;align-items:center;gap:12px;font-weight:800;font-size:25px;letter-spacing:.12em">__SELO__@AGORAPRACA</div></div>
<div id="linha" style="position:absolute;left:80px;right:110px;top:226px;height:40px"></div>
<div id="cred" class="sh" style="position:absolute;left:80px;right:110px;top:306px;font-size:22px;font-weight:600;color:rgba(255,255,255,.82)"></div>
<div id="cont" style="position:absolute;right:110px;top:340px;font-weight:800;font-size:22px;letter-spacing:.12em;color:#FF3B30;text-align:right"></div>`;
const linha=document.getElementById('linha'), cred=document.getElementById('cred');
function desenhaLinha(dia,t){
  let h='<div style="position:absolute;left:0;right:0;top:19px;height:3px;background:rgba(255,255,255,.25)"></div>';
  DIAS.forEach((d,i)=>{const x=i*25; const at=i===dia, pas=dia>i;
    h+=`<div style="position:absolute;left:${x}%;top:0;transform:translateX(${i===0?'0':i===4?'-100%':'-50%'});text-align:${i===0?'left':i===4?'right':'center'}">
    <div style="width:16px;height:16px;border-radius:50%;margin:${i===0?'12px 0 0':i===4?'12px 0 0 auto':'12px auto 0'};background:${at?RD:pas?'#fff':'rgba(255,255,255,.35)'};box-shadow:${at?'0 0 0 6px rgba(255,59,48,.35)':'none'}"></div>
    <div style="font-weight:800;font-size:20px;letter-spacing:.1em;margin-top:8px;color:${at?'#fff':pas?'rgba(255,255,255,.75)':'rgba(255,255,255,.4)'}">${d}</div></div>`;});
  if(dia>=0){h+=`<div style="position:absolute;left:0;top:19px;height:3px;width:${dia*25}%;background:#fff"></div>`;}
  linha.innerHTML=h;
}
// versões que caíram
const QUEDAS=__QUEDAS__;
function contador(t){const n=QUEDAS.filter(q=>t>=q).length; return n;}
// fundo
let bgAtual='';
function poeFundo(c,lt,dur){
  const b=c.bg; const k=c.t0+'';
  if(b[0]==='foto'){
    if(bgAtual!==k){bg.innerHTML=`<img src="__FOTOS__/${b[1]}" style="filter:${b[7]?'grayscale(1) contrast(1.1)':'none'}">`; bgAtual=k;}
    const im=bg.firstChild; if(!im.naturalWidth) return im.decode().then(()=>poeFundo(c,lt,dur));
    const s0=Math.max(1080/im.naturalWidth,1920/im.naturalHeight);
    const s=s0*lerp(b[2],b[3],cl(lt/dur)); const w=im.naturalWidth*s, h=im.naturalHeight*s;
    const x=-(w-1080)*b[4], y=-(h-1920)*b[5];
    im.style.width=w+'px'; im.style.height=h+'px'; im.style.transform=`translate(${x}px,${y}px)`;
    esc.style.background=`linear-gradient(to bottom,rgba(20,20,20,.88) 0,rgba(20,20,20,${b[6]}) 560px,rgba(20,20,20,${b[6]}) 1100px,rgba(20,20,20,.92) 1500px,rgba(20,20,20,.95) 1920px)`;
  } else if(b[0]==='video'){
    const i=Math.min(Math.floor(lt*FPS)+1, 9999);
    const src=`__TMP__/v_${b[1]}/${String(i).padStart(4,'0')}.jpg`;
    bg.innerHTML=`<img src="${src}" style="width:1080px;height:1920px">`; bgAtual='';
    esc.style.background=`linear-gradient(to bottom,rgba(20,20,20,.9) 0,rgba(20,20,20,${b[2]}) 600px,rgba(20,20,20,${b[2]}) 1050px,rgba(20,20,20,.9) 1450px,rgba(20,20,20,.95) 1920px)`;
    return bg.firstChild.decode().catch(()=>{});
  } else if(b[0]==='bandeira'){
    bg.innerHTML=bandeira(lt); bgAtual='';
    esc.style.background='linear-gradient(to bottom,rgba(20,20,20,.9) 0,rgba(20,20,20,.62) 600px,rgba(20,20,20,.7) 1200px,rgba(20,20,20,.95) 1920px)';
  } else { bg.innerHTML=''; bgAtual=''; esc.style.background='#141414'; }
}
function bandeira(t){
  const W=1500,H=1100,x0=-200,y0=520; let s=`<svg width="1080" height="1920"><g>`;
  const onda=(x)=>Math.sin(x/180 - t*2.2)*38 + Math.sin(x/90 - t*3.1)*10;
  for(let i=0;i<13;i++){ let p=''; const h=H/13, ya=y0+i*h;
    for(let x=0;x<=W;x+=30){p+=(x?'L':'M')+(x0+x)+','+(ya+onda(x)+x*0.05);}
    for(let x=W;x>=0;x-=30){p+='L'+(x0+x)+','+(ya+h+onda(x)+x*0.05);}
    s+=`<path d="${p}Z" fill="${i%2? '#e8e4dc':'#b22234'}" opacity=".95"/>`;}
  const cw=W*0.42, ch=H*7/13; let p='';
  for(let x=0;x<=cw;x+=30){p+=(x?'L':'M')+(x0+x)+','+(y0+onda(x)+x*0.05);}
  for(let x=cw;x>=0;x-=30){p+='L'+(x0+x)+','+(y0+ch+onda(x)+x*0.05);}
  s+=`<path d="${p}Z" fill="#3c3b6e"/>`;
  for(let r=0;r<9;r++)for(let c=0;c<(r%2?5:6);c++){const x=(c+(r%2?1:0.5))*cw/6.2, y=(r+0.7)*ch/9.4; s+=`<circle cx="${x0+x}" cy="${y0+y+onda(x)+x*0.05}" r="9" fill="#fff"/>`;}
  return s+'</g></svg>';
}
// gráficos
function barras(lt){ const p=ease((lt-0.3)/1.4);
  const l=(51.79*p).toFixed(2).replace('.',','), f=(48.21*p).toFixed(2).replace('.',',');
  return `<div style="position:absolute;left:80px;right:110px;top:1060px">
  <div style="display:flex;justify-content:space-between;font-weight:800;font-size:34px"><span>LULA</span><span class="serif" style="font-size:64px;color:${RD}">${l}%</span></div>
  <div style="height:34px;background:rgba(255,255,255,.15);margin:10px 0 40px"><div style="height:100%;width:${51.79*p}%;background:${RD}"></div></div>
  <div style="display:flex;justify-content:space-between;font-weight:800;font-size:34px"><span>FLÁVIO</span><span class="serif" style="font-size:64px">${f}%</span></div>
  <div style="height:34px;background:rgba(255,255,255,.15);margin-top:10px"><div style="height:100%;width:${48.21*p}%;background:#fff"></div></div>
  <div class="sub" style="font-size:32px">Votos válidos no segundo turno · TSE</div></div>`;}
function queda(lt){ const p=ease((lt-0.2)/1.0); const y1=lerp(0,520,p); const pct=(13.88*p).toFixed(2).replace('.',',');
  return `<svg width="1080" height="1920" style="position:absolute;left:0;top:0">
  <line x1="120" y1="760" x2="960" y2="760" stroke="rgba(255,255,255,.25)" stroke-width="3" stroke-dasharray="10 10"/>
  <polyline points="120,760 520,760 ${lerp(520,900,p)},${760+y1}" fill="none" stroke="${RD}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="${lerp(520,900,p)}" cy="${760+y1}" r="20" fill="${RD}"/>
  <text x="120" y="735" fill="rgba(255,255,255,.7)" font-family="Archivo" font-weight="800" font-size="28" letter-spacing="3">SEXTA (23)</text></svg>
  <div style="position:absolute;left:80px;right:110px;top:1340px"><div class="serif sh" style="font-size:170px;line-height:.9;color:${RD}">-${pct}%</div>
  <div class="serif sh" style="font-size:52px;line-height:1.12;margin-top:20px">Ibovespa na segunda, a maior queda desde 2020</div></div>`;}
function relogio(lt){ const h=lerp(8,11,ease((lt-0.1)/1.6)); const ah=(h%12)*30, am=(h%1)*360;
  return `<svg width="1080" height="1920" style="position:absolute;left:0;top:0"><g transform="translate(540,900)">
  <circle r="250" fill="rgba(20,20,20,.75)" stroke="#fff" stroke-width="10"/>
  ${Array.from({length:12},(_,i)=>`<line x1="0" y1="-215" x2="0" y2="${i%3?-195:-175}" stroke="#fff" stroke-width="${i%3?5:10}" transform="rotate(${i*30})"/>`).join('')}
  <line x1="0" y1="20" x2="0" y2="-130" stroke="#fff" stroke-width="16" stroke-linecap="round" transform="rotate(${ah})"/>
  <line x1="0" y1="26" x2="0" y2="-195" stroke="${RD}" stroke-width="9" stroke-linecap="round" transform="rotate(${am})"/>
  <circle r="16" fill="${RD}"/></g></svg>`;}
function mapa(lt){ // lt: tempo desde 40.0
  const sc=0.86, ox=(1080-1080*0.86)/2, oy=500, P=MAPA.pts;
  const pt=(k)=>[P[k][0]*sc+ox, P[k][1]*sc+oy];
  let s=`<svg width="1080" height="1920" style="position:absolute;left:0;top:0"><g opacity="${ease(lt/0.8)}">`;
  for(const c of MAPA.paises){ const dest=c.id==='ar'||c.id==='ec'||c.id==='us'||c.id==='br';
    s+=`<path d="${c.d}" transform="translate(${ox},${oy}) scale(${sc})" vector-effect="non-scaling-stroke" fill="${c.id==='br'?'#3a3733':dest?'#2c2a27':'#211f1d'}" stroke="${dest?'rgba(255,255,255,.45)':'rgba(255,255,255,.14)'}" stroke-width="${dest?2:1}"/>`;}
  for(const [n,[x,y]] of Object.entries(MAPA.rot)) s+=`<text x="${x*sc+ox}" y="${y*sc+oy}" fill="rgba(255,255,255,.42)" font-family="Archivo" font-weight="800" font-size="24" letter-spacing="5" text-anchor="middle">${n}</text>`;
  const A=pt('ponte'), B=pt('guayaquil'), C=pt('miami');
  const curva=(p,q,k)=>{const mx=(p[0]+q[0])/2, my=(p[1]+q[1])/2; const dx=q[0]-p[0], dy=q[1]-p[1]; return [mx-dy*k, my+dx*k];};
  const c1=curva(A,B,-0.22), c2=curva(B,C,-0.18);
  const bez=(p,c,q,u)=>[ (1-u)*(1-u)*p[0]+2*(1-u)*u*c[0]+u*u*q[0], (1-u)*(1-u)*p[1]+2*(1-u)*u*c[1]+u*u*q[1] ];
  const u1=ease((lt-5.0)/2.6), u2=ease((lt-8.0)/2.6);
  const trilha=(p,c,q,u)=>{let d=`M${p[0]},${p[1]}`; for(let i=1;i<=40;i++){const v=u*i/40; const r=bez(p,c,q,v); d+=`L${r[0]},${r[1]}`;} return d;};
  if(u1>0) s+=`<path d="${trilha(A,c1,B,u1)}" fill="none" stroke="${RD}" stroke-width="7" stroke-dasharray="18 12"/>`;
  if(u2>0) s+=`<path d="${trilha(B,c2,C,u2)}" fill="none" stroke="${RD}" stroke-width="7" stroke-dasharray="18 12"/>`;
  const pulso=(p,t0)=>{ if(lt<t0) return ''; const k=((lt-t0)%1.2)/1.2; return `<circle cx="${p[0]}" cy="${p[1]}" r="${14+k*46}" fill="none" stroke="${RD}" stroke-width="5" opacity="${1-k}"/><circle cx="${p[0]}" cy="${p[1]}" r="15" fill="${RD}" stroke="#fff" stroke-width="4"/>`;};
  s+=pulso(A,0.8)+pulso(B,7.6)+pulso(C,10.6);
  // avião
  let av=null, ang=0;
  if(lt>=5.0 && lt<7.6){const r=bez(A,c1,B,u1), r2=bez(A,c1,B,Math.min(1,u1+0.02)); av=r; ang=Math.atan2(r2[1]-r[1],r2[0]-r[0]);}
  else if(lt>=8.0 && lt<10.6){const r=bez(B,c2,C,u2), r2=bez(B,c2,C,Math.min(1,u2+0.02)); av=r; ang=Math.atan2(r2[1]-r[1],r2[0]-r[0]);}
  if(av) s+=`<g transform="translate(${av[0]},${av[1]}) rotate(${ang*180/Math.PI+90}) scale(1.5)"><path d="M0,-30 L5,-10 L28,4 L28,10 L5,4 L4,20 L12,27 L12,31 L0,27 L-12,31 L-12,27 L-4,20 L-5,4 L-28,10 L-28,4 L-5,-10 Z" fill="#fff" stroke="#141414" stroke-width="2"/></g>`;
  s+='</g></svg>';
  // legendas
  const leg=(t0,txt,x,y,al,t1=99)=>{ if(lt<t0||lt>=t1) return ''; const o=Math.min(ease((lt-t0)/0.4), cl((t1-lt)/0.25));
    return `<div style="position:absolute;${al==='r'?'right':'left'}:${x}px;top:${y}px;opacity:${o};transform:translateY(${(1-o)*20}px);max-width:520px;text-align:${al==='r'?'right':'left'}">${txt}</div>`;};
  const caixa=(h,t)=>`<div style="background:rgba(20,20,20,.88);border-left:7px solid ${RD};padding:16px 22px"><div class="serif" style="font-size:52px;color:${RD}">${h}</div><div style="font-size:30px;line-height:1.25;margin-top:4px">${t}</div></div>`;
  s+=leg(1.0, caixa('22h50','Entra na Argentina pela ponte Tancredo Neves, em Misiones'), 1080-A[0]-40, A[1]+50, 'r', 3.4);
  s+=leg(3.4, caixa('23h30','Decola de Puerto Iguazú num voo privado, com destino declarado ao Equador'), 380, A[1]+50, 'l', 7.6);
  s+=leg(7.6, caixa('Escala','Guayaquil, no Equador, já na quarta (28)'), B[0]+40, B[1]-20, 'l', 10.6);
  s+=leg(10.6, caixa('10h23','Pousa em Miami, segundo a Folha'), C[0]+40, C[1]-10, 'l');
  return s;
}
function carta(lt){ const p=ease(lt/0.9);
  const pag=(n,x,y,r,d)=>{const q=ease((lt-d)/0.7); return `<img src="__MIDIA__/flavio-carta-p${n}.png" style="position:absolute;left:${x}px;top:${y+(1-q)*300}px;width:470px;transform:rotate(${r*q}deg);opacity:${q};box-shadow:0 30px 80px rgba(0,0,0,.7)">`;};
  return pag(3,520,560,8,0.4)+pag(2,330,540,2,0.2)+pag(1,110,560,-5,0);}
function soma(lt){ const a=ease((lt-0.3)/1.0), b=ease((lt-1.4)/1.0); const W=880;
  const seg=(w,c,txt,num)=>`<div style="width:${w}px;height:140px;background:${c};display:flex;flex-direction:column;justify-content:center;padding:0 18px;overflow:hidden;white-space:normal;color:${c==='#fff'?'#141414':'#fff'}"><div class="serif" style="font-size:46px">${num}</div><div style="font-size:19px;line-height:1.15;font-weight:800;letter-spacing:.04em">${txt}</div></div>`;
  const tot=14.1;
  return `<div style="position:absolute;left:80px;top:760px;width:${W}px">
  <div class="rot">O QUE LULA E FLÁVIO GANHARAM DO 1º PARA O 2º TURNO</div>
  <div style="display:flex;margin-top:14px;opacity:${a}">${seg(W*10.4/tot*a,'#FF3B30','LULA','+10,4 mi')}${seg(W*3.7/tot*a,'#fff','FLÁVIO','+3,7 mi')}</div>
  <div class="rot" style="margin-top:60px">DE ONDE VIERAM</div>
  <div style="display:flex;margin-top:14px;opacity:${b}">${seg(W*9.3/tot*b,'#8d8983','OUTROS 10 CANDIDATOS NO 1º TURNO','9,3 mi')}${seg(W*4.8/tot*b,'#5a5753','VOTOS VÁLIDOS A MAIS NO 2º TURNO','4,8 mi')}</div>
  <div class="serif sh" style="font-size:58px;margin-top:50px;opacity:${b}">As duas contas dão 14,1 milhões</div></div>`;}
// animações dos itens
function anima(n,t){ const {a,b,tipo,d}=n;
  if(t<a||t>=b){d.style.opacity=0; return;}
  const i=(t-a), o=(b-t); let op=Math.min(1, i/0.35, o/0.22); let tr='';
  if(tipo==='up') tr=`translateY(${(1-ease(i/0.45))*40}px)`;
  if(tipo==='left') tr=`translateX(${(1-ease(i/0.45))*-80}px)`;
  if(tipo==='stamp'||tipo==='stamp2'){ const k=cl(i/0.2); const sc=lerp(2.4,1,ease(k)); op=Math.min(k*1.4,1,o/0.2);
    const tremor=i<0.45&&i>0.2? Math.sin(i*90)*6*(0.45-i)/0.25:0; tr=`translate(${tremor}px,${tremor}px) scale(${sc})`; }
  d.style.opacity=op; d.style.transform=tr;
  // conteúdo dinâmico
  const q=d.querySelector('#barras'); if(q) q.innerHTML=barras(i);
  const c=d.querySelector('#c34'); if(c) c.textContent=Math.round(34*ease((i-0.2)/1.2));
  const z=d.querySelector('#queda'); if(z) z.innerHTML=queda(i);
  const r=d.querySelector('#relogio'); if(r) r.innerHTML=relogio(i);
  const m=d.querySelector('#mapa'); if(m) m.innerHTML=mapa(t-__MAPA_T0__);
  const k=d.querySelector('#carta'); if(k) k.innerHTML=carta(i);
  const s=d.querySelector('#soma'); if(s) s.innerHTML=soma(i);
  const v=d.querySelector('#velho'); if(v){ const tt=t-__TROCA__;
    if(tt>0){ const p=ease(tt/0.5); v.style.textDecoration='line-through'; v.style.textDecorationThickness='7px'; v.style.textDecorationColor='#fff'; v.style.opacity=lerp(1,.55,p);
      let nv=document.getElementById('novo'); if(!nv){nv=document.createElement('span');nv.id='novo';nv.style.color='#FF3B30';nv.textContent=' líder';v.after(nv);} nv.style.opacity=p;
      d.querySelector('#depois').style.opacity=ease((tt-0.4)/0.5);} }
}
window.draw=async function(t){
  const c=CENAS.find(x=>t>=x.t0&&t<x.t1)||CENAS[CENAS.length-1];
  const lt=t-c.t0, dur=c.t1-c.t0;
  const pr=poeFundo(c,lt,dur);
  hud.style.opacity = t>=ASS?0:1;
  desenhaLinha(c.dia,t); cred.textContent=c.cred;
  const n=contador(t);
  document.getElementById('cont').innerHTML = (n>0&&t<74.5)? `VERSÕES QUE CAÍRAM: ${n} DE 3` : '';
  nodes.forEach(x=>anima(x,t));
  if(pr) await pr;
  const imgs=[...document.images].filter(i=>!i.complete); await Promise.all(imgs.map(i=>i.decode().catch(()=>{})));
  return n;
};
</script></body></html>'''


def run(c):
    subprocess.run(c, shell=True, check=True)


def prepara_videos():
    for nome, (arq, ini, dur, filtro) in VIDEOS.items():
        d = os.path.join(TMP, f"v_{nome}")
        os.makedirs(d, exist_ok=True)
        run(f'ffmpeg -v error -y -ss {ini} -t {dur} -i "{arq}" -an -vf "fps={FPS},{filtro},setsar=1,eq=contrast=1.04:saturation=0.92" -q:v 3 {d}/%04d.jpg')


def main():
    so_quadros = [float(x) for x in sys.argv[1:]]  # ex.: python3 flavio_4dias.py 1 9 45  -> só prévias
    os.makedirs(TMP, exist_ok=True)
    if not os.path.isdir(os.path.join(TMP, "v_bregman")):
        prepara_videos()
    mapa = json.load(open(MAPA))
    html = (HTML.replace("__CSS__", CSS).replace("__CENAS__", json.dumps(CENAS)).replace("__ITENS__", json.dumps(ITENS))
            .replace("__MAPA__", json.dumps(mapa)).replace("__FPS__", str(FPS)).replace("__ASS__", str(ASS))
            .replace("__SELO__", SELO.format(w=38)).replace("__FOTOS__", "file://" + FOTOS).replace("__MIDIA__", "file://" + MIDIA)
            .replace("__TMP__", "file://" + TMP).replace("__QUEDAS__", json.dumps(QUEDAS)).replace("__MAPA_T0__", str(MAPA_T0)).replace("__TROCA__", str(TROCA)))
    pag = os.path.join(TMP, "doc.html")
    open(pag, "w", encoding="utf-8").write(html)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + pag)
        pg.wait_for_timeout(500)
        if so_quadros:
            for t in so_quadros:
                pg.evaluate("t => draw(t)", t)
                pg.screenshot(path=os.path.join(TMP, f"previa_{t:05.1f}.jpg"), type="jpeg", quality=80)
            b.close(); print("prévias em", TMP); return
        mudo = os.path.join(TMP, "mudo.mp4")
        ff = subprocess.Popen(f"ffmpeg -v error -y -f image2pipe -framerate {FPS} -c:v mjpeg -i - -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p {mudo}",
                              shell=True, stdin=subprocess.PIPE)
        n = int(TOTAL * FPS)
        for i in range(n):
            pg.evaluate("t => draw(t)", i / FPS)
            ff.stdin.write(pg.screenshot(type="jpeg", quality=90))
            if i % 300 == 0:
                print(f"quadro {i}/{n}", flush=True)
        ff.stdin.close(); ff.wait()
        b.close()
    run(f"python3 {MOLDES}/trilha.py {TMP}/trilha.wav {TOTAL:.3f} '{json.dumps(CORTES)}'")
    saida = os.path.join(RAIZ, "video", "doc-flavio-4-dias.mp4")
    run(f'ffmpeg -v error -y -i {mudo} -i {TMP}/trilha.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af "volume=-3dB,loudnorm=I=-18:TP=-1.5" -t {TOTAL:.2f} -movflags +faststart {saida}')
    run(f"ffmpeg -v error -y -ss 2.4 -i {saida} -frames:v 1 -q:v 3 {saida.replace('.mp4', '.jpg')}")
    print("ok:", saida)


if __name__ == "__main__":
    main()
