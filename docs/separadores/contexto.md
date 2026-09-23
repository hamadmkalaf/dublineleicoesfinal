# Contexto — Separadores de fila e fita no chão no Hall 2

> **Tema:** como as 100 unifilas (Tensa de 2 m) e a fita adesiva de piso repartem
> entre si o trabalho de conduzir 11,5 mil eleitores da porta até a mesa
> receptora, no RDS Ballsbridge Hall 2, no 1º turno de 04/10/2026.
>
> Documento gerado ao fim da conversa de 17–18/09/2026, para ser lido por quem
> pegar este tema noutro repositório, sem o histórico. O roteiro de
> transferência que trouxe este tema para cá teve o seu registro de execução
> guardado em `docs/TRANSFERENCIA_REALIZADA.md`.

---

## 1. O problema, em um parágrafo

O Posto tem **100 unifilas** no orçamento (item d, EUR 1.303,00) e um salão que
precisa conduzir cada eleitor da porta até a mesa. A espera acontece **fora**, no
pátio de fila do Ring 3; dentro do Hall 2 o que há é o percurso porta → mesa, mais
o serpenteado à frente das três mesas de maior comparecimento. A chefia aprovou
**fita adesiva no chão** como
estrutura de fila, com o papel de sinalização das seções colado junto. A
pergunta que esta conversa respondeu não foi "como montar a fila com unifila",
e sim **que parte do desenho não pode ser fita** — porque o traçado completo do
Hall 2 pediria 395 unifilas, e as orçadas são 25% disso.

## 2. O que este tema herda, e não discute

Nada aqui mexe no que já estava fechado. O desenho lê estas decisões e as
respeita:

| Decisão | Quando | Onde vive |
|---|---|---|
| 28 mesas receptoras, agregação principal → agregada do Cartório | — | `data/decisoes.json` |
| Cenário `Paredes_ABC`: 9 mesas na oeste, 9 na norte, 10 na leste | 15/09 | `cenarios/paredes-abc-20260915.json` |
| Uma entrada por parede: A→oeste (S4), B→norte (S5), C→leste (S6) | 15/09 | `decisoes.entradas` |
| Portas: S4/S5/S6 entradas, S2/S8 saídas, S7 preferencial | 16/09 | `decisoes.sinalizacao_portas` |
| Zonas protegidas: recuos de S3, S7, R1, N2, O2 e faixa de emergência leste | 16/09 | `decisoes.zonas_protegidas` |
| Serpenteado de ~20 pessoas à frente de cada mesa de alta carga | 16/09 | `decisoes.serpenteados` |
| Módulo de 4,10 m de profundidade, 0,90 m de largura | — | `data/prancheta_hall2.json` |
| 16 grupos de mesas (A1–A5, B1–B5, C1–C6) e as suas seções | — | `data/grupos_mesas.json` |

As três mesas de alto comparecimento — as "vermelhas" até 22/09, **roxas** no
desenho desde então, porque vermelho passou a ser a cor da zona C — são os grupos **A3**
(seções 3313 · 3889), **B2** (3315 · 3778) e **C5** (3322 · 3752), com 586 a 590
comparecentes esperados cada.

## 3. As premissas de material

**A unifila rende menos do que o orçamento sugere.** Uma cinta de 2,00 m só fica
esticada com os postes a cerca de **1,80 m** — 90% do comprimento da cinta é a
regra corrente dos fabricantes. E **cada trecho independente custa um poste a
mais**, o terminal. Um trecho contínuo de L metros custa `ceil(L / 1,80) + 1`
postes. Os "200 metros" do orçamento são comprimento nominal de cinta:
esticados e repartidos em trechos, as 100 unidades rendem perto de **170 m de
linha útil**.

**A fita se compra por cor, em rolo.** A conta útil não é "metros de fita", é
"metros de cada cor" — é isso que quem compra precisa. Rolo de referência: 50 m.
Margem de 10% para o retoque do meio-dia e perdas de corte.

**As fitas em estoque** (foto de 17/09): azul, amarelo e laranja, **165 m** —
está por confirmar se são 165 m por cor ou no total.

## 4. O traçado

