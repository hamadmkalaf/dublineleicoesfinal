# Memória do projeto — Eleições 2026, Posto de Dublin

Organização logística do 1º turno (04/10/2026, 8h–17h) e do eventual 2º turno
(25/10/2026) na jurisdição de Dublin. Documentos em português.

Este repositório é o **final**: carrega as versões vigentes de dois temas
transferidos do repositório de trabalho `hamadmkalaf/eleicoes2026`, e só o que é
necessário para chegar a elas.

| Tema | Onde vive | Estado |
|---|---|---|
| **Voluntários de apoio e fluxo do eleitor** | `docs/voluntarios/` · `mapa/voluntarios_postos.html` | os 17 postos e os 4 cenários de efetivo |
| **Separadores de fila e fita no chão no Hall 2** | `docs/separadores/` · `scripts/separadores_fila.py` | desenho definitivo de 17/09, revisto em 22/09 (zona C vermelha, avenida A até 40 m); 98 unifilas, 777 m de fita |
| **Arranjo do Hall 2** — cenário, `decisoes.json`, prancheta | `scripts/arranjo_paredes.py` · `confere_arranjo.py` · `gera_prancheta_por_secao.py` | trazidos em 22/09; a prancheta sai deles |
| **Sinalização** — 37 peças e o plano consolidado | `mapa/sinalizacao/` · `scripts/paleta.py`, `tabela_mestra.py`, `artes_sinalizacao.py`, `plano_consolidado.py` | revisão de 23/09 |
| **Artefatos** — rota, prancheta, Ring 3, sinalização | `mapa/` · manifesto em `mapa/artefatos.json` | fonte versionada, não só a URL |

---

## Fatos fixos

| Item | Valor | Fonte |
|---|---|---|
| Eleitores aptos | 16.794 | `saidas/dados.json`, dos CSVs oficiais do TSE |
| Seções / urnas | 51 seções agregadas em 28 urnas | idem |
| Residentes em Dublin / interior | 12.581 / 4.213 | idem |
| Comparecimento esperado | **11.499** (base B: taxa de 2022 do condado de origem por seção) | prancheta `Paredes_ABC`, 15/09 |
| Local | RDS, Merrion Road, Ballsbridge, Dublin 4 | contrato |
| Segurança contratada | 20 pessoas, 7h30–17h30, + 1 na véspera | orçamento (EUR 6.774,84) |

## Geometria do local (planta de 16/09/2026)

O Ring 3 como pátio de fila está **confirmado** (18/09), com as **três zonas iguais**.
A montagem — 23 raias por zona, vão de 1,20 m, **228 CCBs** (200 em estoque + **28 a
contratar**, ~EUR 364,56), 506 m de fita grossa, lotação **2.105** — está em
`mapa/ring3_montagem.html` (folha revista em 23/09, gerada por
`scripts/ring3_montagem.py` no repositório de origem) e no `Mapa-Ring3` de
`mapa/sinalizacao/`.

**Revisão de 23/09 do Ring 3 — as laterais A|B e B|C fecham inteiras.** Até 22/09
o vão de 1,20 m entre zonas era só espaço vazio: não havia barreira onde afixar a
fita que separa uma zona da outra, e a divisória existia no desenho mas não no
chão. Agora cada zona tem a sua **própria linha de CCBs** ao longo dos 32,0 m —
duas linhas por vão, uma em cada face —, e entre elas fica um **corredor de
serviço de 1,20 m**, largura que o desenho já exigia para passar maca e fiscal
contra o fluxo. São **64 CCBs a mais**, e é o que leva o total de 180 para 228:
**28 acima do estoque de 200, a contratar**. Cada linha tem **6 portões** de uma
CCB a cada 8 m (12 ao todo), para o corredor de serviço se alcançar de qualquer
ponto. *A alternativa registrada na folha* — uma só linha de CCBs no eixo do vão,
196 CCBs, cabe no estoque — foi descartada: ela deixa 0,60 m de cada lado e mata
a passagem de maca, que é decisão anterior.

