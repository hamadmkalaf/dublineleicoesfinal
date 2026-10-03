# Montagem da fita no chão — Hall 2, lista de corte

Gerado em 2026-10-03 por `scripts/separadores_montagem.py`, a partir da geometria de `scripts/separadores_fila.py` (desenho definitivo de 17/09, cenário `Paredes_ABC`). Mapa cotado: `saidas/montagem_fita_hall2.svg` (e `.png`); página para o celular: `saidas/montagem_fita_hall2.html`.

**Medidas em metros.** `x` conta da parede oeste; `y` conta da linha das portas da fachada sul (a mesma origem de `data/prancheta_hall2.json`). Um ponto é `(x; y)`.

## Regras que valem para tudo

- Avenida: duas fitas paralelas a **3,00 m** uma da outra (a boca da A tem 3,20 m, porque o trilho externo encosta na alvenaria entre S4 e S5).
- A fita só abre **vão de 1,10 m** onde entra um ramal. Fora isso é contínua.
- O que é **unifila** não leva fita: as bocas de A e C (6,00 m de cada trilho, contados da porta), a avenida B inteira e os três serpenteados. Montar a unifila primeiro; a fita começa onde o último poste acaba.
- Ramal: canal de 1,10 m, na cor da zona, do trilho da avenida até a frente da mesa. Linha de espera **zebrada** a 1,50 m da mesa, atravessando o canal. Marcas de 0,25 m a cada 0,65 m, da linha de espera para fora.
- Rótulo no chão por **grupo e seção**, nunca por número de mesa.

## 1. Na porta: onde cada fita começa

| Avenida | Porta | Trilho interno | Trilho externo | Entre fitas |
|---|---|---|---|---|
| **A** | S4 (vão 5,93 m, x 19,10–25,03) | x = 21,83 · 2,73 m do batente oeste | x = 25,03 · no batente leste | **3,20 m** |
| **B** | S5 (vão 5,93 m, x 25,32–31,25) | x = 26,80 · 1,48 m do batente oeste | x = 29,80 · 1,45 m do batente leste | **3,00 m** |
| **C** | S6 (vão 5,93 m, x 31,54–37,47) | x = 32,00 · 0,46 m do batente oeste | x = 35,00 · 2,47 m do batente leste | **3,00 m** |

Entre a fita externa de A e a interna de B: 1,77 m. Entre a externa de B e a interna de C: 2,20 m. A alvenaria entre portas tem 0,29 m.

## 2.1. Avenida A · azul · S4 → parede oeste

**Trilho interno (lado da parede)** — 47,13 m no total: 6,00 m em unifila, 31,60 m em fita.

| # | De `(x; y)` | Até `(x; y)` | m | Unifila | Fita | Observação |
|---|---|---|---:|---:|---:|---|
| 1 | (21,83; 0,00) | (21,83; 3,40) | 3,40 | 3,40 | — |  |
| 2 | (21,83; 3,40) | (11,00; 3,40) | 10,83 | 2,60 | 8,23 | a unifila acaba em (19,23; 3,40); daí em diante, fita |
| 3 | (11,00; 3,40) | (11,00; 36,30) | 32,90 | — | 23,37 | 9 pedaços com 9 vãos de 1,10 m (abaixo) |

Pedaços do segmento 3 (x = 11,00), de sul para norte. Cada vão é a boca de um ramal; o primeiro pedaço começa onde a unifila acaba (3,40).

| Pedaço | y de | y até | m | Vão seguinte (y) |
|---|---:|---:|---:|---|
| 1 | 3,40 | 7,48 | 4,08 | 7,48–8,58 |
| 2 | 8,58 | 11,38 | 2,80 | 11,38–12,48 |
| 3 | 12,48 | 13,78 | 1,30 | 13,78–14,88 |
| 4 | 14,88 | 17,68 | 2,80 | 17,68–18,78 |
| 5 | 18,78 | 22,57 | 3,79 | 22,57–23,67 |
| 6 | 23,67 | 25,37 | 1,70 | 25,37–26,47 |
| 7 | 26,47 | 29,27 | 2,80 | 29,27–30,37 |
| 8 | 30,37 | 31,67 | 1,30 | 31,67–32,77 |
| 9 | 32,77 | 35,57 | 2,80 | 35,57–36,67 |

**Trilho externo (lado do campo)** — 47,33 m no total: 6,00 m em unifila, 41,33 m em fita.

