# Mapas, plantas e artefatos

Os artefatos que sustentam a geometria do projeto **têm fonte versionada aqui**. Antes
existia só a URL da publicação, que não é versionamento: o repositório versiona o
arquivo; a publicação pode mudar ou sair do ar sem deixar rastro.

O manifesto **[`artefatos.json`](artefatos.json)** registra, para cada um, a URL, a
versão publicada de que a cópia foi tirada, e o `sha256` do arquivo neste repositório.
**É assim que se percebe que uma cópia envelheceu:** se o artefato for republicado, o
`sha256` deixa de bater.

## O que está versionado

| Arquivo | Artefato | O que é |
|---|---|---|
| [`voluntarios_postos.html`](voluntarios_postos.html) | Escala de Voluntários | Os 17 postos sobre a rota e sobre a planta do salão, com seletor dos quatro cenários. |
| [`rota_do_eleitor.html`](rota_do_eleitor.html) | Rota do Eleitor RDS | Os pontos **P0–P7**, a tabela mestra seção → porta e o plano de sinalização. É a origem dos códigos de posto. |
| [`prancheta_hall2.html`](prancheta_hall2.html) | Prancheta pelas Seções | Coordenadas reais das portas e das 28 mesas. A planta do salão em `voluntarios_postos.html` foi gerada delas. |
| [`ring3_montagem.html`](ring3_montagem.html) | Montagem do Ring 3 | O cenário 3 adaptado, revisto em 23/09: 23 raias por zona, três zonas iguais, vão de 1,20 m, **228 CCBs** (200 em estoque + 28 a contratar), 506 m de fita grossa, lotação 2.105, boca da A a oeste, as quatro aberturas da face norte cotadas e as laterais A\|B e B\|C fechadas nas duas faces, com corredor de serviço de 1,20 m e 12 portões. |
| [`sinalizacao_interna.html`](sinalizacao_interna.html) | Sinalização RDS Hall 2 | As peças internas do salão. |
| [`sinalizacao/`](sinalizacao/) | Sinalização Eleições 2026 (v2, 17/09) | As **37 peças** P0–P7, os dois mapas de posição e o `canvas.json`, na revisão de 23/09. Fonte das cores de rolo e da convenção de rotular por grupo e seção. |
| [`plano_sinalizacao.html`](plano_sinalizacao.html) | Plano de sinalização, peça por peça | O plano consolidado (v7, 23/09), montado por `scripts/plano_consolidado.py` a partir das peças. |

As cópias são a página **tal como o serviço a entregou**, invólucro da plataforma
incluído — não foram editadas. A única exceção é `voluntarios_postos.html`, que já
estava no repositório antes: é byte a byte igual ao artefato publicado a menos desse
invólucro, e por isso foi mantida como está.

O artefato de sinalização é um Artifact do tipo *Design*, e o seu `index.html` é só a
casca da plataforma. O que vale é o conteúdo, em `sinalizacao/`: um arquivo `.dc.html`
por peça, mais `canvas.json` com o título e a posição de cada prancha.

> **Esses `.dc.html` são fonte, não página pronta.** Cada um carrega um `./support.js`
> e um `<x-dc>` que só o runtime do tipo *Design* resolve — abrir um deles direto no
> navegador não desenha a peça. Para ver as peças, use a URL do artefato; para saber o
> que cada peça diz, medida a medida, leia o arquivo. O runtime em si (4 MB de
> `artifact-type/`) **não** foi versionado: é da plataforma, não do projeto.

### As peças, por ponto da rota

| Ponto | Peças |
|---|---|
| **P0** · calçada | `P0-Consulta` (fence banner 2080 × 820) · `P0-Mestra` (tabela mestra, ×2) |
| **P1** · portão | `P1-Portao` |
| **P2** · lateral leste | `P2-ParedeLeste` (PVC 2000 × 1000, ×3) |
| **P3** · entrada do Ring | `P3-EntradaRing` |
| **P4** · bocas das zonas | `P4-ZonaA` · `P4-ZonaB` · `P4-ZonaC` · `P4-FimCorredorC` (fim do corredor da parede leste, 23/09) |
| **P5** · portas e preferencial | `P5-Preferencial` · `P5-VinilA/B/C` (letra de 300 mm no vidro) · `P5-VinilPref` (porta S7) |
| **P6** · painéis e grupos | `P6-PainelA/B/C` (pull-up 1000 × 2000) · **`P6-BlocoA1` a `P6-BlocoC6`** — as dezesseis placas de grupo (pull-up 850 × 2000) |
| **P7** · saída | `P7-Saida` (correx A2, ×2) |
| Mapas | `Mapa-Ring3` · `Mapa-Hall2` · `Main` (o sistema visual) |

