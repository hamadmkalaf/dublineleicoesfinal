# Contexto do projeto — Eleições 2026, posto de votação de Dublin

> Documento escrito em **17/09/2026**, na consolidação das branches em `main`.
> Serve para quem chega ao repositório sem nenhum histórico: o que é o projeto,
> de onde vêm os números, o que já foi decidido, o que ainda está em disputa,
> como a árvore está organizada e como reproduzir cada peça.
>
> Ele **não substitui** os documentos de trabalho: o [`README.md`](../README.md)
> é o roteiro operacional, o [`CLAUDE.md`](../CLAUDE.md) são as regras de quem
> mexe no desenho, e a
> [`CONFERENCIA_PRANCHETA_2026-09-15.md`](../CONFERENCIA_PRANCHETA_2026-09-15.md)
> é o porquê, com números, de cada decisão do arranjo. Este documento é o mapa
> que liga os três.

---

## 1. O problema

A Embaixada do Brasil em Dublin organiza a votação dos brasileiros residentes
na Irlanda para a eleição presidencial de 2026.

| | |
|---|---|
| **1º turno** | domingo, **4 de outubro de 2026**, 8h–17h |
| **2º turno** (se houver) | domingo, **25 de outubro de 2026**, mesmo local e horário |
| **Local** | **Royal Dublin Society (RDS), Hall 2** — Merrion Road, Ballsbridge, Dublin 4 |
| **Eleitorado** | **16.794 aptos** em **51 seções** |
| **Urnas** | **28 mesas receptoras** (1 urna por mesa), num único local |
| **Comparecimento esperado** | **11.499** (base B — ver §2) |

O projeto responde a uma pergunta operacional: **como fazer 11,5 mil pessoas
entrarem, se identificarem, votarem e saírem de um pavilhão, em nove horas, sem
que a fila estoure.** Tudo o mais — agregação de seções, planta, filas,
sinalização, orçamento, voluntários, comunicação — é consequência disso.

Duas restrições moldaram o desenho:

- **A identificação é por caderno físico impresso** (decisão de 13/09). Isso
  impõe o gargalo: nas três urnas mais carregadas, o posto precisa fechar cada
  eleitor em **≤ 55 s** para terminar às 17h.
- **A fila tem de caber dentro do Hall 2** — o RDS proibiu fila no terreno
  dele. É este o ponto em disputa descrito em §6.1.

Contexto do ano: 2026 coincide com a presidência irlandesa do Conselho da UE, o
que reduziu a oferta de espaços e encareceu a locação (o local mais barato,
usado no 2º turno de 2022, estava indisponível).

---

## 2. Os números, e de onde eles vêm

Nada no repositório é digitado à mão. Todo número sai de uma das fontes abaixo,
e as duas conferências (§5) falham se alguma peça divergir delas.

| Fonte | Emissão | O que fixa |
|---|---|---|
| `data/oficiais/aptos_por_secao_dublin_2026-07-13.pdf` | ELO, 13/07/2026 | as 51 seções, com aptos e condado de origem |
| `data/oficiais/secoes_agregadas_dublin_2026.pdf` | Cartório Eleitoral | os 28 pares principal → agregada |
| `data/oficiais/mrv_mesarios_dublin_2026-09-13.pdf` | Convoca+, 13/09/2026 | os 109 mesários nomeados, por MRV |
| `data/raw/eleitorado_local_votacao_2026_ZZ.csv` | TSE, 13/08/2026 | eleitorado do exterior, seção a seção |
| `data/raw/Filtrado_Dublin.csv` | TSE, 14/07/2026 | perfil do eleitorado de Dublin |
| `data/prancheta_hall2.json` | medido da planta do RDS | geometria do salão, do módulo e das 18 portas |
| `data/fotos/` | levantamento de 24/08/2026 | fotos do local, usadas na rota e na sinalização |

**A agregação.** 51 seções → 28 urnas. 23 urnas somam duas seções (429 a 797
eleitores cada); 5 operam com uma só. As três urnas críticas são todas de duas
seções de Dublin: **MRV 22** (3313 + 3889), **MRV 24** (3322 + 3752) e
**MRV 23** (3315 + 3778). Um quarto do eleitorado (**4.213**) mora fora de
Dublin — 19 seções espalhadas por Cork, Galway, Donegal, Limerick, Kerry, Mayo
e outros condados.