| # | De `(x; y)` | Até `(x; y)` | m | Unifila | Fita | Observação |
|---|---|---|---:|---:|---:|---|
| 1 | (25,03; 0,00) | (25,03; 6,40) | 6,40 | 6,00 | 0,40 | a unifila acaba em (25,03; 6,00); daí em diante, fita |
| 2 | (25,03; 6,40) | (14,00; 6,40) | 11,03 | — | 11,03 |  |
| 3 | (14,00; 6,40) | (14,00; 36,30) | 29,90 | — | 29,90 |  |

## 2.2. Avenida B · amarelo · S5 → parede norte

**Trilho interno (lado da parede)** — 35,40 m no total: 35,40 m em unifila, 0,00 m em fita.

| # | De `(x; y)` | Até `(x; y)` | m | Unifila | Fita | Observação |
|---|---|---|---:|---:|---:|---|
| 1 | (26,80; 0,00) | (26,80; 35,40) | 35,40 | 35,40 | — |  |

**Trilho externo (lado do campo)** — 35,40 m no total: 35,40 m em unifila, 0,00 m em fita.

| # | De `(x; y)` | Até `(x; y)` | m | Unifila | Fita | Observação |
|---|---|---|---:|---:|---:|---|
| 1 | (29,80; 0,00) | (29,80; 35,40) | 35,40 | 35,40 | — |  |

## 2.3. Avenida C · laranja · S6 → parede leste

**Trilho interno (lado da parede)** — 40,00 m no total: 6,00 m em unifila, 34,00 m em fita.

| # | De `(x; y)` | Até `(x; y)` | m | Unifila | Fita | Observação |
|---|---|---|---:|---:|---:|---|
| 1 | (32,00; 0,00) | (32,00; 3,20) | 3,20 | 3,20 | — |  |
| 2 | (32,00; 3,20) | (33,50; 5,20) | 2,50 | 2,50 | — |  |
| 3 | (33,50; 5,20) | (33,50; 39,50) | 34,30 | 0,30 | 34,00 | a unifila acaba em (33,50; 5,50); daí em diante, fita |

**Trilho externo (lado do campo)** — 40,00 m no total: 6,00 m em unifila, 23,00 m em fita.

| # | De `(x; y)` | Até `(x; y)` | m | Unifila | Fita | Observação |
|---|---|---|---:|---:|---:|---|
| 1 | (35,00; 0,00) | (35,00; 3,20) | 3,20 | 3,20 | — |  |
| 2 | (35,00; 3,20) | (36,50; 5,20) | 2,50 | 2,50 | — |  |
| 3 | (36,50; 5,20) | (36,50; 39,50) | 34,30 | 0,30 | 23,00 | a unifila acaba em (36,50; 5,50); daí em diante, fita; 11 pedaços com 10 vãos de 1,10 m (abaixo) |

Pedaços do segmento 3 (x = 36,50), de sul para norte. Cada vão é a boca de um ramal; o primeiro pedaço começa onde a unifila acaba (5,50).

| Pedaço | y de | y até | m | Vão seguinte (y) |
|---|---:|---:|---:|---|
| 1 | 5,50 | 6,60 | 1,10 | 6,60–7,70 |
| 2 | 7,70 | 9,00 | 1,30 | 9,00–10,10 |
| 3 | 10,10 | 12,90 | 2,80 | 12,90–14,00 |
| 4 | 14,00 | 15,30 | 1,30 | 15,30–16,40 |
| 5 | 16,40 | 19,20 | 2,80 | 19,20–20,30 |
| 6 | 20,30 | 21,60 | 1,30 | 21,60–22,70 |
| 7 | 22,70 | 25,50 | 2,80 | 25,50–26,60 |
| 8 | 26,60 | 28,30 | 1,70 | 28,30–29,40 |
| 9 | 29,40 | 31,10 | 1,70 | 31,10–32,20 |
| 10 | 32,20 | 35,00 | 2,80 | 35,00–36,10 |
| 11 | 36,10 | 39,50 | 3,40 | fim do trilho |

## 3. Distribuidor do T (parede norte) · fita amarela · y = 35,40

Linha reta de x = 10,20 a x = 42,30, interrompida pela boca da avenida B (x 26,80–29,80, onde os postes chegam) e pelos 9 vãos dos ramais. 20,28 m de fita em 9 pedaços, de oeste para leste:

| Pedaço | x de | x até | m |
|---|---:|---:|---:|
| 1 | 10,20 | 11,31 | 1,11 |
| 2 | 12,41 | 15,21 | 2,80 |
| 3 | 16,31 | 18,01 | 1,70 |
| 4 | 19,11 | 24,68 | 5,57 |
| 5 | 25,78 | 26,80 | 1,02 |
| 6 | 29,80 | 30,98 | 1,18 |
| 7 | 32,08 | 34,88 | 2,80 |
| 8 | 35,98 | 37,28 | 1,30 |
| 9 | 38,38 | 41,18 | 2,80 |

