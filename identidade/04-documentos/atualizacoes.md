# Agora Praça · Atualizações depois de 16/10/2026

Decisões tomadas pelo Felipe depois do briefing e das Regras da casa de 16/10. Em caso de conflito, vale este arquivo. Última revisão: 27/10/2026.

## Contas e infraestrutura

- Instagram: @agorapraca (o @agora.praca do LEIA-ME antigo ficou para trás).
- Site: publicado pelo Cloudflare Pages a partir do repositório `agora-praca-site` no GitHub, branch `main`. O caminho antigo pelo Netlify não vale mais.

## Editorias

| Editoria | Cobre |
| --- | --- |
| Política | Votações, governo, eleições, Justiça Eleitoral, dinheiro público |
| Serviço | Benefícios, prazos, golpes, concursos, leis novas, segurança digital |
| Ciência | Meio ambiente, clima, saúde, endemias, pesquisas científicas e documentários |

Ciência substituiu Meio Ambiente em 22/10/2026, porque cobre o meio ambiente e vai além dele. O endereço antigo agorapraca.com.br/meio-ambiente/ redireciona para /ciencia/.

## Formatos

Prioridade: Reel, depois carrossel, depois card. Três moldes fixos:

| Molde | Quando usar |
| --- | --- |
| Reel de notícia | Quase toda notícia, de 12 a 20 segundos |
| Primeira Página | Só o resumo do dia, em carrossel vermelho |
| Agora Explica | Só vídeo explicativo com narração do Felipe, fundo creme e coreto 3D |

Saíram de uso: card com foto em cima e faixa vermelha embaixo, card claro só com texto e as frases "Em uma linha".

## Reel de notícia

- Imagem na faixa de cima (foto, vídeo, satélite ou gráfico), número grande em vermelho, manchete em Libre Caslon Text, assinatura no fim.
- Foto colorida ou em preto e branco, conforme a imagem pedir: cor quando ela informa (fogo, mapa, satélite, calor).
- Tarja vermelha no topo: EDITORIA · SUBTEMA (ex.: CIÊNCIA · CLIMA, SERVIÇO · MEI, POLÍTICA · ELEIÇÕES 2026).
- Cortes na batida de 72 BPM (0,83 s). Número ou manchete no primeiro segundo. Assinatura de no máximo 2 segundos.
- Gráfico sempre que houver número: barras que crescem, contadores, mapa que se acende.
- O molde em código está em `03-moldes-video/agora.py`.

## Imagens

- Pode: Agência Brasil, Agência Senado e Câmara com crédito; divulgação oficial; satélite e dados públicos (NASA, NOAA, Inpe); Pixabay, Unsplash e Pexels como "Imagem ilustrativa"; domínio público (CDC, NASA, Wikimedia Commons).
- Nunca: AFP, Reuters, Getty, imagem de TV.
- Foto de arquivo leva o ano no crédito. Gráfico e mapa próprios levam "Agora Praça".
- Capa do site: foto em 16:9 (1200x675), sem texto, separada da capa do Reel. Regras no `README.md` da raiz.

## Texto

- Manchete diz quem e quanto.
- Horário de Brasília primeiro, Mato Grosso entre parênteses.
- Toda legenda: o fato, o contexto, a ressalva quando houver, fontes, "Atualizado em" com a data e o fecho "Acompanhe o Agora Praça para entender os fatos por trás das manchetes."
- Roteiro de narração para teleprompter: só o texto, em parágrafos, com MAIÚSCULAS nas palavras de ênfase e "/" nas pausas.
- Em semana de eleição, mesma régua para os dois candidatos, só fatos.
- Toda informação vinda de pauta é ponto de partida: checar na fonte primária antes de publicar.

## Correções

- Erro nosso vai para a página de Correções do site (agorapraca.com.br/sobre/#correcoes) e ganha nota "Correção em [data]" no topo da matéria.
- "Atualização" fica para informação nova, quando não houve erro.
