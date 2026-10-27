# Agora Praça · Pasta de identidade

Esta pasta guarda tudo o que um chat novo precisa para trabalhar no Agora Praça sem o Felipe reenviar arquivos. Leia nesta ordem:

1. `04-documentos/atualizacoes.md`: as decisões tomadas depois de 16/10/2026. Onde houver conflito com os documentos mais antigos, vale este arquivo.
2. `04-documentos/regras-da-casa.md`: princípios, apuração, correção, linguagem, imagens, cuidados jurídicos, política comercial e eleitoral, uso de IA.
3. `04-documentos/briefing-2026-10-16.md`: quem é o Felipe, como ele quer que a IA trabalhe, marca, voz e infraestrutura (versão de 16/10).

## O que tem aqui

| Pasta | Conteúdo |
| --- | --- |
| `01-marca/` | Logo oficial (clara e negativa), ícone de perfil e favicon, em SVG e PNG |
| `02-templates/` | Modelos oficiais de 16/10 (card, capa de Reels, carrossel, card de Correção), como referência visual |
| `03-moldes-video/` | Molde único dos Reels em código (`agora.py`), trilha (`trilha.py`) e as fontes Archivo e Libre Caslon Text |
| `04-documentos/` | Regras da casa, briefing e atualizações |

Os arquivos de marca são oficiais. Só mudam com aprovação explícita do Felipe.

## O site

- Repositório: `felipejablonski-jpg/agora-praca-site`, branch `main`, publicado pelo Cloudflare Pages em agorapraca.com.br.
- Conteúdo em `_src/conteudo.py`; gerar com `python3 _src/build.py`. Detalhes no `README.md` da raiz.
- O site é a casa mãe: toda notícia tem matéria completa lá, com ou sem Reel.

## Links de trabalho

- Manual visual (documento editável): https://claude.ai/artifact/42NQ7rKAnSa1cDDCRyyVoG
- Quadro de design (logo e templates): https://claude.ai/artifact/3HNYZJ675ZAd8w3wpyhUHq
- Regras da casa, versão editável: https://claude.ai/artifact/XqfxEjf3KDWrXdJm6pysyi

Atenção: tudo nesta pasta fica público em agorapraca.com.br/identidade/. Não guarde aqui senha, dado pessoal nem fonte sigilosa.
