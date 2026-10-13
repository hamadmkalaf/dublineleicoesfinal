# Ranking de linhas úteis para chegar ao RDS em 25/10/2026 (dia da maratona)

Refeito em 13/10/2026 (sessão 4). Substitui a versão de 07/10 e a seção 6 do `sessao1.md`.
Portão de referência: **Anglesea Road** (decisão da Embaixada de 1/10, ainda por acertar com o RDS).
Para comparação, cada parada traz também a caminhada até o portão principal da Merrion Road.

**Regra desta versão:** todo horário de fechamento de via vem do **organizador** (página
"Road Closures" de 13/10). O "11h" da Dublin Bus **não é usado** — nem para a Merrion Road
nem para a volta das linhas ao centro. A Dublin Bus fornece só **o trajeto** de cada linha no
dia; a hora em que esse trajeto fica possível é a da reabertura, pelo organizador, das ruas
que ele usa.

## 1. Como o ranking foi montado

**Fontes (acessadas em 13/10/2026, salvo indicação):**

| Fonte | O que forneceu |
|---|---|
| Página "Road Closures" do organizador, 13/10 (`Road Closures - Irish Life Dublin Marathon (2026-10-13).pdf`) | **Todos os horários de fechamento e reabertura.** |
| Documento operacional da Dublin Bus, 12/10 (`Dublin Bus - Diversions Document (2026-10-12).pdf`) | Trajeto de cada linha no dia (encurtamentos, desvios, terminais). Supera o aviso público de 07/10 (`diversions_dublinmarathon.pdf`), que dizia o mesmo trajeto. |
| GTFS da NTA, `GTFS_Dublin_Bus.zip` (feed com início em 12/10/2026) | Horário programado de domingo 25/10 (service_id 187), parada a parada; traçados das linhas para o mapa. |
| `routing.openstreetmap.de` (OSRM a pé) | Caminhada de cada parada até os dois portões. Remedida em 13/10: mesmos valores de 07/10 (±1 m). |
| E-mails da Garda (18/9 e 25/9) e da prefeitura (7/10) | Paradas confirmadas (774, 758, 759). Os horários da Garda ficam como divergência, não como base. |
| `irishrail.ie` (obras, 28/9) e GTFS da Irish Rail | DART sem trens entre Grand Canal Dock e Bray de 24 a 26/10. |

**Os fechamentos que decidem o ranking (organizador):**

| Via | Fecha | Reabre | O que afeta |
|---|---|---|---|
| Merrion Road (sentido cidade) | 9h25 | 17h30 | A porta do RDS |
| Northumberland Road, Haddington Rd → Mount St Lower | 3h30 | 20h30 | Rota normal de 4, 7 e 7A |
| Northumberland Road, Haddington Rd → Lansdowne Rd | 6h | 18h30 | idem |
| Mount Street Lower | 3h30 | 17h30 | idem |
| Merrion Square North, Holles Street | 3h30 | 20h | idem |
| **Leeson Street Lower e Hatch Street** | 3h30 | **13h** | **O trajeto que a Dublin Bus dá para E1, E2, 39A, 11, 11B e 14 voltarem do centro a Donnybrook** ("Charlotte Way, Hatch Street to Leeson Street") |
| Earlsfort Terrace | 7h | 11h | Desvio de 11, 14, 39A e 44 |
| Stillorgan Road (N11), corredor de ônibus | 9h15 / 9h30 | 16h30 / 17h | Ônibus do eixo em tráfego geral |
| Viaduto da UCD | 9h30 | 17h | 39A termina na 771; E1/E2 passam por baixo |
| Nutley Lane | 8h40 | 17h | Linha 47 |
| Foster's Avenue (os dois sentidos) | 9h10 | 16h30 | Retorno pela N11 de quem vem de carro |

**Premissas (rotuladas como tal):**

- **Ponto do portão da Anglesea:** 53,32578 N, 6,23124 O — meio da testada do RDS Arena na
  Anglesea Road (OpenStreetMap). Um portão 150 m para o norte ou para o sul muda cada caminhada
  em até ±2 min.
