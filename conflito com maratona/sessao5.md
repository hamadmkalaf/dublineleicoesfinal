# Sessão 5 — Acessos de carro à Donnybrook Road no dia da maratona

Registro para retomar em outra sessão. 13/10/2026, mesma conversa da `sessao3.md`, depois da
sessão 4, que rodou em paralelo no mesmo branch. Branch: `conflitomaratona`. PR rascunho:
https://github.com/hamadmkalaf/dublineleicoesfinal/pull/29.

## 1. Pedido e entrega

| Pedido | Entregue | Onde |
|---|---|---|
| "Busque o mapa de Dublin em APIs e identifique as diferentes maneiras de acessar a Donnybrook Road, vindo de diferentes pontos da cidade (Norte, Sul, Leste e Oeste)" | Roteamento de carro, de 22 origens, de 15 em 15 min das 7h45 às 17h15, com os fechamentos do organizador de 13/10 | `acessos_donnybrook_road.md` |

O modo é **carro**; ônibus já estava em `ranking_linhas_rds.md`. A pé, nada foi refeito.

## 2. Achados principais

1. **O percurso é um anel fechado e Donnybrook fica dentro.** Ranelagh, Rathmines, Harold's
   Cross, Crumlin, Kimmage e Ballsbridge oeste também ficam dentro, e quem sai deles chega o dia
   todo sem desvio.
2. **A N11 subindo do sul é a única porta sempre aberta.** Das ~9h25 às ~10h30 é a única para
   norte, centro e leste: Strand Road → Rock Road → Booterstown Avenue → N11, com ~2× o tempo
   normal. É a mesma orientação da Garda de 18/9, achada pelo modelo sem que lhe fosse dada,
   o que serve de validação.
3. Depois das 10h30, norte e centro voltam por Charlemont St → Leeson St Upper → Morehampton
   Rd. O sul usa a N11 das 9h10 às 16h–16h30. O oeste usa M50 → N11 das ~9h às 14h–15h.
   **Sandymount fica do lado de fora das 9h25 às 17h30.**
4. **Entradas laterais na N11 entre Foster's Ave e Nutley Lane não servem** (corredores nos
   dois corredores de ônibus). A Booterstown Ave chega à N11 ao sul da Foster's Ave. Isso
   responde em parte ao pedido 10 de `divergencias_garda_dublinbus.md` §5.

## 3. Fontes e ferramentas

| Fonte | Resultado |
|---|---|
| `download.bbbike.org/osm/bbbike/Dublin/Dublin.osm.pbf` (gerado 10/10/2026, 59 MB) | **Funcionou.** Base do grafo, lido com `osmium` (pip). |
| `valhalla1.openstreetmap.de` | Funcionou para o dia normal (validação). **Não serve para os fechamentos:** `exclude_polygons` limitado a 10 km de perímetro. |
| `nominatim.openstreetmap.org` | Funcionou (origens). "Swords" sem condado caiu na Swords Road; corrigido com "Swords, Fingal". |
| `routing.openstreetmap.de` (OSRM), `photon.komoot.io` | Respondem; não usados no fim. |
| `overpass-api.de`, `download.geofabrik.de` | **Não** (conexão recusada). |

## 4. Arquivos criados nesta sessão

| Arquivo | O que é |
|---|---|
| `conflito com maratona/acessos_donnybrook_road.md` | O documento: conclusão, portas, tabela por origem e horário, pedidos, método. |
| `conflito com maratona/dados/acessos_donnybrook_2026-10-25.json` | Resultado completo: origem × horário × porta (minutos do modelo, km, corredor). |
| `conflito com maratona/dados/acessos_donnybrook_resumo.txt` | Resumo por origem e faixa de horário (minutos do modelo, sem fator). |
| `conflito com maratona/dados/percurso_maratona_osm.json` · `.png` | Traçado do percurso no grafo OSM e a figura de conferência. |
| `conflito com maratona/dados/origens_acessos.json` | As 22 origens. |
| `scripts/acessos_donnybrook/` | `1_carrega_osm.py`, `2_percurso.py`, `3_acessos.py`, `4_resumo.py`, `grafo.py`, `fechamentos.py`. |

## 5. Pendências

1. **Perguntas à Garda** (`acessos_donnybrook_road.md` §5): pontos de travessia controlada; a
   conversão Booterstown Ave / Mount Merrion Ave → N11 para o norte; os acessos da N4 em
   Chapelizod. Juntar aos pedidos de `divergencias_garda_dublinbus.md` §5 antes de mandar.
2. **Mensagem ao eleitor de carro**, por região (§4 do documento): não redigida nem traduzida.
3. **Mapa visual dos acessos:** não feito. O `mapa/linhas_maratona.html` é de ônibus. Pode
   ganhar uma camada "carro" com as portas e a volta por Booterstown.
4. **Demanda por hora:** se a janela 9h25–10h30 empurrar comparecimento para a tarde, ela se
   soma ao retorno das linhas às 13h. Fica registrado como risco, sem número.

## 6. Notas de ambiente

- **Outra sessão (a 4) empurrou para o mesmo branch durante esta.** O primeiro push foi
  recusado; resolvido com `git fetch` + merge, sem conflito. Antes de cada push, `git fetch`.
- A primeira rodada do roteamento morreu sem mensagem (cópia do dicionário de predecessores a
  cada porta). A versão salva não copia; leva ~16 min e cabe na memória.
