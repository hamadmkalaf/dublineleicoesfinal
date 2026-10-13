# Sessão 2 — Conflito do 2º turno (25/10/2026) com a Maratona de Dublin

Registro para retomar em outra sessão. Sessão de 07/10/2026 (tarde), registro gravado em
13/10/2026. Branch: `conflitomaratona`. PR rascunho:
https://github.com/hamadmkalaf/dublineleicoesfinal/pull/29. Continuação de `sessao1.md`.

## 1. O que foi pedido e o que foi entregue

| Pedido | Entregue | Onde |
|---|---|---|
| Ler `sessao1.md`, os e-mails da Garda e o PDF de desvios da Dublin Bus; acessar as APIs de transporte (NTA/GTFS, dublinbus.ie, bustimes.org, Nominatim, Overpass, Citymapper) | Feito. Rede liberada nesta sessão; ver §3 para o que respondeu e o que não respondeu. | — |
| Ranking de linhas úteis para o RDS com escala de acessibilidade pela caminhada | Feito | `ranking_linhas_rds.md` |
| Lista de divergências Garda × Dublin Bus | Feito, mais prefeitura, organizador e Irish Rail | `divergencias_garda_dublinbus.md` |
| Representação visual do caminho das linhas | Feito: mapa SVG georreferenciado com três cenários | `mapa/linhas_maratona.html` · https://claude.ai/artifact/Wn9NNUuFZukE5sZp9L1W53 |

Ambos os documentos **substituem as seções 5 e 6 do `sessao1.md`** e corrigem parte das
seções 3 e 7. Um ponteiro foi acrescentado ao fim do `sessao1.md` (§11).

## 2. Fatos novos, por ordem de impacto

1. **O DART não para em Sandymount nem em Lansdowne Road de 24 a 26/10/2026.** Obras da
   Irish Rail entre Grand Canal Dock e Bray (anúncio de 22/9, página de obras atualizada em
   28/9). O GTFS da NTA confirma: o serviço de domingo (id 296) é retirado em 25/10 e o
   serviço especial (id 239) não para em nenhuma estação entre Grand Canal Dock e Dún
   Laoghaire. O DART roda só Malahide ↔ Grand Canal Dock. Leap Card aceito nos ônibus TFI.
   **A pergunta pendente à prefeitura sobre "quem desce em Sandymount" perde o objeto.**
   Ninguém (Garda, prefeitura, Dublin Bus) havia mencionado.
2. **7 e 7A são desviadas por Strand Road desde as 8h**, sem a janela "até 11h" que a
   sessão 1 supunha. O aviso de 07/10 não traz divisão de horário para elas. Nenhuma viagem
   da 7/7A passa pelo RDS no dia. A **4** tem a divisão: rota normal pela Merrion Road até
   11h, desvio depois.
3. **A costa sul (Dún Laoghaire – Blackrock) perde DART e 7/7A no mesmo dia.** Sobra a E2,
   que só opera o trecho sul a partir das 11h. É o eleitorado com mais a perder.
4. **Três horas diferentes para o fechamento da Merrion Road:** 9h40 (organizador), 10h
   (Garda), 11h (Dublin Bus mantém a 4 até lá). Para o plano, 9h40 a 17h30.
5. **As paradas de Donnybrook ficam a 11–13 min a pé do portão da Anglesea, não a 10**
   (medido no OSRM a pé, 4,8 km/h). O portão da Anglesea é 2–3 min mais perto de Donnybrook
   que o da Merrion Road e a caminhada não cruza o percurso.
6. **7E, 27X, 7B e 7D têm zero viagens de domingo** no GTFS. Confirmado com fonte primária.
7. **S2** passa no RDS em dia normal, mas no dia não roda até 10h30 e depois termina em
   Burlington Mews. Fora do ranking.
8. **A página de tráfego do organizador (salva em 07/10) é texto de 2025** com datas
   misturadas ("October 26th", "Friday 24th"), e sua nota de DART descreve as obras de 2025
   (lado norte), o oposto de 2026. Não usar.

## 3. Fontes: o que respondeu e o que não