- **Velocidade de caminhada: 4,8 km/h (80 m/min).** Idosos e pessoas com carrinho levam
  30–50% mais.
- **Frequência:** horário programado de domingo na parada de referência (GTFS). Os desvios mudam
  rotas, não frequências; no dia a real tende a ser menor, sobretudo na N11 sem corredor.
- **Leitura literal do organizador:** a página lista ruas inteiras ("Hatch Street", "Leeson
  Street Lower"). Se o bloqueio for só de um trecho, as linhas podem voltar antes das 13h — a
  Dublin Bus conta com 11h. O plano usa 13h; a diferença vira pergunta (§5).

**Escala de acessibilidade a pé** (até o portão da Anglesea; o usuário fixou 10 min como aceitável):

| Nível | Caminhada | Leitura |
|---|---|---|
| **A** | até 600 m (≤ 7,5 min) | Na porta. |
| **B** | 601–1.000 m (7,5–12,5 min) | Dentro da tolerância de 10 min, com folga de 2,5. |
| **C** | 1.001–1.500 m (12,5–19 min) | Caminhada longa; só com sinalização e voluntário no trajeto. |
| **D** | mais de 1.500 m (> 19 min) | Não serve como acesso principal. |

**Serviço no dia:** ●● o dia todo nas paradas relevantes · ● só a partir das 13h ·
○ não passa.

## 2. Caminhadas medidas (OSRM a pé, rede normal)

| Parada (código) | Linhas em 25/10 | Até Anglesea | Até Merrion | Nível |
|---|---|---|---|---|
| RDS Ballsbridge, sentido Blackrock (416) | nenhuma (4, 7, 7A desviadas) | 438 m · 5,5 min | 48 m · 0,6 min | A |
| RDS Ballsbridge, sentido cidade (485/486) | nenhuma | 504 m · 6,3 min | 46 m · 0,6 min | A |
| Merrion Road (417, em frente à Embaixada) | nenhuma | 600 m · 7,5 min | 246 m · 3,1 min | A |
| Pembroke Road (2798) | nenhuma (a rua fica entre ruas fechadas) | 854 m · 10,7 min | 681 m · 8,5 min | B |
| **Donnybrook / Garda Station (774)** | E1 ●●; E2, 39A, 11B ● | **884 m · 11,0 min** | 1.106 m · 13,8 min | B |
| Donnybrook Depot, sentido cidade (772) | E1 ●●; E2, 39A ● | 882 m · 11,0 min | 1.504 m · 18,8 min | B |
| Donnybrook Depot, sentido UCD (760) | E1 ●●; E2, 39A ● | 903 m · 11,3 min | 1.540 m · 19,2 min | B |
| **Victoria Avenue (758)** | E1 ●●; E2, 39A, 11B ● | **932 m · 11,7 min** | 1.158 m · 14,5 min | B |
| Donnybrook Village, sentido cidade (775) | E1 ●●; E2, 39A, 11B ● | 955 m · 11,9 min | 1.158 m · 14,5 min | B |
| Donnybrook Village, sentido UCD (757) | E1 ●●; E2, 39A, 11B ● | 1.013 m · 12,7 min | 1.162 m · 14,5 min | C |
| **Donnybrook Stadium (759)** | E1 ●●; E2, 39A, 11B ● | **1.025 m · 12,8 min** | 1.247 m · 15,6 min | C |
| Donnybrook Stadium, sentido cidade (773) | idem | 1.066 m · 13,3 min | 1.288 m · 16,1 min | C |
| Morehampton Terrace (776) | E1 ●●; 44 no desvio | 1.114 m · 13,9 min | 1.140 m · 14,2 min | C |
| Teresian School (771, terminal da 39A) | 39A ● | 1.256 m · 15,7 min | 1.878 m · 23,5 min | C |
| Waterloo Road (753) | nenhuma (38, 38A, 39, 70 terminam no centro) | 1.423 m · 17,8 min | 1.250 m · 15,6 min | C |
| Tritonville Road (desvio de 4/7/7A) | 4, 7, 7A desviadas ●● | 1.469 m · 18,4 min ⚠ | 1.252 m · 15,7 min | C ⚠ |
| Sandford Road / Norwood Park (855/884) | 11, 44 em dia normal | 1.496–1.521 m · 19 min | 1.721 m · 21,5 min | C/D |
| Park Avenue, Sandymount (7739/7740) | 47 (desviada), C1/C2 | 1.521–1.593 m · 19–20 min ⚠ | 1.298 m · 16,2 min | D ⚠ |
| Sandymount Green (desvio de 4/7/7A) | 4, 7, 7A desviadas ●● | 1.664 m · 20,8 min ⚠ | 1.327 m · 16,6 min | D ⚠ |
| Grand Canal Dock (DART, terminal sul no dia) | DART | 1.832 m · 22,9 min | 1.616 m · 20,2 min | D |
| Sussex Road (terminal da E1 até 13h) | E1 | 1.950 m · 24,4 min | 1.778 m · 22,2 min | D |
| Ranelagh (Luas verde) | Luas | 2.336 m · 29,2 min | 2.363 m · 29,5 min | D |
| Strand Road / Merrion Gates (desvio de 4/7/7A/47) | 4, 7, 7A, 47 desviadas | 2.757 m · 34,5 min ⚠ | 2.534 m · 31,7 min | D ⚠ |

⚠ = a leste da Merrion Road: exige atravessar o percurso da maratona a pé.

As paradas de Donnybrook ficam a **11–13 min** do portão da Anglesea, e a caminhada
(Donnybrook Road → Anglesea Road) corre inteira **fora do percurso**. O portão da Anglesea é
2–3 min mais perto de Donnybrook que o da Merrion Road.

## 3. O ranking

Ordenado por **janela útil no dia × frequência**, com a caminhada como desempate. Frequência
de domingo programada (GTFS de 12/10) na parada de Donnybrook (774/758), por sentido.

### Nível 1 — eixo de Donnybrook, o único que funciona no dia

| # | Linha | Serviço no dia | Caminhada | Frequência de domingo (programada) | Observações |
|---|---|---|---|---|---|
| **1** | **E1** Bray/Ballywaltrim – Northwood | ●● | B (774/758: 11–12 min) | 8–13h: 17 viagens/sentido (~17 min); 13–17h: 16 (~15 min) | **A única linha que serve Donnybrook o dia inteiro.** Até 13h roda só Bray ↔ Sussex Road: a volta ao centro que a Dublin Bus prevê para 11h passa por Hatch Street e Leeson Street Lower, fechadas até 13h. Quem vem do norte ou do centro não a alcança antes das 13h sem caminhar até Sussex Road (24 min do portão). Paradas 774/758/759 confirmadas pela prefeitura. |
| **2** | **39A** Ongar – UCD | ● (13h) | B (774/758); terminal 771: C | 8–13h: nada em Donnybrook; 13–17h: 16 (~15 min) | Até 13h roda só Ongar ↔ Luke Street (centro). Depois, cidade ↔ Teresian School (771), por causa do viaduto da UCD fechado até 17h. Liga o oeste e o noroeste (Blanchardstown, Ongar, Navan Road). |
| **3** | **E2** Dún Laoghaire – Harristown | ● (13h) | B (774/758) | 8–13h: nada em Donnybrook; 13–17h: 16 (~15 min) | Até 13h roda só Harristown ↔ Nassau Street; o trecho sul, que passa por Donnybrook, **não é operado**. O "shuttle" das 6h–11h cobre só Dún Laoghaire ↔ Stillorgan SC. **Contradiz a prefeitura** ("o dia todo"). |

### Nível 2 — passam pelo corredor por causa do desvio; paradas não confirmadas

| # | Linha | Serviço no dia | Caminhada | Frequência de domingo | Observações |
|---|---|---|---|---|---|
| **4** | **14** Dundrum Luas – Beaumont | ●● (só Dundrum ↔ Adelaide Rd até 13h) | B/C, se parar em Donnybrook Rd | 8–13h: 8–9/sentido (~30 min); 13–17h: 12 (~20 min) | Até 13h, Dundrum ↔ Adelaide Road via Stillorgan Rd e Donnybrook Rd (não precisa de Hatch St). A rota inteira usa Hatch St e só volta às 13h. Única ligação direta de Dundrum, Churchtown e Goatstown. **Pedir à Dublin Bus que confirme paradas.** |
| **5** | **11B** Phoenix Park – Donnybrook Stadium | ● (13h) | B/C (759: 13 min; 774: 11 min) | 13–17h: 8/sentido (~30 min) | Desvio por Hatch St e Leeson St: 13h. No horário de domingo só começa perto do meio-dia, então a regra do organizador custa pouco aqui. |
| **6** | **11** Phoenix Park – Sandyford | ● (13h) | B/C, se parar em Donnybrook Rd | 13–17h: 8/sentido (~30 min) | Sem serviço de manhã. Depois, desviada por Hatch St – Earlsfort Terrace – Leeson St – Donnybrook – Stillorgan Rd. |
| **7** | **44** Enniskerry – DCU | ● (13h, ver obs.) | C (Morehampton Terrace / Donnybrook Village: 12–14 min) | 1 ônibus/hora/sentido | O desvio da Dublin Bus vale desde as 8h e passa por Hatch Street (fechada até 13h). **Pela regra do organizador, a parte do centro só roda a partir das 13h; a ponta sul (Enniskerry – Dundrum – Morehampton Rd) pode rodar antes, sem confirmação.** Horária: pouco útil. |

### Nível 3 — paradas na porta, sem serviço no dia

| # | Linha | Serviço no dia | Caminhada | Frequência de domingo | Observações |
|---|---|---|---|---|---|
| **8** | **4** Monkstown – Heuston | ○ | A em dia normal (416/485: 5,5–6,3 min) | 8–13h: 12/sentido em dia normal | **Não passa pelo RDS em 25/10.** A rota normal (GTFS) entre o centro e o RDS é Merrion Sq North → Holles St → Mount Street Lower → Northumberland Road → Lansdowne Rd → RDS, e o organizador fecha esse trecho **desde 3h30**; a Merrion Road (sentido cidade) fecha às 9h25. O documento da Dublin Bus de 12/10 a desvia em Merrion Gates por Strand Road, sem hora própria (= desde 8h), e até 13h ela termina em Townsend St. **Muda a versão de 07/10**, que dava a 4 pela Merrion Road até 11h com 3–4 ônibus por sentido. |
| **9** | **7 / 7A** Brides Glen / Loughlinstown – Mountjoy Sq | ○ | A em dia normal | ~40 min cada; 20 min juntas | Mesmo trajeto da 4 entre o centro e Merrion Gates; desviadas por Strand Road desde as 8h. Sem 4, 7, 7A e DART, **Blackrock, Monkstown e Dún Laoghaire ficam sem acesso direto** ao RDS; a alternativa é a E1 desde Loughlinstown/Cornelscourt (o dia todo) ou a E2 a partir das 13h. |

### Fora do ranking

| Linha | Por quê |
|---|---|
| **S2** Heuston – Sean Moore Rd | Passa no RDS em dia normal (~3/hora), mas no dia não roda até 10h30 e depois termina em Burlington Mews (Waterloo Rd), a 18 min, sem passar pelo RDS. |
| **47, C1, C2** | Paradas de Sandymount a 19–20 min, do outro lado do percurso; 47 horária e desviada por Rock Road desde as 8h; C1/C2 terminam em Wolfe Tone Quay até 11h. |
| **7E, 27X, 7B, 7D** | **Zero viagens aos domingos** no GTFS. |
| **37, 38, 38A, 39, 70** | No dia terminam no centro (Luke Street; a 70 depois em Townsend Street); não chegam a Waterloo Road / Burlington Road. |
| **DART (Sandymount, Lansdowne Road)** | **Fechadas de 24 a 26/10** por obras da Irish Rail; o DART roda só Malahide ↔ Grand Canal Dock. O Leap Card é aceito nos ônibus TFI, o que empurra a costa sul para a E1. |
| **Luas** | Ranelagh (linha verde) a 29 min a pé. |
| **Outros operadores** (Aircoach 700 e 702, Bus Éireann 2 e 133, Wexford Bus 740) | Usam ruas fechadas (Merrion Rd, Nutley Lane ou N11) e **nenhum publicou desvio**. Não contar com eles. |

## 4. O que isso muda no plano

1. **A janela crítica passa a ser 8h–13h, não 8h–11h.** Durante cinco das nove horas de
   votação, só a E1 (~3,5 ônibus/hora/sentido, ~315 lugares/hora a ~90 por ônibus — premissa)
   e a 14 (2/hora, paradas não confirmadas) servem o corredor, e as duas vindo do sul.
   Se a chegada fosse uniforme (premissa), ~6.400 dos 11.499 eleitores esperados chegariam
   nessa janela. Só uma parte vem de ônibus, mas a E1 sozinha não absorve uma fatia grande.
2. **Quem mora no norte, no oeste ou no centro e quer votar antes das 13h** não tem ônibus até
   Donnybrook. Opções: caminhar desde Sussex Road / Leeson St Bridge (24 min), orientar para a
   tarde, ou transporte próprio.
3. **A costa sul (Dún Laoghaire – Blackrock) perde DART, 4, 7 e 7A.** Resta a E1 desde
   Loughlinstown/Cornelscourt, ou a E2 a partir das 13h.
4. **Mensagem ao eleitor:** "venha pela E1 (a partir das 13h também E2 e 39A), desça em
   Donnybrook (paradas 774, 758 ou 759) e caminhe 11–13 min pela Donnybrook Road e pela
   Anglesea Road". Nada de Merrion Road, nada de linha 4, nada de DART.
5. **Sinalização desde a parada 774**: a caminhada passa de 10 min e tem uma curva
   (Donnybrook Road → Anglesea Road) que o eleitor não conhece.
6. **Fixar o portão com o RDS antes de imprimir qualquer mapa.**

## 5. Perguntas que podem mover o 13h

- **Organizador / Garda:** o fechamento de Hatch Street e Leeson Street Lower até 13h vale para
  a rua inteira ou só para a área de largada? Se o trecho Hatch St → Leeson St Bridge reabrir
  antes, E2, 39A e 11B voltam a Donnybrook antes das 13h.
- **Dublin Bus:** a volta ao centro "from 1100hrs" é compatível com Hatch Street fechada até
  13h? Se não for, que trajeto as linhas usam entre 11h e 13h? (Alternativa natural: Adelaide
  Road – Leeson Street Bridge, que a 14 já usa.)

## 6. Reprodução

```
python3 -I scripts/transporte_gtfs_domingo.py <pasta GTFS descompactada> "conflito com maratona/dados/gtfs_dublinbus_domingo_2026-10-25.json" 1500
python3 -I scripts/transporte_caminhadas.py "conflito com maratona/dados/gtfs_dublinbus_domingo_2026-10-25.json" caminhadas.json
python3 -I scripts/transporte_shapes_gtfs.py <pasta GTFS descompactada> "conflito com maratona/dados/shapes_linhas.json"
python3 -I scripts/transporte_mapa_linhas.py "conflito com maratona/dados" mapa/linhas_maratona.html
```

O GTFS (40 MB) não está no repositório; baixe de
`https://www.transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip`. Todos os
intermediários do mapa (`shapes_linhas.json`, `nom_rds.json`, `geometrias_mapa.json`,
`caminhadas_ate_portoes.json`) estão em `conflito com maratona/dados/`.
