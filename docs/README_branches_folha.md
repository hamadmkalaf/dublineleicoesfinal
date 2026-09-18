# Trechos de README das branches-folha da origem

Linhas que cada branch-folha de `hamadmkalaf/eleicoes2026` acrescentou ao README da branch padrão, preservadas aqui porque o README consolidado (`README_origem_2026-09-14.md`) não as tinha.

## Branch `claude/ring-3-horizontal-queue-pe4x3f` (2026-09-15)

- **`saidas/plano_ring3_horizontal.md`**, **`saidas/ring3.json`**,
  **`saidas/ring3_horizontal.html`** e **`saidas/ring3_*.svg`** — o Ring 3
  girado, os números por entrada e as plantas em escala das geometrias
  comparadas.
## Ring 3 — a fila externa

`scripts/ring3.py` modela o compound de fila ao ar livre do RDS, **44,0 × 35,0 m
(medida oficial)**, 14 m ao sul da fachada do Hall 2. O eleitor entra pelo
**canto nordeste**, desce rente ao gradil leste e vira no fundo: o corredor de
chegada é um **L** de 3,0 m, e as três zonas são alimentadas pelo trecho de
fundo. Restam dois desenhos, pela direção das raias.

```bash
python3 scripts/ring3.py              # plano, JSON e as plantas em SVG
python3 scripts/gera_pagina_ring3.py  # a página
```

| | Raias N–S | Raias L–O |
|---|---:|---:|
| Lotação (toda em raia) | 1.997 | 1.964 |
| Raias por zona | 8/10/8 | 23/23/23 |
| Meias-voltas | 23 | 66 |
| Separadores | 371 | 371 |
| A comprar (estoque 200) | 171 | 171 |

**Só duas coisas são separador**, por decisão do Posto: as divisórias entre as
raias (708,4 m) e a parede que separa a zona C da corrente que desce pelo
corredor lateral (32,0 m). Saíram da conta o contorno das zonas — que passa a
ser fita, 160,2 m —, a parede do corredor de chegada (39,8 m) e as raias do
apron até as portas (87,7 m): 288 m, 144 separadores a menos.

### Cenário 3 — CCB só na ponta, fita grossa no resto

A divisória vira fita do tipo de isolamento, ancorada por **um CCB na ponta
livre** (o vão da meia-volta). A separação da zona C continua barreira inteira.

| | N–S barreira inteira | N–S CCB na ponta | L–O CCB na ponta |
|---|---:|---:|---:|
| Separadores | 371 | **39** | 82 |
| A comprar (estoque 200) | 171 | **0** | 0 |
| Fita grossa | — | 662,4 m | 576,4 m |
| Lotação | 1.997 | 1.997 | 1.964 |

A barreira deixa de ser proporcional ao *comprimento* da raia e passa a ser
proporcional ao *número* de raias — por isso o girado, com 66 divisórias curtas,
custa mais que o N–S com 23 longas. Ressalva registrada no plano: cada divisória
fica com 28,8 m de vão livre de fita; com apoio a cada 5 m seriam 115 apoios, e
se forem CCB o total volta a 154.

Cada corrida que a conta soma está desenhada em `saidas/ring3_barreiras_*.svg`,
colorida pelo componente; o mapa **é** a conta, e `scripts/ring3.py` recusa a
gerar a planta se os dois não fecharem (`confere_mapa`).

O plano vigente (`scripts/layout_ring3.py`, `saidas/plano_ring3.md`) não está
neste repositório: foi produzido em sessão anterior e não chegou a ser
versionado. Reconstruído das cotas publicadas, continua servindo de aferição do
modelo de densidade — reproduz os 855 dos serpenteados e os 547 das baias.



## Branch `claude/filas-sem-ring-3-b9qvqi` (2026-09-15)


## Plano de filas sem o Ring 3

`plano_filas_sem_ring3.md` — desenho de formação de filas dentro do Hall 2 sem
depender do Ring 3, com dimensionamento de unifila/CCB e avaliação da
alternativa de fila na rua.