**Revisão de 22/09 do Ring 3.** A boca de entrada da **zona A fica no extremo oeste**
(as de B e C seguem a leste): com 23 raias, ímpar, a raia de cima anda no sentido
contrário ao da boca, e só assim a A descarrega junto à S4. **Cada zona sai por uma
abertura de 2,0 m na face norte do gradil, a mais próxima da sua porta**, cotada do
canto nordeste, por onde a corrente entra: corredor de chegada 0–3,00 m · saída C
13,87–15,87 m · saída B 22,50–24,50 m · saída A 31,13–33,13 m. C e B saem dentro do
vão da própria porta; a saída da A termina a 2,91 m do eixo da S4, no batente oeste do
vão, e atravessa o apron em diagonal. A B sai pelo meio: a metade oeste da raia de cima
(5,43 m) fica fechada por 1 CCB atravessada, e custa 13 lugares. Essa conta fechava
em 180 CCBs dentro do estoque; o fechamento das laterais em 23/09 a levou a 228.

O percurso tem três trechos físicos distintos. **Ring 3 é o pátio de fila ao ar
livre; Hall 2 é o salão de votação.**

**Ring 3 — pátio de fila.** Recinto ao ar livre de gradil permanente, 44,0 × 35,0 m,
ao sul do Hall 2. Entrada única pelo **canto nordeste**. Um **corredor de chegada de
3,0 m** desce pelo lado leste; um **trecho de fundo de 3,0 m** corre na base e
distribui para as três zonas. Zonas lado a lado, separadas por vãos de 1,20 m e
**iguais entre si: 12,87 m cada** — C a leste, a primeira que se alcança; B ao centro;
A a oeste, a mais distante. As larguras saem do esperado por entrada de `Paredes_ABC`,
e dão **706 pessoas de lotação por zona**. Cada zona tem **23 raias** ao longo de 32,0 m
(passo de 1,39 m). A fila avança de baixo para cima; a cabeça de cada zona fica no
topo, voltada para o Hall.

**Apron.** Faixa pavimentada de **14,0 m** entre a cabeça das filas e a fachada sul
do Hall 2. Espaço de travessia, sem raias.

**Hall 2 — salão de votação.** Portas na fachada sul: **S4 = entrada A, S5 = entrada
B, S6 = entrada C, S7 = preferencial**; **S2 e S8 são saídas**; S1, S3 e S9 ficam
livres. As 28 mesas ficam encostadas nas paredes: **parede oeste = zona A (9 urnas),
parede norte = zona B (9 urnas), parede leste = zona C (10 urnas)**. A **sala de apoio é
um recuo para dentro da parede oeste**, entre a O1 e a parede norte, **fora do piso do
salão** (22/09): não é zona protegida, e o que fica livre é o acesso a ela a partir de
y = 38,50. Na mesma revisão as mesas a norte da O2 (A3, A4, A5) andaram **1,50 m para o
norte**, para afastar a 3313·3889 do recuo da O2 (0,24 → 1,74 m); a parede oeste tem
27,63 m úteis. **Em 23/09 a parede oeste trocou dois pares de posição**: os dois
pares de maior carga (3309·1314 + 3142·1278 e 3161·3307 + 3311·3913) foram para o
norte da parede, e os dois de menor carga (513·1105 + 1352·522 e 3078·2847 +
3179·530) para o sul, junto à boca da avenida A — quem tem fila maior fica longe
da avenida de trânsito. **O código de grupo é posicional**: A1 é sempre o par mais
ao sul da parede oeste, então os códigos acompanharam a troca e hoje A1 = 513·1105
e 1352·522, A4 = 3309·1314 e 3142·1278, A5 = 3161·3307 e 3311·3913. Quem impõe a
ordem é `ORDEM_FIXA` em `arranjo_paredes.py`; quem reetiqueta é
`scripts/grupos_mesas.py`. Faixa livre de 3 m junto à parede leste para as saídas de emergência
L1–L4. Portas O1 e N1 fechadas; O2, N2 e H1 livres. Serpentinas internas de 20
pessoas nas três mesas maiores (3313, 3315, 3322).

Correspondência que amarra tudo: **zona do Ring → porta do Hall → parede do salão**,
com a mesma letra em toda a rota.

| Zona | Ring 3 | Porta | Parede | Urnas | Aptos | Comparecimento esperado |
|---|---|---|---|---|---|---|
| A | oeste (12,87 m) | S4 | oeste | 9 | 5.695 | 3.834 |
| B | centro (12,87 m) | S5 | norte | 9 | 5.600 | 3.832 |
| C | leste (12,87 m) | S6 | leste | 10 | 5.499 | 3.833 |

