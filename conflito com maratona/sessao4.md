# Sessão 4 — Conflito do 2º turno (25/10/2026) com a Maratona de Dublin

Registro para retomar em outra sessão. Sessão de 13/10/2026. Branch: `conflitomaratona`.
PR rascunho: https://github.com/hamadmkalaf/dublineleicoesfinal/pull/29. Continuação de
`sessao3.md`.

## 1. O que foi pedido e o que foi entregue

| Pedido | Entregue | Onde |
|---|---|---|
| Ler `sessao3.md` e verificar se a base confere com o PDF "Dublin Bus Diversions Document" | Feito: confronto linha a linha com o aviso público de 07/10 e com as afirmações da base | §2–§5 |
| Atualizar a sessão | Este registro, o PDF versionado e um ponteiro no fim de `sessao3.md` | — |

**Nenhum documento de análise foi corrigido** (`divergencias_garda_dublinbus.md`,
`ranking_linhas_rds.md`, mapa). As correções estão em §6 e somam às da `sessao3` §5.

## 2. A fonte nova

`Dublin Bus - Diversions Document (2026-10-12).pdf` — 21 páginas, documento Word gerado em
12/10/2026 às 12h48 UTC (autor "GIT&T"). É o **documento operacional interno** da Dublin Bus
(instruções a controladores e inspetores), não o aviso ao público. A base usava o aviso
público "Dublin Marathon 2026" de 07/10 (`diversions_dublinmarathon.pdf`), que é uma
reescrita deste.

O próprio documento avisa: "Times for the implementation and removal of diversions are a
guide and may vary on the day". Regra geral do documento: **desvios a partir das 8h até a
reabertura pela Garda, salvo indicação em contrário na linha.**

O texto é extraível com `pdftotext`; três páginas têm imagens (p. 8: terminal da 39A na
parada 771; p. 18: bus gate de Crumlin Road; p. 1: logotipo).

## 3. O que confere com a base

Rota a rota, o documento de 12/10 diz o mesmo que o aviso de 07/10 em tudo o que a base usa:

| Linha | Afirmação da base | Documento de 12/10 |
|---|---|---|
| 7/7A | Desviadas por Strand Road desde as 8h, sem janela | Confere (sem hora própria → 8h) |
| E1 | Até 11h só Bray ↔ Sussex Road; depois rota inteira pelo corredor | Confere |
| E2 | Até 11h só Harristown ↔ Nassau St; shuttle Dún Laoghaire ↔ Stillorgan SC 6h–11h | Confere (ver §5, item 2) |
| 39A | Até 11h Ongar ↔ Luke St; depois cidade ↔ parada 771 (Teresian School) | Confere; a p. 8 explica: termina na 771 "due to Belfield Closure" |
| 11 / 11B | 11 sem serviço antes das 11h; ambas pelo corredor Leeson St–Donnybrook depois | Confere |
| 14 | Até 11h Dundrum ↔ Adelaide Rd via Stillorgan Rd e Donnybrook Rd; sem lado norte | Confere |
| 44 | Desviada por Morehampton Rd e Stillorgan Rd o dia todo | Confere |
| 47 | Desviada por Mount Merrion Ave, Rock Rd e Merrion Gates desde as 8h | Confere |
| S2 | Sem serviço até 10h30; após 11h termina em Burlington Mews | Confere |
| 37, 38, 38A, 39, 70 | Terminam no centro | Confere (Luke St; a 70 após 11h termina em Townsend St — a base generaliza "Luke Street", sem efeito) |
| C1–C4 | Não chegam a Sandymount antes das 11h | Confere (Wolfe Tone Quay até 11h) |
| Pré e pós-corrida | Merrion Square fechada sexta 10h, sábado e segunda até 18h | Confere |

**A divergência 2.1 (prefeitura "E1, E2 e 39A ao longo do dia") continua de pé**: o texto
de 12/10 mantém E2 e 39A fora de Donnybrook antes das 11h.

## 4. O que muda: a linha 4 provavelmente não passa pelo RDS em momento algum

**A base diz** (ranking, Nível 3, item 8; divergências 1.1; `sessao2` §2.4; `sessao3` §3;
mapa): a 4 segue a rota normal pela Merrion Road até 11h, com primeiros ônibus no RDS às
8h20 e 8h24 e "3 a 4 ônibus por sentido antes do fechamento"; daí a terceira hora para a
Merrion Road ("11h pela Dublin Bus").