**O comparecimento.** É sempre a **base B**: a taxa de 2022 aplicada por
domicílio de origem da seção (`scripts/comparecimento.py`), que dá **11.499**
esperados. Os números antigos — "~12.000", ou as taxas fixas de 74% em Dublin e
50% no interior — estão **superados** e o `CLAUDE.md` proíbe reintroduzi-los.

**A carga por entrada**, do `data/decisoes.json` commitado, é a razão de ser do
arranjo atual:

| Entrada | Porta | Parede | Mesas | Aptos | Esperados |
|---|---|---|---|---|---|
| A | S4 | oeste | 9 | 5.695 | **3.834** |
| B | S5 | norte | 9 | 5.600 | **3.832** |
| C | S6 | leste | 10 | 5.499 | **3.833** |

Amplitude de 2 eleitores entre as portas. Repare que os **aptos** são bem
desiguais (5.499 a 5.695) e os **esperados** quase idênticos: o arranjo
equilibra quem aparece, não quem está inscrito — é por isso que ele depende da
base B e cai junto com ela se a base mudar.

> **Cuidado de comparabilidade.** Circulam duas fotografias do eleitorado que
> **não são intercambiáveis**: a base de 16.794 aptos (a deste repositório) e o
> arquivo do TRE com **14.626** aptos, já agregado em 20 mesas, que vive no
> Drive do Posto. A diferença (~2.168) parece vir de limpeza de cadastro,
> concentrada no interior. Propostas calculadas sobre bases diferentes não se
> comparam — ver §1 de
> [`handoff_agregacao_dublin_2026.md`](../handoff_agregacao_dublin_2026.md) e
> §2.5 de
> [`contexto_eleicoes_dublin_2026.md`](../contexto_eleicoes_dublin_2026.md).

---

## 3. A cronologia das decisões

| Quando | O que ficou decidido | Onde vive |
|---|---|---|
| jul/2026 | negociação da agregação com o TRE/TSE: 51 seções → 28 urnas | `contexto_eleicoes_dublin_2026.md`, `handoff_agregacao_dublin_2026.md` |
| 06/09 | base de comparecimento **B**; MRV do DJE como identidade da mesa; entradas S4/S5/S6, saídas S2/S8 | `scripts/comparecimento.py`, `data/decisoes.json` |
| 24/08 | levantamento fotográfico do RDS | `data/fotos/` |
| 11–12/09 | barreiras internas, fitas no piso, dashboard | `saidas/barreiras_hall2.html`, `docs/registro_fitas_no_piso_2026-09-12.md` |
| 13/09 | identificação por **caderno físico**; 4 seguranças (não 20); fila identificada por **letra** (A/B/C); duas numerações de mesa (MRV oficial + número eleitor 1–28) | `CONFERENCIA_PRANCHETA_2026-09-15.md`, `orcamento_final.md` |
| 14/09 | **sem checkpoint**: fitas no piso levam da porta à mesa; postes Tensa só nas filas de mesa | `docs/alternativa_fitas_no_piso.md`, `plano_filas_*.md` |
| 15/09 | **uma entrada por parede** — A→oeste, B→norte, C→leste (arranjo **Paredes_ABC**); **Ring 3 abandonado** | `cenarios/paredes-abc-20260915.json`, `CONFERENCIA_PRANCHETA_2026-09-15.md` |
| 16/09 | recuos de 3 m em N2 e O2; faixa de emergência na fachada leste; sala de apoio entre O1 e a parede norte; serpenteado de ~20 pessoas à frente de cada mesa vermelha; **sinalização v2** (mesa sem número, consulta reduzida a seção → porta) | `data/decisoes.json` (`zonas_protegidas`, `serpenteados`), `scripts/sinalizacao_v2.py` |
| 17/09 | estratégia de comunicação em redes sociais; **consolidação das branches em `main`** | `ESTRATEGIA-COMUNICACAO-REDES-SOCIAIS.md`, este documento |

O que está **congelado** (mudar é decisão do Posto, não da sessão) está na
tabela do [`CLAUDE.md`](../CLAUDE.md).

---

## 4. O desenho vigente, em seis blocos