Spread de 0,05% pela base B, com uma das três urnas grandes (3313, 3315, 3322) em
cada zona. A distribuição está equilibrada; não mexer sem refazer a conta.
`scripts/zonas_balanceadas.py` confere a composição com um estimador mais grosso
(74%/50%), que chega a 3.860 / 3.755 / 3.802 — mesma conclusão, 2% de diferença.

A rota também tem os pontos **P0 a P7** do plano de sinalização: **P0** é a mesa
"descubra sua seção" na calçada da Merrion Road, **fora** do portão. Depois do
portão toda peça pressupõe a seção conhecida, então P0 é o único ponto que resolve
quem chega sem o número.

## Cenários de efetivo de voluntários (decisão de 17/09/2026)

Quatro cenários, numerados por quantas pessoas de apoio existem. **C4 é referência de
teto, não meta de recrutamento** — o Posto não o considera realista para 2026.

| | Pessoas no pico | Postos ocupados (de 17) | Turnos e reserva |
|---|---|---|---|
| **C1 · Contingência** | 9 — o efetivo de hoje | 5 | não |
| **C2 · Próximo degrau** | 15 | 7 | não |
| **C3 · Operacional** | 24 | 13 | não |
| **C4 · Pleno** | 49 (43 postos + 15% de reserva) | 17 | sim, 61 escaladas |

Histórico do efetivo: eram 25 voluntários; 14 foram cedidos para cobrir dispensas de
mesário e **não voltam** — mesário é função nomeada, com treinamento próprio. Campanha
de reserva em curso.

**C1 (9):** 3 no P0 da calçada, 1 no trecho de fundo do Ring (R3), 1 na porta
preferencial S7 (A3), 3 nas mesas de alta carga (H3) e 1 na coordenação (T1).

**C2 (15)** acrescenta o quarto operador do P0, as três cabeças de fila (R5, uma por
zona) e duas bocas do trecho de fundo (R2, zonas C e A).

O preenchimento é uma **fila contínua da posição 10 à 49**, para funcionar com
qualquer número intermediário — com 13 pessoas preenche-se até a posição 13, com 17 até
a 17. A fila está em `docs/voluntarios/lista_postos.md` e em
`mapa/voluntarios_postos.html`.

C1 e C2 só fecham com três compensações contratadas: os 20 seguranças assumindo
presença de fila por escrito no briefing, uma CCB de separação no apron no lugar do
posto A1, e a campanha "descubra sua seção antes de sair de casa".

## Regras do tema dos separadores de fila

- **Leia `docs/separadores/contexto.md` antes de tocar na geometria.** As três
  decisões de 17/09 e a regra *"as avenidas levam para dentro; as bandas trazem para
  fora"* são o que sustenta o desenho inteiro.
- **Nunca edite `data/decisoes.json`, `data/prancheta_hall2.json` nem
  `cenarios/paredes-abc-20260915.json` a partir deste tema.** Eles são **lidos**, não
  escritos. Pertencem ao arranjo do Hall 2, e editá-los à mão quebra as conferências.
  Quem os escreve é `scripts/arranjo_paredes.py --grava` (desde 22/09 neste
  repositório): os trechos livres de cada parede estão em `PAREDES`, a ordem das
  unidades da oeste em `ORDEM_FIXA`, e `confere_arranjo.py` confere os sete itens.
  Depois dele, `scripts/grupos_mesas.py --grava` realinha `data/grupos_mesas.json`
  (`coord`, `por_mesa`) e `gera_prancheta_por_secao.py` refaz a prancheta.
- **Cores do layout final (22/09):** zona C vermelha `#C8102E` (rolo a comprar), e por
  isso as três mesas de alta carga saem em **roxo** (`classes.cores.alta` de
  `decisoes.json`), as portas de emergência em verde-água e os avisos em cinza —
  vermelho só significa "zona C". A avenida A termina em y = 40,0 m, para servir o
  ramal da mesa em 37,62 m. Fita da Definitiva: **777 m, 11 rolos a comprar**;
  barreira em **98 unifilas em 133 m**, reserva móvel 2.