**O documento de 12/10 diz:** "{until 1100hrs this route will operate to and from Townsend
Street}", seguido do desvio por Pearse St, Ringsend, Sandymount e Strand Road até Merrion
Gates, **sem hora própria**. Pela regra geral do documento, sem hora própria vale **8h**. O
texto da 4 é palavra por palavra o da 7/7A, que a base já trata como desviada desde as 8h.

**Leitura coerente (inferência, a confirmar):** a partir das 8h a 4 faz Monkstown → Merrion
Gates → Strand Road → Ringsend → Pearse St, e até 11h termina em Townsend St em vez de
seguir para Heuston. O "11h" é a hora do **encurtamento no centro**, não da Merrion Road.

**Por que a leitura da base não se sustenta fisicamente.** No GTFS da NTA (feed baixado em
13/10), a 4 faz exatamente o mesmo trajeto da 7 entre o centro e Merrion Gates: Merrion Sq
North → Holles St → **Mount Street Lower** → Mount Street Bridge → **Northumberland Road**
(parada Haddington Road) → Lansdowne Road → RDS (416/485) → Merrion Road. Pela página do
organizador de 13/10 (`sessao3` §3–§4), Mount Street Lower fecha **3h30–17h30** e
Northumberland Road **3h30–20h30 / 6h–18h30**; Merrion Square Sul e Leste estão fechadas
desde sexta. A 4 não tem como ir de Townsend St ao RDS pela "rota normal" na manhã da
corrida. No sentido cidade, o próprio documento a desvia **em Merrion Gates**, antes do RDS.

**De onde veio o erro:** o aviso público de 07/10 põe o desvio por Strand Road sob um
subtítulo "From 11.00hrs" e, sob "Until 11.00hrs", escreve "Depart Townsend Street and back
on to normal route". A base leu isso como "rota normal pela Merrion Road até 11h". O
documento operacional não tem esse subtítulo. **Onde os dois divergem, o operacional, mais
novo e de quem executa o desvio, deve prevalecer** — mas é inferência; vai como pergunta
à Dublin Bus.

**Consequências:**

- A linha 4 passa de ◐ para **○** no ranking, junto com a 7/7A. Nenhuma linha passa na porta
  do RDS no dia.
- A divergência 1.1 deixa de ser "9h25 × 10h × 11h": a Dublin Bus **não dá hora** para a
  Merrion Road. Ficam duas fontes: organizador 9h25 e Garda 10h. O plano 9h25–17h30 não
  muda.
- O pedido 8 à Garda (tolerância para a 4 entre 9h25/9h40 e 11h) **perde o objeto**. O
  pedido 2 à Dublin Bus vira: "confirmem que a 4 é desviada por Strand Road desde as 8h e
  não passa pelo RDS".
- **Mensagem ao eleitor: nenhuma mudança** — a base já recomendava não anunciar a 4. O que
  muda é o mapa e o ranking, que hoje mostram a 4 pela Merrion Road no cenário "até 11h".

## 5. Informação nova ou ambígua no documento

1. **Largada às 8h45** ("Race Start time 08:45hrs"). Segunda fonte para a hora que a
   `sessao3` §4 dava como de fonte única (TFI). O 8h40 dos cadeirantes segue só no TFI.
2. **E2: subtítulo "Route E2 after 1030hrs"**, mas o texto abaixo diz "From 1100hrs". Pode
   ser só erro de digitação; se não for, a E2 voltaria a Donnybrook 30 min antes. Perguntar.
3. **Tabela de terminais provisórios (p. 19) põe a E2 e a 11 em Sussex Road desde as 8h.**
   Contradiz o texto (E2 termina em Nassau Street; a 11 não roda antes das 11h). A tabela se
   chama "Monday Race Day" e omite a 4 em Townsend St: é modelo reaproveitado de outro ano e
   não deve ser usada. **Especulação:** uma leitura dessa tabela ("E2 até Sussex Road") pode
   explicar a resposta da prefeitura de "E1, E2 e 39A ao longo do dia".
