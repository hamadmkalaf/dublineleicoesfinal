# Memória do projeto — Eleições 2026, Posto de Dublin

Organização logística do 1º turno (04/10/2026, 8h–17h) e do eventual 2º turno
(25/10/2026) na jurisdição de Dublin. Documentos em português.

Este repositório é o **final**: carrega as versões vigentes de dois temas
transferidos do repositório de trabalho `hamadmkalaf/eleicoes2026`, e só o que é
necessário para chegar a elas.

| Tema | Onde vive | Estado |
|---|---|---|
| **Voluntários de apoio e fluxo do eleitor** | `docs/voluntarios/` · `mapa/voluntarios_postos.html` | os 17 postos e os 4 cenários de efetivo |
| **Separadores de fila e fita no chão no Hall 2** | `docs/separadores/` · `scripts/separadores_fila.py` | desenho definitivo de 17/09, fechado |
| **Artefatos** — rota, prancheta, Ring 3, sinalização | `mapa/` · manifesto em `mapa/artefatos.json` | fonte versionada, não só a URL |
| **Artes para o eleitor** (feed, 1080 × 1080) | `docs/artes_eleitor.md` · `scripts/artes_eleitor.py` → `saidas/artes/` | 4 peças; o logotipo ainda é marcação de lugar |

---

## Fatos fixos

| Item | Valor | Fonte |
|---|---|---|
| Eleitores aptos | 16.794 | `saidas/dados.json`, dos CSVs oficiais do TSE |
| Seções / urnas | 51 seções agregadas em 28 urnas | idem |
| Residentes em Dublin / interior | 12.581 / 4.213 | idem |
| Comparecimento esperado | **11.499** (base B: taxa de 2022 do condado de origem por seção) | prancheta `Paredes_ABC`, 15/09 |
| Local | RDS, Merrion Road, Ballsbridge, Dublin 4 | contrato |
| Segurança contratada | 20 pessoas, 7h30–17h30, + 1 na véspera | orçamento (EUR 6.774,84) |

## Geometria do local (planta de 16/09/2026)

O Ring 3 como pátio de fila está **confirmado** (18/09), com as **três zonas iguais**.
A montagem — 23 raias por zona, vão de 1,20 m, ~180 CCBs dos 200 em estoque, 506 m de
fita grossa, lotação 2.118 (706 por zona) — está em `mapa/ring3_montagem.html` e no
`Mapa-Ring3` de `mapa/sinalizacao/`. **A folha de montagem desenha as zonas desiguais
(12,23 / 14,14 / 12,23 m): nesse ponto ela está superada.** A soma das três não muda —
38,6 m —, então nenhuma conta que dependa do total se altera.

O percurso tem três trechos físicos distintos. **Ring 3 é o pátio de fila ao ar
livre; Hall 2 é o salão de votação.**

**Ring 3 — pátio de fila.** Recinto ao ar livre de gradil permanente, 44,0 × 35,0 m,
ao sul do Hall 2. Entrada única pelo **canto nordeste**. Um **corredor de chegada de
3,0 m** desce pelo lado leste; um **trecho de fundo de 3,0 m** corre na base e
distribui para as três zonas. Zonas lado a lado, separadas por vãos de 1,20 m e
**iguais entre si: 12,87 m cada** — C a leste, a primeira que se alcança; B ao centro;
A a oeste, a mais distante. As larguras saem do esperado por entrada de `Paredes_ABC`,
e dão **706 pessoas de lotação por zona**. Cada zona tem **23 raias** ao longo de 32,0 m
(passo de 1,39 m). A fila avança de baixo para cima; a cabeça de cada zona fica no
topo, voltada para o Hall.

**Apron.** Faixa pavimentada de **14,0 m** entre a cabeça das filas e a fachada sul
do Hall 2. Espaço de travessia, sem raias.