- **O recuo das avenidas foi desenhado em 23/09 e recusado.** O pedido era
  alargar a banda de fila de cada parede empurrando a avenida daquela parede para
  o centro (bandas de 13,00 / 14,00 / 13,00 m). Não entrou: com a banda norte em
  14,00 m — o máximo que a geometria dá, porque acima disso o T da avenida B cai
  em cima do serpenteado da C5, em y = 30,25 — as avenidas B e C ficavam a 1,50 m
  uma da outra e espremiam o campo central, que é a reserva de fila. A conta do
  que custaria está em `docs/separadores/contexto.md` §5: 960 m de fita e 18
  rolos, contra 6 unifilas devolvidas. **`BANDA_PAREDE` continua oeste 11,00 ·
  norte 9,00 · leste 10,80 m**, e as faixas de avenida disjuntas em A
  11,00–25,03 · B 26,80–29,80 · C 32,00–36,50.
- **A conferência das avenidas sai com código 1** quando a geometria quebra. Rode
  `python3 scripts/separadores_fila.py` (sem `--grava`) antes de qualquer commit que
  toque em `AVENIDAS`, `BANDA_PAREDE` ou nas zonas protegidas. Sem `--grava` ele não
  escreve nada e já serve de teste em integração contínua.
- As constantes que mudam tudo estão no topo de `scripts/separadores_fila.py`:
  `VAO_POSTE`, `BANDA_PAREDE`, `LARG_CANAL`, `PASSO_FILA`, `CORES_ZONA`,
  `ESTOQUE_FITA`.
- **Rotular sempre por grupo de mesas e por seção, nunca por número de mesa.** O
  eleitor sabe a sua seção; não sabe que mesa é a sua.
- Três armadilhas conhecidas: mudar uma banda e esquecer a fita; contar a boca da
  avenida B duas vezes (ela entra inteira, não leva item de boca); e rotular por
  número de mesa. As três estão descritas em `docs/separadores/contexto.md`.

## Regra da tabela mestra seção → porta

A tabela "SUA SEÇÃO → SUA PORTA" das quatro peças de triagem — **P0-Mestra,
P1-Portao, P2-ParedeLeste e P3-EntradaRing** — é **agrupada por porta** desde
21/09/2026: bloco A, bloco B, bloco C, lado a lado, e dentro de cada bloco as
seções em ordem crescente, lidas de cima para baixo em três colunas. A letra sai
uma vez, na tarja colorida do bloco, e não mais em 51 pastilhas repetidas.

- **Não edite essas quatro peças à mão.** Rode `python3 scripts/tabela_mestra.py
  --grava`. Sem `--grava` o script confere e sai com código 1 se as peças
  divergirem do que ele geraria, e já serve de teste em integração contínua.
- A correspondência seção → porta vem de `data/grupos_mesas.json`, que é **lido,
  nunca escrito** por esse script.
- As escalas tipográficas de cada peça estão no dicionário `ESCALAS`, no topo do
  script. Elas foram dimensionadas para caber no canvas de cada peça (P2 é
  1000 × 500; as outras três, 1040 × 410) com zero estouro. Mexeu em `num`,
  `alt` ou `cab`: rerrenderize e confira que nada transborda.
- O custo conhecido do agrupamento: quem não sabe a sua porta varre até três
  blocos em vez de uma lista ordenada. A compensação é o dígito, que subiu de
  17 px para 26 px (34 mm → 52 mm no impresso) porque a pastilha por linha saiu.
- **Cada seção sai com o fundo na cor da sua porta**, a mesma da tarja do bloco:
  A em `#33507E` com dígito branco (8,1:1), B em `#E8C63A` com dígito **marinho
  `#042B5A`** (8,4:1) e, desde 22/09, C em **vermelho `#C8102E` com dígito branco**
  (5,9:1 — marinho sobre o vermelho dá 2,4:1 e reprova). Os três blocos viram três
  campos de cor. As razões de A e B são as da prancha do sistema, reconferidas.
