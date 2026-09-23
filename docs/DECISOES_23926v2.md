# Decisões 23926v2 — consolidado

**Segunda rodada de 23/09/2026**, e é isso que o nome quer dizer: `23926` é a data,
`v2` é a rodada. A primeira do mesmo dia está em
[`DECISOES_2026-09-23.md`](DECISOES_2026-09-23.md).

Três frentes: **economia de CCB no Ring 3**, **a pequena avenida da parede norte no
Hall 2** e **o mapa simplificado de apresentação**, a primeira peça do projeto feita
para sair dele.

Duas coisas desta rodada desfazem trabalho da v1, e estão escritas aqui de propósito:
a parede contínua da lateral do Ring e o T da avenida B.

**Estado no fim da rodada:** branch `23926v2` nos dois repositórios. Os
geradores passam em modo conferência (sem `--grava`, código 0), à exceção de
`qr_tse.py`, que pede o módulo `segno` e já falhava antes desta rodada. Os dois
artefatos tocados nesta rodada já foram republicados nas URLs do manifesto — ver §4.

---

## 1. Ring 3 — CCB só onde a fita amarra

**Pedido do Posto:** *"Na separação entre A/B/C e dos vãos entre os corredores,
não use CCBs em todos os pontos. Use apenas nos pontos onde a fita terminaria na
separação… O espaço entre os CCBs será coberto por fitas"*, e *"na cobertura até
a boca das zonas A, B e C, vamos usar também fitas entre os CCBs. Atente-se que
os CCBs devem terminar na porta da boca."*

Em 23/09 a lateral de cada zona virou parede contínua de 32,0 m porque a ponta
fixa de cada divisória é fita, e fita precisa de ponto fixo. Estava certo quanto
ao ponto fixo e errado quanto à parede: **fita precisa de ponto fixo onde amarra,
não ao longo de tudo.**

**A conta está numa alternância que o desenho já tinha.** A ponta fixa de uma
divisória fica do lado oposto ao seu vão de meia-volta, e o vão de meia-volta
troca de lado a cada raia. Logo, numa linha de lateral amarram as divisórias
**ímpares** da zona vizinha; na outra linha, as pares. São **11 pontos por linha,
não 22**, a **2,78 m** um do outro — mais do que um painel de 2,00 m alcança.
Um painel por ponto: 11 por linha em vez de 16.

O fechamento contra o trecho de fundo alterna do mesmo jeito, com painel nas duas
pontas: o de fora encosta na lateral da zona e o de dentro é a **porta da boca**,
como o pedido exige. Três painéis por zona em vez de cinco, com vãos de fita de
2,00 m — abaixo dos 3,84 m que o desenho já aceita na divisória da zona B.

| | 23/09 | **23/09 (v2)** |
|---|---:|---:|
| CCBs, total | 228 | **202** |
| das quais laterais | 64 | **44** |
| das quais fechamento do fundo | 15 | **9** |
| A contratar (estoque de 200) | 28 · ~EUR 364,56 | **2 · ~EUR 26,04** |
| Fita grossa | 506,0 m | **558,0 m** |
| Lotação | 2.105 | 2.105 — não muda |

Nenhuma cota de geometria se move: largura de zona, 23 raias, módulo de 1,39 m,
bocas de 2,87 m e as quatro aberturas da face norte continuam iguais.

**O portão a cada 8 m sai de cena.** Os 12 portões de 23/09 — painel sem grampo —
só existiam no briefing. A passagem passa a ser o próprio vão de fita: 11 por
face, sendo 36 de 0,78 m, 4 de 1,17 m e **4 de 1,78 m**, um por linha, junto ao
trecho de fundo, que passa maca. Nenhum ponto da zona fica a mais de 1,4 m de um
vão, contra 4 m de um portão.

