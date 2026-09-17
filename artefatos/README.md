# Artefatos — cópia de leitura

34 páginas exportadas do claude.ai em 17/09/2026, **byte a byte**: cada uma foi
baixada pelo arquivo publicado, não reescrita pelo modelo. `CHECKSUMS.sha256`
prova isso, e `sha256sum -c CHECKSUMS.sha256` reconfere a qualquer momento.

**A fonte de verdade de cada página é o URL, não o arquivo.** O artefato continua
no claude.ai, com o URL e as permissões dele; o que está aqui é cópia congelada
da versão lida. Para atualizar um artefato, republique **no mesmo URL**
(parâmetro `url` da ferramenta `Artifact`). Republicar sem `url` cria um segundo
artefato com o mesmo título, e depois ninguém sabe qual é o bom.

## O panorama é um bundle, e é o centro

`Posto de Dublin 2026` não é uma página: são **17 arquivos**, em
`panorama/`. Ele carrega cópias próprias de quase tudo — e duas peças que **não
existem como artefato solto em lugar nenhum**:

| Arquivo | O que é |
|---|---|
| `panorama/pecas/decisoes.html` | o registro de decisões D1–D9: o que foi decidido em 13–14/09, o que está em aberto, e a matriz "se … então …" |
| `panorama/pecas/instrucoes.html` | as instruções de gerenciamento de fluxo para treinar os 26 voluntários e os 4 seguranças |

As versões dentro do bundle **não são as mesmas** das soltas. `pecas/rota.html`
tem 712 KB contra 64 KB do artefato `Rota do Eleitor RDS`; `pecas/barreiras.html`
tem 199 KB contra 61 KB do solto. Guardamos as duas: a solta tem URL próprio e
pode ter sido compartilhada.

## ⚠️ `panorama/pecas/instrucoes.html` está superado no ponto que mais importa

Ele é de **14/09** e distribui as mesas pelas zonas do **Ring 3** — A 3.642 /
B 4.215 / C 3.642, com cada entrada espalhada pelas três paredes. A decisão de
**15/09**, congelada em `congelado/`, abandonou o Ring 3 e deu **uma parede
inteira a cada entrada** (A 3.834 oeste / B 3.832 norte / C 3.833 leste).

A tabela "Zona · Porta · Mesas" da seção 3 e os gatilhos de escalada da seção 10
desse documento, portanto, **não valem**. É o documento que iria para a mão da
equipe no dia — regenerá-lo a partir do arranjo congelado é trabalho a fazer, e
depende dos geradores abaixo.

## Os geradores que faltam

Nenhuma destas páginas tem gerador neste repositório. Os rodapés dos próprios
artefatos nomeiam onze arquivos que nunca foram commitados:

| Nomeado em | Arquivo citado | O que produz |
|---|---|---|
| `planta-base-do-hall2.html` | `scripts/salao.py` | geometria do salão — "fonte única do projeto" |
| `planta-base-do-hall2.html` | `scripts/decisoes.py` | papéis das portas |
| `prancheta-pelas-secoes.html` | `scripts/gera_prancheta_por_secao.py` | **o arranjo congelado** |
| `prancheta-pelas-secoes.html` | `CONFERENCIA_PRANCHETA_2026-09-15.md` | conferência contra os PDFs do Cartório |
| `panorama/pecas/decisoes.html` | `scripts/decisoes_abertas.py` | o registro de decisões |
| `panorama/pecas/instrucoes.html` | `scripts/gera_instrucoes_fluxo.py` | as instruções de fluxo |
| `panorama/pecas/decisoes.html` | `scripts/simula_fluxo.py` | simulação de fila e de fechamento |
| `ring3-cenarios-de-fila.html` | `scripts/ring3.py` | cenários de fila do Ring 3 |
| vários | `docs/plano_filas.md` · `docs/decisoes_em_aberto.md` · `docs/instrucoes_fluxo.md` | os documentos derivados |
| `panorama/pecas/decisoes.html` | `DOCUMENTACAO_PROJETO.md` | documentação do projeto (§4.2, §9.7) |

Só `scripts/ring3_montagem.py`, `scripts/gera_pagina_ring3.py`,
`scripts/mapa_agregacoes.py` e `scripts/gera_pagina.py` sobreviveram, e estão em
`hamadmkalaf/eleicoes2026`. **Sem os onze acima, nenhuma destas páginas pode ser
regerada — só lida.** É por isso que o congelamento em `congelado/` existe.

## As duas reproduzíveis conferem