## Divergências entre artefatos

**Resolvida — a largura das três zonas.** As zonas do Ring 3 são **iguais, 12,87 m
cada** (decisão do Posto, 18/09). A folha `ring3_montagem.html` foi regenerada e
republicada em 22/09 com as três iguais; a divergência com o `Mapa-Ring3` acabou.

A soma das três não muda (38,60 contra 38,61 m), então **nenhuma conta que dependa do
total se altera**: os 888 m de fila e os ~926 m de barreira da §5 de
`docs/voluntarios/contexto.md` continuam valendo como estavam.

**Superada — "preferencial em qualquer porta".** A tabela de `rota_do_eleitor.html`
diz, na linha do P5, que a entrada preferencial vale em *"qualquer porta"*. **Não vale:**
decisão do Posto de 21/09, o preferencial entra **pela S7, a porta à direita da C**. A peça
`P5-Preferencial` já diz isso; `rota_do_eleitor.html` não foi editada porque é cópia fiel do
artefato publicado, como o `ring3_montagem.html`. Quem republicar a Rota do Eleitor corrige lá.

**Resolvida — o número de CCBs.** Com as três zonas iguais o fechamento do fundo cai
de 16 para 15 CCBs (179), e a CCB atravessada que fecha a meia raia morta da B (saída
pelo meio, 22/09) devolve o total a **180**. Em 23/09 o fechamento das laterais A|B e
B|C acrescenta 64 CCBs e leva o total a **228**, das quais 28 a contratar. A folha e o
`Mapa-Ring3` dizem o mesmo.

**Revisão de 23/09.** Prancheta (v6), Ring 3 (v3), plano de sinalização (v7) e escala
de voluntários (v5) foram republicados e as cópias refeitas; o manifesto tem as
versões e os sha256 novos. O que mudou está em `CLAUDE.md` e nos commits de 23/09:
a parede oeste trocou dois pares de posição, as três avenidas recuaram para o centro
do salão, as laterais do Ring 3 fecharam e a sinalização ganhou a `P4-FimCorredorC` e
as marcas de ponta de corredor nos painéis A e C.

## Dois achados a levar ao plano de sinalização

Vieram do tema dos separadores. O desenho dos separadores já os aplica; o plano de
sinalização, ainda não.

1. O x-banner da parede leste está em **x = 45,70** e devia estar em **42,70** — a
   45,70 ele fica atrás das mesas, dentro da faixa protegida das saídas de emergência
   L1–L4.
2. Nos três grupos de alto comparecimento (A3, B2, C5), os **4,60 m** caem dentro do
   serpenteado; nesses três o banner recua para **8,60 m**.

## O que ainda falta

| O quê | Onde deve ficar | Observação |
|---|---|---|
| **Plantas em imagem** do Ring 3 e do Hall 2 | `plantas/` | A geometria do `CLAUDE.md` é prosa escrita a partir delas. Sem as imagens, a descrição perde a fonte. |
| **Caderno nominal de seções** (51 seções × nome do eleitor, do Cartório) | `data/` | Insumo do posto P0. **Pode não existir** — ver pendência 3 de `docs/voluntarios/contexto.md`. Obtê-la é a melhoria de maior retorno por euro gasto. |

## Como reconferir as cópias

```bash
python3 - <<'EOF'
import hashlib, json
m = json.load(open("mapa/artefatos.json", encoding="utf-8"))
for a in m["artefatos"]:
    if "sha256" not in a: continue
    atual = hashlib.sha256(open(a["caminho"], "rb").read()).hexdigest()
    print(("ok  " if atual == a["sha256"] else "MUDOU "), a["caminho"])
EOF
```

Se um arquivo mudou, ou alguém o editou à mão — o que não se deve fazer, porque estas
cópias são espelho do artefato — ou o artefato foi republicado e a cópia precisa ser
refeita a partir da URL do manifesto.