**Hall 2 — salão de votação.** Portas na fachada sul: **S4 = entrada A, S5 = entrada
B, S6 = entrada C, S7 = preferencial**; **S2 e S8 são saídas**; S1, S3 e S9 ficam
livres. As 28 mesas ficam encostadas nas paredes: **parede oeste = zona A (9 urnas),
parede norte = zona B (9 urnas), parede leste = zona C (10 urnas)**. Sala de apoio no
canto noroeste. Faixa livre de 3 m junto à parede leste para as saídas de emergência
L1–L4. Portas O1 e N1 fechadas; O2, N2 e H1 livres. Serpentinas internas de 20
pessoas nas três mesas maiores (3313, 3315, 3322).

Correspondência que amarra tudo: **zona do Ring → porta do Hall → parede do salão**,
com a mesma letra em toda a rota.

| Zona | Ring 3 | Porta | Parede | Urnas | Aptos | Comparecimento esperado |
|---|---|---|---|---|---|---|
| A | oeste (12,87 m) | S4 | oeste | 9 | 5.695 | 3.834 |
| B | centro (12,87 m) | S5 | norte | 9 | 5.600 | 3.832 |
| C | leste (12,87 m) | S6 | leste | 10 | 5.499 | 3.833 |

Spread de 0,05% pela base B, com uma das três urnas grandes (3313, 3315, 3322) em
cada zona. A distribuição está equilibrada; não mexer sem refazer a conta.
`scripts/zonas_balanceadas.py` confere a composição com um estimador mais grosso
(74%/50%), que chega a 3.860 / 3.755 / 3.802 — mesma conclusão, 2% de diferença.

A rota também tem os pontos **P0 a P7** do plano de sinalização: **P0** é a mesa
"descubra sua seção" na calçada da Merrion Road, **fora** do portão. Depois do
portão toda peça pressupõe a seção conhecida, então P0 é o único ponto que resolve
quem chega sem o número.

## Cenários de efetivo de voluntários (decisão de 17/09/2026)

Quatro cenários, numerados por quantas pessoas de apoio existem. **C4 é referência de
teto, não meta de recrutamento** — o Posto não o considera realista para 2026.

| | Pessoas no pico | Postos ocupados (de 17) | Turnos e reserva |
|---|---|---|---|
| **C1 · Contingência** | 9 — o efetivo de hoje | 5 | não |
| **C2 · Próximo degrau** | 15 | 7 | não |
| **C3 · Operacional** | 24 | 13 | não |
| **C4 · Pleno** | 49 (43 postos + 15% de reserva) | 17 | sim, 61 escaladas |

Histórico do efetivo: eram 25 voluntários; 14 foram cedidos para cobrir dispensas de
mesário e **não voltam** — mesário é função nomeada, com treinamento próprio. Campanha
de reserva em curso.

**C1 (9):** 3 no P0 da calçada, 1 no trecho de fundo do Ring (R3), 1 na porta
preferencial S7 (A3), 3 nas mesas vermelhas (H3) e 1 na coordenação (T1).

**C2 (15)** acrescenta o quarto operador do P0, as três cabeças de fila (R5, uma por
zona) e duas bocas do trecho de fundo (R2, zonas C e A).

O preenchimento é uma **fila contínua da posição 10 à 49**, para funcionar com
qualquer número intermediário — com 13 pessoas preenche-se até a posição 13, com 17 até
a 17. A fila está em `docs/voluntarios/lista_postos.md` e em
`mapa/voluntarios_postos.html`.

C1 e C2 só fecham com três compensações contratadas: os 20 seguranças assumindo
presença de fila por escrito no briefing, uma CCB de separação no apron no lugar do
posto A1, e a campanha "descubra sua seção antes de sair de casa".

## Regras do tema dos separadores de fila

- **Leia `docs/separadores/contexto.md` antes de tocar na geometria.** As três
  decisões de 17/09 e a regra *"as avenidas levam para dentro; as bandas trazem para
  fora"* são o que sustenta o desenho inteiro.
- **Nunca edite `data/decisoes.json`, `data/prancheta_hall2.json` nem
  `cenarios/paredes-abc-20260915.json` a partir deste tema.** Eles são **lidos**, não
  escritos. Pertencem ao arranjo do Hall 2, e editá-los à mão quebra as conferências.