| Fonte | Resultado |
|---|---|
| `transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip` (feed 06/10/2026) | **Funcionou.** Serviço de domingo 25/10 = service_id 291. Base do ranking. |
| `GTFS_All.zip` e `GTFS_Irish_Rail.zip` (mesmo diretório) | Funcionaram. Outros operadores (Aircoach 700/702, Bus Éireann 2/133, Wexford Bus 740) e DART. |
| `routing.openstreetmap.de` (OSRM, perfis `routed-foot` e `routed-car`) | Funcionou. Caminhadas, percurso da maratona e desvios. |
| `nominatim.openstreetmap.org` | Funcionou com User-Agent identificado (403 sem ele). Geometria da Anglesea Road e do RDS. |
| `photon.komoot.io` | Funcionou (geocodificação alternativa). |
| `overpass-api.de` e espelhos | **Não**: conexão recusada; `maps.mail.ru` deu 504. |
| `dublinbus.ie` | **Não**: 403 ao robô. Usou-se o PDF salvo em 07/10. |
| `irishlifedublinmarathon.ie/traffic-information` | **Não** ao vivo (desafio anti-robô). Usou-se o PDF salvo. |
| `transportforireland.ie/events/dublin-marathon-october-irish-life/` | Funcionou via WebFetch: 25/10/2026, 8h40 cadeirantes, 8h45 onda 1, desvios 3h–21h. |
| `irishrail.ie/en-ie/news/irishrail-engineering-works` e `dublinpublictransport.ie` | Funcionaram: obras 24–26/10, Grand Canal Dock – Bray fechado. |
| `bustimes.org/api/` e `citymapper.com` | Respondem, mas não acrescentam nada ao GTFS. |
| API em tempo real da NTA (`api.nationaltransport.ie/gtfsr`) | 401 sem chave; irrelevante para planejar. |
| 28 capturas do Citymapper na pasta | Transcritas por subagente: só percursos e nomes de paradas; **nenhuma frequência, horário ou nota de domingo**. |

## 4. Método do ranking (resumo; detalhe em `ranking_linhas_rds.md`)

- **Portão da Anglesea (premissa):** 53,32578 N, 6,23124 O, meio da testada do RDS Arena,
  tirado da geometria do OSM. Portão principal da Merrion Road: 53,32830 N, 6,22920 O.
- **Caminhada:** OSRM a pé na rede normal, convertida a 80 m/min (4,8 km/h). Paradas a leste
  da Merrion Road exigem cruzar o percurso; marcadas com ⚠.
- **Escala:** A ≤ 600 m (≤ 7,5 min) · B 601–1.000 m (7,5–12,5 min) · C 1.001–1.500 m
  (12,5–19 min) · D > 1.500 m.
- **Serviço no dia:** do aviso da Dublin Bus de 07/10, por janela (até 11h / a partir de 11h).
- **Frequência:** horário programado de domingo na parada mais próxima (GTFS); o aviso muda
  rotas, não frequências; no dia a real tende a ser menor.

**Resultado:** Nível 1 = E1 (dia todo, ~19 min de manhã, ~15 min à tarde), 39A e E2 (só
após 11h, ~15 min), todas em B (11–12 min a pé). Nível 2 = 14, 11B (a partir de ~12h), 11,
44, no corredor de desvio, paradas não confirmadas. Nível 3 = 4 (A, 6 min, mas só até o
fechamento) e 7/7A (não rodam por ali). Fora: S2, 47, C1/C2, 7E/27X/7B/7D, DART, Luas,
outros operadores sem aviso de desvio.

**Capacidade (premissa):** após 11h, E1+E2+39A ≈ 12 ônibus/hora/sentido ≈ 1.080 lugares/hora;
antes das 11h, só a E1, 3–4 ônibus/hora ≈ 300 lugares. O risco é das 8h às 11h.

## 5. Divergências (resumo; detalhe em `divergencias_garda_dublinbus.md`)

