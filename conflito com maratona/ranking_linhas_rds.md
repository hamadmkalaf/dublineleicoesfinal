# Ranking de linhas úteis para chegar ao RDS em 25/10/2026 (dia da maratona)

Sessão de 07/10/2026. Complementa e **substitui a seção 6 do `sessao1.md`**.
Portão de referência: **Anglesea Road** (decisão da Embaixada de 1/10, ainda por acertar com o RDS).
Para comparação, cada parada traz também a caminhada até o portão principal da Merrion Road.

## 1. Como o ranking foi montado

**Fontes usadas nesta sessão (todas acessadas em 07/10/2026):**

| Fonte | O que forneceu |
|---|---|
| GTFS da NTA, `GTFS_Dublin_Bus.zip` (feed de 06/10/2026, válido até 06/10/2027) | Horário programado de domingo 25/10 (service_id 291) de cada linha, parada a parada. |
| GTFS da NTA, `GTFS_All.zip` e `GTFS_Irish_Rail.zip` | Outros operadores (Aircoach, Bus Éireann, Go-Ahead) e o DART. |
| Aviso de desvios da Dublin Bus de 07/10 (`diversions_dublinmarathon.pdf`) | O que de fato roda no dia, por linha e por janela (antes/depois das 11h). |
| E-mails da Garda (18/9 e 25/9) e da prefeitura (7/10) | Fechamentos de ruas e as três paradas confirmadas (774, 758, 759). |
| `routing.openstreetmap.de` (roteador a pé OSRM sobre OpenStreetMap) | Caminhada real, pela rede de calçadas, de cada parada até os dois portões. |
| `nominatim.openstreetmap.org` | Geometria da Anglesea Road e do RDS para fixar o ponto do portão. |
| `irishrail.ie` (obras programadas, atualização de 28/9) e `transportforireland.ie` (página do evento) | Obras do DART no fim de semana e horário oficial da largada em 2026. |

Não foi possível usar: `dublinbus.ie` (403 ao robô), a página de tráfego do site da
maratona ao vivo (desafio anti-robô; usou-se o PDF salvo em 07/10), `overpass-api.de`
(conexão recusada) e a API em tempo real da NTA (exige chave; irrelevante para planejar).
Citymapper e bustimes.org respondem, mas não acrescentam nada ao GTFS.

**Premissas (rotuladas como tal):**

- **Ponto do portão da Anglesea:** 53,32578 N, 6,23124 O — meio da testada do RDS Arena na
  Anglesea Road, obtido da geometria do OpenStreetMap. O RDS ainda não disse qual portão
  abre; um portão 150 m para o norte ou para o sul muda cada caminhada em até ±2 min.
- **Velocidade de caminhada: 4,8 km/h (80 m/min)**, ritmo de adulto sem pressa. Idosos e
  pessoas com carrinho levam 30–50% mais.
- As caminhadas são medidas na rede normal. **Para cruzar a Merrion Road no dia é preciso
  atravessar o percurso da maratona**, e não se sabe se haverá pontos de travessia com
  fiscal. Por isso, paradas a leste da Merrion Road (Sandymount, Strand Road) recebem um
  aviso próprio.
- A frequência de domingo vem do horário programado; o aviso da Dublin Bus muda rotas,
  não frequências. No dia, a frequência real tende a ser menor.

**Escala de acessibilidade a pé** (até o portão da Anglesea; o usuário fixou 10 min
como aceitável):

| Nível | Caminhada | Leitura |
|---|---|---|
| **A** | até 600 m (≤ 7,5 min) | Na porta. |
| **B** | 601–1.000 m (7,5–12,5 min) | Dentro da tolerância de 10 min, com folga de 2,5. |
| **C** | 1.001–1.500 m (12,5–19 min) | Caminhada longa; só com sinalização e voluntário no trajeto. |
| **D** | mais de 1.500 m (> 19 min) | Não serve como acesso principal. |

**Serviço no dia** (segundo o aviso de 07/10 e os e-mails): ●● roda o dia todo nas paradas
relevantes · ● só a partir das 11h · ◐ só até o fechamento da Merrion Road · ○ não passa.

## 2. Caminhadas medidas (OSRM a pé, rede normal)