**As portas.** Entradas **S4 (A)**, **S5 (B)** e **S6 (C)** na fachada sul;
saídas **S2** e **S8**; **S7** preferencial (idoso, gestante, PcD, com
acompanhante — vão de 1,27 m, medido); **O1** e **N1** fechadas. A numeração é
por fachada e é **gerada** por `scripts/planta_base.py`, não escrita à mão.

**As mesas.** Arranjo **Paredes_ABC**: cada entrada serve uma parede inteira,
9 mesas a oeste, 9 ao norte, 10 a leste. Convivem duas numerações — o **MRV**
oficial (cadernos, convocação, comunicação interna) e o **número eleitor** 1 a
28, que começa na mesa mais ao sul da parede oeste e segue em sentido horário
(é o que aparece em destaque na sinalização). Peça:
`saidas/prancheta_por_secao.html`.

**Dentro do salão.** Sem checkpoint: **fitas no piso** levam da porta à mesa.
Postes Tensa só nas filas de mesa (4 m no par, 10 m nas três vermelhas). Três
zonas protegidas de 16/09: recuo de 3 m em N2 e O2, faixa de emergência de 3 m
na fachada leste, sala de apoio entre O1 e a parede norte (7,80 m de
profundidade — **é suposição, falta medir em campo**).

**A sinalização (v2, 16/09).** O eleitor precisa saber só a **seção**; a
consulta encolheu para *seção → porta* e as mesas deixaram de exibir número na
sinalização externa. Ponto "descubra sua seção" (**P0**) na calçada da Merrion
Road, fora do recinto. Tudo o que é externo vai em mesh amarrado em grade,
gradil ou CCB, sem base. **16 peças externas, 21 internas, EUR 1.820** (faixa
orçada: EUR 1.700–1.900). Páginas: `saidas/rota_do_eleitor_v2.html` e
`saidas/sinalizacao_hall2_v2.html`.

**O orçamento.** [`orcamento_final.md`](../orcamento_final.md) é uma tabela
preenchível em duas partes: o que **já existe** (contratado ou em mãos,
R1–R8) e o que **ainda custa** e depende de decisão ou cotação (C1–C16).
Referência: os EUR 15.703,32 do telegrama revisado. Quatro linhas foram orçadas
para o Ring 3 e precisam ser reavaliadas (§6.1).

**A comunicação.** [`ESTRATEGIA-COMUNICACAO-REDES-SOCIAIS.md`](../ESTRATEGIA-COMUNICACAO-REDES-SOCIAIS.md)
(+ versão .docx) cobre Instagram, Facebook, WhatsApp, TikTok e X, com o
objetivo declarado de **não** influenciar o voto, e sim fazer o eleitor chegar
sabendo a seção, a fila, o documento e o número do candidato. Atende parte do
item 3 do `PENDENCIAS.md`; o item 4 (mesários) continua aberto.

---

## 5. Como a árvore está organizada

```
README.md            roteiro operacional: o que está decidido, o que está aberto, como rodar
CLAUDE.md            regras de quem mexe no desenho (o que nunca fazer)
PENDENCIAS.md        tarefas do Posto + "em aberto no desenho do Hall 2"
DOCUMENTACAO_PROJETO.md   a consolidação das sete etapas (06/09) — com aviso de safra
CONFERENCIA_PRANCHETA_2026-09-15.md   a conferência e os onze adendos: o porquê do arranjo
contexto_*.md · plano_*.md · orcamento_*.md · handoff_*.md · pesquisa_*.md · registro_*.md

data/raw/        fontes do TSE — NÃO renomear (os parsers abrem pelo nome literal)
data/oficiais/   os três PDFs do Cartório Eleitoral
data/fotos/      levantamento de 24/08
data/*.json      decisões, prancheta medida, decisões em aberto
scripts/         os geradores (Python) e os templates HTML
simulador/       motor de fluxo (Node 22)
cenarios/        arranjos das mesas — o vigente é paredes-abc-20260915.json
saidas/          tudo o que os scripts geram (inclusive saidas/dashboard/)
docs/            passagens de sessão, READMEs de origem, instruções de fluxo, este documento
referencias/     recebidos de terceiros (planta do RDS, material da MRV, propostas do TSE)
artefatos/       cópias de leitura das páginas publicadas no claude.ai
transferencia/   roteiros e registro da migração vinda de hamadmkalaf/eleicoes2026
```

