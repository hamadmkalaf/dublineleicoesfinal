# Sessão 4 — Conflito do 2º turno (25/10/2026) com a Maratona de Dublin

Registro para retomar em outra sessão. Sessão de 13/10/2026. Branch: `conflitomaratona`.
PR rascunho: https://github.com/hamadmkalaf/dublineleicoesfinal/pull/29. Continuação de
`sessao3.md`.

## 1. O que foi pedido e o que foi entregue

| Pedido | Entregue | Onde |
|---|---|---|
| Ler `sessao3.md` e verificar a base contra o "Dublin Bus Diversions Document" (PDF) | Confronto linha a linha (§2–§3) | este registro |
| **"Refaça tudo. Ignore o horário de 11h passado pela Dublin Bus. Use o do organizador. Refaça o ranking e os mapas."** | Ranking, divergências e mapa refeitos com a regra do §4; GTFS novo, caminhadas remedidas, mapa reproduzível só com o repositório; correções pendentes da `sessao3` §5 aplicadas | `ranking_linhas_rds.md`, `divergencias_garda_dublinbus.md`, `mapa/linhas_maratona.html`, `dados/`, `scripts/` |

## 2. A fonte nova

`Dublin Bus - Diversions Document (2026-10-12).pdf` — 21 páginas, documento Word de 12/10
(autor "GIT&T"). É o **documento operacional interno** da Dublin Bus; a base usava o aviso
público de 07/10 (`diversions_dublinmarathon.pdf`), que é uma reescrita dele. Regra geral do
documento: desvios a partir das 8h, salvo indicação na linha; "times … are a guide".

## 3. Resultado do confronto (antes do refazer)

- **Confere** com a base em todos os trajetos: 7/7A, E1, E2 (e o shuttle 6h–11h), 39A (771
  "due to Belfield Closure"), 11, 11B, 14, 44, 47, S2, linhas que terminam no centro, C1–C4,
  pré e pós-corrida.
- **Linha 4:** o documento diz "until 1100hrs this route will operate to and from Townsend
  Street" e dá o desvio por Strand Road sem hora própria (= 8h), com texto idêntico ao da 7/7A.
  No GTFS a 4 usa o mesmo corredor da 7 (Merrion Sq N → Holles St → Mount St Lower →
  Northumberland Rd → RDS), fechado pelo organizador desde 3h30. **A 4 não passa pelo RDS no
  dia.** A versão de 07/10 a dava pela Merrion Road até 11h.
- **Novo:** largada às 8h45 (segunda fonte); E1/E2 sem o viaduto de Belfield até 17h; subtítulo
  "E2 after 1030hrs" contra texto "1100hrs"; inspetor na 771 desde 10h; tabela de terminais
  ("Monday Race Day") contraditória com o texto, não usar.

## 4. A regra adotada no refazer

**Todo horário de fechamento e reabertura vem do organizador** (página "Road Closures" de
13/10). **O "11h" da Dublin Bus não é usado** — nem para a Merrion Road nem para a volta das
linhas ao centro. A Dublin Bus fornece o **trajeto**; a hora em que ele fica possível é a da
reabertura, pelo organizador, das ruas que ele usa.

Aplicada linha a linha, a regra muda uma coisa grande: o trajeto que a Dublin Bus dá para E1,
E2, 39A, 11, 11B e 14 voltarem do centro a Donnybrook "from 1100hrs" passa por **Hatch Street
e Leeson Street Lower, que o organizador fecha das 3h30 às 13h**. Logo:

| | Versão de 07/10 | Agora (organizador) |
|---|---|---|
| Merrion Road | 9h40 (página de 2025) / 10h / 11h | **9h25–17h30** |
| Linha 4 no RDS | até 11h (3–4 ônibus/sentido) | **nenhuma viagem** (corredor fechado desde 3h30) |
| E1 | só do sul até 11h | **só do sul até 13h** (Bray ↔ Sussex Road) |
| E2, 39A, 11, 11B em Donnybrook | a partir de 11h | **a partir de 13h** |
| 14 | Dundrum ↔ Adelaide Rd até 11h | idem até 13h (não usa Hatch St) |
| 44 | o dia todo | parte do centro só a partir de 13h (usa Hatch St) |
| Janela crítica | 8h–11h | **8h–13h** |
| Cenários do mapa | normal · até 11h · após 11h | **normal · 8h–13h · 13h–17h** |

**Ressalva (premissa):** o organizador lista ruas inteiras. Se o bloqueio de Hatch St / Leeson
St Lower for só da área de largada, as linhas voltam antes. Virou o pedido 1 ao organizador e
o pedido 2 à Dublin Bus (`divergencias_garda_dublinbus.md` §5).

## 5. O que foi refeito

1. **GTFS:** feed da NTA com início em 12/10 (service_id de domingo 25/10 = 187). Janelas de
   frequência trocadas de 8–11h/11–17h para **8–13h/13–17h**. E1 em Donnybrook: 17 viagens por
   sentido de 8h a 13h (~17 min), 16 de 13h a 17h (~15 min).