| Parada (código) | Linhas em dia normal | Até Anglesea | Até Merrion | Nível |
|---|---|---|---|---|
| RDS Ballsbridge, sentido Blackrock (416) | 4, 7, 7A, S2, Aircoach 702 | 438 m · 5,5 min | 48 m · 0,6 min | A |
| RDS Ballsbridge, sentido cidade (485/486) | 4, 7, 7A, S2 | 504 m · 6,3 min | 46 m · 0,6 min | A |
| Merrion Road (417, em frente à Embaixada) | 4, 7, 7A, Bus Éireann 2 | 600 m · 7,5 min | 246 m · 3,1 min | A |
| Sandymount Station, ponto de ônibus (2808) | — no dia | 739 m · 9,2 min | 516 m · 6,5 min | B |
| Pembroke Road (2798) | 4, 7, 7A (a rua está no percurso da maratona) | 854 m · 10,7 min | 681 m · 8,5 min | B |
| **Donnybrook / Garda Station (774)** | E1, E2, 39A, 11B | **884 m · 11,0 min** | 1.106 m · 13,8 min | B |
| Donnybrook Depot, sentido cidade (772) | E1, E2, 39A, Aircoach 700 | 882 m · 11,0 min | 1.504 m · 18,8 min | B |
| Donnybrook Depot, sentido UCD (760) | E1, E2, 39A | 903 m · 11,3 min | 1.540 m · 19,2 min | B |
| **Victoria Avenue (758)** | E1, E2, 39A, 11B | **932 m · 11,7 min** | 1.158 m · 14,5 min | B |
| Donnybrook Village, sentido cidade (775) | E1, E2, 39A, 11B | 955 m · 11,9 min | 1.158 m · 14,5 min | B |
| Donnybrook Village, sentido UCD (757) | E1, E2, 39A, 11B | 1.013 m · 12,7 min | 1.162 m · 14,5 min | C |
| **Donnybrook Stadium (759)** | E1, E2, 39A, 11B, Aircoach 700 | **1.025 m · 12,8 min** | 1.247 m · 15,6 min | C |
| Donnybrook Stadium, sentido cidade (773) | idem | 1.066 m · 13,3 min | 1.288 m · 16,1 min | C |
| Morehampton Terrace (776) | E1, E2, 39A, 11B, 44 no desvio | 1.114 m · 13,9 min | 1.140 m · 14,2 min | C |
| Teresian School (771, terminal da 39A após 11h) | 39A | 1.256 m · 15,7 min | 1.878 m · 23,5 min | C |
| Waterloo Road (753) | 38, 38A, 39, 70 (cortadas no dia) | 1.423 m · 17,8 min | 1.250 m · 15,6 min | C |
| Tritonville Road (desvio de 4/7/7A após 11h) | 4, 7, 7A desviadas | 1.469 m · 18,4 min ⚠ | 1.252 m · 15,7 min | C ⚠ |
| Sandford Road / Norwood Park (855/884) | 11, 44 em dia normal | 1.496–1.521 m · 19 min | 1.721 m · 21,5 min | C/D |
| Park Avenue, Sandymount (7739/7740) | 47, C1, C2 | 1.521–1.593 m · 19–20 min ⚠ | 1.298 m · 16,2 min | D ⚠ |
| Sandymount Green (desvio de 4/7/7A) | 4, 7, 7A desviadas | 1.664 m · 20,8 min ⚠ | 1.327 m · 16,6 min | D ⚠ |
| Grand Canal Dock (DART, terminal sul no dia) | DART | 1.832 m · 22,9 min | 1.616 m · 20,2 min | D |
| Sussex Road (terminal da E1 até 11h) | E1 | 1.950 m · 24,4 min | 1.778 m · 22,2 min | D |
| Ranelagh (Luas verde) | Luas | 2.336 m · 29,2 min | 2.363 m · 29,5 min | D |
| Strand Road / Merrion Gates (desvio de 4/7/7A/47) | 4, 7, 7A, 47 desviadas | 2.757 m · 34,5 min ⚠ | 2.534 m · 31,7 min | D ⚠ |

⚠ = a leste da Merrion Road: exige atravessar o percurso da maratona a pé.

**Duas leituras que saltam da tabela.** Primeiro, as paradas de Donnybrook ficam a
11–13 min do portão da Anglesea, **não a 10**: a tolerância do usuário fica estourada
por 1 a 3 min, o que ainda é aceitável, mas pede sinalização desde a parada. Segundo,
o portão da Anglesea é **2–3 min mais perto de Donnybrook** que o da Merrion Road, e
a caminhada Donnybrook → Anglesea corre inteira **fora do percurso** da maratona
(Donnybrook Road → Anglesea Road). Essa é a vantagem concreta de mudar o portão.

## 3. O ranking

Ordenado por **janela útil no dia × frequência**, com a caminhada como desempate. As
frequências são as de domingo no horário programado, na parada mais próxima.

### Nível 1 — eixo de Donnybrook, o único que funciona no dia