**As quatro cadeias de geração** (detalhe e comandos no
[`README.md`](../README.md) §3):

| | Cadeia | O que produz |
|---|---|---|
| **A** | consolidada de 14/09 | agregação, planta-base, prancheta, simulador, Ring 3, decisões, barreiras, fitas, dashboard |
| **B** | branches de 15/09 | filas sem Ring 3, voluntários, sinalização interna, zonas balanceadas, Ring 3 montado |
| **C** | 16/09 | as 28 mesas a partir dos PDFs, o arranjo Paredes_ABC, a prancheta por seção |
| **D** | sinalização v2 | `rota_do_eleitor_v2.html`, `sinalizacao_hall2_v2.html` (só biblioteca padrão) |

**A ordem entre elas importa**: a cadeia C roda por último, e
`data/decisoes.json` versionado é a versão de 16/09.

**As duas conferências** são o portão de qualidade — saem com código 1 se algo
divergir, e a CI (`.github/workflows/confere.yml`) roda as duas a cada push:

```bash
python3 scripts/confere_prancheta.py   # os dados, contra os três PDFs oficiais
python3 scripts/confere_arranjo.py     # os sete itens do arranjo
```

> **`scripts/arranjo_paredes.py --grava` não é determinístico.** A busca é
> semeada pelo arranjo que já está em `data/decisoes.json`, e há vários
> arranjos igualmente equilibrados. Rodando sobre o estado commitado, ele
> reproduz o Paredes_ABC byte a byte; rodando depois de `gera_decisoes.py`, ele
> escolhe **outro** arranjo — e a sinalização publicada, que lista qual seção
> entra por qual porta, passa a mentir em silêncio. Trate o arranjo como
> **estado commitado, não como saída**.

---

## 6. O que está em disputa, e o que ficou inconsistente

Esta é a seção que economiza uma sessão inteira de quem retoma o projeto.

### 6.1 Ring 3: sim ou não — a decisão mais cara em aberto

O "Ring 3" era a fila **externa**, no terreno do RDS. Duas sessões de 16/09
dizem coisas opostas, e as duas estão neste repositório:

- **Abandonado** (15/09): o RDS proibiu fila no terreno dele e não houve
  autorização de Brasília. O plano passou a ser fila **dentro** do Hall 2 —
  `plano_filas_confinado_hall2.md`, `saidas/filas_sem_ring3.json`.
- **Montado e publicado** (16/09, sessão paralela): "Montagem do Ring 3",
  cenário 3 adaptado, 180 CCBs, 506 m de fita, lotação 2.118 —
  `saidas/ring3_montagem.html`.

**Decidir qual vale é o primeiro item de qualquer sessão nova.** A decisão
arrasta: quatro linhas do orçamento (R7 separadores CCB, R8 espaço, C5 fita de
contorno, C6 placas de porta nas CCBs), o dimensionamento das filas e quatro
pendências técnicas da folha do Ring 3 (a ponta fixa da divisória, medir uma
CCB na entrega, a boca real do fundo que não dá 1,00 m, e duas premissas a
confirmar com o *safety officer* do RDS).

### 6.2 Dois estimadores de comparecimento sobre o mesmo arranjo

| Script | Por porta (A/B/C) | Total |
|---|---|---|
| `scripts/comparecimento.py` (base B) — **o vigente** | 3.834 / 3.832 / 3.833 | 11.499 |
| `scripts/zonas_balanceadas.py` | 3.860 / 3.755 / 3.802 | 11.417 |

O arranjo é o mesmo e os aptos batem; só o estimador difere — e o segundo usa
as taxas fixas 74/50 que o `CLAUDE.md` proíbe. Enquanto os dois existirem,
confira de qual script veio qualquer número por porta antes de usá-lo.

### 6.3 Dois geradores de `data/decisoes.json` que não conversam

`gera_decisoes.py` (cadeia A, 14/09) reescreve o arquivo com o cenário
Hamad_Final; `gera_decisoes_base.py` + `arranjo_paredes.py` (cadeia C, 16/09)
reescrevem com o Paredes_ABC. Nunca conviveram na origem — eram branches
separadas. A regra adotada é a da §5 (a cadeia C roda por último). **Unificar
os dois é trabalho de projeto, ainda não feito.**