- **Ressalva de 21/09, em aberto.** A prancha do sistema diz: *"a letra
  identifica a fila; a cor é apoio. Em nenhuma peça a cor aparece sozinha"* —
  porque para um deuteranope o amarelo da B e a abóbora da C viram dois
  amarelo-esverdeados com 1,9:1 entre si. Nas pastilhas agrupadas a letra saiu
  da linha e ficou só na tarja do bloco. O bloco está logo acima e é grande,
  mas a pastilha, sozinha, é cor sem letra. Se isso incomodar, a correção é pôr
  a letra de volta em cada pastilha — ao custo do dígito, que encolhe.

## Regra das artes que saem de dados

`scripts/artes_sinalizacao.py` gera, de `data/grupos_mesas.json`:

- **`P6-BlocoA1` a `P6-BlocoC6`** — as **dezesseis** placas de grupo, uma por par
  de mesas, não só as dos grupos grandes. **O código do grupo é o título da
  placa:** quem está no par C3 lê `C3` em 104 px no alto do banner, o mesmo
  código que o painel da porta C usa na sua lista. Isso fecha a cadeia
  porta → grupo → seção com o mesmo rótulo nos dois pontos. **Desde 22/09 as
  seções saem agrupadas por mesa** (`por_mesa`, principal antes da agregada),
  com uma **seta para o lado da mesa**: a placa fica entre as duas mesas do par,
  de frente para o salão. A regra de lado está em `lados()`: na parede oeste a
  mesa de menor y fica à esquerda (sul), na norte a de menor x (oeste), na
  leste a de maior y (norte). Grupos de uma mesa só (A3, B2, C5, C1) não levam
  seta.
- **`P0-Consulta`** — "não sabe sua seção?" com o **QR estático para a consulta
  por nome no site do TSE**, gerado por `scripts/qr_tse.py` (nível H) em
  `data/qr_tse.svg`. São **duas peças, uma de cada lado do portão**, cada uma ao
  lado de uma `P0-Mestra`. O SVG recebido em 22/09 leva a um encurtador de
  terceiro e fica só como referência em `Identidadevisual/`, com nota.
- **`P4-ZonaA/B/C`** — corpo branco, a cor da porta só no bloco da letra, sem a
  linha "parede · Sx", seções em células com borda de 3 px e dígito de 40 px
  (80 mm). O bloco da letra tem 240 px para as seis células caberem.
- **`P5-Preferencial` e `P5-VinilPref`** — os cinco pictogramas brasileiros de
  atendimento preferencial, em `scripts/_pictogramas.py`, na ordem da
  referência de 21/09: **idoso com bengala · gestante · adulto com criança de
  colo · pessoa com muleta · laço do espectro autista**. A primeira versão
  trazia cadeira de rodas no lugar da muleta; foi corrigida. **Desde 22/09 a
  P5-Preferencial é empilhada como a placa de referência do Posto**: fundo azul
  `#1E3674` (medido na referência), moldura branca arredondada, título numa
  caixa branca, pictogramas brancos, em Montserrat e **sem a faixa
  institucional** — decisão do Posto. Canvas 1040 × 410 (2080 × 820 mm).
- **`P6-PainelA`, `P6-PainelB` e `P6-PainelC`** — os três painéis de porta,
  pull-up de 500 × 1000 px (1000 × 2000 mm), também **gerados de
  `grupos_mesas.json`** desde 23/09: a lista de grupos de cada porta sai na ordem
  em que o eleitor os encontra ao longo do corredor daquela parede. Desde 23/09
  cada painel diz onde fica a **ponta** de cada corredor: o primeiro grupo leva
  "LOGO NA ENTRADA DO CORREDOR" e o último, "NO FIM DO CORREDOR, O MAIS DISTANTE".
  Na porta A isso é A1 e A5; na C, C1 e C6.
- **`P4-FimAvenidaB`** — fence banner de 1040 × 410 no **T da avenida B**, o
  único ponto do salão em que todo o fluxo de uma entrada tem de escolher um
  lado. À esquerda, na direção da porta A, ficam B1, B2 e B3; à direita, na da
  porta C, B4 e B5. O corte é **por mesa**, não por grupo: o par B3 fica
  escarranchado no vão da avenida, com uma mesa de cada lado do eixo, então sai à
  esquerda com a ressalva no rodapé de que está bem em frente. A primeira versão
  desta peça foi feita para o fim do corredor C e **descartada** — o pedido era a
  avenida B.
