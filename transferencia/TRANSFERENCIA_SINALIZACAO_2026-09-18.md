# Transferência — Sistema de sinalização do posto de Dublin

> **Tema:** levar o sistema de sinalização — geradores, dados, identidade,
> artes e orçamento — para outro repositório, de forma que ele regenere tudo
> sozinho e ninguém precise reconstituir uma decisão de cabeça.
>
> Escrito em **18/09/2026**. Diferente de
> [`TRANSFERENCIA_SINALIZACAO.md`](TRANSFERENCIA_SINALIZACAO.md), que é de
> 16/09 e trata da migração das duas páginas publicadas para este repositório:
> aquele documento está **superado** por este no que diz respeito a formatos,
> cores e orçamento.
>
> O contexto do assunto está em
> [`docs/CONTEXTO_SINALIZACAO_2026-09-18.md`](../docs/CONTEXTO_SINALIZACAO_2026-09-18.md).
> Leia-o antes deste. Este aqui diz **o que copiar e em que ordem**.

---

## 1. O conjunto mínimo: 12 arquivos, 1,3 MB

Foi verificado nesta sessão: os 12 arquivos abaixo, copiados para um diretório
vazio, regeneraram **as 21 pranchas, as 18 artes e o plano consolidado byte a
byte idênticos** aos daqui. Nada mais é necessário para produzir a sinalização.

```
scripts/
  sinalizacao_v2.py                 as peças, os blocos, o orçamento, as duas páginas
  ring3_montagem.py                 as zonas do Ring 3, as bocas e o BOM
  pranchas/
    comum.py                        paleta, logotipo, faixa institucional
    gera_pranchas.py                as peças externas e a saída
    gera_internas.py                os painéis, os banners de bloco, as duas plantas
    gera_main.py                    a prancha do sistema e o índice do canvas
    gera_artes.py                   HTML + PDF + PNG em tamanho real, com a checagem de corte
    gera_plano_consolidado.py       o documento com a arte ao lado do ponto
data/
  decisoes.json                     o arranjo Paredes_ABC: mesas, entradas, esperados
  prancheta_hall2.json              a geometria do salão e das 18 portas
  prancheta_paredes_abc.json        a prancheta na forma que a sinalização lê
saidas/
  dados.json                        as 51 seções com aptos e condado
```

**Dependências:** Python 3 com biblioteca padrão para tudo, mais `playwright`
só para o `--render` do `gera_artes.py`. Nenhum acesso à rede, exceto a fonte
do Google Fonts que as páginas carregam para exibir.

### A ordem, que não é negociável

```bash
python3 scripts/ring3_montagem.py            # 1. PRIMEIRO: escreve saidas/ring3_montagem.json
python3 scripts/sinalizacao_v2.py            # 2. lê o JSON acima; sem ele, para com erro
python3 scripts/pranchas/gera_pranchas.py    # 3. as peças externas
python3 scripts/pranchas/gera_internas.py    # 4. as internas e as plantas
python3 scripts/pranchas/gera_main.py        # 5. o sistema e o índice do canvas
python3 scripts/pranchas/gera_artes.py --render   # 6. as artes + a checagem de corte
python3 scripts/pranchas/gera_plano_consolidado.py # 7. o documento consolidado
```

O passo 1 antes do 2 é a única ordem que morde: `sinalizacao_v2.py` lê
`saidas/ring3_montagem.json` para as coordenadas das zonas, e **falha em vez de
adivinhar** se ele não existir. Antes de 17/09 essas coordenadas estavam
digitadas nos dois lugares, e foi assim que a geometria do Ring 3 ficou
proporcional a cotas mortas por dois dias sem ninguém notar.

---

## 2. O que mais levar, e por quê

Não é necessário para gerar, mas quem receber sem isso vai reconstituir errado:

| O quê | Por quê |
|---|---|
| `docs/CONTEXTO_SINALIZACAO_2026-09-18.md` | o contexto do assunto; sem ele os números não têm procedência |
| `docs/identidade_visual.md` | as regras de aplicação da identidade e os dois choques que ela tem com a operação |
| `referencias/identidade_visual_tse_2026/` (9 imagens, 4,6 MB) | a origem da paleta e do logotipo. **O commit em que chegaram não estava em branch nenhuma** e teria sido coletado pelo GC |
| `Orçamentos/Sinalização/` (12 cotações + LEIAME) | o orçamento inteiro depende delas; sem elas o preço volta a ser premissa |
| `saidas/artes_sinalizacao/` (~8 MB) | os PDFs prontos para a gráfica. Regeneráveis, mas caros de refazer se a pressa for de horas |

---

## 3. Como provar que a transferência deu certo

Rode a cadeia inteira no destino e confira **estes valores**. Qualquer um
diferente significa que faltou arquivo ou que a ordem foi trocada.

| Comando | Tem de imprimir |
|---|---|
| `ring3_montagem.py` | `larguras {'A': 12.87, 'B': 12.86, 'C': 12.87}` · `CCB: 179` · `compra 0 \| sobra 21` · `fita grossa 506.0 m` |
| `sinalizacao_v2.py` | `blocos: [5, 5, 6]` · `secoes/porta: [18, 16, 17]` · `TOTAL 1139.57` |
| `gera_main.py` | `21 pranchas` |
| `gera_artes.py --render` | as 18 peças e, no fim, **`nenhuma arte cortada`** |
| `gera_plano_consolidado.py` | `18 fichas` |

