> ## ⚠ ESTE ARQUIVO ESTÁ DESATUALIZADO NUM PONTO — RING 3
>
> **O Ring 3 foi CONFIRMADO pelo Posto em 16/09/2026.** Tudo o que este
> documento diz sobre o Ring 3 ter sido abandonado, proibido pelo RDS ou "não
> existir mais" está **revertido**, e a fila externa no terreno do RDS voltou a
> ser o plano. A fila confinada dentro do Hall 2 é contingência.
>
> Com a confirmação, as larguras das zonas também mudaram: elas eram
> proporcionais às cotas do Ring 3 antigo (A 3.642 / B 4.215 / C 3.642) e
> passaram a sair do esperado por entrada de Paredes_ABC — **12,87 · 12,86 ·
> 12,87 m**, 179 CCBs, percurso máximo de 296 m.
>
> Esta branch é uma das origens da consolidação em `main` e não recebeu essa
> correção: ela vive em `main` (`data/decisoes.json`, bloco `ring3`;
> `scripts/ring3_montagem.py`; `docs/CONTEXTO_DO_PROJETO.md` §6.1). **Leia a
> `main` antes de usar qualquer número de Ring 3 deste arquivo.**

# Eleições 2026 — Posto de Dublin, RDS Ballsbridge, Hall 2

Planejamento do posto de votação do Consulado/Embaixada em Dublin para o
**1º turno de 4/10/2026, das 8h às 17h**, no **Hall 2 do RDS, Merrion Road,
Ballsbridge, Dublin 4**.

## O resultado, em uma linha

**16.794 aptos** em **51 seções**, agregadas em **28 mesas**, distribuídas em
**3 paredes** (oeste A, norte B, leste C) com **uma entrada por parede** —
11.499 eleitores esperados repartidos em **3.833 · 3.835 · 3.831**, amplitude
de 4 eleitores (0,10% do terço perfeito).

O desenho vive no cenário `cenarios/paredes-abc-20260915.json` e na peça
`saidas/prancheta_por_secao.html`.

## A cadeia, em sete passos

Nenhum passo depende de rede. Os dois primeiros precisam de `pandas` e
`openpyxl`; do terceiro em diante, de `pdfplumber`.

```bash
pip install pandas openpyxl pdfplumber

python3 scripts/mapa_agregacoes.py             # 1. os CSV do TSE  → saidas/dados.json
python3 scripts/gera_pagina.py                 # 2. a página das agregações
python3 scripts/gera_decisoes_base.py --grava  # 3. os PDFs        → as 28 mesas
python3 scripts/arranjo_paredes.py --grava     # 4. o arranjo, as zonas e o cenário
python3 scripts/gera_prancheta_por_secao.py    # 5. a prancheta pelas seções
python3 scripts/confere_prancheta.py           # 6. confere os dados
python3 scripts/confere_arranjo.py             # 7. confere os sete itens do arranjo
```

Como isso se encadeia:

```
data/raw/*.csv ──▶ mapa_agregacoes ──▶ saidas/dados.json ──┐
                                                            ├─▶ gera_decisoes_base
data/oficiais/*.pdf ──▶ fontes_oficiais ───────────────────┤      │
                        comparecimento ────────────────────┘      ▼
                                                     data/decisoes.json (bloco mesas)
                                                                  │
data/prancheta_hall2.json ──────────────▶ arranjo_paredes ◀───────┘
                                              │
                    cenarios/paredes-abc-20260915.json
                    data/decisoes.json (camada de layout)
                                              │
                                              ▼
                              gera_prancheta_por_secao
                                              │
                              saidas/prancheta_por_secao.html
```

A ordem 3 → 4 importa: `data/decisoes.json` é lido **e** escrito — o passo 3
põe as 28 mesas, o passo 4 escreve a camada de layout por cima.

## As duas conferências

```bash
python3 scripts/confere_prancheta.py   # os dados, contra os três PDFs oficiais
python3 scripts/confere_arranjo.py     # os sete itens do arranjo
```

As duas **saem com código 1** se algo divergir. Rode as duas antes de qualquer
commit que toque em dados ou arranjo — a integração contínua
(`.github/workflows/confere.yml`) roda as duas a cada push, mas achar o erro
antes do push é mais barato.

## As fontes

Os três PDFs de `data/oficiais/` são fonte primária:

| Arquivo | Emissão | O que traz |
|---|---|---|
| `aptos_por_secao_dublin_2026-07-13.pdf` | ELO, 13/07/2026 | as 51 seções com aptos e condado de origem |
| `secoes_agregadas_dublin_2026.pdf` | Cartório Eleitoral | os 28 pares principal → agregada |
| `mrv_mesarios_dublin_2026-09-13.pdf` | Convoca+, 13/09/2026 | os 109 mesários nomeados, por MRV |

A geometria do salão sai de `RDS_Hall_2_Floorplan_(1).pdf`, medida em
`data/prancheta_hall2.json`.

## A peça publicada

A prancheta pelas seções está publicada em
<https://claude.ai/artifact/Szv5egKpHy3umh4udAybvr>. Republicar a partir do
mesmo arquivo (`saidas/prancheta_por_secao.html`) mantém o endereço.

## A prancheta manipulável

```bash
python3 scripts/gera_editor.py     # → saidas/editor.html
```

O editor abre no cenário de trabalho (Paredes_ABC), desenha as 28 mesas em
escala, as zonas protegidas e os serpenteados de 16/09, e serve para **estudar
posição**: arrastar uma mesa, girar de 90 em 90, medir distâncias, ver o que
isso faz com os corredores. Ele não recalcula nada e não decide nada — o que
sai dele é um cenário, que só vira desenho depois de gravado em `cenarios/` e
de a cadeia rodar de novo.

Ele não entra nos sete passos de propósito: nada da cadeia depende dele.

## O que veio dos outros branches do repositório antigo

Estes não são gerados aqui; vieram por decisão item a item na transferência de
16/09. Os que carregam conteúdo superado abrem com um **aviso de safra** que
diz exatamente o quê.

| Arquivo | O que é |
|---|---|
| `DOCUMENTACAO_PROJETO.md` | a documentação consolidada das sete etapas (06/09) |
| `orcamento_final.md`, `orcamentos_itens_pequenos.md` | o orçamento, entregável |
| `handoff_agregacao_dublin_2026.md` | a única origem escrita das taxas de 2022 por condado |
| `pesquisa_horarios_pico_votacao.md` | a base da curva de chegada |
| `saidas/analise_gargalos.md` | o que decide identificação em uma ou duas posições |
| `plano_filas_tres_portas.md` | o plano de filas vigente, com dois desenhos em `saidas/` |
| `data/fotos/*.jpg` | o levantamento fotográfico do local, 24/08 |

Ficaram para trás, por decisão: o dashboard (20 páginas de antes de 15/09), o
simulador de fluxo, o plano de sinalização do Ring 3 (ver `PENDENCIAS` §8), a
documentação do Ring 3 e as passagens de sessão.

## Onde está o resto

- `CONFERENCIA_PRANCHETA_2026-09-15.md` — a conferência e os onze adendos: o
  porquê de cada decisão do arranjo. **Leia antes de mexer no desenho.**
- `contexto_eleicoes_dublin_2026.md` — o histórico do problema.
- `PENDENCIAS` — o que falta, por dono.
- `TRANSFERENCIA.md` — o manifesto que originou este repositório.
- `CLAUDE.md` — as regras para quem (ou o que) for trabalhar aqui.
