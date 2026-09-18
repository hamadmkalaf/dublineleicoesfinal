# Artes da sinalização — arquivos para a gráfica

Uma peça por nome, em três formatos:

| Formato | Para quê |
|---|---|
| `.pdf` | **é o que vai para a gráfica** — a página do PDF tem a medida física da peça |
| `.html` | a mesma arte, aberta no navegador; imprimir dá a peça no tamanho certo |
| `.png` | conferência na tela, ~3,8 px por mm |

`indice.json` lista cada peça com medida, quantidade e o ponto onde é instalada.

## As 18 peças

Formatos de catálogo do fornecedor (Helloprint IE) — peça fora de catálogo
custa mais e demora mais. Cotações em `Orçamentos/Sinalização/`.

| Arquivo | Formato | Medida | Qtd | Onde |
|---|---|---|---|---|
| `P0-consulta` | fence banner | 2080 × 820 | 1 | calçada da Merrion Road, antes do portão |
| `P0-tabela-mestra` | fence banner | 2080 × 820 | 2 | gradil da Merrion Road |
| `P1-portao` | fence banner | 2080 × 820 | 2 | grades do portão de eleitores |
| `P2-parede-leste` | banner PVC | 2000 × 1000 | 3 | vãos entre as saídas de emergência da lateral leste |
| `P3-entrada-ring3` | fence banner | 2080 × 820 | 1 | CCB do corredor de chegada do Ring 3 |
| `P4-boca-zona-A/B/C` | fence banner | 2080 × 820 | 1 cada | CCB antes da boca de cada zona |
| `P5-vinil-porta-A/B/C` | vinil recortado | 1200 × 700 | 1 cada | por dentro do vidro da fachada sul |
| `P5-preferencial` | fence banner | 2080 × 820 | 1 | gradil do apron, junto à S7 |
| `P6-painel-porta-A/B/C` | pull-up | 1000 × 2000 | 1 cada | logo depois de cada entrada |
| `P6-bloco-A3`, `P6-bloco-C4` | pull-up | 850 × 2000 | 16 no total | boca do corredor de cada grupo de mesas |
| `P7-saida` | correx A2 | 594 × 420 | 2 | sobre os vãos da S2 e da S8 |

`P6-bloco-*` são **dois exemplares** de um modelo que se repete 16 vezes (5 na
parede oeste, 5 na norte, 6 na leste), cada um com as seções do seu grupo. Os
14 restantes saem do mesmo gerador.

**O fence banner é amarrado com tie wraps** — o fornecedor vende como opção da
peça — e existe em malha perfurada windproof 270 g, que é o que o vento da
Merrion Road pede. Nenhuma peça externa tem base.

## Como refazer

```bash
python3 scripts/pranchas/gera_pranchas.py     # as peças externas
python3 scripts/pranchas/gera_internas.py     # as internas e as plantas
python3 scripts/pranchas/gera_artes.py --render   # HTML + PDF + PNG daqui
```

O `--render` **confere se alguma arte está cortada** e falha se estiver. Não
pule: as quatro peças de tabela mestra já foram para o canvas com metade das
seções fora da peça, e o corte não aparece sem essa checagem.

## Antes de mandar imprimir

1. **O logotipo destas peças é marcação de lugar.** A arte oficial do TSE tem
   de vir em vetor, e o uso da marca por posto no exterior precisa de
   autorização. Ver `docs/identidade_visual.md` §4.
0. **O prazo é a decisão mais urgente.** Pela cotação de 18/09, a entrega Saver
   é grátis e chega em 28/09, mas o arquivo tem de subir até 18/09 às 13:30.
   Standard (+ € 35) chega 23/09; Express (+ € 38), 22/09.
2. **Confirmar as três cores contra o rolo de fita.** Os hexes foram lidos da
   foto do estoque, não medidos.
3. **A fonte** da campanha não foi identificada; estas peças usam Archivo e
   Nunito Sans como substitutas.
4. **Conferir a sangria** com a gráfica: as artes não têm sangria, são do
   tamanho exato da peça.