**Banda da seção.** Cada parede usada reserva uma faixa que contém o módulo
(4,10 m), o serpenteado (4,20 m) e a circulação de saída: **11,00 m na oeste,
9,00 m na norte, 10,80 m na leste**. A banda vai da parede até o trilho mais
próximo da avenida daquela parede, e alargá-la é literalmente empurrar a avenida
para o centro do salão — foi o que se tentou em 23/09, e não passou (§5).

**Avenidas.** Uma por entrada, 3,00 m de largura (a A tem 3,20 m, para o trilho
externo encostar na alvenaria de 0,29 m entre S4 e S5).

- **A (azul, S4 → oeste).** Sai pelos 3,20 m **leste** de S4 — a metade oeste da
  porta está sobre o recuo de emergência S3, que vai até x = 21,47 —, sobe
  3,40 m, vira a oeste por baixo das mesas da parede oeste e sobe rente à banda.
  Distribui em **pente**, 5 aberturas.
- **B (amarela, S5 → norte).** Sobe reta, 35,4 m, e **termina em T**: todo o
  fluxo da entrada B (3.832 esperados) passa por um só metro quadrado antes de
  se repartir. É a fragilidade conhecida do traçado.
- **C (vermelho desde 22/09; laranja até então, S6 → leste).** Sai pelos 3 m **oeste** de S6 — a leste de
  x = 35,09 está o recuo da preferencial S7 — e abre para a banda leste, 6
  aberturas.

**Ramal de mesa.** Canal de 1,10 m da avenida até 1,50 m da mesa: 6,90 m na
oeste, 4,90 m na norte, 6,70 m na leste. O ramal atravessa a banda inteira, então
alargar a banda alonga os 28 ramais de uma vez — é daí que viria quase toda a
fita a mais do recuo recusado em 23/09. Marcas de 0,65 m no chão — o passo de
projeto do plano de filas —, que dão ao mesário a leitura do tamanho da fila sem
contar cabeças.

**Linha de espera.** Faixa cheia de 1,10 m a 1,50 m da mesa. É a linha do sigilo
do voto: só passa quem o mesário chamar. É o único elemento do desenho com
função procedimental, não de fluxo.

**Saída.** Campo livre, sem canal. Quem já votou está disperso e sem pressa;
canalizar a saída dobraria a fita e criaria 28 cruzamentos com os ramais.

## 5. As decisões desta conversa

### 17/09 — as três que o Posto fixou

**1. As cores são as das fitas em estoque.** A azul `#33507E`, B amarelo
`#E8C63A`, C laranja `#DE7343` — as mesmas do artefato de sinalização; **desde
22/09 a C é vermelha `#C8102E`**, rolo a comprar, e as três mesas de alta carga,
as portas de emergência e os avisos deixaram o vermelho semântico (roxo
`#6A1B9A`, verde-água `#0E8A74` e cinza `#333A42`), para que vermelho signifique
só "zona C" no desenho
(`Ek3FfeYnwvQLZEs4ZJ5Zzr`), que já as usa nos painéis de porta. *Consequência
que isso força:* amarelo virou cor de zona, então a **linha de espera não pode
mais ser amarela** — passa a **zebrado preto-e-branco**. Saída em branco,
preferencial em verde. São **seis cores de rolo** ao todo.

**2. Rótulo por grupo de mesas e por seção, nunca por número de mesa.** É a
convenção que o artefato já fixou — *"Nenhum traz número de mesa: só as seções
do grupo"* — e ela está certa: o eleitor sabe a sua seção, não sabe que mesa é a
sua.

**3. As avenidas nunca se cruzam.** Cada uma vive numa faixa de x própria, e as
três faixas são disjuntas: A 11,00–25,03, B 26,80–29,80, C 32,00–36,50. A folga
entre a B e a C é de 2,20 m. Foi essa folga que matou o recuo de 23/09: com as
avenidas recuadas ela caía para 1,50 m e o campo central ficava espremido entre
duas avenidas quase encostadas.

### 23/09 — o recuo das avenidas foi desenhado e recusado

