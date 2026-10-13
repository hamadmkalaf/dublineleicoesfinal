# Sessão 3 — Conflito do 2º turno (25/10/2026) com a Maratona de Dublin

Registro para retomar em outra sessão. Sessão de 13/10/2026. Branch: `conflitomaratona`.
PR rascunho: https://github.com/hamadmkalaf/dublineleicoesfinal/pull/29. Continuação de
`sessao2.md`.

## 1. O que foi pedido e o que foi entregue

| Pedido | Entregue | Onde |
|---|---|---|
| Ler `sessao2.md` e verificar se a base confere com a página "Road Closures" do organizador (PDF capturado em 13/10, 14h51) | Feito: confronto via a via, abaixo | §2–§4 |
| Atualizar a sessão | Este registro, o PDF versionado e um ponteiro no fim de `sessao2.md` | — |

**Nenhum documento de análise foi corrigido ainda** (`divergencias_garda_dublinbus.md`,
`ranking_linhas_rds.md`, mapa). A lista do que corrigir está em §5.

## 2. A fonte nova

`Road Closures - Irish Life Dublin Marathon (2026-10-13).pdf` — impressão de
`irishlifedublinmarathon.ie/road-closures/`, 5 páginas. **As tabelas são imagens** (o
`pdftotext` não as lê; foram extraídas com `pdfimages` e lidas uma a uma). Duas tabelas:

- *Local street closures* (3 partes): centro, área da largada e da chegada.
- *Marathon route closures, Sunday 25 October 2026* (4 partes): o percurso.

É a página **de 2026**: data 25/10, montagem a partir de sexta 23/10. Confirma o que a
`sessao2` §2.8 dizia da página de tráfego salva em 07/10
(`Traffic Information - Irish Life Dublin Marathon.pdf`): aquela era texto de 2025
("Friday 24th", "October 26th"). **A página de 07/10 fica superada por esta, inclusive nos
horários**, e era dela que a base tirava o "9h40" e o "6h–18h30". A página avisa que os
horários estão "subject to change".

## 3. Divergências encontradas, por impacto no RDS

| Via | Base (página de 07/10, texto de 2025) | PDF de 13/10 | Consequência |
|---|---|---|---|
| **Merrion Road** (só sentido cidade) | 9h40–17h30 | **9h25–17h30** | 15 min mais cedo. Três fontes, três horas: **9h25** organizador × 10h Garda × 11h Dublin Bus (diferença de 1h35). Pela regra da hora mais cedo (divergências 1.3), o plano passa a **9h25–17h30**. A linha 4 vale só para quem chega até ~9h15. |
| **Nutley Lane** | 9h40–17h | **8h40–17h** | 1 h mais cedo; fica perto da Dublin Bus (47 desviada desde 8h). A divergência 1.5 agora é só com a Garda (10h). |
| **Northumberland Road** | 6h–18h30, um trecho | **Dois trechos:** Haddington Rd → Mount St Lower **3h30–20h30**; Haddington Rd → Lansdowne Rd 6h–18h30 | Reforça a divergência 1.6: a hora da Garda (10h) não se sustenta. |
| **Foster's Avenue** | "in bound only under Garda traffic" | **"both sides"**, 9h10–16h30 | Fechada nos dois sentidos. Ver §4, item 3. |
| **Stillorgan Rd (N11), corredor de ônibus**, 1º trecho | 9h30–16h30 | **9h15**–16h30 | 2º trecho e viaduto da UCD seguem 9h30–17h. Confirma que só o corredor fecha (divergência 1.7). |
| Milltown Rd / Dartry Rd / Orwell Rd e Orwell Park | 9h25 / 9h25 / 8h45 | 9h10 / **8h** / 8h | Marginal: 14/44/11 já são desviadas pela Dublin Bus. |
| Terenure Rd East / Fortfield / Templeogue / Kimmage Rd West | 9h15 / 9h10 / 9h10 / 9h | 9h / 9h / 9h / 8h | Fora da área do RDS. |
| St Stephen's Green South | 7h–10h30 | Percurso 8h15–10h30; tabela local 7h–11h | Fora da área do RDS. |

**O que confere:** data 25/10/2026; Leeson Street Lower 3h30–13h (divergências 1.3);
reabertura da Merrion Road às 17h30, cobrindo toda a votação; **Donnybrook Road,
Morehampton Road, Leeson Street Upper, Anglesea Road e Simmonscourt Road não aparecem**,
coerente com a Garda ("abertas o dia todo") e com a rota a pé Donnybrook → Anglesea.
Ausência na lista não é prova de abertura.

**Efeito na mensagem ao eleitor:** nenhum. "E1 (após 11h também E2 e 39A), descer em
Donnybrook, caminhar pela Anglesea Road" continua valendo; a linha 4 fica ainda menos
anunciável.

## 4. O que o PDF não resolve