Garda × Dublin Bus: hora da Merrion Road (10h × 11h); sentido da Merrion Road (Garda fecha
só o sentido cidade, Dublin Bus trata como fechada nos dois); início das restrições (10h ×
8h/11h); Donnybrook Road "aberta o dia todo" mas E2/39A/11 não rodam por lá de manhã (os
cortes vêm da largada no centro); Nutley Lane (10h × 47 desviada desde 8h); Northumberland
Road (Garda 10h × organizador 6h–18h30 × 7/7A desde 8h); N11 "aberta" mas sem corredores de
ônibus (os corredores são o percurso); orientação da Garda para quem vem do norte vale para
carro e não tem equivalente em ônibus; Anglesea Road sem nenhuma linha; concordam só em
Rock Road/Merrion Gates/Strand Road.

Prefeitura × aviso: "E1, E2 e 39A ao longo do dia" × E2 e 39A só após 11h. Mesma data (7/10).

## 6. Pedidos consolidados (quem, o quê)

**Dublin Bus / NTA:** (1) E2 e 39A antes das 11h em Donnybrook: sim ou não, por escrito,
citando o aviso; se não, pedir que operem o trecho sul desde as 8h. (2) Última viagem da 4
pelo RDS; alguma da 7/7A passa? (3) 14, 11 e 44 param em 774/758/759 e Morehampton Road no
desvio? (4) Atraso estimado na N11 sem corredor e reforço. (5) Qual ônibus substitui o DART
no trecho sul em 25/10 e se para em Donnybrook.
**Garda (insp. Wogan):** (6) Merrion Road entre Ballsbridge e Serpentine Avenue aberta no
sentido saída? (7) Northumberland Road: 6h ou 10h? (8) Tolerância para a 4 entre 9h40 e 11h?
(9) Rota a pé Donnybrook Road → Anglesea Road com fiscal na esquina.
**Prefeitura:** (10) Retirar a pergunta sobre Sandymount, informar que fecha. (11) Cobrar
da Dublin Bus a resposta ao item 1.
**RDS:** (12) Qual portão da Anglesea abre; retorno de veículos dentro do recinto.

## 7. Arquivos criados ou alterados nesta sessão

| Arquivo | O que é |
|---|---|
| `conflito com maratona/ranking_linhas_rds.md` | Ranking, método, tabela de caminhadas, consequências para o plano. |
| `conflito com maratona/divergencias_garda_dublinbus.md` | As divergências, correções ao `sessao1.md`, pedidos por destinatário. |
| `conflito com maratona/dados/gtfs_dublinbus_domingo_2026-10-25.json` | Saída do GTFS: por linha e sentido, parada mais próxima e viagens de domingo por hora. Versão enxuta. |
| `conflito com maratona/dados/caminhadas_ate_portoes.json` | Caminhada de 32 pontos até os dois portões. |
| `conflito com maratona/dados/dart_2026-10-25.json` | Serviço de domingo normal × serviço especial de 25/10 no GTFS da Irish Rail. |
| `conflito com maratona/dados/geometrias_mapa.json` | Polilinhas do percurso, do desvio de 4/7/7A, do corredor de desvio e das caminhadas (OSRM). |
| `mapa/linhas_maratona.html` | O mapa. Registrado em `mapa/artefatos.json` (chave `linhas_maratona`) e no `mapa/README.md`. |
| `scripts/transporte_gtfs_domingo.py` | Lê um GTFS descompactado e grava o JSON acima. `python3 -I scripts/transporte_gtfs_domingo.py <gtfs> saida.json 1500` |
| `scripts/transporte_caminhadas.py` | Mede as caminhadas no OSRM. `python3 -I scripts/transporte_caminhadas.py saida.json caminhadas.json` |
| `scripts/transporte_mapa_linhas.py` | Gera o mapa a partir de `shapes_linhas.json`, `geometrias_mapa.json` e `nom_rds.json`. **`shapes_linhas.json` e `nom_rds.json` não foram versionados** (eram intermediários na área de rascunho); para regenerar o mapa é preciso reextrair as shapes do GTFS (o trecho de código está no início do gerador da sessão, não no script salvo) e refazer a consulta ao Nominatim. Pendência em §9. |
| `conflito com maratona/sessao1.md` | Ganhou a §11 com o ponteiro para esta sessão. |