O Posto pediu **mais espaço para as filas encostadas nas paredes de mesa**:
empurrar A e C 2 a 3 m para o lado da B (*"para não afetar a visibilidade dos
painéis"*) e a B 5 a 10 m para o centro. Foi desenhado, com bandas de 13,00 m na
oeste, 14,00 na norte e 13,00 na leste, e **recusado à vista da planta**. Fica
aqui porque a conta e o motivo valem para quem retomar a ideia.

**Por que a banda norte não passava de 14,00 m.** O T da avenida B é a borda sul
da banda norte, e ele tem de cair entre o serpenteado do grupo C5, cuja raia mais
ao norte está em y = 30,25, e o ramal do grupo C6, em y = 31,65. Com 14,00 m o T
cai em y = 30,40 e passa a 0,15 m do serpenteado; com 15,00 m ele cairia **em
cima** dele. A próxima posição livre só aparece ao sul do serpenteado (y < 27,45),
o que daria uma banda norte de 17 m, e ela engoliria um pedaço da banda leste.
**Os 5 m eram o máximo que a geometria dava sem mexer no serpenteado da C5**, que
é decisão de 16/09.

**Por que não passou.** Com esses 5 m, as avenidas B e C ficavam a **1,50 m** uma
da outra no meio do salão — a folga entre elas é hoje de 2,20 m —, e o campo
central, que é a reserva de fila e a única área livre de escala do salão, era
espremido entre duas avenidas quase encostadas. O desenho ficou pior do que o
problema que ele resolvia.

**O que custava, se voltasse à mesa.** Cada um dos 28 ramais atravessa a banda
inteira, então todos cresciam junto — o da norte dobrava, de 4,90 para 9,90 m — e
a fita ia de 777 para **960 m** (base de 23/09; a vigente é 802), com os rolos a
comprar subindo de 11 para **18**
(o amarelo, hoje com saldo positivo, passaria a pedir 3). Em troca, a avenida B
encurtava 5,00 m em cada trilho e devolvia 6 unifilas, que iriam para as bocas de
A e C e para a reserva móvel. **Barreira e fita andavam em sentidos opostos, e a
fita é a linha mais cara das duas.**

### A regra que completa a terceira

A regra "avenidas não se cruzam" só vale se o fluxo de **saída** também não as
atravessar. Daí:

> **As avenidas levam para dentro; as bandas trazem para fora.**

Quem votou sai andando pela banda da sua própria parede até S2 (banda oeste) ou
S8 (banda leste). Nenhum fluxo de saída atravessa avenida nenhuma, e o campo
central deixa de ser circulação — vira reserva de fila, que é o que ele precisa
ser. O preço, dito com todas as letras: a saída atravessa os **ramais** da sua
própria parede. É um cruzamento entre um fluxo contínuo e um intermitente, numa
banda larga — o mais barato dos disponíveis.

### A alocação definitiva

| Trecho | m | unifilas |
|---|---:|---:|
| Boca da avenida A (S4), dois trilhos, 6 m cada | 12,0 | 10 |
| Boca da avenida C (S6), dois trilhos, 6 m cada | 12,0 | 10 |
| Avenida B, os dois trilhos até a pequena avenida | 67,2 | 40 |
| Serpenteados dos grupos A3, B2 e C5 | 37,8 | 36 |
| **Total** | **129 m** | **96** |
| Reserva móvel | | **4** |

A avenida B entra inteira e por isso não tem item de boca separado — contar as
duas coisas seria contar os primeiros 6 m duas vezes.

**Por que aqui.** A barreira paga os três pontos onde a fita não faz o serviço:
(a) a **boca**, porque as três portas são contíguas — 0,29 m de alvenaria entre
elas, 18,4 m de porta no total — e quem entra pela errada não se perde, é
*conduzido até a parede errada*; (b) a **avenida B**, porque atravessa 34 m de
piso aberto com a reserva de fila encostada nos dois flancos; (c) as **três
de alta carga**, os únicos lugares com multidão parada declarada.

**A pequena avenida da parede norte (23/09 (v2)).** A avenida B deixa de encostar no
T: o **último par de unifilas** sai, a barreira para em y = 33,60 e esse 1,80 m
vira uma faixa transversal de 1,80 × 25,50 m entre as bandas oeste e leste. As
duas bordas são fita, nenhuma é barreira, e é ela que resolve o ponto mais
frágil do traçado — a escolha de lado passa a ser feita **andando**, e não
parada num metro quadrado. A faixa **não** acompanha o distribuidor até
x = 42,30: fora das bandas ela cortaria o ramal do A5 (y = 33,72) e o do C6
(y = 35,55), e `confere_avenida_norte()` reprova o desenho se isso mudar.
Devolve 2 unifilas e custa 24,7 m de fita amarela.

### A fita, por cor

| Cor | Necessário | Em estoque | Saldo |
|---|---:|---:|---:|
| Azul (zona A) | 253,1 m | 165 m | **−88,1 m** |
| Amarelo (zona B) | 174,5 m | 165 m | **−9,5 m** |
| Vermelho (zona C) | 241,2 m | — (era laranja) | **−241,2 m** |
| Zebrado preto-e-branco (linha de espera) | 30,8 m | — | comprar |
| Verde (preferencial S7) | 20,0 m | — | comprar |
| Branco (rota de saída) | 82,0 m | — | comprar |
| **Total** | **802 m** | | |
| **Com 10% de retoque** | **882 m** | | |

**Faltam 11 rolos de 50 m**: 2 azul, 5 vermelho, 1 zebrado, 1 verde, 2 branco.
Ordem de EUR 140–220 (*estimativa, a cotar*). Até 22/09 eram 8 rolos (2 azul,
2 laranja): a **revisão de 22/09** trocou a zona C de laranja para vermelho, e
o rolo laranja em estoque (165 m) deixa de servir ao desenho. Os 8 m a mais de
azul são a avenida A, que passou a terminar em y = 40,0 para servir o ramal da
mesa 3179·0530, deslocada para 37,62 m na mesma revisão. O recuo das avenidas de
23/09 levaria a conta a 18 rolos, e não entrou. Em **23/09 (v2)** a pequena avenida
acrescentou 24,7 m de amarelo e virou o saldo dessa cor de +15,2 para −9,5 m —
**sem mudar os 11 rolos**, porque os 4 rolos que o amarelo já pedia cobrem a
diferença.

Azul e vermelho passam tanto do amarelo porque as bandas oeste e leste são bem
mais fundas que a norte, então os seus ramais são mais compridos. **A parede
norte é barata em fita justamente porque a avenida B chega perpendicular:** o T
que era a fragilidade do traçado é também o que encurta os seus ramais — e é,
desde 23/09, o ponto que a peça `P4-FimAvenidaB` resolve, agora lida na boca da
pequena avenida de 23/09 (v2).

## 6. Achados

**1. A conferência pegou um erro real.** A primeira versão da boca da avenida A
ficava sobre o **recuo de emergência S3** (x 14,22–21,47). Só apareceu porque a
regra das avenidas foi escrita como conferência executável, e não como
afirmação no texto. A boca foi para a metade leste de S4.

**2. O x-banner da parede leste está fora do salão útil.** O
`sinalizacao_v2.json` põe os seis x-banners da zona C em **x = 45,70**, medido a
4,60 m dos 50,30 m da fachada. Mas a linha das mesas da parede leste é
**x = 47,30** — os 3 m entre 47,30 e 50,30 são a faixa protegida das saídas de
emergência L1–L4. A 45,70 o x-banner fica atrás das mesas, dentro da faixa. O
valor certo é **42,70**. A oeste (4,60) e a norte (39,80) estão corretas.

**3. Nos três grupos de alta carga, 4,60 m cai dentro do serpenteado.** O
serpenteado de A3, B2 e C5 ocupa de 4,10 a 8,30 m da parede; um x-banner a
4,60 m fica no meio dele. Nesses três o banner recua para **8,60 m** — logo
atrás da última raia, ainda visível de toda a fila.

Os achados 2 e 3 são correções ao **plano de sinalização**, não a este desenho;
o desenho já os aplica.

## 7. Onde eu discordo do desenho aprovado

**O papel colado no chão não é lido — é pisado.** Um A4 no chão some atrás do
corpo de quem está na frente, e depois de 11,5 mil pares de pés em nove horas
vira farrapo antes do meio-dia. Duas correções que não custam nada: papel
**plastificado**, colado **fora da linha de pisada**; e o número que *decide* à
altura dos olhos, no x-banner — já orçado no item (c), EUR 1.961,00. O chão diz
*por onde andar*; o banner diz *para onde ir*.

**A reserva de 4 unifilas é insuficiente.** Fita colada às 7h não se move às
13h. A barreira é a única parte do desenho que responde a uma surpresa — e as
surpresas deste projeto têm nome: MRV 24 e MRV 11 ainda sem mesário confirmado.
A pequena avenida de 23/09 (v2) devolveu 2 unidades e a reserva foi de 2 para 4, o que
não muda a ordem de grandeza. **Pedido: mais 15 unidades, EUR 195,45**, para
levar a reserva a 19. É 1,2% do orçamento do 1º turno.

## 8. Efeitos de segunda e terceira ordem

**A fita não é vencida, é desacreditada.** Uma linha colada é permeável por
definição. O problema não é o primeiro eleitor que corta caminho: é que ele
economiza 30 segundos **à vista de todos**, e um corte impune normaliza o corte.
Duas consequências de desenho: a barreira rende mais perto da **cabeça** da
fila, onde cortar compensa mais; e onde só há fita, o que a sustenta é
**presença humana** — o que amarra este plano ao dimensionamento de pessoal de
fluxo, não só ao de segurança.

**A cor só funciona se for aprendida antes de chegar.** Se o eleitor descobre no
portão que é "azul", a triagem vira leitura de título na porta — e a porta é o
gargalo não paralelizável. A tabela seção → cor → grupo tem de sair **antes** no
Instagram, na página da Embaixada e na divulgação alternativa. Isto converte um
item do plano de comunicação em **dependência do plano físico**.

**Fila desordenada gera reclamação formal; fila longa, não.** Quem espera 40
minutos numa fila visivelmente ordenada reclama do TSE; quem espera 20 numa fila
em que viu alguém furar reclama do Posto. A ordem visível é ativo reputacional,
e é o que se perde primeiro quando a fita cede.

## 9. O que não está resolvido

**Bloqueante.** Ninguém confirmou que o **RDS permite fita adesiva no piso do
Hall 2**. O manual do expositor do RDS não é público, e os manuais de outros
eventos no mesmo recinto tratam de adesivo em painéis, não em piso. Vários
recintos proíbem ou exigem resíduo zero com remoção integral. **Se a resposta
for não, este desenho inteiro cai** — e as 100 unifilas passariam a ter de fazer
sozinhas um trabalho de 395.

**Também em aberto:**

1. Submeter o layout de barreira ao responsável de incêndio do RDS — barreira em
   zona de egresso muda o cálculo de evacuação, e isso se submete, não se
   comunica.
2. As 15 unifilas adicionais e os 11 rolos de fita (5 deles vermelhos, desde 22/09).
3. Se os 165 m em estoque são por cor ou no total.
4. As bandas de 11,00 / 9,00 / 10,80 m pressupõem o módulo de 4,10 m da planta
   medida e o serpenteado de 4,20 m. Conferir com a mesa, a cabine e a urna
   reais.
5. A boca da avenida A deixa **36 cm** entre o trilho interno (x = 21,83) e o
   recuo S3 (até 21,47). É a folga mais apertada do traçado.
6. O **T da parede norte**. Se houver folga, vale estudar uma segunda perna para
   a avenida B — mas isso mexe na atribuição mesa → entrada, fechada desde
   15/09.
7. Quem cola os 802 m de fita, e quando. É trabalho de véspera com o salão
   vazio.

## 10. Fontes

Premissas de material:
[Queue Solutions](https://queuesolutions.com/retractable-belt-barriers/) ·
[Displays2Go](https://www.displays2go.com/C-24746/Retractable-Stanchions-Nylon-Belt-Barriers-Queue-Lines) ·
[Safety Direct2U](https://www.direct2u.co.uk/safety/standard-rectractable-belt-barrier-systems)

Documentos do projeto de que este tema depende: `plano_filas_confinado_hall2.md` (não transferido — vive em `claude/filas-sem-ring-3-b9qvqi`, no repositório de origem)
(passo de fila de 0,65 m, teto de densidade, o achado de que 28 urnas só cabem a
60 s por eleitor), `docs/separadores/CONFERENCIA_PRANCHETA_2026-09-15.md` (o porquê de cada
decisão de arranjo) e o artefato de sinalização
[`Ek3FfeYnwvQLZEs4ZJ5Zzr`](https://claude.ai/artifact/Ek3FfeYnwvQLZEs4ZJ5Zzr)
(cores, grupos e peças).