- **`mapa/plano_sinalizacao.html`** é montado por `scripts/plano_consolidado.py`,
  que embute o corpo atual de cada `.dc.html` e aplica as revisões de texto de
  cada rodada de forma idempotente. Mesmo contrato: sem `--grava` confere.
- São **vetor redesenhado**, não a imagem de referência. As duas referências
  guardadas em `Identidadevisual/` são raster: a de 17/09 tem 575 px e a de
  21/09, 950 px **com marca d'água de banco de imagens** — ela anuncia
  "EPS/CDR" mas o que chegou é o JPEG de vitrine. Esticada para os 2080 mm do
  fence banner qualquer das duas sai borrada, e a arte do banco não pode ser
  reproduzida sem a licença. Os cinco símbolos em si são de uso corrente e não
  têm dono; o que se redesenha é eles, não o layout vendido.
- Mesmo contrato dos outros geradores: sem `--grava` confere e sai com código 1.
- O dígito das placas escala com quantas seções o grupo tem (`DIGITO`, no topo do
  script): 130 px para uma seção, 80 px para quatro. Mexeu ali, rerrenderize.

## Regra da paleta

`data/paleta.json` é a fonte única, e `scripts/paleta.py` confere. Sem
`--grava` ele sai com código 1 se alguma peça usar cor de fora.

- **Identidade**, medida pixel a pixel no logotipo vetorizado que o Posto
  entregou em 21/09 — não estimada: grafite `#404041`, ouro `#E5AE0F`, azul
  `#3487AA`, verde `#5F882E`. Até 21/09 as quatro estavam erradas em **todas**
  as 36 peças: `#F2CE3A` no lugar do ouro, `#4888A8` e `#5A8CAA` no do azul,
  `#588018` e `#648232` no do verde.
- **O logotipo é corpo estranho e guarda as cores dele.** Fora do lockup o ouro
  não aparece: é o que a prancha do sistema quer dizer com *"só no logotipo"*.
  O ouro sobre a faixa clara dá 1,8:1, e isso é aceito porque a WCAG isenta
  marca registrada.
- **Faixa institucional: off-white `#F0F0E8` com régua marinha `#042B5A`.** Essa
  decisão é de 17/09 e está escrita na prancha do sistema — *"a faixa virou
  off-white com régua marinha; o amarelo agora só significa porta B"* —, mas as
  peças seguiram até 21/09 com uma tarja escura `#5A6E6E` que não existe na
  marca. Motivo da decisão: uma faixa amarela no topo diria "porta B" a 30 m em
  toda peça, inclusive nas de A e de C.
- **Tipografia do plano: marinho `#042B5A`**, não o grafite do logotipo. O
  grafite só é legítimo acima do fim da faixa; `scripts/paleta.py` reprova
  grafite no corpo da peça.
- **Fonte: Montserrat** (`data/paleta.json`, campo `fonte`). É a fonte da
  campanha, informada pelo Posto em 21/09. Archivo e Nunito Sans eram marcação
  de lugar. Montserrat é **mais larga no mesmo corpo**, então a troca mexe em
  medida e não só em estilo: as 36 peças foram remedidas no DOM com a fonte
  real instalada, não com substituta. `scripts/paleta.py` reprova Archivo e
  Nunito Sans.
- **A autorização de uso da marca para posto no exterior foi concedida**
  (21/09). O que ainda é reprodução, e não arquivo oficial, é o desenho do
  lockup nas peças.
- **As cores de zona não se ajustam à identidade.** `#33507E` e `#E8C63A` são
  **cor de rolo de fita já comprado** (`CORES_ZONA` em
  `scripts/separadores_fila.py`): a peça impressa persegue a fita. Por isso o
  amarelo da B e o ouro da marca convivem sendo dois amarelos — e por isso a
  tarja da B nunca encosta no logotipo. **Em 22/09 o Posto trocou o laranja da
  C por vermelho `#C8102E`**: o rolo vermelho ainda não existe, então o hex é
  proposta até a compra — quando o rolo chegar, o hex se ajusta a ele, em
  `CORES_ZONA`, em `data/paleta.json` (`substituicoes_22_09`) e nas 37 peças
  via `paleta.py --grava`. A tinta sobre a C é branca. O azul `#1E3674` da
  P5-Preferencial é cor própria dessa peça (`preferencial` em `paleta.json`).
