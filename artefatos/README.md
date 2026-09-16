# Artefatos exportados do claude.ai

Cópias de leitura das páginas publicadas no claude.ai durante o projeto.
**A fonte de verdade de cada página é o URL, não o arquivo.** O arquivo aqui
serve para consulta, busca e histórico; para atualizar uma página, republique
**no mesmo URL** (parâmetro `url` da ferramenta Artifact). Republicar sem
`url` cria um segundo artefato com o mesmo título.

Exportação feita em 16/09/2026 com a ferramenta Artifact (`action: read`),
copiando o arquivo gravado em disco sem reescrever. A coluna "versão" é o
identificador de versão que o serviço devolveu na leitura.

## Versões finais (fonte de verdade no URL)

| Título | URL | Versão lida | Arquivo |
|---|---|---|---|
| Posto de Dublin 2026 (painel-índice, 17 arquivos) | https://claude.ai/artifact/4VRSyeuFu8nSm1TFJ7xWXC | 1789410025-07c2 | `posto-de-dublin-2026/index.html` |
| Prancheta pelas Seções | https://claude.ai/artifact/Szv5egKpHy3umh4udAybvr | 1789567370-1e62 | `prancheta-pelas-secoes.html` |
| Sinalização RDS Hall 2 | https://claude.ai/artifact/BcT5yzxRkSaUsbbHQQgjWF | 1789503624-5cec | `sinalizacao-rds-hall2.html` |
| Filas sem o Ring 3 (3 arquivos) | https://claude.ai/artifact/P3x8Hy3j8gnEYKdwwfCSTe | 1789475839-3b72 | `filas-sem-o-ring3/index.html` |
| Prancheta do Hall 2 | https://claude.ai/artifact/XTd4LLmW9Fyh3UDLtjoc2T | 1789406076-9671 | `prancheta-do-hall2.html` |
| Fitas no piso do Hall 2 | https://claude.ai/artifact/T77jvrJmLK1HxTT4qFRAGY | 1789181821-dec8 | `fitas-no-piso-do-hall2.html` |
| Barreiras do Hall 2 | https://claude.ai/artifact/V1mFt2njTvD2VzntDK6Crt | 1789137041-b22f | `barreiras-do-hall2.html` |
| Simulador do Hall 2 | https://claude.ai/artifact/X1MEdK3CosTCZH9486JesV | 1788870698-77fa | `simulador-do-hall2.html` |
| Rota do Eleitor RDS | https://claude.ai/artifact/1PQjgzstbiNorfJgagXhB5 | 1788713592-113f | `rota-do-eleitor-rds.html` |
| Planta-base do Hall 2 | https://claude.ai/artifact/9xHx31DwUUtEtgpsbxZHxf | 1788713595-eb82 | `planta-base-do-hall2.html` |

As duas páginas que **têm gerador neste repositório** não estão nesta pasta,
porque a versão final delas é a que os scripts produzem em `saidas/`:

| Título | URL | Gerador | Saída |
|---|---|---|---|
| Montagem do Ring 3 | https://claude.ai/artifact/FcQs4H7fM3RcBxmyFywazV | `scripts/ring3_montagem.py` + `scripts/gera_pagina_ring3.py` | `saidas/ring3_montagem.html` |
| Urnas de Dublin | https://claude.ai/artifact/8YfHrRWvw7j8rZEZ2PgKiv | `scripts/mapa_agregacoes.py` + `scripts/gera_pagina.py` | `saidas/dublin_agregacoes.html` |

## O painel "Posto de Dublin 2026"

É um artefato de 17 arquivos: a página-índice mais cópias das outras peças em
`pecas/`, `ferramentas/` e `historico/`, ligadas por caminhos relativos. A
pasta `posto-de-dublin-2026/` reproduz essa árvore inteira, então
`posto-de-dublin-2026/index.html` abre e navega localmente.

Atenção a duas coisas:

- As cópias dentro do painel são **instantâneos de 15/09/2026**, não os URLs
  vivos. Onde o artefato avulso foi atualizado depois (Prancheta pelas
  Seções, Sinalização, Filas sem o Ring 3), o arquivo avulso nesta pasta é
  mais novo que a cópia dentro de `posto-de-dublin-2026/pecas/`.
- Quatro peças **só existem dentro do painel**, sem artefato avulso:
  `pecas/decisoes.html` (registro de decisões D1 a D9),
  `pecas/instrucoes.html` (instruções de fluxo para a equipe),
  `pecas/plano_filas.html` (plano de distribuição de filas) e
  `ferramentas/ring3.html` ("Ring 3 ao vivo"). São as únicas cópias.

## Histórico (superadas por versão posterior)

Decisão sobre os três "provavelmente superados" do manifesto, tomada abrindo
cada um e comparando com o painel:

| Título | URL | Por que é histórico | Arquivo |
|---|---|---|---|
| As 28 Mesas nas Paredes (31/08) | https://claude.ai/artifact/3AtxC7Qro6LvLwob25nK3d | O próprio painel a arquiva em `historico/`; byte a byte igual à cópia de lá. Superada pela Prancheta do Hall 2. | `historico/as-28-mesas-nas-paredes-2026-08-31.html` |
| Fluxo do Posto de Dublin (28/08) | https://claude.ai/artifact/QTbGi2qDxYy76BnSXmxJSD | Idem: o painel a arquiva como `historico/fluxo_ilhas`. Superada pela Rota do Eleitor e pelas Fitas no piso. | `historico/fluxo-do-posto-de-dublin-2026-08-28.html` |
| Quantas mesas cabem no Hall 2 (03/09) | https://claude.ai/artifact/Jci5uV3yxscF1Fw2teRfdX | O painel carrega uma versão **mais nova** em `pecas/mesas.html` (numeração por MRV, decisão de 06/09). O URL avulso ficou na versão anterior. | `historico/quantas-mesas-cabem-no-hall2-2026-09-03.html` |

**"Ring 3, cenários de fila"** (https://claude.ai/artifact/QrLDxdnNexR5x5iPjLi51Y)
não foi exportado como avulso: está superado pela Montagem do Ring 3, e a
única cópia que vale guardar é a que o painel já carrega em
`posto-de-dublin-2026/pecas/ring3_quatro.html`.

**"Teses Temáticas"** é de outro projeto e não foi migrado.

## O que não veio junto

Os scripts que geraram estas páginas (`scripts/salao.py`, `scripts/ring3.py`,
`scripts/decisoes.py`, `scripts/tres_portas.py`, `scripts/comparecimento.py`
e outros citados nos rodapés) **nunca foram commitados** em nenhum
repositório e não são recuperáveis. Estas páginas são, portanto, o único
registro do que eles calcularam. Não as regenere: não há com quê.
