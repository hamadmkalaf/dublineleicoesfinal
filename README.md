# Eleições 2026 — Posto de Dublin

Organização logística do 1º turno (**04/10/2026**, 8h–17h) no RDS Ballsbridge,
Dublin 4, e do eventual 2º turno (25/10/2026). Repositório **final**: carrega as
versões vigentes, não o histórico de trabalho.

> A memória do projeto — fatos fixos, geometria, cenários e regras — está em
> [`CLAUDE.md`](CLAUDE.md).

---

## Os dois temas

### Voluntários de apoio e fluxo do eleitor

O desenho do voluntariado que organiza o percurso do eleitor: quais funções
existem, onde cada uma fica, quantas pessoas cada uma exige, e como a escala se
comporta com o efetivo que o Posto realmente tem.

| Arquivo | O que é |
|---|---|
| [`docs/voluntarios/lista_postos.md`](docs/voluntarios/lista_postos.md) | **A fonte única.** Os 17 postos, os 4 cenários, a fila de preenchimento da posição 10 à 49, as compensações. É o documento do briefing. |
| [`docs/voluntarios/contexto.md`](docs/voluntarios/contexto.md) | Contexto consolidado: o princípio de projeto, os achados com a conta, as correções feitas no caminho, as premissas. **Leitura obrigatória antes de mexer em número.** |
| [`docs/voluntarios/dimensionamento.md`](docs/voluntarios/dimensionamento.md) | O raciocínio: taxas de chegada, dimensionamento, achados das plantas, riscos de segunda e terceira ordem. Carrega um aviso de que seus códigos de posto são da revisão anterior (RE1–T2, e não P0–T2). |
| [`mapa/voluntarios_postos.html`](mapa/voluntarios_postos.html) | Os postos marcados sobre a rota e sobre a planta do salão, com seletor dos quatro cenários. Não depende de nenhum arquivo do repositório; busca as fontes tipográficas no Google Fonts, então **sem internet ele abre e funciona, com outra tipografia**. |
| `scripts/zonas_balanceadas.py` | Confere a composição das três zonas contra os dados. |

**O que não pode se perder:** a sinalização atende o caso padrão e o voluntário
atende a exceção; **P0 é o posto crítico** da rota inteira; C4 é referência de teto,
não meta de recrutamento; o preenchimento é uma fila contínua da posição 10 à 49;
e **voluntário orienta, não decide** — identificação é monopólio legal do mesário.

### Separadores de fila e fita no chão no Hall 2

Como as 100 unifilas e a fita adesiva de piso repartem entre si o trabalho de
conduzir 11,5 mil eleitores da porta até a mesa. **Desenho definitivo, fechado em
17/09**; o que falta é resposta de terceiros.

| Arquivo | O que é |
|---|---|
| [`docs/separadores/plano_separadores_fila.md`](docs/separadores/plano_separadores_fila.md) | O desenho definitivo: decisões, geometria, as 98 unifilas, a fita por cor, os achados e as pendências. |
| [`docs/separadores/contexto.md`](docs/separadores/contexto.md) | O contexto consolidado. **Leia antes de mexer em qualquer número.** |
| [`docs/separadores/CONFERENCIA_PRANCHETA_2026-09-15.md`](docs/separadores/CONFERENCIA_PRANCHETA_2026-09-15.md) | Registro histórico de 15/09 — o porquê de cada decisão de arranjo, e onde o abandono do Ring 3 está registrado. |
| `scripts/separadores_fila.py` | Monta o catálogo de barreira, precifica em postes, calcula a fita por cor, **confere a regra das avenidas** e desenha tudo. |
| `saidas/separadores_definitivo.svg` · `.png` | A planta que vale. |
| `saidas/separadores_detalhe.svg` · `.png` | O corte do ramal: barreira → fita → mesa. |
| `saidas/separadores_opcao1.svg` · `opcao2.svg` | As duas alternativas descartadas, mantidas como registro. |
| `saidas/separadores_fila.json` | Premissas, catálogo e as três alocações. |

**Números do desenho:** 98 unifilas em 133 m, reserva móvel de 2 · 769 m de fita
(846 m com 10% de retoque), em 20 rolos de 50 m, seis cores · faltam **8 rolos**
(2 azul, 2 laranja, 1 zebrado, 1 verde, 2 branco) e, por pedido, **15 unifilas**.

---

## Como rodar

Sem dependências externas: só a biblioteca padrão do Python 3. Nada acessa a rede.

