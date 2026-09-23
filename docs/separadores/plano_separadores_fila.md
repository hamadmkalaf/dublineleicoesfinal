# Separadores de fila no Hall 2 — desenho definitivo

**Decidido em 17/09/2026.** A estrutura de fila é **fita no chão**; as 100
unifilas do orçamento (item d, EUR 1.303,00) vão onde a fita comprovadamente
não funciona. Este documento fixa o desenho, as cores, os rótulos e a
metragem.

Desenho: `saidas/separadores_definitivo.svg` · detalhe do ramal:
`saidas/separadores_detalhe.svg` · números: `scripts/separadores_fila.py`.
Geometria lida do cenário fechado `Paredes_ABC` — não altera nenhuma decisão de
15 e 16/09, nem a agregação de seções.

> **Revisão de 23/09/2026.** **A parede oeste trocou dois pares de posição** (a
> prancheta manda; ver `contexto.md` §5): os dois pares de maior carga foram para
> o norte da parede, longe da boca da avenida A, e os códigos de grupo
> acompanharam a posição — **A1 continua sendo o par mais ao sul**, mas agora é o
> das seções 513·1105 e 1352·522. **A geometria das avenidas não mudou.** O
> recuo das avenidas para o centro do salão foi pedido, desenhado e **recusado à
> vista da planta** no mesmo dia: com a avenida B recuada 5 m, ela e a C ficavam
> a 1,50 m uma da outra no meio do salão e espremiam o campo de reserva de fila.
> O registro do que ele custaria está na seção 4.

---

## 1. As três decisões de 17/09

**1. As cores são as das fitas já em estoque.** Zona A azul, zona B amarelo,
zona C laranja — as mesmas do artefato de sinalização, que já as usa nos painéis
de porta. *Desde 22/09 a zona C é vermelha* (adendo na seção 4). As zonas são as áreas servidas por cada porta: A = S4 = parede oeste,
B = S5 = parede norte, C = S6 = parede leste.

| Zona | Porta | Parede | Cor | Hex |
|---|---|---|---|---|
| A | S4 | oeste | azul | `#33507E` |
| B | S5 | norte | amarelo | `#E8C63A` |
| C | S6 | leste | vermelho (laranja até 22/09) | `#C8102E` |

> **Consequência que isso força:** amarelo virou cor de zona, então a **linha de
> espera não pode mais ser amarela** — viraria a cor da zona B no chão da zona
> A. Passa a **zebrado preto-e-branco**, que não colide com nenhuma zona e lê
> como "pare" em qualquer cultura. A rota de saída fica em branco e a
> preferencial em verde.

**2. Rótulo por grupo e por seção, nunca por número de mesa.** É a convenção que
o artefato de sinalização já fixou — *"Nenhum traz número de mesa: só as seções
do grupo"* — e ela está certa: o eleitor sabe a sua seção, não sabe que mesa é
a sua. As 28 mesas estão agrupadas em **16 grupos**: A1–A5 (5 na oeste), B1–B5
(5 na norte), C1–C6 (6 na leste). O agrupamento está versionado em
`data/grupos_mesas.json`, extraído do `sinalizacao_v2.json` e conferido contra o
artefato.

**3. As avenidas nunca se cruzam.** Não é promessa: é conferido. Cada avenida
vive numa faixa de x própria, e as três faixas são disjuntas.

```
A:  11,00 .. 25,03 m
B:  26,80 .. 29,80 m
C:  32,00 .. 36,50 m
```

`scripts/separadores_fila.py` roda essa conferência a cada execução e **sai com
código 1** se alguma avenida cruzar outra ou invadir zona protegida. Ela já
pegou um erro real: a primeira boca da avenida A ficava sobre o **recuo de
emergência S3** (x 14,22–21,47). A boca foi para a metade **leste** de S4, com o
trilho externo encostado na alvenaria de 0,29 m que separa S4 de S5.

---

## 2. Como o retorno também deixa de cruzar

A regra "avenidas não se cruzam" só vale se o fluxo de **saída** também não as
atravessar. Daí a regra que a completa:

> **As avenidas levam para dentro; as bandas trazem para fora.**

Quem votou não volta pelo campo central: sai andando pela **banda da sua própria
parede** até S2 (banda oeste) ou S8 (banda leste). Nenhum fluxo de saída
atravessa avenida nenhuma, e o campo central deixa de ser circulação — vira
reserva de fila, que é o que ele precisa ser.

Isso tem um preço, dito com todas as letras: a saída atravessa os **ramais** da
sua própria parede — 9 na oeste, 10 na leste. É um cruzamento entre um fluxo
contínuo (saída) e um intermitente (quem entra no seu ramal), dentro de uma
banda larga. É o cruzamento mais barato dos disponíveis, e é o preço de não ter
nenhum no campo central.

### A geometria

| Elemento | Medida |
|---|---|
| Banda da seção — oeste | 11,00 m da parede até o trilho da avenida |
| Banda da seção — norte | 9,00 m |
| Banda da seção — leste | 10,80 m |
| Avenidas | 3,00 m (A: 3,20 m, para encostar na alvenaria S4\|S5) |
| Ramal de mesa | canal de 1,10 m, da avenida até a linha de espera |
| Linha de espera | 1,50 m da mesa |
| Marcas de fila | tique a cada 0,65 m no canal |

**Avenida A (azul, S4 → oeste).** Sai pelos 3,20 m leste de S4, sobe 3,40 m,
vira a oeste por baixo das mesas da parede oeste e sobe rente à banda.
Distribui em **pente**: 5 aberturas, uma por grupo.

**Avenida B (amarela, S5 → norte).** Sobe reta e, **desde 24/09, a barreira dela
para em 33,6 m** — um par de unifilas antes da banda norte. Não distribui em
pente: chega perpendicular e termina numa **pequena avenida transversal**.

**A pequena avenida da parede norte (24/09).** Até 23/09 a avenida B encostava no
T, e o T era o único ponto do salão em que todo o fluxo de uma entrada (3.832
esperados) escolhia um lado **parado**, num metro quadrado. Tirando o último par
de unifilas — uma em cada trilho — a barreira para 1,80 m antes, e esse 1,80 m
vira uma faixa transversal de **1,80 × 25,50 m**, entre y = 33,60 e y = 35,40,
de x = 11,00 a x = 36,50. As duas bordas são fita; nenhuma é barreira. A escolha
de lado passa a acontecer **andando**, e a `P4-FimAvenidaB` é lida na boca dela.

Ela **para nas bordas das bandas oeste e leste** e não acompanha o distribuidor
até x = 42,30: fora delas cortaria o ramal do **A5** (y = 33,72) a oeste e o do
**C6** (y = 35,55) a leste, que correm em y constante na mesma altura — e a regra
de 17/09 é que ninguém cruze fila parada. `confere_avenida_norte()` reprova o
desenho se isso mudar; foi ela que apontou os dois ramais.

**Avenida C (vermelho, S6 → leste).** Sai pelos 3 m oeste de S6 — a leste de
x = 35,09 está o recuo da preferencial S7 — e abre para a banda leste, 6
aberturas.

---

## 3. As 96 unifilas

| Trecho | m | unifilas |
|---|---:|---:|
| Boca da avenida A (S4) · trilho do lado da parede | 6,0 | 5 |
| Boca da avenida A (S4) · trilho do lado do campo de retorno | 6,0 | 5 |
| Boca da avenida C (S6) · trilho do lado da parede | 6,0 | 5 |
| Boca da avenida C (S6) · trilho do lado do campo de retorno | 6,0 | 5 |
| Avenida B · trilho oeste do corredor | 33,6 | 20 |
| Avenida B · trilho leste do corredor | 33,6 | 20 |
| Serpenteado do grupo **A3** · seções 3313 · 3889 | 12,6 | 12 |
| Serpenteado do grupo **B2** · seções 3315 · 3778 | 12,6 | 12 |
| Serpenteado do grupo **C5** · seções 3322 · 3752 | 12,6 | 12 |
| **Total** | **129 m** | **96** |
| Reserva móvel | | **4** |