1. **Shelbourne Road, Haddington Road e Pembroke Road** (a Garda fecha às 10h) não estão na
   lista; nem Rock Road, Merrion Gates e Strand Road; nem Mount Street Upper (a chegada).
   Mount Street Lower está (3h30–17h30) e Mount Street Crescent fecha desde sábado 6h.
2. **Hora da largada** não aparece. O 8h40 (cadeirantes) / 8h45 (onda 1) segue com fonte
   única, a página do evento no TFI.
3. **Foster's Avenue fechada nos dois sentidos** pode afetar a orientação da Garda para
   quem vem de carro do norte ("Strand Road até Booterstown e volta pela N11"), se o
   retorno usar Foster's Avenue. **Especulação: o trajeto não foi medido.** Vira pergunta
   à Garda.
4. A nota "N11 open both ways as runners pass over the UCD flyover", que estava na página
   de 07/10, não aparece no PDF de hoje. Pode só não ter sido impressa (o PDF traz só as
   tabelas).

## 5. Correções pendentes na base (não feitas nesta sessão)

| Arquivo | Trecho | Dizia | Passa a dizer |
|---|---|---|---|
| `sessao2.md` | §2.4 e §5 | Merrion Road 9h40 (organizador); "para o plano, 9h40 a 17h30" | 9h25; plano 9h25–17h30 |
| `divergencias_garda_dublinbus.md` | 1.1 | organizador 9h40; pedir tolerância 9h40–11h | 9h25; tolerância 9h25–11h |
| idem | 1.5 e 3.3 | Nutley Lane 9h40–17h | 8h40–17h |
| idem | 1.6 e 3.4 | Northumberland Road 6h–18h30 | dois trechos: 3h30–20h30 e 6h–18h30 |
| idem | 3.2 | Merrion Road 9h40–17h30 | 9h25–17h30 |
| idem | 3.5 | N11 bus lane 9h30–17h | 9h15–16h30 e 9h30–17h |
| idem | seção 3 (cabeçalho) e lista de fontes | página de tráfego salva em 07/10 | página "Road Closures" de 13/10; a de 07/10 fica superada |
| idem | §6, pedido 8 | tolerância para a 4 entre 9h40 e 11h | entre 9h25 e 11h |
| idem | §6 (novo pedido à Garda) | — | Foster's Avenue fechada nos dois sentidos afeta o retorno pela N11 de quem vem do norte? |
| `ranking_linhas_rds.md` | linha 123 (linha 4) | "o organizador marca 9h40" | 9h25 |
| `scripts/transporte_mapa_linhas.py` e `mapa/linhas_maratona.html` | legenda e nota dos cenários | "9h40–11h", "Merrion Road fechada 9h40–17h30", "9h40 pelo organizador" | 9h25. Regenerar o mapa exige os intermediários não versionados (`sessao2` §9, item 1); se não der, editar o HTML e o gerador em paralelo. |

## 6. Pendências (somam às da `sessao2` §9)

1. **Aplicar as correções de §5.**
2. **Reconferir a página "Road Closures" na semana da eleição** (é "subject to change").
   O site respondeu ao navegador do usuário; ao robô, a página de tráfego deu desafio
   anti-robô na sessão 2.
3. **Pedido novo à Garda:** Foster's Avenue (§4, item 3) e, de novo, a hora de
   Northumberland Road, agora com o horário de 3h30 do organizador.
4. As pendências 1–7 da `sessao2` §9 seguem abertas; nenhuma foi resolvida nesta sessão.

## 7. Arquivos criados ou alterados nesta sessão

| Arquivo | O que é |
|---|---|
| `conflito com maratona/Road Closures - Irish Life Dublin Marathon (2026-10-13).pdf` | Fonte nova: página "Road Closures" do organizador, 13/10/2026. |
| `conflito com maratona/sessao3.md` | Este registro. |
| `conflito com maratona/sessao2.md` | Ganhou a §11 com o ponteiro para esta sessão. |

## 8. Notas de ambiente

- A `sessao2.md` só existia no remoto no início da sessão; foi preciso `git pull` do branch
  `conflitomaratona` antes de lê-la.
- As tabelas do PDF são imagens: `pdfimages -png` extrai as sete tabelas legíveis.

## 9. Sessão 4 (13/10/2026) — documento operacional da Dublin Bus

O "Dublin Bus Diversions Document" de 12/10
(`Dublin Bus - Diversions Document (2026-10-12).pdf`) confirma o aviso de 07/10 em quase
tudo, mas **a linha 4 provavelmente é desviada por Strand Road desde as 8h e não passa pelo
RDS**: o "até 11h" é o encurtamento em Townsend St, não a Merrion Road. Com isso, a Merrion
Road fica com duas horas (9h25 organizador × 10h Garda), não três. Também traz a largada às
8h45 e o viaduto de Belfield fechado para E1/E2 até 17h. Confronto e correções em
`sessao4.md`.
