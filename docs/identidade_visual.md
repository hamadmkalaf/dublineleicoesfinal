# Identidade visual da sinalização — Eleições 2026, posto de Dublin

> Escrito em 17/09/2026, quando o Posto entregou o material da identidade
> oficial. As imagens de referência estão em
> `referencias/identidade_visual_tse_2026/` (capturas do material do TSE —
> recebido de terceiros, não gerado aqui).

## 1. A identidade oficial, e o que ela fixa

A campanha é a **Eleições 2026 · #VOTONADEMOCRACIA**, da Justiça Eleitoral. O
que ela traz, e que a sinalização do posto não inventa:

| Elemento | O que é |
|---|---|
| Logotipo | "ELEIÇÕES 2026" com o **E estilizado** em três faixas onduladas (amarelo, azul, verde) — lê a bandeira; "ELEIÇÕES" em marinho, "2026" em ouro |
| Assinatura | marca **Justiça Eleitoral** no canto superior esquerdo |
| Hashtag | **#VOTONADEMOCRACIA**, com "NA" em azul no meio do lettering escuro |
| Campo | amarelo dominante, ou off-white; o marinho é a tipografia, não o fundo |
| Grafismos | a estrela de quatro pontas (✦) e a linha ondulada |
| Tipografia | display condensada, bold, caixa alta; texto em sans humanista de terminações arredondadas |

### A paleta oficial (carta "CORES", amostrada em 18/09)

Onze tons em três famílias, "inspirados nas cores vibrantes da nossa bandeira
nacional". São estes que pintam fundo, faixa e texto de apoio nas peças —
antes de 18/09 a sinalização era branca e marinho, e não era a identidade.

| Família | Tons |
|---|---|
| Verdes | `#5A6E6E` ardósia · `#648232` · `#96B43C` · `#B4C83C` limão |
| Azuis | `#5A6E96` · `#6E82A0` · `#5A8CAA` · `#78AAC8` |
| Quentes | `#DC963C` laranja · `#DCB43C` ouro · `#E6BE3C` amarelo |

### O logotipo

| Elemento | O que é |
|---|---|
| "ELEIÇÕES" | **carvão `#3F3F3F`**, não marinho |
| o **E** | três ondas grossas — `#E8B800` amarelo, `#4888A8` azul, `#588018` verde — ocupando a caixa alta da letra; é a bandeira |
| "2026" | **ouro `#E8B800`**, corpo maior que o da palavra acima |
| hashtag | **#VOTO<span>NA</span>DEMOCRACIA**, o "NA" em azul |
| assinatura | **nenhuma** — a marca da Justiça Eleitoral saiu das peças por decisão do Posto (18/09) |

Ondas de amplitude baixa e traço grosso: é isso que faz três **barras** que se
leem como um E. Desenhadas finas, o bloco vira rabisco e "ELEIÇÕES" abre um
buraco no meio — foi o primeiro desenho, e não servia.

### O fundo das peças

`#F2EFE2` **osso**, não branco; divisões em `#E4DFCC`. A faixa institucional
do topo é **ardósia `#5A6E6E`**, com o logotipo em branco e ouro.

## 2. Onde a identidade e a operação se chocam

A identidade é feita para **tela e peça institucional**. A sinalização do posto
é feita para ser **lida em movimento, a 15–60 m, na chuva**. Dois choques, e as
decisões que tomei:

**1. O amarelo é o campo da campanha, e o campo da sinalização não pode ser
amarelo.** Se as peças de porta forem amarelas, as três portas ficam iguais e a
cor deixa de codificar. **Decisão:** o amarelo fica na **faixa institucional**
(topo de cada peça, com o logotipo e a assinatura), e o corpo da peça é o campo
da cor da porta. A peça continua reconhecível como Eleições 2026 pela faixa, e
continua codificando pela cor.

**2. A cor de cada porta é a cor da fita comprada.** Decisão do Posto, 17/09:
as três fitas de piso já estão em mãos, e são elas que mandam. A peça impressa
persegue a fita, não o contrário — o eleitor liga a placa ao chão que está
pisando. Saem o azul `#1f5fa8`, o âmbar `#b8760a` e o magenta `#8b3a8e`.