A avenida B entra **inteira** e por isso não tem item de boca separado — contar
as duas coisas seria contar os primeiros 6 m duas vezes.

**Por que aqui e não noutro lugar.** A barreira paga os três pontos onde a fita
não faz o serviço: (a) a **boca**, porque as três portas são contíguas e quem
entra pela errada não se perde — é conduzido até a parede errada; (b) a
**avenida B**, porque atravessa o piso aberto com a reserva de fila encostada nos
dois flancos; (c) as **três de alta carga** (roxas no desenho desde 22/09;
"vermelhas" até então), porque são os únicos lugares com multidão parada
declarada (~20 pessoas cada, decisão de 16/09).

**A reserva de 4 continua insuficiente, e isto não é detalhe.** Fita colada às 7h
não se move às 13h; a barreira é a única parte do desenho que responde a uma
surpresa. A pequena avenida devolveu 2 unidades — era 2, é 4 —, o que muda a
ordem de grandeza de coisa nenhuma. **Pedido: mais 15 unidades, EUR 195,45**,
para levar a reserva a 19. É 1,2% do orçamento do 1º turno.

Para o registro: o traçado completo — as três avenidas com os dois trilhos
inteiros, o T da parede norte, as 28 cabeças de fila, as bocas de saída e o
canal preferencial — pediria da ordem de 390 unifilas. As 100 orçadas são
**um quarto disso**. Por isso a fita faz o grosso.

---

## 4. A fita: metragem e estoque

| Cor | Onde | Necessário | Em estoque | Saldo |
|---|---|---:|---:|---:|
| **Azul** | avenida A, 9 ramais oeste, marcas, galões | **253,1 m** | 165 m | **−88,1 m** |
| **Amarelo** | avenida B, as duas bordas da pequena avenida, 9 ramais, marcas | **174,5 m** | 165 m | **−9,5 m** |
| **Vermelho** (era laranja até 22/09) | avenida C, 10 ramais leste, marcas, galões | **241,2 m** | — | **−241,2 m** |
| Zebrado preto-e-branco | as 28 linhas de espera | 30,8 m | — | comprar |
| Verde | canal da preferencial S7 | 20,0 m | — | comprar |
| Branco | rota de saída, setas do campo livre | 82,0 m | — | comprar |
| **Total** | | **802 m** | | |
| **Com 10% de retoque** | | **882 m** | | |

**Falta bastante fita azul, e toda a vermelha.** Assumindo 165 m **por cor** em
estoque (a confirmar — se for 165 m no total, a falta triplica), faltam **88 m de
azul e 241 m de vermelho**, mais as três cores que ainda não existem. O amarelo
passou a faltar em 24/09: a pequena avenida acrescentou 24,7 m e virou o saldo de
+15,2 para **−9,5 m**. Em rolos de 50 m a conta **não muda**, porque os 4 rolos de
amarelo já cobriam os 165 m de estoque mais a diferença: **2 azul + 5 vermelho +
1 zebrado + 1 verde + 2 branco = 11 rolos a comprar**, ordem de **EUR 140–220**
(*estimativa minha, a cotar*).

*Adendo de 23/09 — o recuo das avenidas, e por que ele não entrou.* O Posto pediu
alargar a banda de fila de cada parede empurrando a avenida daquela parede para
dentro do salão: 2 a 3 m para A e C, 5 a 10 m para B. O desenho foi feito, com
bandas de **13,00 / 14,00 / 13,00 m**, e **recusado à vista da planta**: a banda
norte só podia crescer 5 m (acima disso o T da avenida B cai em cima do
serpenteado do grupo C5, cuja raia mais ao norte está em y = 30,25), e com esses
5 m as avenidas B e C ficavam a **1,50 m** uma da outra no meio do salão,
espremendo o campo central que é a reserva de fila. O que ele custaria, para quem
quiser retomar a ideia: como cada um dos 28 ramais atravessa a banda inteira,
eles cresciam junto — o da norte dobrava, de 4,90 para 9,90 m — e a fita ia de
777 para **960 m** (a base de 23/09; hoje a vigente é 802), com os rolos a comprar
subindo de 11 para **18** (o amarelo, que então fechava com saldo positivo,
passaria a pedir 3). Em troca, a avenida B encurtava 5,00 m em cada trilho e
devolvia 6 unifilas. **A geometria vigente continua a de 22/09, com a única
mudança de 24/09: o par de unifilas que virou a pequena avenida da parede
norte.**