Além disso, `sinalizacao_v2.py` **falha em vez de gravar** se as 51 seções não
aparecerem uma vez cada, se os aptos não somarem 16.794 ou se as 28 mesas não
fecharem. Se ele gravou, a base do TSE bate.

> **`gera_artes.py --render` não é opcional.** A peça corta o que passa da
> borda, e arte cortada não parece cortada — parece uma peça com menos
> conteúdo. Quatro peças já foram publicadas com metade das 51 seções fora da
> arte antes de essa checagem existir.

---

## 4. As sete coisas que o destino precisa saber, ou vai errar

1. **As cores das portas não são da paleta.** São as das **fitas de piso
   compradas** — azul `#33507E`, amarelo `#E8C63A`, abóbora `#DE7343`. Trocá-las
   por tons da paleta quebra a ligação com o chão que o eleitor pisa. Os hexes
   foram **lidos da foto do estoque, não medidos**: confirmar contra o rolo.

2. **Cada porta tem duas cores.** A da fita, para **preenchimento**, e uma
   **tinta** escurecida (`#33507E`, `#7D6004`, `#9C4118`) para **texto sobre
   fundo claro**. Usar a cor da fita como texto dá 1,7:1 no amarelo. Nas páginas
   são os tokens `--a/--b/--c` e `--a-ink/--b-ink/--c-ink`.

3. **A faixa institucional nunca é amarela.** Com a porta B amarela, uma faixa
   amarela em toda peça diria "B" a 30 m, inclusive nas peças de A e de C.

4. **O logotipo é marcação de lugar.** Mostra onde a arte oficial entra e
   quanto ocupa. **Nenhuma peça deve ser impressa a partir dele**: falta o
   vetor do TSE e a autorização de uso da marca para posto no exterior. A marca
   da Justiça Eleitoral saiu das peças por decisão do Posto.

5. **Nenhuma peça leva inglês**, e **nenhuma mesa tem número**. As duas são
   decisões, não esquecimento: a mesa saiu na revisão de 16/09, e o inglês em
   18/09.

6. **Os formatos são de catálogo do fornecedor.** Fence banner 2080 × 820,
   pull-up 1000 × 2000 e 850 × 2000, PVC 2000 × 1000. Peça fora de catálogo
   custa mais e demora mais. Mudar medida sem olhar o catálogo é como o plano
   anterior chegou a supor € 60 numa peça que sai por € 32.

7. **A escala das pranchas é 1 px = 2 mm.** Quem mexer no layout precisa saber
   disso para julgar corpo de letra: 40 px na prancha são 80 mm no impresso.

---

## 5. O que **não** levar

- **`saidas/pranchas_sinalizacao/` e `saidas/artes_sinalizacao/` como fonte.**
  São geradas. Editá-las à mão se perde na próxima rodada. Leve as artes como
  entregável, nunca como original.
- **`transferencia/TRANSFERENCIA_SINALIZACAO.md`** (a de 16/09) como se fosse
  atual. Ela descreve o plano antes das fitas, dos formatos e das cotações.
- **`scripts/gera_plano_sinalizacao.py`** e o resto da cadeia de sinalização
  anterior à v2. Continuam na árvore por histórico; o plano vigente é o v2.
- **As URLs dos artefatos, se o destino for outro Posto.** Elas apontam para
  páginas deste projeto.

---

## 6. Pendências que viajam junto

Vão para o destino em aberto. As duas primeiras têm prazo.

1. **Decidir a entrega.** Arquivo até 18/09 às 13:30 para a Saver (grátis)
   chegar em 28/09; Standard + € 35 chega 23/09; Express + € 38, 22/09. A
   eleição é 4/10.
2. **Republicar** a Rota do Eleitor (`1PQjgzstbiNorfJgagXhB5`) e a Sinalização
   Hall 2 (`BcT5yzxRkSaUsbbHQQgjWF`) **nas mesmas URLs** — as duas ainda estão
   nas cores e formatos antigos. Publicar sem `url` cria um segundo artefato
   com o mesmo título.
3. **Confirmar as três cores** contra o rolo de fita.
4. **Vetor do logotipo** e autorização de uso da marca.
5. **Cotar as quatro linhas que são premissa**: 3 banners PVC, 3 vinis, 2
   placas correx, fixação.
6. **A fonte da campanha** não foi identificada; as peças usam Archivo e Nunito
   Sans como substitutas.
7. **Medir o vão da S7** (1,27 m) e conferir a posição das portas contra a
   planta cotada do RDS.
8. **O desvio da zona A**: a boca fica 2,91 m a oeste do eixo da porta A. Ou
   vira trabalho de orientador, ou o Ring se desloca para leste.
9. **Sangria**: as artes são do tamanho exato da peça, sem sangria. Conferir
   com a gráfica antes de enviar.

---

## 7. Se o destino for um repositório novo, do zero

Nesta ordem:

1. Copie os 12 arquivos do §1, preservando os caminhos.
2. Copie o que o §2 lista.
3. Rode a cadeia do §1 e confira os valores do §3.
4. Só então mexa em qualquer coisa. Se um número do §3 não bater, **pare**: é
   arquivo faltando, não é para ajustar o script até fechar.

Um detalhe de `gera_main.py`: ele preserva `createdOnFiles` e `attachments` do
`canvas.json` anterior, se houver. Num repositório novo não há, e ele cria um
`createdOnFiles` com a data de hoje — o que é o correto para um canvas novo.
Se o destino for republicar **no mesmo canvas**, traga o `canvas.json` junto
para não apagar o estado que a página escreve por conta própria.