**O que isso custa, e é a parte que não pode se perder.** Vão de 0,78 m coberto
por fita é fronteira que se vê, não fronteira que custa atravessar: quem estiver
na zona A pode pisar no corredor de serviço, subir e voltar à zona A mais
adiante. É o corte lateral que 23/09 havia fechado, e ele volta. Atenuam, sem
eliminar: o corredor é estreito e visível dos dois lados, é por onde circulam R3,
R4 e R5, e atravessar leva para a **zona vizinha**, onde ninguém pode votar. Se o
Posto quiser o corte fechado outra vez, os 26 painéis economizados são exatamente
o que o compra de volta.

**A parede da zona C não entrou na economia.** A mesma regra ali daria 11 painéis
em vez de 16, total **197** e compra **zero, com três de sobra** — está calculada
e desenhada como variante (`PAREDE_C = 'amarracao'`) e não está adotada. Essa
parede não dá para a zona vizinha: dá para o corredor por onde passam os 16,8 mil
que entram, e um vão ali é atalho para o meio da fila da própria zona, que vale
cerca de 150 m de percurso. **É decisão do Posto: EUR 26,04 contra 32 m de parede
anticorte.**

Implementação em `hamadmkalaf/eleicoes2026`: `scripts/ring3_montagem.py`
(`LATERAL='amarracao'`, `FUNDO='amarracao'`, `linha_amarrada()`).

## 2. Hall 2 — a pequena avenida da parede norte

**Pedido do Posto:** *"Crie uma pequena avenida — removendo o último par de
unifilas — antes das filas da parede norte."*

Até 23/09 a avenida B encostava no T, e o T era o único ponto do salão em que
todo o comparecimento de uma entrada — 3.832 esperados — escolhia um lado
**parado**, num metro quadrado. Tirando o último par de unifilas, uma em cada
trilho, a barreira para em y = 33,60 e esse 1,80 m vira uma faixa transversal de
**1,80 × 25,50 m**. As duas bordas são fita; nenhuma é barreira. A escolha de
lado passa a acontecer andando.

**Ela para nas bordas das bandas oeste e leste** e não acompanha o distribuidor
até x = 42,30: fora delas cortaria o ramal do **A5** (y = 33,72) a oeste e o do
**C6** (y = 35,55) a leste, que correm em y constante na mesma altura — e a regra
de 17/09 é que ninguém cruze fila parada. Isso não foi conferido à mão:
`confere_avenida_norte()` reprova o desenho, e foi ela que apontou os dois
ramais.

| | 23/09 | **23/09 (v2)** |
|---|---:|---:|
| Unifilas em barreira | 98 em 133 m | **96 em 129 m** |
| Reserva móvel | 2 | **4** |
| Fita | 777 m | **802 m** (+24,7 m de amarelo) |
| Rolos a comprar | 11 | 11 — não muda |

O amarelo vira de saldo positivo (+15,2 m) para negativo (−9,5 m) sobre os 165 m
em estoque, **sem mudar a compra**: os 4 rolos que essa cor já pedia cobrem a
diferença.

**Efeito na sinalização.** A `P4-FimAvenidaB` continua amarrada na última unifila
da avenida B — a mesma peça de hardware —, mas ela deixa de ficar em cima do T e
passa a ficar na boca da avenida pequena. A ficha do plano e o marcador P4 no mapa
acompanham, por `revisao_23_09_v2()` em `plano_consolidado.py`, de forma idempotente.
**A arte impressa não muda**: o que muda é onde ela é amarrada.

## 3. O mapa simplificado de apresentação

**Pedido do Posto:** um mapa para divulgar na internet e apresentar às equipes,
com a entrada pela Merrion Road (portão B), o caminho pela lateral externa do
Hall 2, a entrada no Ring 3 e nas zonas, e um mapa do Hall 2 contendo **somente**
as mesas numeradas pelas seções, as portas A/B/C, as saídas, a entrada
preferencial e as avenidas de cada entrada e de cada zona até a seção.