| # | Linha | Serviço no dia | Caminhada | Frequência de domingo (programada) | Observações |
|---|---|---|---|---|---|
| **1** | **E1** Bray/Ballywaltrim – Northwood | ●● | B (774/758: 11–12 min) | 8–11h: 9 ônibus/sentido (~19 min); 11–17h: 24 (~15 min) | A única linha que serve Donnybrook **nas duas janelas**. Até 11h roda só Bray ↔ Sussex Road (Leeson St): quem vem do norte da cidade **não** a alcança antes das 11h. Paradas 774/758/759 confirmadas por escrito pela prefeitura. |
| **2** | **39A** Ongar – UCD | ● | B (774/758: 11–12 min); terminal 771: C | 8–11h: nada em Donnybrook; 11–17h: 23–24 (~15 min) | Até 11h roda só Ongar ↔ Luke Street (centro). Depois, cidade ↔ Teresian School (771) por Donnybrook. Liga o oeste e o noroeste (Blanchardstown, Ongar, Navan Road) em um só ônibus. |
| **3** | **E2** Dún Laoghaire – Harristown | ● | B (774/758: 11–12 min) | 8–11h: nada em Donnybrook; 11–17h: 23–24 (~15 min) | Até 11h roda só Harristown ↔ Nassau Street; o trecho sul (Dún Laoghaire – Nassau St, que passa por Donnybrook) **não é operado**. O "shuttle" das 6h–11h cobre só Dún Laoghaire ↔ Stillorgan SC. **Contradiz a prefeitura**, que diz "o dia todo" — ver `divergencias_garda_dublinbus.md`. |

**Capacidade do eixo, para dimensionar (premissa):** depois das 11h, E1 + E2 + 39A somam
~12 ônibus/hora por sentido; a ~90 lugares cada, ~1.080 lugares/hora por sentido. O
comparecimento esperado é de 11.499 pessoas em 9 h, ~1.280/hora, das quais só uma parte
vem de ônibus. Antes das 11h, com **só a E1 (3–4 ônibus/hora, ~300 lugares)**, o eixo
fica apertado. O risco é das 8h às 11h, não da tarde.

### Nível 2 — passam pelo corredor por causa do desvio; paradas não confirmadas

| # | Linha | Serviço no dia | Caminhada | Frequência de domingo | Observações |
|---|---|---|---|---|---|
| **4** | **14** Dundrum Luas – Beaumont | ●● (parcial até 11h) | B/C, se parar em Donnybrook Rd | 2–3 ônibus/hora/sentido (~20–30 min) | Até 11h roda só Dundrum ↔ Adelaide Road, via Stillorgan Rd e Donnybrook Rd; depois, rota inteira pelo mesmo corredor. Única ligação direta de Dundrum, Churchtown e Goatstown. **Pedir à Dublin Bus que confirme paradas.** |
| **5** | **11B** Phoenix Park – Donnybrook Stadium | ● (a partir de ~12h) | B/C (759: 13 min; 774: 11 min) | 12 viagens/sentido, 11h45–17h50 (~30 min) | Domingo só começa ao meio-dia. Termina em Donnybrook Stadium, sem desvio no trecho sul. Serve o norte (Phibsborough, Cabra) e o centro. |
| **6** | **11** Phoenix Park – Sandyford | ● | B/C, se parar em Donnybrook Rd | 2 ônibus/hora/sentido (~30 min) | Sem serviço antes das 11h. Depois, desviada por Leeson St – Donnybrook – Stillorgan Rd. Em dia normal passa por Ranelagh e Milltown, a 19 min do portão. |
| **7** | **44** Enniskerry – DCU | ●● | C (Morehampton Terrace / Donnybrook Village: 12–14 min) | 1 ônibus/hora/sentido | Desviada por Morehampton Rd e Stillorgan Rd o dia todo. Frequência horária a torna pouco útil, mas liga Enniskerry, Dundrum e Drumcondra sem baldeação. |

### Nível 3 — paradas na porta, mas sem serviço na maior parte do dia

| # | Linha | Serviço no dia | Caminhada | Frequência de domingo | Observações |
|---|---|---|---|---|---|
| **8** | **4** Monkstown – Heuston | ◐ | **A** (416/485: 5,5–6,3 min) | Primeiros ônibus no RDS: 8h20 (sentido Blackrock) e 8h24 (sentido cidade); 8–11h: 2/hora/sentido | A Dublin Bus mantém a rota normal pela Merrion Road **até 11h**; a Garda fecha a Merrion Road **às 10h** e o organizador marca **9h40**. Na prática, 3 a 4 ônibus por sentido antes do fechamento. Depois das 11h é desviada por Ringsend – Sandymount – Strand Road e só se aproxima a 18–21 min, do outro lado do percurso. **Não anunciar aos eleitores.** |
| **9** | **7 / 7A** Brides Glen / Loughlinstown – Mountjoy Sq | ○ | A em dia normal | ~40 min cada; 20 min juntas | O aviso de 07/10 **não traz janela "até 11h" para 7 e 7A**: a diversão por Strand Road vale desde as 8h. Nenhum ônibus da 7/7A passa pelo RDS no dia. **Corrige a `sessao1.md`**, que as tratava como úteis até as 10h. Sem a 7/7A e sem o DART (abaixo), **Blackrock, Monkstown e Dún Laoghaire ficam sem acesso direto** ao RDS; a alternativa é a E2 a partir das 11h, ou a E1 a partir de Loughlinstown/Cornelscourt. |

