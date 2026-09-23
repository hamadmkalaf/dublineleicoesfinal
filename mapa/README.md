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
| [`ring3_montagem.html`](ring3_montagem.html) | Montagem do Ring 3 | O cenário 3 adaptado: 23 raias por zona, vão de 1,20 m, **180 CCBs** dos 200 em estoque, 506 m de fita grossa, lotação 2.118. |
| [`sinalizacao_interna.html`](sinalizacao_interna.html) | Sinalização RDS Hall 2 | As peças internas do salão. |
| [`acesso_2turno.html`](acesso_2turno.html) · [`acesso_2turno.kml`](acesso_2turno.kml) | Acesso no 2º turno | **Gerados por `scripts/acesso_2turno.py`**, não copiados de artefato publicado: a página do plano de acesso no dia da maratona, e as camadas para o Google My Maps. Regenerar com `--grava`; não editar à mão. |
| [`acesso_2turno_print.png`](acesso_2turno_print.png) | Acesso no 2º turno, sobre o Google Maps | O plano marcado sobre o print de satélite (`acesso_2turno_print_base.png`), por `scripts/acesso_2turno_print.py`. Posições em pixel lidas à mão sobre esse print. |
| [`sinalizacao/`](sinalizacao/) | Sinalização Eleições 2026 (v2, 17/09) | As **21 peças** P0–P7, os dois mapas de posição e o `canvas.json`. Fonte das seis cores de rolo e da convenção de rotular por grupo e seção. |

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
| **P4** · bocas das zonas | `P4-ZonaA` · `P4-ZonaB` · `P4-ZonaC` |
| **P5** · portas e preferencial | `P5-Preferencial` · `P5-VinilA/B/C` (letra de 300 mm no vidro) |
| **P6** · painéis e grupos | `P6-PainelA/B/C` (pull-up 1000 × 2000) · `P6-BlocoA3` · `P6-BlocoC4` |
| **P7** · saída | `P7-Saida` (correx A2, ×2) |
| Mapas | `Mapa-Ring3` · `Mapa-Hall2` · `Main` (o sistema visual) |

## Divergências entre artefatos

**Resolvida — a largura das três zonas.** As zonas do Ring 3 são **iguais, 12,87 m
cada** (decisão do Posto, 18/09), como desenha o `Mapa-Ring3` do artefato de
sinalização (17/09). `ring3_montagem.html` (16/09) desenha **12,23 / 14,14 / 12,23 m**
e, nesse ponto, **está superado** — é uma cópia fiel do artefato publicado e por isso
não foi editada. `CLAUDE.md` já registra as três iguais.

A soma das três não muda (38,60 contra 38,61 m), então **nenhuma conta que dependa do
total se altera**: os 888 m de fila e os ~926 m de barreira da §5 de
`docs/voluntarios/contexto.md` continuam valendo como estavam.

**Em aberto — o número de CCBs.** 180 em `ring3_montagem.html`, **179** no
`Mapa-Ring3`. Os dois dentro dos 200 em estoque, então não muda a compra; muda a lista
de montagem. A diferença é pequena o bastante para ser o arredondamento dos postes
terminais quando as zonas passam de desiguais para iguais — **hipótese, não
verificação**: quem montar a lista confere contra o pátio.

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
