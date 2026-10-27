# Molde dos Reels

`agora.py` monta qualquer Reel do Agora Praça no padrão: 1080x1920, 30 fps, tarja, crédito, @agorapraca, assinatura e trilha.

Precisa de Python 3 com Playwright (Chromium), ffmpeg, numpy e scipy, e das fontes desta pasta instaladas.

```python
import sys; sys.path.insert(0, "identidade/03-moldes-video")
from agora import *

T = tarja("ciencia", "clima")
CENAS = [
    dict(tipo="foto", arquivo="foto.jpg", cor=True, mov="in", batidas=4,
         html=topo(T, "Foto: Nome/Agência Brasil") + numero("50 mil", "manchete", "subtítulo")),
    dict(tipo="anim", batidas=5,
         html=topo(T, "Fonte: ...", fundo="preto") + "<!-- HTML com uma função JS draw(t) -->"),
    dict(tipo="fixa", batidas=2, html=assinatura("Fonte 1, Fonte 2")),
]
montar(CENAS, "saida.mp4", "pasta-das-imagens")
```

- `tipo`: `foto`, `video` (com `inicio` em segundos), `anim` (HTML com `draw(t)`, renderizado quadro a quadro) ou `fixa`.
- `cor=False` deixa a imagem em preto e branco.
- `mov`: `in`, `out`, `dir` ou `esq`.
- `batidas`: duração da cena em batidas de 0,83 s.