4. **Inspetor na parada 771 (Teresian School) "from 1000hrs to race finish"** para o
   terminal da 39A, embora o texto ponha a 39A ali só após 11h. Pode ser só posicionamento
   antecipado. Perguntar se a 39A chega antes das 11h.
5. **E1 e E2 "not to use flyover at Belfield until 17:00hrs".** Terceira fonte para o
   viaduto da UCD fechado até 17h (organizador: 9h30–17h; Garda: viaduto no percurso).
   Confirma a divergência 1.7. Os ônibus passam por baixo; as paradas de Donnybrook não
   mudam.
6. A lista "Road Reopen Times" (p. 21) traz Pembroke Rd, Fosters Avenue, Clonskeagh Rd,
   Milltown, Orwell Rd — **sem horários** e sem a Merrion Road.
7. A Garda responsável pela área do RDS aparece como "Milltown to Pembroke Road" e
   "Clonskeagh to Belfield"; o comandante geral é "TBC".

## 6. Correções pendentes na base (somam às da `sessao3` §5; não aplicadas)

| Arquivo | Trecho | Dizia | Passa a dizer |
|---|---|---|---|
| `ranking_linhas_rds.md` | Nível 3, item 8 (linha 4) | ◐; nível A; primeiros ônibus no RDS 8h20/8h24; 3–4 ônibus antes do fechamento | ○; desviada por Strand Road desde as 8h (documento operacional de 12/10); até 11h termina em Townsend St; não passa pelo RDS |
| idem | §1, fontes | aviso de 07/10 | acrescentar o documento operacional de 12/10 |
| `divergencias_garda_dublinbus.md` | 1.1 | Dublin Bus mantém a 4 pela Merrion Road até 11h | Dublin Bus não dá hora para a Merrion Road; a 4 é desviada desde as 8h; a divergência fica organizador × Garda |
| idem | 1.2 | "a 4 também nos dois sentidos após 11h" | desde as 8h |
| idem | 1.7 | — | acrescentar: E1/E2 sem o viaduto de Belfield até 17h (terceira fonte) |
| idem | §6, pedido 2 | última viagem da 4 pelo RDS | confirmar que a 4 é desviada desde as 8h; E2 "after 1030hrs"; 39A na 771 a partir das 10h?; tabela de terminais (E2/11 em Sussex Road) |
| idem | §6, pedido 8 | tolerância para a 4 | retirar |
| `sessao2.md` §2.4 e `sessao3.md` §3 | Merrion Road | "três horas: 9h25 × 10h × 11h" | duas horas: 9h25 (organizador) × 10h (Garda) |
| `scripts/transporte_mapa_linhas.py` e `mapa/linhas_maratona.html` | cenário "até 11h", legenda e parada 416 | "Linha 4 pela Merrion Road (até o fechamento, 9h40–11h)"; "linha 4 só até ~10h" | a 4 desviada por Strand Road nos três cenários do dia; somar à correção de horários da `sessao3` §5 |

## 7. Pendências (somam às da `sessao3` §6)

1. **Aplicar as correções de §6 e da `sessao3` §5.** Fazer junto, porque tocam os mesmos
   trechos.
2. **Perguntar à Dublin Bus** (substitui o pedido 2 da `sessao2` §6): a 4 desviada desde as
   8h?; E2 "after 1030hrs" ou 11h?; 39A na 771 desde as 10h?; a tabela de terminais vale?
3. Reconferir o documento operacional na semana da eleição ("times are a guide").

## 8. Arquivos criados ou alterados nesta sessão

| Arquivo | O que é |
|---|---|
| `conflito com maratona/Dublin Bus - Diversions Document (2026-10-12).pdf` | Fonte nova: documento operacional da Dublin Bus, 12/10/2026. |
| `conflito com maratona/sessao4.md` | Este registro. |
| `conflito com maratona/sessao3.md` | Ganhou a §9 com o ponteiro para esta sessão. |

## 9. Notas de ambiente

- O branch local estava atrás do remoto no início da sessão (só `sessao1.md`); foi preciso
  `git pull origin conflitomaratona` para ver `sessao2.md` e `sessao3.md`.
- O GTFS da Dublin Bus (`GTFS_Dublin_Bus.zip`, 40 MB) baixou normalmente; a sequência de
  paradas da 4 e da 7 saiu de `trips.txt` + `stop_times.txt` + `stops.txt`.