`montagem-do-ring3.html` e `urnas-de-dublin.html` foram comparadas com
`saidas/ring3_montagem.html` e `saidas/dublin_agregacoes.html` de
`hamadmkalaf/eleicoes2026`. A única diferença é o invólucro que o serviço de
publicação acrescenta (`<!doctype html>`, `<head>` com o CSS de base, `<body>`):
**todo o conteúdo gerado bate linha a linha**. Os dois geradores que sobraram
ainda produzem exatamente o que está publicado.

## As páginas

| Página | URL | Versão lida | Arquivo | Gerador |
|---|---|---|---|---|
| Posto de Dublin 2026 | [link](https://claude.ai/artifact/4VRSyeuFu8nSm1TFJ7xWXC) | 16/09/2026 | `panorama/` (17 arquivos) | perdido |
| Prancheta pelas Seções | [link](https://claude.ai/artifact/Szv5egKpHy3umh4udAybvr) | 16/09/2026 | `prancheta-pelas-secoes.html` | perdido — fonte do congelado |
| Montagem do Ring 3 | [link](https://claude.ai/artifact/FcQs4H7fM3RcBxmyFywazV) | 16/09/2026 | `montagem-do-ring3.html` | `scripts/ring3_montagem.py` + `gera_pagina_ring3.py` |
| Urnas de Dublin | [link](https://claude.ai/artifact/8YfHrRWvw7j8rZEZ2PgKiv) | 13/08/2026 | `urnas-de-dublin.html` | `scripts/mapa_agregacoes.py` + `gera_pagina.py` |
| Rota do Eleitor RDS | [link](https://claude.ai/artifact/1PQjgzstbiNorfJgagXhB5) | 16/09/2026 | `rota-do-eleitor-rds.html` | perdido |
| Filas sem o Ring 3 | [link](https://claude.ai/artifact/P3x8Hy3j8gnEYKdwwfCSTe) | 15/09/2026 | `filas-sem-o-ring3/` (+2 SVG) | perdido |
| Sinalização RDS Hall 2 | [link](https://claude.ai/artifact/BcT5yzxRkSaUsbbHQQgjWF) | 15/09/2026 | `sinalizacao-rds-hall2.html` | perdido |
| Prancheta do Hall 2 | [link](https://claude.ai/artifact/XTd4LLmW9Fyh3UDLtjoc2T) | 14/09/2026 | `prancheta-do-hall2.html` | perdido |
| Fitas no piso do Hall 2 | [link](https://claude.ai/artifact/T77jvrJmLK1HxTT4qFRAGY) | 12/09/2026 | `fitas-no-piso-do-hall2.html` | perdido |
| Barreiras do Hall 2 | [link](https://claude.ai/artifact/V1mFt2njTvD2VzntDK6Crt) | 11/09/2026 | `barreiras-do-hall2.html` | perdido |
| Ring 3, cenários de fila | [link](https://claude.ai/artifact/QrLDxdnNexR5x5iPjLi51Y) | 11/09/2026 | `ring3-cenarios-de-fila.html` | `scripts/ring3.py`, perdido |
| Simulador do Hall 2 | [link](https://claude.ai/artifact/X1MEdK3CosTCZH9486JesV) | 08/09/2026 | `simulador-do-hall2.html` | perdido |
| Planta-base do Hall 2 | [link](https://claude.ai/artifact/9xHx31DwUUtEtgpsbxZHxf) | 06/09/2026 | `planta-base-do-hall2.html` | `scripts/salao.py`, perdido |
| Quantas mesas cabem no Hall 2 | [link](https://claude.ai/artifact/Jci5uV3yxscF1Fw2teRfdX) | 03/09/2026 | `quantas-mesas-cabem-no-hall2.html` | perdido |
| As 28 Mesas nas Paredes | [link](https://claude.ai/artifact/3AtxC7Qro6LvLwob25nK3d) | 31/08/2026 | `as-28-mesas-nas-paredes.html` | perdido |
| Fluxo do Posto de Dublin | [link](https://claude.ai/artifact/QTbGi2qDxYy76BnSXmxJSD) | 28/08/2026 | `fluxo-do-posto-de-dublin.html` | perdido |

Os dois últimos também vivem dentro do bundle, em `panorama/historico/` — o
próprio panorama já os tratava como histórico, o que resolve a decisão 3.3 de
`TRANSFERENCIA.md` para eles: **migram como histórico, não como versão final**.

`Teses Temáticas — Arquivo de Pesquisa` não foi exportado: é de outro projeto.

## Verificar

```bash
cd artefatos && sha256sum -c CHECKSUMS.sha256
```