- **A conferência das avenidas sai com código 1** quando a geometria quebra. Rode
  `python3 scripts/separadores_fila.py` (sem `--grava`) antes de qualquer commit que
  toque em `AVENIDAS`, `BANDA_PAREDE` ou nas zonas protegidas. Sem `--grava` ele não
  escreve nada e já serve de teste em integração contínua.
- As constantes que mudam tudo estão no topo de `scripts/separadores_fila.py`:
  `VAO_POSTE`, `BANDA_PAREDE`, `LARG_CANAL`, `PASSO_FILA`, `CORES_ZONA`,
  `ESTOQUE_FITA`.
- **Rotular sempre por grupo de mesas e por seção, nunca por número de mesa.** O
  eleitor sabe a sua seção; não sabe que mesa é a sua.
- Três armadilhas conhecidas: mudar uma banda e esquecer a fita; contar a boca da
  avenida B duas vezes (ela entra inteira, não leva item de boca); e rotular por
  número de mesa. As três estão descritas em `docs/separadores/contexto.md`.

## Regras das artes para o eleitor

- **Nada de conteúdo novo.** Cada número, data e frase das artes sai de fonte já
  versionada aqui — `CLAUDE.md`, o briefing de 23/09, `P1-Portao.dc.html` e
  `data/prancheta_hall2.json`. A procedência está tabelada em `docs/artes_eleitor.md`.
- **A conferência sai com código 1** quando a tabela mestra deixa de ter 51 seções
  ou discorda das bocas de zona. Rode `python3 scripts/artes_eleitor.py --confere`
  antes de qualquer commit que toque em `mapa/sinalizacao/`.
- **A letra identifica a fila; a cor é apoio** — a regra de `Main.dc.html` vale
  também para a peça pública. A cor da porta é a cor da fita comprada:
  A `#33507E`, B `#E8C63A`, C `#DE7343`.
- **O logotipo das artes é marcação de lugar.** A arte oficial em vetor tem de vir
  do TSE, com a fonte da campanha e a autorização de uso da marca por posto no
  exterior. Não publicar sem trocar.
- **Divergência aberta sobre a porta preferencial:** as artes e o briefing de
  23/09 dizem "a porta à direita da C" (S7); a peça `P5-Preferencial`, de 17/09,
  diz "qualquer porta". As duas não podem ir para a rua juntas.

## Convenções

- Números de eleitorado vêm sempre de `saidas/dados.json` (CSV oficial), nunca do
  PNG do mapa de agregações do TSE, que tem erro de digitação conhecido (seção 3752
  listada sob a principal 3222; a correta é 3322).
- Premissas não observadas (fator de pico, tempo por eleitor, permanência média)
  são rotuladas como premissas no texto.
- Voluntário orienta, não decide: não toca em documento, não confere título, não
  diz a ninguém se pode votar. Identificação é monopólio legal do mesário.
- **Um branch só, com merge de volta.** A confusão no repositório de origem teve
  causa conhecida: cada sessão trabalhou num branch próprio e nenhuma mesclou de
  volta, e o sintoma mais caro foi um gerador lendo um `decisoes.json` que outro
  branch já havia superado.

## Pendências que movem números

1. **O RDS permite fita adesiva no piso do Hall 2?** Bloqueante: se não, o desenho
   dos separadores cai inteiro, e as 100 unifilas passariam a ter de fazer sozinhas
   um trabalho de 395.
2. Método de identificação do eleitor — eletrônico/biométrico ou caderno físico
   (`PENDENCIAS.md` item 5). Decide tempo por eleitor e criticidade do balcão de
   consulta.
3. Confirmação da expectativa de comparecimento.
4. Orçamento final, incluindo o apoio ao voluntariado (~EUR 1.700–1.900), as 15
   unifilas adicionais (EUR 195,45) e os 8 rolos de fita.

A lista completa e por tema está em `PENDENCIAS.md` e nas seções finais dos dois
contextos.