| Porta | Fita | Cor | Texto sobre ela | Contraste |
|---|---|---|---|---|
| **A** (S4, parede oeste) | azul | **`#33507E`** | branco | 8,1:1 |
| **B** (S5, parede norte) | amarela | **`#E8C63A`** | **marinho `#042B5A`** | 8,4:1 |
| **C** (S6, parede leste) | abóbora | **`#DE7343`** | **marinho `#042B5A`** | 4,4:1 |

> Os três hexes foram **lidos a olho da foto do estoque**, não medidos. Antes
> de fechar arte com a gráfica, confirme contra o rolo — a referência do
> produto, ou uma foto do rolo sobre papel branco em luz de dia. Um erro aqui
> aparece no dia, com a placa ao lado da fita.

**Duas consequências que não são de gosto:**

**a) A faixa institucional deixou de ser amarela.** Com a porta B amarela, uma
faixa amarela no topo de toda peça passaria a dizer "B" a 30 m — inclusive nas
peças de A e de C. A faixa virou **off-white `#F0F0E8` com régua marinha**, e o
amarelo só aparece dentro do logotipo. O amarelo agora significa uma coisa só:
porta B.

**b) A cor da fita não serve como cor de texto.** Amarelo `#E8C63A` sobre fundo
claro dá **1,7:1** — ilegível. Cada porta passa a ter duas cores com o mesmo
matiz: a da fita, para **preenchimento**, e uma **tinta** escurecida, para
**texto sobre fundo claro**.

| Porta | Preenchimento (fita) | Tinta (texto) | Contraste da tinta |
|---|---|---|---|
| A | `#33507E` | `#33507E` (a mesma) | 7,3:1 |
| B | `#E8C63A` | `#7D6004` | 5,3:1 |
| C | `#DE7343` | `#9C4118` | 5,9:1 |

Nas páginas geradas isso são os tokens `--a/--b/--c` (fita) e
`--a-ink/--b-ink/--c-ink` (tinta), em `scripts/sinalizacao_v2.py`.

> **A cor é apoio, e agora isso é necessidade, não precaução.** A decisão do
> Posto de 13/09 — quem identifica a fila é a **letra** — deixou de ser folga.
> Para um deuteranope, o amarelo de B e a abóbora de C viram dois
> amarelo-esverdeados (`#D1D136` e `#9D9D3B`) que só diferem em claridade; e
> entre si, as duas cores têm contraste de **1,9:1**. Sob chuva, ao longe ou de
> relance, B e C podem se confundir. **A letra é o que separa as duas** — em
> nenhuma peça a cor aparece sem ela, e nas peças de B e C a letra tem de ser a
> maior coisa no campo.

## 3. Regras de aplicação

1. **Toda peça carrega a faixa institucional**: off-white `#F0F0E8` com régua
   marinha embaixo, marca Justiça Eleitoral à esquerda, logotipo Eleições 2026
   à direita, altura de 9% a 18% da peça. Nunca amarela — ver §2.a.
2. **Uma informação por peça.** A peça externa responde a uma pergunta só
   (qual é a minha porta?); a interna, a outra (onde está a minha seção?).
3. **Número de seção sempre com quatro dígitos**, como no e-Título.
4. **Mesa não tem número na sinalização** (revisão de 16/09): o eleitor procura
   a seção, não a mesa.
5. **Bilíngue só onde há quem não fala português** — portão, preferencial e
   saída levam inglês; as tabelas de seção, não (são números).
6. **Corpo mínimo por distância de leitura**: 30 mm a 6 m, 40 mm a 8 m,
   80 mm a 15 m, 120 mm a 20 m, 150 mm a 30 m, 300 mm a 60 m. Os valores por
   peça estão em `saidas/sinalizacao_v2.json`, campo `corpo`.
7. **Nada de base no externo**: mesh amarrada ilhós a ilhós (grade, gradil,
   CCB). A regra é do vento, não do gosto — ver §6 de
   `saidas/rota_do_eleitor_v2.html`.

## 4. O que ainda falta

- **Os arquivos vetoriais oficiais.** As referências aqui são capturas de tela;
  o logotipo e a marca da Justiça Eleitoral precisam vir em vetor do TSE antes
  de qualquer arte ir para a gráfica. Nenhuma peça deste repositório deve ser
  impressa a partir do logotipo redesenhado na proposta.
- **A fonte.** A display condensada da campanha não foi identificada nas
  referências. A proposta usa substitutas livres; trocar quando o Posto tiver
  o manual da marca.
- **Aprovação do uso da marca** pelo TSE/Cartório Eleitoral para peças de
  posto no exterior.