## 4. Da fita à mesa, por parede

| Parede | Fita da avenida | → linha de espera | → frente do módulo | → parede | Marcas no canal |
|---|---|---:|---:|---:|---:|
| **oeste** | x = 11,00 (trilho interno de A) | 5,40 m | 6,90 m | 11,00 m | 8 |
| **norte** | y = 35,40 (distribuidor do T) | 3,40 m | 4,90 m | 9,00 m | 5 |
| **leste** | x = 36,50 (trilho externo de C) | 5,20 m | 6,70 m | 10,80 m | 8 |

A parede leste é a linha das mesas, x = 47,30; os 3,00 m até a fachada (50,30) são a faixa protegida das saídas de emergência L1–L4.

## 5. Os 28 ramais

Eixo do canal medido da **parede norte** (paredes oeste e leste) ou da **parede oeste** (parede norte). "Espaço" é a fita contínua entre este ramal e o vizinho, nos dois sentidos.

| Nº | Grupo | Seções | Parede | Eixo `(x; y)` | Eixo, da referência | Espaço até os vizinhos | Canal | Marcas |
|---:|---|---|---|---|---|---|---:|---:|
| 1 | **A1** | 3309 · 1314 | oeste | (11,00; 8,03) | 36,37 m da parede norte | 2,80 | 6,90 | 8 |
| 2 | **A1** | 3142 · 1278 | oeste | (11,00; 11,93) | 32,47 m da parede norte | 2,80 / 1,30 | 6,90 | 8 |
| 3 | **A2** | 3161 · 3307 | oeste | (11,00; 14,33) | 30,07 m da parede norte | 1,30 / 2,80 | 6,90 | 8 |
| 4 | **A2** | 3311 · 3913 | oeste | (11,00; 18,23) | 26,17 m da parede norte | 2,80 / 3,79 | 6,90 | 8 |
| 5 | **A3** | 3313 · 3889 | oeste | (11,00; 23,12) | 21,28 m da parede norte | 3,79 / 1,70 | 2,70 até o serpenteado | serp. |
| 6 | **A4** | 513 · 1105 | oeste | (11,00; 25,92) | 18,48 m da parede norte | 1,70 / 2,80 | 6,90 | 8 |
| 7 | **A4** | 1352 · 522 | oeste | (11,00; 29,82) | 14,58 m da parede norte | 2,80 / 1,30 | 6,90 | 8 |
| 8 | **A5** | 3078 · 2847 | oeste | (11,00; 32,22) | 12,18 m da parede norte | 1,30 / 2,80 | 6,90 | 8 |
| 9 | **A5** | 3179 · 530 | oeste | (11,00; 36,12) | 8,28 m da parede norte | 2,80 | 6,90 | 8 |
| 10 | **B1** | 512 · 2855 | norte | (11,86; 35,40) | 11,86 m da parede oeste | 2,80 | 4,90 | 5 |
| 11 | **B1** | 1160 · 3845 | norte | (15,76; 35,40) | 15,76 m da parede oeste | 2,80 / 1,70 | 4,90 | 5 |
| 12 | **B2** | 3315 · 3778 | norte | (18,56; 35,40) | 18,56 m da parede oeste | 1,70 / 5,57 | 0,70 até o serpenteado | serp. |
| 13 | **B3** | 3108 · 3422 | norte | (25,23; 35,40) | 25,23 m da parede oeste | 5,57 / 2,80 | 4,90 | 5 |
| 14 | **B3** | 3302 · 3181 | norte | (29,13; 35,40) | 29,13 m da parede oeste | 2,80 / 1,30 | 4,90 | 5 |
| 15 | **B4** | 3305 · 521 | norte | (31,53; 35,40) | 31,53 m da parede oeste | 1,30 / 2,80 | 4,90 | 5 |
| 16 | **B4** | 3306 · 518 | norte | (35,43; 35,40) | 35,43 m da parede oeste | 2,80 / 1,30 | 4,90 | 5 |
| 17 | **B5** | 3308 | norte | (37,83; 35,40) | 37,83 m da parede oeste | 1,30 / 2,80 | 4,90 | 5 |
| 18 | **B5** | 3832 | norte | (41,73; 35,40) | 41,73 m da parede oeste | 2,80 | 4,90 | 5 |
| 19 | **C6** | 511 · 1100 | leste | (36,50; 35,55) | 8,85 m da parede norte | 2,80 | 6,70 | 8 |
| 20 | **C6** | 517 · 1292 | leste | (36,50; 31,65) | 12,75 m da parede norte | 1,70 / 2,80 | 6,70 | 8 |
| 21 | **C5** | 3322 · 3752 | leste | (36,50; 28,85) | 15,55 m da parede norte | 1,70 / 1,70 | 2,50 até o serpenteado | serp. |
| 22 | **C4** | 3054 · 1099 | leste | (36,50; 26,05) | 18,35 m da parede norte | 2,80 / 1,70 | 6,70 | 8 |
| 23 | **C4** | 3216 · 527 | leste | (36,50; 22,15) | 22,25 m da parede norte | 1,30 / 2,80 | 6,70 | 8 |
| 24 | **C3** | 3862 | leste | (36,50; 19,75) | 24,65 m da parede norte | 2,80 / 1,30 | 6,70 | 8 |
| 25 | **C3** | 3245 · 519 | leste | (36,50; 15,85) | 28,55 m da parede norte | 1,30 / 2,80 | 6,70 | 8 |
| 26 | **C2** | 3229 · 3821 | leste | (36,50; 13,45) | 30,95 m da parede norte | 2,80 / 1,30 | 6,70 | 8 |
| 27 | **C2** | 3688 | leste | (36,50; 9,55) | 34,85 m da parede norte | 1,30 / 2,80 | 6,70 | 8 |
| 28 | **C1** | 3442 | leste | (36,50; 7,15) | 37,25 m da parede norte | 1,30 | 6,70 | 8 |