2. **Caminhadas:** remedidas no OSRM; mesmos valores de 07/10 (±1 m). Nada muda.
3. **Ranking** (`ranking_linhas_rds.md`): reescrito. A 4 passa a ○. E2, 39A, 11, 11B passam a
   "a partir de 13h". Nova seção de fechamentos do organizador e de perguntas que podem mover
   o 13h. Capacidade: 8h–13h só a E1 (~315 lugares/hora/sentido, premissa) e a 14.
4. **Divergências** (`divergencias_garda_dublinbus.md`): reescrito com o organizador como
   referência. Saem a "terceira hora" da Merrion Road e o pedido de tolerância para a 4. Entram
   1.4 (Hatch St / Leeson St Lower × "from 1100hrs"), Foster's Avenue, largada às 8h45 e as
   contradições internas do documento da Dublin Bus.
5. **Mapa** (`mapa/linhas_maratona.html`, republicado em
   https://claude.ai/artifact/Wn9NNUuFZukE5sZp9L1W53, versão 1791901856-900f): cenários
   normal · 8h–13h · 13h–17h; 4/7/7A em cinza nos dois cenários do dia; tabela de caminhadas
   gerada do JSON; tabela nova de fechamentos do organizador. Conferido em captura (desktop claro
   e escuro, telefone 400 px; sem rolagem horizontal).
6. **Mapa reproduzível** (pendência 1 da `sessao2` §9, resolvida): `scripts/transporte_shapes_gtfs.py`
   grava `dados/shapes_linhas.json` (330 KB) a partir do GTFS; `dados/nom_rds.json` (polígono do
   RDS, OSM way 8106838) versionado; o gerador lê tudo de `conflito com maratona/dados/`.
7. **Correções da `sessao3` §5:** aplicadas pela reescrita (9h25, Nutley Lane 8h40, Northumberland
   em dois trechos, N11 9h15/9h30, fonte de 13/10). O gerador e o mapa não têm mais "9h40".

## 6. Pendências (substituem as da `sessao3` §6; somam às da `sessao2` §9 ainda abertas)

1. **Mandar os pedidos** de `divergencias_garda_dublinbus.md` §5. Os que movem a mensagem ao
   eleitor: 1 (organizador: Hatch St / Leeson St Lower), 2 e 3 (Dublin Bus: trajeto entre 11h e
   13h; E2/39A de manhã) e 7 (substituto do DART).
2. **Capacidade 8h–13h:** com só a E1 do sul, decidir entre transporte próprio, orientar o voto
   à tarde ou pedir reforço à Dublin Bus. A janela cresceu de 3 para 5 horas.
3. **Reconferir a página do organizador e o documento da Dublin Bus na semana da eleição.**
4. Da `sessao2` §9, seguem abertas: fixar o portão com o RDS (2), mensagem ao eleitor redigida
   e traduzida (4), sinalização desde a parada 774 (5), mapa simplificado para o eleitor (6).
   A 1 foi resolvida (§5, item 6); a 7 está no item 2 acima.

## 7. Arquivos criados ou alterados nesta sessão

| Arquivo | O que é |
|---|---|
| `conflito com maratona/Dublin Bus - Diversions Document (2026-10-12).pdf` | Fonte nova: documento operacional da Dublin Bus. |
| `conflito com maratona/ranking_linhas_rds.md` | Reescrito (§5, item 3). |
| `conflito com maratona/divergencias_garda_dublinbus.md` | Reescrito (§5, item 4). |
| `conflito com maratona/dados/gtfs_dublinbus_domingo_2026-10-25.json` | Refeito com o GTFS de 12/10 e as janelas 8–13h/13–17h. |
| `conflito com maratona/dados/caminhadas_ate_portoes.json` | Chave "Sussex Road (terminal E1 ate 13h)"; nome da 771. Distâncias inalteradas. |
| `conflito com maratona/dados/shapes_linhas.json` · `nom_rds.json` | Novos: intermediários do mapa, agora versionados. |
| `scripts/transporte_shapes_gtfs.py` | Novo: extrai os traçados do GTFS. |
| `scripts/transporte_gtfs_domingo.py` | Janelas 8–13h/13–17h; grava a versão enxuta direto. |
| `scripts/transporte_mapa_linhas.py` · `mapa/linhas_maratona.html` | Cenários, legenda, notas e tabelas pelo organizador. |
| `mapa/artefatos.json` · `mapa/README.md` | Versão, descrição e sha256 do mapa. |
| `conflito com maratona/sessao3.md` | §9 com o ponteiro para esta sessão. |
| `conflito com maratona/sessao4.md` | Este registro. |

## 8. Reprodução

```
curl -O https://www.transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip && unzip GTFS_Dublin_Bus.zip -d <gtfs>
python3 -I scripts/transporte_gtfs_domingo.py <gtfs> "conflito com maratona/dados/gtfs_dublinbus_domingo_2026-10-25.json" 1500
python3 -I scripts/transporte_shapes_gtfs.py <gtfs> "conflito com maratona/dados/shapes_linhas.json"
python3 -I scripts/transporte_mapa_linhas.py "conflito com maratona/dados" mapa/linhas_maratona.html
```

## 9. Notas de ambiente

- O branch local estava atrás do remoto no início; foi preciso `git pull origin conflitomaratona`.
- Rede: TFI (GTFS), OSRM e Nominatim responderam. As tabelas do organizador são imagens
  (`pdfimages -png`).
- Chromium/Playwright local serviu para as capturas de conferência do mapa.