*Adendo de 22/09.* Até essa revisão a zona C era laranja e a conta fechava em 8
rolos (2 azul + 2 laranja). A decisão do Posto — vermelho no lugar do laranja, a
mesma da sinalização — deixa o rolo laranja em estoque sem uso neste desenho e
acrescenta os 5 rolos vermelhos. Os 8 m a mais de azul (244,8 → 253,1) são a
avenida A, que passou a terminar em y = 40,0 m em vez de 36,3 para servir o ramal
da mesa 3179·0530, deslocada para 37,62 m na mesma revisão. O vermelho `#C8102E`
é proposta até o rolo ser comprado: a peça impressa persegue a fita, então o hex
final é o do rolo.

Por que azul e vermelho passam tanto do amarelo: as bandas oeste (11,00 m) e
leste (10,80 m) são mais fundas que a norte (9,00 m), então os 9 ramais de A e os
10 de C são mais compridos — 6,90 e 6,70 m contra 4,90 m — e a avenida A ainda
tem a perna que vira para oeste. **A parede norte é barata em fita justamente
porque a avenida B chega perpendicular**: o T que é a fragilidade do traçado é
também o que encurta os seus ramais.

**O que a metragem não diz:** 802 m de fita colada, curva a curva, com 6 cores e
16 marcadores de grupo, é trabalho de véspera com o salão vazio — não meia hora
antes da abertura.

---

## 5. O desenho da fita, no detalhe

`saidas/separadores_detalhe.svg` mostra o trecho em escala: onde a barreira
acaba e a fita leva até a mesa.

| Elemento | Especificação |
|---|---|
| Avenida | 2 linhas contínuas a 3,00 m, galão a cada 5 m no sentido da marcha |
| Ramal | canal de 1,10 m, na cor da zona |
| Marcas de fila | tique de 0,25 m a cada **0,65 m** — 8 marcas = 8 pessoas |
| Linha de espera | faixa cheia de 1,10 m, **zebrado preto-e-branco**, a 1,50 m da mesa |
| Pegadas | duas, depois da linha: identificação e urna |
| Papel do grupo | plastificado, **fora da linha de pisada**, na borda do canal |

As marcas de 0,65 m são o passo de projeto do `plano_filas_confinado_hall2.md` (não transferido — vive em `claude/filas-sem-ring-3-b9qvqi`, no repositório de origem).
Materializadas no chão, dão ao mesário e ao pessoal de fluxo uma leitura
instantânea do tamanho da fila sem contar cabeças.

**O papel no chão confirma, nunca decide.** Um A4 no chão some atrás do corpo de
quem está na frente. O número que decide vai à altura dos olhos, no x-banner do
grupo — já orçado no item (c), EUR 1.961,00.

---

## 6. Dois achados para a sinalização

**1. O x-banner da parede leste está fora do salão útil.** O
`sinalizacao_v2.json` põe os seis x-banners da zona C em **x = 45,70**, medido a
4,60 m dos 50,30 m da fachada. Mas a linha das mesas da parede leste é
**x = 47,30** — os 3 m entre 47,30 e 50,30 são a **faixa protegida das saídas de
emergência L1–L4**. A 45,70 o x-banner fica atrás das mesas, dentro da faixa. O
valor certo é **42,70** (47,30 − 4,60). A oeste (4,60) e a norte (39,80) estão
corretas.

**2. Nos três grupos de alta carga, 4,60 m cai dentro do serpenteado.** O
serpenteado de A3, B2 e C5 ocupa de 4,10 a 8,30 m da parede. Um x-banner a
4,60 m fica no meio dele. Nesses três, o banner recua para **8,60 m** — logo
atrás da última raia, ainda visível de toda a fila.