### Fora do ranking

| Linha | Por quê |
|---|---|
| **S2** Heuston – Sean Moore Rd | Passa no RDS em dia normal (3/hora), mas no dia **não roda até 10h30** e, a partir das 11h, termina em Burlington Mews (Waterloo Rd), a 18 min. |
| **47, C1, C2** | Paradas de Sandymount a 19–20 min, do outro lado do percurso; 47 horária e desviada por Rock Road; C1/C2 não chegam a Sandymount antes das 11h. |
| **7E, 27X, 7B, 7D** | **Zero viagens aos domingos** no GTFS (7E: 7 viagens semanais; 27X: 15; 7B: 45; 7D: 10). Confirma a hipótese da `sessao1.md` com a fonte primária. |
| **37, 38, 38A, 39, 70** | No dia terminam em Luke Street (centro); não chegam a Waterloo Road / Burlington Road. |
| **DART (Sandymount, Lansdowne Road)** | **Fechadas de 24 a 26/10** por obras da Irish Rail: sem trens entre Grand Canal Dock e Bray; o DART roda só Malahide ↔ Grand Canal Dock. O GTFS confirma: o serviço de domingo (296) é retirado em 25/10 e o serviço especial (239) não para em nenhuma estação entre Grand Canal Dock e Dún Laoghaire. A pergunta pendente à prefeitura sobre "quem desce em Sandymount" **perde o objeto**. O Leap Card é aceito nos ônibus TFI, o que empurra o eleitorado da costa sul para a E2/E1. |
| **Luas** | Ranelagh (linha verde) a 29 min a pé. Não serve. |
| **Outros operadores** (Aircoach 700 em Donnybrook Stadium, 2/hora; Aircoach 702 no RDS, 1/hora; Bus Éireann 2 e 133; Wexford Bus 740) | Passam pelo corredor em dia normal, mas **nenhum publicou desvio** e todos usam ruas fechadas (Merrion Rd, Nutley Lane ou N11). Não contar com eles. |

## 4. O que isso muda no plano

1. **A mensagem ao eleitor tem um só eixo:** "venha pela E1 (ou, a partir das 11h, pela
   E2 e pela 39A), desça em Donnybrook (paradas 774, 758 ou 759) e caminhe 11–13 min
   pela Donnybrook Road e pela Anglesea Road até o portão". Nada de Merrion Road,
   nada de DART.
2. **A janela crítica é 8h–11h**, quando só a E1 serve o corredor, e só a partir do sul.
   Quem mora no norte ou no oeste da cidade e quer votar cedo depende de chegar ao
   centro e caminhar, ou de esperar as 11h. Vale pedir à Dublin Bus que a E2 e a 39A
   rodem o trecho sul desde as 8h (a Donnybrook Road está aberta, pela Garda).
3. **A costa sul (Dún Laoghaire – Blackrock) perde DART e 7/7A ao mesmo tempo.** É o
   grupo com mais a perder; a E2 só a partir das 11h não cobre a manhã.
4. **Sinalização desde a parada 774**: a caminhada passa de 10 min e tem uma curva (de
   Donnybrook Road para Anglesea Road) que o eleitor não conhece. Um voluntário na
   esquina ou uma placa resolvem.
5. Cada caminhada aqui pressupõe o portão no meio da testada da Anglesea Road. **Fixar
   o portão com o RDS antes de imprimir qualquer mapa.**

## 5. Reprodução

```
python3 -I scripts/transporte_gtfs_domingo.py <pasta GTFS descompactada> saida.json 1500
python3 -I scripts/transporte_caminhadas.py saida.json caminhadas.json
```

O primeiro lê o GTFS da NTA e grava, para cada linha e sentido com parada a até 1.500 m
do portão, a parada mais próxima e as viagens de domingo 25/10 por hora. O segundo mede
a caminhada de cada parada até os dois portões no roteador a pé do OpenStreetMap. As
saídas desta sessão estão em `dados/`. O GTFS (37 MB) não está no repositório; baixe de
`https://www.transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip`.
