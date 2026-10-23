# Agora Praça

Site do Agora Praça (agorapraca.com.br), publicado pelo Cloudflare Pages a partir da branch `main`.

- Conteúdo: `_src/conteudo.py` (notícias, Primeira Página, vídeos)
- Gerar o site: `python3 _src/build.py` na raiz
- Estilo: `_src/estilo.css` · página Quem somos: `_src/sobre.html`
- Imagens em `img/`, vídeos em `video/`, telas da Primeira Página em `pp/`

## Capas do site

Toda matéria tem capa própria do site, em 16:9 (1200x675), separada da capa do Reel e do card do Instagram. O Reel, o card e o carrossel entram no corpo da matéria, nunca como capa.

- Campos em `conteudo.py`: `"capa"` (caminho da imagem) e `"capa_credito"`.
- Foto: recorte 16:9 sem texto por cima. Arte de dados: desenhada para 16:9, com todo o texto dentro da imagem.
- Gerador: `python3 _src/capas.py [slug]` cria as capas definidas em `CAPAS` dentro de `img/capa/`.
- O `build.py` para com erro se alguma matéria publicada estiver sem capa. Só em caso raro, `"sem_capa": "motivo"` dispensa.