O GTFS (37 MB) não está no repositório; baixar de
`https://www.transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip`.

## 8. O mapa (`mapa/linhas_maratona.html`)

SVG georreferenciado (projeção equirretangular com cos 53,325°, caixa 53,303–53,346 N ×
6,262–6,198 O), sem tiles externos porque a plataforma de artefatos bloqueia imagens de
outros domínios. Camadas: malha cinza (todas as shapes de ônibus da caixa), polígono do RDS,
percurso da maratona (OSRM a pé na N11 + shape da linha 7 de Merrion Road a Mount Street),
corredor de desvio 14/11/44, eixo E1/E2/39A (shape da E1), linha 4, 7/7A, desvio por Strand
Road (OSRM carro), caminhadas, pontos (774, 758, 759, 771, 416/485, dois portões, DART
Sandymount e Lansdowne Road, Sandymount). Três cenários por botão (dia normal, até 11h, a
partir de 11h), com nota explicativa e legenda. Tabela de caminhadas ao pé.

Conferido em captura de tela (desktop 1100 px, dois cenários). Não conferido: largura de
telefone e tema escuro além do código.

## 9. Pendências

1. **Versionar os intermediários do mapa** (`shapes_linhas.json`, `nom_rds.json`) ou fazer o
   gerador extrair as shapes do GTFS diretamente, para que o mapa seja reproduzível só com o
   repositório.
2. **Fixar o portão com o RDS.** Toda caminhada e o mapa pressupõem o meio da testada do
   RDS Arena. ±150 m = ±2 min.
3. **Mandar os 12 pedidos de §6.** O mais urgente é o item 1 (E2/39A de manhã) e o 5
   (substituto do DART), porque mudam a mensagem ao eleitor.
4. **Mensagem ao eleitor:** "venha pela E1 (ou, após 11h, E2 e 39A), desça em Donnybrook
   (774, 758 ou 759), caminhe 11–13 min pela Donnybrook Road e Anglesea Road". Nada de
   Merrion Road, nada de DART. Ainda não redigida nem traduzida.
5. **Sinalização desde a parada 774** (uma curva que o eleitor não conhece): peça nova no
   plano de sinalização, ainda não desenhada. O `CLAUDE.md` e `docs/voluntarios/` continuam
   com o portão e o P0 na Merrion Road; não foram alterados.
6. **Mapas de caminho para o eleitor** (pedido original da sessão 1): o mapa desta sessão é o
   de planejamento; falta a versão simplificada para imprimir ou mandar por WhatsApp.
7. **Capacidade da manhã:** se a Dublin Bus não antecipar E2/39A, estudar transporte próprio
   ou orientar para votar à tarde.

## 10. Notas de ambiente

- A rede desta sessão alcançou TFI, OSRM, Nominatim, Irish Rail; não alcançou Overpass,
  dublinbus.ie e a página ao vivo do organizador. Se a próxima sessão bloquear algo, a lista
  de domínios a liberar está em `sessao1.md` §8.
- **O `git push` recebeu "Internal Server Error" do GitHub em nove tentativas ao longo de dez
  minutos** e voltou a funcionar meia hora depois. Enquanto isso os arquivos subiram pela API
  do GitHub (dois commits via `push_files`), e o histórico local foi mesclado depois. Se
  acontecer de novo, a API é a saída; o JSON grande precisou ser enxuto para caber.
- O `amend` de commit foi bloqueado pelo classificador do modo automático; usar commits novos.

## 11. Sessão 3 (13/10/2026) — horários do organizador revistos

A página "Road Closures" do organizador de 13/10
(`Road Closures - Irish Life Dublin Marathon (2026-10-13).pdf`) **supera a página de tráfego
salva em 07/10** e muda horários que este registro usa: **Merrion Road fecha às 9h25, não
9h40** (plano: 9h25–17h30); Nutley Lane às 8h40; Northumberland Road em dois trechos
(3h30–20h30 e 6h–18h30); Foster's Avenue fechada nos dois sentidos. Confronto completo e
lista de correções pendentes em `sessao3.md`.