- As quatro cores do laço do espectro autista são do símbolo, não do plano, e
  ficam de fora da conferência.

## Convenções

- Números de eleitorado vêm sempre de `saidas/dados.json` (CSV oficial), nunca do
  PNG do mapa de agregações do TSE, que tem erro de digitação conhecido (seção 3752
  listada sob a principal 3222; a correta é 3322).
- Premissas não observadas (fator de pico, tempo por eleitor, permanência média)
  são rotuladas como premissas no texto.
- Voluntário orienta, não decide: não toca em documento, não confere título, não
  diz a ninguém se pode votar. Identificação é monopólio legal do mesário.
- **Um branch só, com merge de volta.** A confusão no repositório de origem teve
  causa conhecida: cada sessão trabalhou num branch próprio e nenhuma mesclou de
  volta, e o sintoma mais caro foi um gerador lendo um `decisoes.json` que outro
  branch já havia superado.

## Pendências que movem números

1. **O RDS permite fita adesiva no piso do Hall 2?** Bloqueante: se não, o desenho
   dos separadores cai inteiro, e as 100 unifilas passariam a ter de fazer sozinhas
   um trabalho de 395.
2. Método de identificação do eleitor — eletrônico/biométrico ou caderno físico
   (`PENDENCIAS.md` item 5). Decide tempo por eleitor e criticidade do balcão de
   consulta.
3. Confirmação da expectativa de comparecimento.
4. Orçamento final, incluindo o apoio ao voluntariado (~EUR 1.700–1.900), as 15
   unifilas adicionais (EUR 195,45) e os 8 rolos de fita.
5. **O vinil da porta S7 (21/09) não está orçado.** A cotação de 18/09 já previa
   **16 pull-ups 850 × 2000 a EUR 24,87 (EUR 398)** — ou seja, as dezesseis placas
   de grupo sempre estiveram no orçamento; o que faltava eram as artes, e é isso
   que a revisão de 21/09 fecha. O que entra de novo é só o quarto vinil de porta,
   da S7 preferencial: a linha passa de 3 para 4 unidades, +EUR 30, e o total sem
   IVA vai de EUR 1.139,57 para EUR 1.169,57 (EUR 1.438,57 com IVA). Ressalva: o
   preço do vinil é uma das quatro linhas que a própria cotação marca como
   **premissa não precificada**, então o quarto vinil herda essa incerteza.

6. **A compra de fita foi parcialmente refeita em 22/09: a zona C passa a vermelho.**
   `#C8102E` é proposta até o rolo ser comprado; o hex final é o do rolo. Faltam
   **11 rolos de 50 m** (2 azul, 5 vermelho, 1 zebrado, 1 verde, 2 branco) e o rolo
   laranja em estoque (165 m) fica sem uso neste desenho. O amarelo da B continua
   brigando com o ouro da marca, e a ressalva de deuteranopia da prancha do
   sistema continua valendo para B; o par B/C deixou de ser dois amarelo-esverdeados.
   O que a decisão arrasta está feito: `CORES_ZONA`, `data/paleta.json`, as 36
   peças e os metros por cor (`docs/separadores/`).
7. **O RDS permite abrir os quatro painéis do gradil da face norte do Ring 3?**
   O corredor de chegada e as três saídas (C, B, A) são aberturas de 2,0 m no
   gradil permanente. Sem isso o desenho das saídas junto às portas não existe.
8. **A URL do QR da P0-Consulta.** A peça aponta para a consulta de seção por
   nome no site do TSE (`URL` em `scripts/qr_tse.py`). Se o Posto preferir outra
   página do TSE, muda a constante e regrava; conferir antes de imprimir.

9. **As 28 CCBs acima do estoque, para fechar as laterais do Ring 3 (23/09).**
   Locação de véspera, ~EUR 364,56 pelo unitário da cotação (EUR 13,02). A
   alternativa sem contratar está desenhada na folha — uma só linha de CCBs no
   eixo do vão, 196 no total —, mas ela reduz a passagem entre zonas a 0,60 m de
   cada lado e mata o corredor de maca. **É decisão de orçamento contra
   segurança, e é do Posto.**

A lista completa e por tema está em `PENDENCIAS.md` e nas seções finais dos dois
contextos.
