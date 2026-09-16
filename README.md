# Eleições 2026 · Posto de Dublin

Repositório final do planejamento do posto de votação de Dublin (Irlanda) para
o 1º turno de **4 de outubro de 2026**, no **Royal Dublin Society, Hall 2**
(Merrion Road, Ballsbridge, Dublin 4). Consolida numa árvore só o que estava
espalhado por 29 branches de `hamadmkalaf/eleicoes2026`, que fica como
arquivo. Como isso foi feito, e o que ficou em aberto por causa disso:
[`transferencia/EXECUCAO_2026-09-16.md`](transferencia/EXECUCAO_2026-09-16.md).

## Leia nesta ordem

1. Este README.
2. [`contexto_eleicoes_dublin_2026.md`](contexto_eleicoes_dublin_2026.md):
   o histórico do problema e a cronologia das decisões (tem trechos
   superados, marcados no texto).
3. [`CONFERENCIA_PRANCHETA_2026-09-15.md`](CONFERENCIA_PRANCHETA_2026-09-15.md):
   a conferência dos números contra os PDFs oficiais e o porquê do arranjo
   final das mesas.
4. [`PENDENCIAS.md`](PENDENCIAS.md) e
   [`docs/decisoes_em_aberto.md`](docs/decisoes_em_aberto.md): o que falta
   fazer e o que falta decidir.
5. [`DOCUMENTACAO_PROJETO.md`](DOCUMENTACAO_PROJETO.md) e os `docs/SESSAO_*.md`:
   documentação das etapas e passagens entre sessões, para quem for retomar
   uma delas.

## 1. O que está decidido

**As agregações.** 16.794 eleitores aptos, 51 seções, 28 urnas num único
local. 23 urnas somam duas seções (429 a 797 eleitores); 5 operam com uma só.
Três urnas críticas, todas de duas seções de Dublin: MRV 22 (3313 + 3889),
MRV 24 (3322 + 3752) e MRV 23 (3315 + 3778). Um quarto do eleitorado (4.213)
mora fora de Dublin. Conferido em 15/09 contra os três PDFs do Cartório
Eleitoral (`data/oficiais/`): nenhuma divergência.

**As portas.** Entradas S4 (A), S5 (B) e S6 (C) na fachada sul; saídas S2 e
S8; S7 preferencial; O1 e N1 fechadas (06/09, confirmado 13/09). Filas
identificadas por letra.

**As mesas.** Arranjo **Paredes_ABC** (15/09, `cenarios/paredes-abc-20260915.json`):
cada entrada serve uma parede inteira, A oeste, B norte, C leste, com 3.834 ·
3.832 · 3.833 comparecentes esperados por porta. Duas numerações convivem: o
MRV oficial (cadernos, convocação) e o número eleitor 1 a 28 (sinalização).
Peça: `saidas/prancheta_por_secao.html`.

**Dentro do salão.** Sem checkpoint: fitas no piso levam da porta à mesa
(14/09). Postes Tensa só nas filas de mesa (4 m no par, 10 m nas três
vermelhas). Identificação pelo caderno físico impõe ≤ 55 s por eleitor nas
três urnas críticas para fechar às 17h.