```bash
# Tema separadores — conferência e relatório, sem gravar. Sai com código 1 se a
# geometria quebrar; serve de teste em integração contínua.
python3 scripts/separadores_fila.py

# O mesmo, gravando os 4 SVG e o JSON em saidas/
python3 scripts/separadores_fila.py --grava

# Tema voluntários — confere a composição das três zonas
python3 scripts/zonas_balanceadas.py
```

### O que a conferência tem de imprimir

`scripts/separadores_fila.py` imprime as faixas de x das três avenidas e **sai com
código 1** se alguma cruzar outra ou invadir zona protegida:

```
As avenidas não se cruzam — faixas de x, disjuntas:
    A:  11.00 ..  25.03 m
    B:  26.80 ..  29.80 m
    C:  32.00 ..  36.50 m
    nenhuma avenida invade zona protegida
```

e, na alocação definitiva, `98 unifilas em 133 m · reserva móvel 2` e
`fita: 769 m (846 m com retoque) · 20 rolos de 50 m`.

`scripts/zonas_balanceadas.py` imprime **3.860 / 3.755 / 3.802**, total de
**11.417**, spread de **2,8%**, e *"Cada zona tem exatamente uma das três urnas
grandes"*. São os números do estimador grosso do script; a base B da prancheta dá
3.834 / 3.832 / 3.833 e 11.499. **As duas convivem de propósito** — ver §6 de
`docs/voluntarios/contexto.md`.

---

## Estrutura

```
CLAUDE.md                     memória do projeto: fatos fixos, geometria, cenários, regras
PENDENCIAS.md                 pendências gerais do Posto
README.md                     este arquivo
cenarios/                     paredes-abc-20260915.json — posição e rotação das 28 mesas
data/                         prancheta_hall2.json, decisoes.json, grupos_mesas.json,
                              paleta.json — fonte única das cores
docs/
  TRANSFERENCIA_REALIZADA.md  o que veio de onde, e o que ficou para trás
  contexto_geral.md           orçamento, layout, histórico e taxas de 2022
  separadores/                o tema dos separadores de fila
  voluntarios/                o tema dos voluntários e do fluxo
mapa/                         fonte versionada dos artefatos + artefatos.json (manifesto)
  sinalizacao/                as 21 peças P0–P7, os dois mapas e o canvas
plantas/                      imagens das plantas do Ring 3 e do Hall 2  (a preencher)
saidas/                       dados.json e as saídas geradas do tema dos separadores
scripts/                      separadores_fila.py, zonas_balanceadas.py,
                              tabela_mestra.py (tabela seção → porta das peças P0–P3),
                              artes_sinalizacao.py + _pictogramas.py (preferencial
                              e as 16 placas de grupo), paleta.py (conferência
                              da paleta, lê data/paleta.json)
Identidadevisual/             identidade visual e banner
Orçamentos/                   orçamentos, incl. sinalização
```

---

## Duas advertências sobre o que **não** está aqui

**1. `saidas/dados.json` é um arquivo órfão.** Ele é a fonte de todos os números de
eleitorado e de comparecimento por urna, mas **o pipeline que o gera não foi
transferido** — `scripts/parse_dados.py`, `scripts/mapa_agregacoes.py`,
`scripts/gera_pagina.py` e os CSVs em `data/raw/` ficaram no repositório de origem,
porque a agregação de seções não é tema deste repositório. Consequência prática:
**ninguém aqui regenera `dados.json`.** Se ele precisar ser refeito, é preciso
voltar a `hamadmkalaf/eleicoes2026`. Ele foi copiado sem alteração, e as
conferências dos dois temas batem contra ele.

**2. Faltam as plantas em imagem.** Os artefatos agora têm fonte versionada em
`mapa/` (ver `mapa/README.md` e o manifesto `mapa/artefatos.json`), mas as **plantas
em imagem** do Ring 3 e do Hall 2, das quais a descrição de geometria do `CLAUDE.md`
foi escrita, continuam fora do repositório. Sem elas, a descrição perde a fonte.

---

## Pendências bloqueantes

1. **O RDS permite fita adesiva no piso do Hall 2?** Se não, o desenho dos
   separadores cai inteiro. Ninguém confirmou.
2. Submeter o layout de barreira ao responsável de incêndio do RDS — barreira em
   zona de egresso muda o cálculo de evacuação, e isso se submete, não se comunica.