Nos três grupos vermelhos (A3, B2, C5) o serpenteado em unifila — 3 trilhos de 4,20 m, raias de 1,40 m — ocupa os 4,20 m à frente do módulo; o ramal de fita vai do trilho da avenida até a borda do serpenteado.

## 6. Fita a colar, pelo que está neste mapa

| Cor | Onde | m |
|---|---|---:|
| Azul | avenida A (fita), 9 ramais da oeste, marcas | 206,7 |
| Amarelo | distribuidor do T, 9 ramais da norte, marcas | 111,3 |
| Laranja | avenida C (fita), 10 ramais da leste, marcas | 202,6 |
| Zebrado | 28 linhas de espera de 1,10 m | 30,8 |

São só os trechos cotados aqui, sem os galões de sentido, as setas de saída, o canal verde da preferencial S7 nem as bocas brancas de S2/S8. A compra de 17/09 (8 rolos; `docs/separadores/plano_separadores_fila.md` §4) foi dimensionada com margem e continua valendo.

## 7. Conferir em campo antes de colar

- **Topo da avenida A.** O trilho interno (o dos vãos) acaba em y = 35,57 e o externo sobe até y = 36,30: 0,90 m para dentro da banda norte, que começa em y = 35,40. Dali para cima o trecho não serve a nenhum ramal e corta a banda por onde o eleitor de B caminha; a mesa B1 (eleitor 10, x = 11,86) fica com a boca do ramal entre as duas fitas. Se o Posto encerrar os dois trilhos em y = 35,40, poupa 1,1 m de fita. É mudança no desenho fechado de 17/09: decisão do Posto, não deste mapa.
- **Topo da avenida C.** O trilho externo (o dos vãos) acaba em y = 39,50 e o interno sobe até y = 39,50: 4,10 m para dentro da banda norte, que começa em y = 35,40. Dali para cima o trecho não serve a nenhum ramal e corta a banda por onde o eleitor de B caminha; a mesa B4 (eleitor 16, x = 35,43) fica com a boca do ramal entre as duas fitas. Se o Posto encerrar os dois trilhos em y = 36,10, poupa 6,8 m de fita. É mudança no desenho fechado de 17/09: decisão do Posto, não deste mapa.
- **Linha de espera dentro do serpenteado.** `data/decisoes.json` põe o serpenteado dos três grupos vermelhos encostado na frente do módulo (de 4,10 a 8,30 m da parede), então a linha de espera a 1,50 m cai dentro da primeira raia. Em campo: colar a linha zebrada a 1,50 m da mesa e começar a primeira raia da unifila depois dela.
- **O item `trilho_sul_A` do catálogo** (y = 3,40, de x = 11,00 a 25,03) coincide com o trilho interno de A até x = 21,83; o resto, de 21,83 a 25,03, fecharia a boca da avenida. Não colar além de 21,83. Ele entra na conta de fita branca de 17/09 (14 m) sem fazer falta na compra.
- **Fita no piso do RDS**: continua sem confirmação escrita (pendência 1 de `PENDENCIAS.md`).