### 6.4 Inconsistências que a própria consolidação resolveu ou expôs

| Onde | O que diz | Situação em 17/09 |
|---|---|---|
| `PENDENCIAS.md` §8 ("em aberto no desenho") | "PLANO DE SINALIZAÇÃO INTERNA — não existe mais nenhum válido. BLOQUEIA imprimir placa." | **Resolvido pela consolidação**: a sinalização v2 de 16/09 nasceu do desenho atual (3 entradas, 2 saídas, S7 preferencial) e está na árvore |
| `PENDENCIAS.md` §6 e §9, `plano_filas_tres_portas.md` | "os scripts ficaram no repositório antigo" | **Superado**: `scripts/plano_filas.py`, `scripts/tres_portas.py` e `scripts/simula_fluxo.py` estão aqui. Continua valendo o alerta de que `plano_filas.py` usa **11.416 fixo no código** em vez da base B (11.499) — corrigir antes de usar |
| `saidas/analise_gargalos.md` (aviso de safra) | "o script citado ficou no repositório antigo" | idem: `scripts/simula_fluxo.py` está na árvore |
| `simulador/teste_portas.js` | 4 de 144 verificações falham (quotas das zonas B e C do Ring 3) | **Falha herdada, anterior à consolidação**, e ligada ao Ring 3 abandonado. Some se o Ring 3 cair de vez; não afeta as duas conferências |
| `docs/CLAUDE_origem_eleicoes2026.md` | descreve branches e PRs do repositório antigo | preservado como registro; **onde divergir do `CLAUDE.md`, vale o `CLAUDE.md`** |

### 6.5 Medidas que ainda são suposição

Três números do desenho não foram medidos em campo, e os três afetam peça
impressa ou capacidade: a **profundidade da sala de apoio** (7,80 m), o **vão
de S7** (1,27 m, que serve um fluxo preferencial pequeno e não absorve uma fila
grande) e o **recorte do canto sudoeste**, que tem duas leituras no repositório
(11,7 × 7,4 m em `plano_filas_tres_portas.md` contra ~8 × 7 m na prancheta
medida). Medir os três na mesma visita.

Some-se a isso que **as taxas de 2022 por condado não têm fonte primária
registrada** — 91% do eleitorado cai na taxa "direto", mas nunca se guardou de
onde ela veio. O que fecha isso é o `perfil_comparecimento_abstencao_2022` do
TSE, recorte ZZ. Não bloqueia nada; melhora a defesa do número.

---

## 7. O que falta (resumo do `PENDENCIAS.md`)

1. **Mesários** — o único item que pode desfazer o desenho no dia. 109 nomeados
   para 112 lugares, 83 confirmados. As duas lacunas críticas são **MRV 24**
   (588 esperados, a 2ª maior carga) e **MRV 11** (504 esperados, sem
   Presidente). Por onde começar a ligar: MRV 24, depois MRV 11.
2. **Decisão D9** — quem identifica e como os cadernos são divididos. É a única
   decisão de fluxo sem opção vigente (`docs/decisoes_em_aberto.md`). Não muda
   o orçamento; muda a equipe e o treinamento.
3. **Orçamento final** — cotar portaloos, walkie-talkies, fita de piso (C16),
   painéis de soleira (C8) e placas por mesa (C9); reavaliar as quatro linhas
   do Ring 3.
4. **Comunicação com mesários** (item 4) — sem plano; a de eleitores (item 3)
   agora tem a estratégia de redes sociais.
5. **Refazer o dimensionamento de filas** contra as zonas de 16/09.
6. **Apresentação final do projeto** como um todo coerente (item 1).

---

## 8. Como este repositório chegou a este estado

O trabalho nasceu em **`hamadmkalaf/eleicoes2026`** e cresceu espalhado por
**29 branches e 10 PRs abertos**. Em 16/09/2026 duas transferências paralelas
tentaram resolver isso, e cada uma virou uma branch deste repositório. Em
**17/09/2026** as três branches vivas foram mescladas em `main`:

| Branch | Commits | O que trouxe |
|---|---|---|
| `claude/transfer-eleicoes-repos-peglu5` | 7 | a **consolidação integral**: 284 arquivos, geradores, simulador, dashboard, artefatos publicados, sinalização v2 e os roteiros de `transferencia/` |
| `claude/eloquent-rubin-6i0uoe` | 2 | a **transferência curada** do Hall 2: 66 arquivos escolhidos item a item, com "avisos de safra" no cabeçalho do que está superado, o editor refeito contra a cadeia nova e a CI das conferências |
| `claude/focused-dijkstra-2z3hk9` | 2 | a estratégia de comunicação em redes sociais (.md e .docx) |

As duas primeiras são **leituras concorrentes do mesmo material** e colidiram
em 14 arquivos. A resolução, arquivo a arquivo, está no corpo do commit de
merge; o critério foi:

- **ficou a versão integral** onde ela carrega anotação que a curada não tem
  (`README.md`, `contexto_eleicoes_dublin_2026.md`,
  `handoff_agregacao_dublin_2026.md`, `CONFERENCIA_PRANCHETA_2026-09-15.md`);
- **ficou a versão curada** onde ela é mais nova: o `CLAUDE.md` do repositório
  vigente (contra uma cópia que ainda descrevia o repositório antigo), os
  avisos de safra e as decisões de 14/09 em `DOCUMENTACAO_PROJETO.md`,
  `orcamento_final.md`, `plano_filas_tres_portas.md` e
  `saidas/analise_gargalos.md`, e o editor (`scripts/gera_editor.py`,
  `scripts/editor_template.html`, `saidas/editor.html`);
- **nada foi descartado**: o `CLAUDE.md` antigo virou
  `docs/CLAUDE_origem_eleicoes2026.md`, o `PENDENCIAS` sem extensão foi fundido
  em `PENDENCIAS.md`, e o manifesto curado virou
  `transferencia/TRANSFERENCIA_HALL2_2026-09-16.md`.

**Verificação feita sobre a árvore mesclada, em 17/09:**

| Verificação | Resultado |
|---|---|
| `scripts/confere_prancheta.py` | **passa** — "nenhuma divergência: a prancheta reproduz as três fontes oficiais"; 4 observações, todas sobre mesários faltando |
| `scripts/confere_arranjo.py` | **passa** — "todos os itens atendidos", os sete itens do arranjo |
| `scripts/sinalizacao_v2.py` | regenera **byte a byte**; imprime `TOTAL 1820.0` na faixa [1700, 1900] |
| `simulador/teste_modelo.js`, `teste_arranjos.js` | passam |
| `simulador/teste_portas.js` | 140/144 — 4 falhas herdadas, do Ring 3 (§6.4) |

O repositório antigo fica como **arquivo**; não receba commits nele.

---

## 9. Regras práticas para quem for trabalhar aqui

1. **Não edite `data/decisoes.json` à mão.** Ele é gerado em duas camadas
   (mesas, depois layout). Edição manual sobrevive até a próxima rodada — ou,
   pior, fica e as conferências passam a mentir.
2. **Não mexa na agregação de seções.** Os pares são do Cartório Eleitoral e os
   109 mesários já foram nomeados em cima dela. Mudar invalida a nomeação.
3. **Não commite sem rodar as duas conferências**, se o commit toca em dados ou
   arranjo.
4. **Não renomeie nada em `data/raw/`** e não mova `scripts/` — os parsers
   abrem pelo nome literal e os caminhos saem de `parent.parent`. Os CSVs estão
   em **latin-1** com separador `;`: não "normalize" para UTF-8.
5. **Toda saída em `saidas/` é gerada.** Editar HTML ou SVG à mão se perde na
   próxima geração.
6. **Peça gerada antes de 15/09/2026 carrega número errado** — a atribuição
   mesa → entrada por cota do Ring 3 e a numeração eleitor antiga. Trazer uma
   dessas sem regerar é trazer número errado para dentro.
7. **`saidas/Dublin_2026_agregacoes.xlsx` nunca sai byte a byte** (o formato
   grava a data): compare abas, não bytes.
8. **O repositório deve ser privado.** Ele reúne planta, barreiras, staff e
   orçamento de um local de votação com data e hora públicas. Foi criado
   público; mudar em *Settings*. Nenhum dos dados identifica eleitores — são
   contagens por seção —, mas o conjunto é sensível como plano de segurança.
9. **Uma branch só, com merge de volta.** A divergência que obrigou a esta
   consolidação nasceu de branch por sessão sem merge.
