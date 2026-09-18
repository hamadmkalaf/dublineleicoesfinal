# Registro da transferência — 18/09/2026

O que foi trazido de `hamadmkalaf/eleicoes2026` para cá, de qual branch, e para
onde. Executado a partir de dois roteiros: `transferencia_voluntarios_fluxo.md` e
`TRANSFERENCIA_SEPARADORES_FILA.md`.

Os dois roteiros cumpriram a sua função ao serem executados e **não foram
copiados**; este arquivo é o registro que fica no lugar deles.

---

## 1. Origens

| Tema | Branch de origem | PR | Commit no topo |
|---|---|---|---|
| Voluntários e fluxo | `claude/elegant-euler-jss6uv` | #24 (rascunho) | `73e15e6`, 18/09 |
| Separadores de fila | `claude/line-separator-layout-j61pe9` | #28 | `17d509e`, 18/09 |

O repositório de origem **não tem `main`**; a sua branch padrão é
`claude/dublin-electoral-sections-3odh1w`, uma branch de trabalho, e nenhuma das
duas branches acima foi mesclada nela. Clonar a branch padrão traz arquivos
desatualizados — foi por isso que cada arquivo abaixo foi tirado da sua branch
nominal, e não da padrão.

**Os insumos compartilhados pelos dois temas são byte a byte idênticos nas duas
branches** — verificado para `contexto_eleicoes_dublin_2026.md`, `PENDENCIAS`,
`saidas/dados.json` e `scripts/parse_dados.py`. Só o `README.md` difere, e ele foi
reescrito. Ou seja: não houve escolha a fazer entre versões concorrentes de nenhum
insumo.

## 2. Tema voluntários e fluxo

| Origem | Destino |
|---|---|
| `lista_postos.md` | `docs/voluntarios/lista_postos.md` |
| `contexto_voluntarios_fluxo.md` | `docs/voluntarios/contexto.md` |
| `plano_voluntarios_apoio.md` | `docs/voluntarios/dimensionamento.md` |
| `voluntarios_postos.html` | `mapa/voluntarios_postos.html` |
| `contexto_eleicoes_dublin_2026.md` | `docs/contexto_geral.md` |
| `saidas/dados.json` | `saidas/dados.json` |
| `scripts/zonas_balanceadas.py` | `scripts/zonas_balanceadas.py` |
| `PENDENCIAS` | `PENDENCIAS.md` |
| `CLAUDE.md`, seções *Geometria do local* e *Cenários de efetivo* | fundidas no `CLAUDE.md` daqui |

## 3. Tema separadores de fila

| Origem | Destino |
|---|---|
| `scripts/separadores_fila.py` | `scripts/separadores_fila.py` |
| `data/grupos_mesas.json` | `data/grupos_mesas.json` |
| `data/prancheta_hall2.json` | `data/prancheta_hall2.json` *(lido, nunca escrito)* |
| `data/decisoes.json` | `data/decisoes.json` *(lido, nunca escrito)* |
| `cenarios/paredes-abc-20260915.json` | `cenarios/paredes-abc-20260915.json` *(lido, nunca escrito)* |
| `plano_separadores_fila.md` | `docs/separadores/plano_separadores_fila.md` |
| `contexto_separadores_fila_hall2.md` | `docs/separadores/contexto.md` |
| `CONFERENCIA_PRANCHETA_2026-09-15.md` | `docs/separadores/CONFERENCIA_PRANCHETA_2026-09-15.md` |
| `saidas/separadores_definitivo.svg` · `.png` | `saidas/` |
| `saidas/separadores_detalhe.svg` · `.png` | `saidas/` |
| `saidas/separadores_opcao1.svg` · `opcao2.svg` | `saidas/` |
| `saidas/separadores_fila.json` | `saidas/` |

Os três arquivos marcados *(lido, nunca escrito)* **pertencem ao tema do arranjo do
Hall 2, não a este**. Vieram como estão. Editá-los à mão quebra as conferências.

`scripts/separadores_fila.py` resolve os seus caminhos a partir de `__file__`, e não
do diretório de trabalho — por isso a estrutura `scripts/` · `data/` · `cenarios/` ·
`saidas/` foi mantida na raiz, e o script **não precisou de nenhuma alteração**.

## 4. Reescritas de caminho aplicadas

Mover arquivos quebra referências no texto. Estas foram conferidas uma a uma:

| Trocado | Por | Onde |
|---|---|---|
| `lista_postos.md` | `docs/voluntarios/lista_postos.md` | contexto (3×), dimensionamento (4×) |
| `plano_voluntarios_apoio.md` | `docs/voluntarios/dimensionamento.md` | contexto |
| `voluntarios_postos.html` | `mapa/voluntarios_postos.html` | contexto, dimensionamento, lista_postos |
| `contexto_eleicoes_dublin_2026.md` | `docs/contexto_geral.md` | contexto, dimensionamento, `zonas_balanceadas.py` (docstring), CONFERENCIA |
| `PENDENCIAS` | `PENDENCIAS.md` | contexto, dimensionamento, CONFERENCIA |
| `contexto_separadores_fila_hall2.md` | `docs/separadores/contexto.md` | plano_separadores_fila |
| `CONFERENCIA_PRANCHETA_2026-09-15.md` | `docs/separadores/CONFERENCIA_...` | contexto dos separadores |

`mapa/voluntarios_postos.html` é autocontido: não referencia nenhum arquivo do
repositório e **não precisou de reescrita**. Confirmado por inspeção.

## 5. O que ficou para trás, e por quê