```bash
cd scripts
python3 filas_sem_ring3.py   # pico de fila por cenário -> saidas/filas_sem_ring3.json
python3 plano_filas.py       # clusters, anel, equipe, materiais -> saidas/plano_filas.json
python3 desenha_plano.py     # desenho em escala -> saidas/plano_filas_sem_ring3.svg
```

`plano_filas_confinado_hall2.md` — supersede as seções 3 a 5 do anterior depois que
o RDS proibiu fila em seu terreno: dimensiona toda a fila dentro do Hall 2 e compara
serpentina norte-sul com leste-oeste.

```bash
python3 serpentina_hall2.py   # capacidade, fronteira urnas x fila -> saidas/serpentina_hall2.json
python3 desenha_serpentina.py # as duas orientações -> saidas/serpentina_hall2.svg
```

`plano_filas_prancheta.md` — quanto cabe **sem mudar o desenho atual**: mesas nas
paredes onde estão, entradas A e B e saída central mantidas. 629 pessoas, e o
transbordo para a rua em cada tempo de atendimento.

```bash
python3 prancheta_capacidade.py  # capacidade e transbordo -> saidas/prancheta_capacidade.json
python3 desenha_prancheta.py     # desenho -> saidas/prancheta_serpentina.svg
```

`plano_filas_tres_portas.md` — a prancheta **Hamad_Final**: entradas S4/S5/S6,
saídas S2/S8, mesas onde estão. Seis blocos, dois por porta, mesma capacidade
por porta: 580 pessoas. Variante com S2 fechada: 747.

```bash
python3 tres_portas.py          # busca da repartição balanceada -> saidas/tres_portas.json
python3 desenha_tres_portas.py  # desenhos -> saidas/tres_portas_serpentina.svg e _s2_fechada.svg
```

## Branch `claude/determined-turing-uf2i0j` (2026-09-15)

python3 voluntarios.py       # gera saidas/postos_voluntarios.{json,md}
python3 postos_hall2.py      # gera saidas/postos_hall2.png
python3 postos_rota_ring3.py # gera saidas/postos_rota_ring3.png
- **`saidas/postos_voluntarios.md`** e **`.json`** — os postos de voluntário,
  por zona, com o que cada um faz.
- **`saidas/postos_hall2.png`** e **`saidas/postos_rota_ring3.png`** — os
  mesmos postos marcados em mapa.
## Plano de voluntários

`plano_voluntarios.md` marca os postos de apoio ao eleitor a partir destes
mesmos dados: 36 postos no pico — 6 na rota até o Ring 3, 12 no Ring 3 e 18
dentro do Hall 2. Conta postos, não pessoas. O cálculo está em
`scripts/voluntarios.py`, com as premissas reunidas no dicionário `PREMISSAS`,
e o histórico da decisão em `contexto_voluntarios_dublin_2026.md`.

Nenhum modelo de tempo de votação por eleitor foi aplicado às agregações, a
pedido: as saídas entregam os totais ordenados e o critério de gargalo fica a
cargo de quem analisa. O plano de voluntários modela fluxo de chegada e
atendimento fora da mesa — não o tempo de voto dentro dela.

## Branch `claude/adoring-keller-zrmecn` (2026-09-16)

## Conferência final (15/09/2026)

`CONFERENCIA_PRANCHETA_2026-09-15.md` confere estes números contra os três
PDFs oficiais do Cartório Eleitoral, agora em `data/oficiais/`, e verifica a
equidade do cenário de trabalho da prancheta. Resultado: **nenhuma
divergência** em 51 seções, 28 agregações e 28 mesas; o cenário `Hamad_Final`
reparte 3.833 · 3.835 · 3.831 esperados entre as paredes oeste, norte e leste.
Para refazer a conferência:

```bash
pip install pdfplumber
python3 scripts/confere_prancheta.py
```

Os PDFs são fonte primária e **substituem o `data/raw/mapa_agregacoes_TSE.png`**,
que trazia o erro de digitação descrito em "Achados".