`scripts/mapa_publico.py` → `mapa/mapa_publico.html`, publicado em
<https://claude.ai/artifact/FuDcD3rNme5wznroJV435t>. E, para a sala,
`scripts/mapa_publico_pptx.py` → `saidas/onde_voce_vota.pptx`: os mesmos dados em
quatro slides, **tudo em forma nativa** — retângulo, linha e caixa de texto —, de modo
que quem receber o arquivo mova uma mesa ou corrija um número sem voltar ao gerador.
Nenhuma imagem colada, porque imagem colada não é editável, é só um desenho dentro de
um arquivo editável. A fonte pedida é a Montserrat, da campanha; quem não a tiver
instalada vê a substituta do sistema.

**É a única peça do projeto feita para sair dele**, e é isso que decide o que ela
*não* mostra: barreira, fita, grupos de mesa, serpenteados, zonas protegidas,
classes de comparecimento e número de MRV ficam de fora. Nada disso é decisão do
eleitor. A regra de rotular **por seção e nunca por número de mesa** vale aqui com
mais força do que em qualquer peça interna: cada mesa traz as suas duas seções, e
só elas.

Três coisas a registrar:

1. **Nenhum número é digitado.** A planta sai de `prancheta_hall2.json` e do
   cenário, as seções de `decisoes.json`, as cores de `paleta.json` e o pátio de
   `data/ring3_montagem.json` — cópia da saída de `ring3_montagem.py`, que vive no
   repositório de trabalho. O encaixe entre a coordenada do Ring e a do salão
   (6,285 m) é **derivado das três portas de entrada**, e o script para se as três
   não derem o mesmo deslocamento.
2. **O trecho entre o portão e o apron é esquemático**, e a folha diz isso: o
   Hall 2, o apron de 14,0 m e o Ring 3 estão em escala e em posição relativa
   medida; a Merrion Road e o portão estão do lado certo, sem cota. A posição
   exata do portão B na Merrion Road ainda não foi medida em campo — **é a
   pendência 7, abaixo**.
3. **O artefato nasce privado.** Divulgar exige abrir o compartilhamento na
   própria página; o link não funciona para terceiros antes disso.

## 4. Artefatos e verificação

| Artefato | Estado |
|---|---|
| Montagem do Ring 3 | **republicada** na mesma URL, versão 4: 202 CCBs, 2 a contratar. |
| Plano de sinalização | **republicado** na mesma URL, versão 9: a P4 na boca da pequena avenida, o marcador em y = 33,60 m e o rodapé corrigido. |
| Onde você vota no RDS | **novo**, publicado nesta rodada. Privado até que o compartilhamento seja aberto. |
| Prancheta, Rota, Escala de voluntários, Sinalização | sem mudança nesta rodada. |

`mapa/artefatos.json` não tem mais nenhuma entrada pendente de publicação e traz os
sha256 das cópias deste repositório; a conferência de sha256 dá `ok` nas sete.

O `Mapa-Ring3` de `mapa/sinalizacao/` foi corrigido de 228 para 202 CCBs. É peça
de referência interna, mantida à mão — não tem gerador.

## 5. O que a rodada deixou em aberto

1. **As 2 CCBs acima do estoque** (~EUR 26,04), ou a variante da parede da zona C,
   que zera a compra e abre um atalho de ~150 m. Decisão do Posto.
2. **O corte lateral pelos vãos de 0,78 m.** Precisa entrar no briefing de R3, R4
   e R5: o corredor de serviço passa a ter 44 entradas, não 12 portões.
3. **Os 11 rolos de fita**, e se os 165 m em estoque são por cor ou no total.
4. **O RDS permite abrir os quatro painéis do gradil da face norte do Ring 3?**
5. **O RDS permite fita adesiva no piso do Hall 2?** Continua bloqueante.
6. **Abrir o compartilhamento do mapa público**, que nasceu privado. As duas folhas
   tocadas nesta rodada — Ring 3 (versão 4) e plano de sinalização (versão 9) — já
   foram republicadas nas mesmas URLs.
7. **A posição do portão B na Merrion Road**, a medir em campo antes de o mapa
   público ser divulgado como orientação de chegada.
8. **O prazo de entrega da gráfica**, que a própria cotação marca como a decisão
   mais urgente.