| Item | Por quê |
|---|---|
| Pipeline de agregação: `scripts/parse_dados.py`, `mapa_agregacoes.py`, `gera_pagina.py`, `data/raw/*.csv` | A agregação de seções não é tema deste repositório. **Consequência: `saidas/dados.json` é órfão aqui** — ninguém o regenera. Está dito no `README.md`. |
| PDFs de referência do Cartório, planilhas de proposta do TSE, `MRV - DUBLIN.pdf`, `RDS_Hall_2_Floorplan_(1).pdf`, `PLANO COM FLUXOS MELHORADO.png` | Fora dos dois temas. Os dois últimos são material histórico: descrevem duas entradas apenas, e são anteriores à planta de 16/09. |
| `saidas/separadores_opcao3.svg` / `.png` | Foi renomeado para `separadores_definitivo` quando a Opção 3 virou definitiva; o arquivo antigo é a geometria velha. |
| PNG das opções 1 e 2 | As alternativas descartadas bastam em SVG. |
| `saidas/sinalizacao_v2.json` | É do tema de sinalização. O que este repositório precisa dele já está extraído em `data/grupos_mesas.json`; o resto traz duas cores superadas e o `pos_banner` errado da parede leste (ver `mapa/README.md`). |
| `plano_filas_confinado_hall2.md` | Vive em `claude/filas-sem-ring-3-b9qvqi`, e não estava na lista de arquivos a levar de nenhum dos dois roteiros. É citado por dois documentos daqui, e as citações estão anotadas como não transferidas. |
| Os dois roteiros de transferência | Cumpriram a função ao serem executados. Este arquivo fica no lugar deles. |

`docs/separadores/CONFERENCIA_PRANCHETA_2026-09-15.md` **não** estava na lista dos
12 arquivos do roteiro dos separadores — é citado por ele como fonte. Foi trazido
porque é onde está o porquê de cada decisão de arranjo do Hall 2. Ele cita scripts e
documentos que ficaram na origem; o cabeçalho do arquivo declara quais, para que não
sejam confundidos com links quebrados.

## 6. Verificação de aceite — resultado

As duas baterias foram rodadas na origem (para estabelecer a linha de base) e aqui,
com resultado idêntico.

### Tema voluntários

| # | Critério | Resultado |
|---|---|---|
| 1 | `zonas_balanceadas.py` imprime 3.860 / 3.755 / 3.802, total 11.417, spread 2,8%, e "cada zona tem exatamente uma das três urnas grandes" | ✅ |
| 2 | As quatro colunas de `lista_postos.md` somam 9, 15, 24 e 43 postos (C4 tem mais 6 de reserva, fechando 49) | ✅ os 17 postos presentes; soma exata `[9, 15, 24, 43]`. **É a conferência que pega cópia parcial** |
| 3 | `mapa/voluntarios_postos.html` abre num navegador, os quatro botões trocam os números dentro dos círculos, e a coluna correspondente da tabela é destacada | ✅ **conferido em navegador** (Chromium headless). Em C1: P0=3, R3=1, A3=1, 22 círculos vagos, coluna 1 destacada, resumo *"C1 · 9 pessoas · 5 dos 17 postos ocupados · 12 vagos"*. Em C4: P0=4, P1=P2=P3=R1=2, nenhum vago, coluna 4 destacada, resumo *"C4 · 49 no pico · 43 postos + 6 de reserva"*. Os números batem com `docs/voluntarios/lista_postos.md` posto a posto. |
| 4 | Nenhum link quebrado | ✅ 143 caminhos conferidos, **0 quebrados**, e 0 links markdown relativos quebrados |
| 5 | O `CLAUDE.md` daqui contém a geometria e a tabela dos quatro cenários | ✅ |

### Tema separadores

| # | Critério | Resultado |
|---|---|---|
| 1 | A conferência das avenidas imprime as três faixas de x disjuntas e nenhuma invasão de zona protegida | ✅ |
| 2 | `98 unifilas em 133 m · reserva móvel 2` e `fita: 769 m (846 m com retoque) · 20 rolos de 50 m` | ✅ |
| 3 | `--grava` duas vezes gera SVG byte a byte idênticos, e idênticos aos copiados | ✅ md5 conferido nos 4 SVG e no JSON, nas duas gravações e contra os arquivos copiados. **É o que prova que as três dependências chegaram inalteradas** |

## 7. Revisão de 18/09 — Ring 3 confirmado e artefatos versionados

Depois da transferência, o Posto **confirmou o Ring 3** como pátio de fila, e os
documentos daqui foram alinhados a isso: `data/decisoes.json`, o `CLAUDE.md`, o
contexto dos separadores e a conferência de 15/09. Onde um trecho tirava a sua
conclusão da hipótese contrária, o trecho foi **reescrito para continuar de pé**, e
não apagado — caso da razão 1 do achado de arranjo, que agora se apoia nas três zonas
iguais do pátio, e das duas notas de densidade.

A confirmação é coerente com os artefatos: a folha `mapa/ring3_montagem.html` (16/09)
traz a montagem com 180 CCBs, e o artefato de sinalização v2 (17/09) diz no cabeçalho
*"Ring 3 confirmado"* e traz um `Mapa-Ring3` entre as suas pranchas. Os dois são
posteriores ao arranjo de 15/09.

Na mesma revisão, os **artefatos ganharam fonte versionada** em `mapa/`, com o
manifesto `mapa/artefatos.json` — URL, versão publicada e `sha256` de cada cópia. Ver
`mapa/README.md`. Das duas divergências entre artefatos que a revisão encontrou, a
largura das três zonas foi **decidida pelo Posto: são iguais, 12,87 m cada**, e
`CLAUDE.md` e a §5 do contexto de voluntários já refletem isso — a soma não muda, então
nenhuma conta se alterou. Continua aberto só o número de CCBs, 180 contra 179.