**A sinalização.** Revisão de 16/09: mesas sem número, o eleitor precisa saber
só a seção, e a consulta encolheu para seção → porta. Ponto "descubra sua
seção" (P0) na calçada da Merrion Road, fora do recinto; tudo o que é externo
vai em mesh amarrado em grade, gradil ou CCB, sem base. 16 peças externas, 21
internas, EUR 1.820 na faixa de EUR 1.700 a 1.900. Páginas:
`saidas/rota_do_eleitor_v2.html`
(https://claude.ai/artifact/1PQjgzstbiNorfJgagXhB5) e
`saidas/sinalizacao_hall2_v2.html`
(https://claude.ai/artifact/BcT5yzxRkSaUsbbHQQgjWF).

**A fila externa está em disputa.** Ver a seção 2.

## 2. O que está aberto

- **Ring 3, sim ou não.** Em 15/09 a conferência registra que o RDS proibiu
  fila no terreno dele e que não houve autorização de Brasília ("o Ring 3
  não existe mais"); o plano passou a ser fila **dentro** do Hall 2
  (`plano_filas_confinado_hall2.md`, `saidas/filas_sem_ring3.json`). Em 16/09,
  em sessão paralela, foi fechada e publicada a **Montagem do Ring 3**
  (`saidas/ring3_montagem.html`: cenário 3 adaptado, 180 CCBs, 506 m de fita,
  lotação 2.118). Os dois estão neste repositório. Decidir qual vale é o
  primeiro item de qualquer sessão nova.
- **Decisão D9**, identificação no caderno físico (`docs/decisoes_em_aberto.md`,
  `saidas/decisoes_em_aberto.html`): a única decisão de fluxo sem opção
  vigente.
- **Os dois geradores de `data/decisoes.json` não conversam** (ver seção 3).
- **Dois estimadores de comparecimento** sobre o mesmo arranjo:
  `scripts/comparecimento.py` (base B) dá 3.834 / 3.832 / 3.833 por porta,
  total 11.499; `scripts/zonas_balanceadas.py` dá 3.860 / 3.755 / 3.802, total
  11.417, com as taxas 74/50 fixas que o `CLAUDE.md` proíbe. O arranjo é o
  mesmo e os aptos batem; só o estimador difere. Detalhe e caminho sugerido em
  `transferencia/EXECUCAO_2026-09-16.md`.
- Quatro pendências técnicas da folha do Ring 3, se o Ring 3 valer: a ponta
  fixa da divisória ainda amarra em fita; medir uma CCB na entrega; a boca
  real do fundo não dá 1,00 m; confirmar com o safety officer do RDS as duas
  premissas marcadas.
- Tudo o mais em [`PENDENCIAS.md`](PENDENCIAS.md): orçamento final,
  comunicação com eleitores e mesários, funcionamento da MRV.

## 3. Como reproduzir

```bash
pip install pandas openpyxl Pillow pdfplumber pymupdf   # e Node 22 para o simulador
```

Há três cadeias, e a ordem entre elas importa.

**A. Cadeia consolidada de 14/09** (agregação, planta-base, prancheta,
simulador, Ring 3 oficial, sinalização externa, decisões, barreiras, fitas no
piso, instruções, dashboard). Os comandos, etapa por etapa, estão em
[`docs/README_origem_2026-09-14.md`](docs/README_origem_2026-09-14.md), seção
"Como rodar". Algumas etapas pedem `cd scripts`, como indicado lá.

**B. Cadeias das branches de 15/09**, cada uma independente, com os comandos
em [`docs/README_branches_folha.md`](docs/README_branches_folha.md): filas sem
o Ring 3 (`filas_sem_ring3`, `plano_filas`, `serpentina_hall2`,
`prancheta_capacidade`, `tres_portas` e os `desenha_*`), voluntários
(`voluntarios`, `postos_hall2`, `postos_rota_ring3`), sinalização interna
(`plano_sinalizacao`, `gera_pagina_sinalizacao`), `zonas_balanceadas`, e o
Ring 3 montado:

```bash
python3 scripts/ring3_montagem.py            # CCB: 180 · compra 0 | sobra 20 → saidas/ring3_planta.svg
python3 scripts/gera_pagina_ring3_montagem.py  # → saidas/ring3_montagem.html
```

**C. Cadeia de 16/09.** Produz o arranjo e a prancheta por seção.

> **Leia antes de rodar.** `scripts/arranjo_paredes.py --grava` **não é
> determinístico**: a busca dele é semeada pelo arranjo que já está em
> `data/decisoes.json`, e há vários arranjos igualmente equilibrados. Rodando
> sobre o estado commitado, reproduz o Paredes_ABC byte a byte. Rodando depois
> de `scripts/gera_decisoes.py` (etapa 1 da cadeia A), que reescreve o arquivo
> com o cenário anterior, ele escolhe **outro** arranjo — igualmente
> equilibrado e diferente, com mesas trocando de parede.
>
> Isso importa porque a sinalização publicada lista quais seções entram por
> qual porta. Um arranjo diferente invalida as duas peças publicadas em
> silêncio. **Trate o arranjo como estado commitado, não como saída:** só rode
> `arranjo_paredes.py --grava` para adotar deliberadamente um arranjo novo, e
> nesse caso regenere e republique a sinalização. Se rodar a cadeia A, devolva
> `data/decisoes.json`, `cenarios/paredes-abc-20260915.json` e
> `saidas/prancheta_por_secao.html` ao commit (`git checkout --`) em vez de
> regenerá-los.

```bash
python3 scripts/gera_decisoes_base.py --grava    # as 28 mesas, aptos e esperados, dos PDFs
python3 scripts/arranjo_paredes.py --grava       # o arranjo e o cenário Paredes_ABC
python3 scripts/gera_prancheta_por_secao.py      # → saidas/prancheta_por_secao.html
python3 scripts/confere_prancheta.py             # sai 1 se algo divergir dos PDFs
python3 scripts/confere_arranjo.py               # sai 1 se o arranjo violar um dos sete itens
```

**D. Sinalização v2** (Rota do Eleitor e Sinalização interna). Independente das
outras: usa só a biblioteca padrão e lê `data/prancheta_paredes_abc.json` e
`saidas/dados.json`.

```bash
python3 scripts/sinalizacao_v2.py   # → saidas/rota_do_eleitor_v2.html, sinalizacao_hall2_v2.html, sinalizacao_v2.json
```

Falha em vez de gravar se as 51 seções não aparecerem uma vez, se os aptos não
somarem 16.794 ou se as 28 mesas não fecharem. Deve imprimir
`blocos: [5, 5, 6]`, `secoes/porta: [18, 16, 17]` e `TOTAL 1820.0`. Conferência
de integridade e o roteiro de republicação dos dois artefatos:
`transferencia/TRANSFERENCIA_SINALIZACAO.md`.

Tudo isso foi executado neste repositório em 16/09/2026; o resultado está em
`transferencia/EXECUCAO_2026-09-16.md`. `saidas/Dublin_2026_agregacoes.xlsx`
nunca é byte a byte (o formato grava a data): compare abas, não bytes.
Toda saída em `saidas/` é gerada; editar à mão se perde na próxima geração.

**Não renomeie os arquivos de `data/raw/`** (`parse_dados.py` os abre pelo
nome literal) e não mova `scripts/` (os caminhos saem de `parent.parent`).

## 4. De onde vêm os dados

| Arquivo | Origem | Papel |
|---|---|---|
| `data/oficiais/aptos_por_secao_dublin_2026-07-13.pdf` | ELO, 13/07 | as 51 seções com aptos e condado de origem |
| `data/oficiais/secoes_agregadas_dublin_2026.pdf` | Cartório Eleitoral | os 28 pares principal → agregada |
| `data/oficiais/mrv_mesarios_dublin_2026-09-13.pdf` | Convoca+, 13/09 | os 109 mesários nomeados por MRV |
| `data/raw/eleitorado_local_votacao_2026_ZZ.csv` | TSE, 13/08 | seção a seção no exterior |
| `data/raw/Filtrado_Dublin.csv` | TSE, 14/07 | perfil do eleitorado de Dublin |
| `data/raw/mapa_agregacoes_TSE.png` | TSE, 13/08 | mapa de pares; **superado pelos PDFs** e com um erro (3752 sob 3222, que é do Porto; a correta é 3322) |
| `data/prancheta_hall2.json` | medido da planta do RDS | geometria do salão, do módulo e das 18 portas |
| `data/fotos/` | levantamento de 24/08 | fotos do RDS usadas na rota e na sinalização |

Os CSVs estão em latin-1, separados por `;`; o `Filtrado_Dublin.csv` vem com
a linha inteira entre aspas e `parse_dados.py` trata isso. Não "normalize"
para UTF-8. Nenhum dos dois identifica eleitores: são contagens por seção.

`referencias/` guarda o que veio de terceiros e não é gerado aqui: a planta do
RDS Hall 2, o material sobre a MRV, a agregação na versão do TSE, a proposta
de agregação e o rascunho à mão do plano com duas entradas (superado).

O repositório deve ser **privado**: reúne planta, barreiras, staff e orçamento
de um local de votação com data e hora públicas. Foi criado público; mudar em
Settings.

## 5. O que é `artefatos/`

Cópias das páginas publicadas no claude.ai, na versão em que foram lidas em
16/09, com URL e versão em [`artefatos/README.md`](artefatos/README.md). A
fonte de verdade de cada página é o URL; para atualizar, republicar no mesmo
URL. As mesmas páginas, regeneradas a partir dos scripts, estão em `saidas/`.

## Estrutura

```
README.md · CLAUDE.md · PENDENCIAS.md · DOCUMENTACAO_PROJETO.md · CONFERENCIA_PRANCHETA_2026-09-15.md
contexto_*.md · plano_*.md · orcamento_*.md · handoff_*.md · registro_*.md · pesquisa_*.md
data/raw/        fontes TSE (nomes intocados)   data/oficiais/  PDFs do Cartório   data/fotos/
data/*.json      decisões, prancheta, MRVs, decisões em aberto
scripts/         os geradores (Python) e templates   simulador/   motor de fluxo (Node)
cenarios/        arranjos das mesas, o vigente é paredes-abc-20260915.json
saidas/          tudo o que os scripts geram, incluindo saidas/dashboard/
docs/            passagens de sessão, READMEs de origem, instruções de fluxo
referencias/     recebidos de terceiros   artefatos/   páginas exportadas do claude.ai
transferencia/   roteiros (TRANSFERENCIA, MIGRACAO, TRANSFERENCIA_SINALIZACAO), manifesto e registro de execução
```
