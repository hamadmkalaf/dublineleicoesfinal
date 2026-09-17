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

### Cores amostradas das referências

| Papel | Hex | Onde aparece |
|---|---|---|
| Amarelo campanha | `#F8C030` | fundo dominante das peças |
| Ouro do logotipo | `#E6B00F` | o "2026" |
| Marinho | `#042B5A` | "ELEIÇÕES", títulos, corpo de texto |
| Azul bandeira | `#398CB0` | faixa do E, caixas de destaque |
| Azul claro | `#77ACCF` | apoios, fundos secundários |
| Verde bandeira | `#95C11F` / `#5F8722` | faixa do E |
| Laranja | `#F07E26` | títulos de campanha, destaques |
| Off-white | `#F0F0E8` | fundo alternativo |

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

**2. As cores de porta em uso não são da paleta oficial.** Até 16/09 eram
azul `#1f5fa8`, âmbar `#b8760a` e magenta `#8b3a8e`. O magenta não existe na
identidade, e o âmbar briga com o amarelo da campanha. **Decisão:** as três
cores passam a ser derivadas da **bandeira no logotipo** — azul, laranja e
verde — escurecidas até o contraste necessário:

| Porta | Antes | **Agora** | Origem | Contraste com branco |
|---|---|---|---|---|
| **A** (S4, parede oeste) | `#1f5fa8` | **`#0B6E9E`** | azul da faixa do E | 5,62:1 |
| **B** (S5, parede norte) | `#b8760a` | **`#B04E0A`** | laranja da campanha | 5,33:1 |
| **C** (S6, parede leste) | `#8b3a8e` | **`#4A7C1E`** | verde da faixa do E | 5,01:1 |

Os três seguram texto branco com folga e entre si, e nenhum se confunde com o
amarelo da faixa institucional.

> **A cor é apoio, não identidade.** A decisão do Posto de 13/09 continua
> valendo: quem identifica a fila para o eleitor é a **letra** (A, B, C). Isso
> é o que protege o plano de um eleitor com daltonia — azul, laranja e verde
> é um trio razoável, mas laranja e verde se aproximam para deuteranopes, e a
> letra resolve. Em nenhuma peça a cor aparece sem a letra ao lado.

## 3. Regras de aplicação

1. **Toda peça carrega a faixa institucional**: amarelo `#F8C030`, marca
   Justiça Eleitoral à esquerda, logotipo Eleições 2026 à direita, altura de
   12% a 18% da peça.
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