Os dois são correções ao plano de sinalização, não a este desenho; o desenho já
os aplica.

---

## 7. O que ficou pelo caminho

Duas alternativas foram desenhadas e descartadas. Ficam em
`saidas/separadores_opcao1.svg` e `saidas/separadores_opcao2.svg` como registro
do porquê.

**Opção 1 — As três avenidas.** Toda a barreira nos flancos das avenidas,
nenhuma nas cabeças de fila. Aposta: o eleitor mal encaminhado custa mais que o
mal enfileirado. Descartada porque deixa as três de alta carga contidas só por fita
— e fila parada é exatamente onde a fita não segura. E, com a geometria
definitiva, custa **106 unifilas**: não cabe.

**Opção 2 — As cabeças de fila.** Toda a barreira nas 19 mesas de maior carga,
boca e avenidas na fita. Aposta: pressão só existe onde a fila é estática.
Descartada porque deixa a boca — o gargalo não paralelizável, 11,5 mil pessoas
por 18,4 m de porta — separada apenas por fita, e porque deixa 9 mesas sem
canal, o que é difícil de explicar ao mesário dessas mesas. Com a geometria
definitiva custa **111 unifilas** — também não cabe.

As duas deixaram de caber quando as bandas oeste e leste se aprofundaram para
11,00 e 10,80 m. **A definitiva é a única das três que cabe nas 100**, e isso não
foi arranjado: foi consequência de pôr as avenidas em faixas disjuntas e de
gastar a barreira onde a fita não serve.

---

## 8. O que ainda depende de terceiros

**Bloqueante, esta semana**

1. **O RDS permite fita adesiva no piso do Hall 2?** Qual tipo, e qual a
   exigência de remoção? O manual do expositor do RDS não é público e os manuais
   de outros eventos no mesmo recinto tratam de adesivo em painéis, não em piso.
   Vários recintos proíbem ou exigem resíduo zero com remoção integral. **Se a
   resposta for não, este desenho inteiro cai.**
2. Submeter o layout de barreira ao responsável de incêndio do RDS — barreira em
   zona de egresso muda o cálculo de evacuação, e isso se submete, não se
   comunica.

**Compras**

3. As **15 unifilas adicionais** (EUR 195,45) para a reserva móvel.
4. **11 rolos de fita**: 2 azul, 5 vermelho, 1 zebrado preto-e-branco, 1 verde,
   2 branco.
5. Confirmar se os 165 m em estoque são **por cor** ou no total.

**A aferir em campo, antes de imprimir**

6. As bandas de 11,00 / 9,00 / 10,80 m pressupõem o módulo de 4,10 m da planta
   medida e o serpenteado de 4,20 m de 16/09. Conferir com a mesa, a cabine e a
   urna reais.
7. A boca da avenida A deixa **36 cm** entre o trilho interno (x = 21,83) e o
   recuo de emergência S3 (até 21,47). É a folga mais apertada do traçado.
8. O **T da parede norte** é o ponto mais frágil. Se houver folga, vale estudar
   uma segunda perna para a avenida B — mas isso mexe na atribuição
   mesa → entrada, fechada desde 15/09.
9. Quem cola os 802 m de fita, e quando.

---

## 9. Como refazer

```bash
python3 scripts/separadores_fila.py           # conferência + relatório
python3 scripts/separadores_fila.py --grava   # + os 4 SVG e o JSON
```

Lê `data/prancheta_hall2.json`, `data/decisoes.json`,
`data/grupos_mesas.json` e `cenarios/paredes-abc-20260915.json`; não escreve em
nenhum deles. A conferência das avenidas sai com **código 1** se a geometria
quebrar a regra de 17/09.

**Fontes das premissas de material:**
[Queue Solutions](https://queuesolutions.com/retractable-belt-barriers/) ·
[Displays2Go](https://www.displays2go.com/C-24746/Retractable-Stanchions-Nylon-Belt-Barriers-Queue-Lines) ·
[Safety Direct2U](https://www.direct2u.co.uk/safety/standard-rectractable-belt-barrier-systems)
