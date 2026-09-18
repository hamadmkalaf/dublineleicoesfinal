# Verificação da transferência — sistema de sinalização

> **Tema:** o registro de que a transferência descrita em
> [`TRANSFERENCIA_SINALIZACAO_2026-09-18.md`](TRANSFERENCIA_SINALIZACAO_2026-09-18.md)
> foi executada neste repositório e **confere** — os sete passos rodaram na
> ordem, e os cinco valores de controle do §3 daquele documento bateram.
>
> Escrito em **18/09/2026**, na sessão que consolidou a sinalização em `main`.

---

## 1. O que foi consolidado

O sistema de sinalização **não veio de `hamadmkalaf/eleicoes2026`**: aquele
repositório nunca teve a cadeia v2 das pranchas. Ela nasceu aqui, na linha de
trabalho que partiu do commit inicial, e ficou **fora de `main`** — enquanto
`main` recebia, por upload, a identidade visual, as cotações e os PDFs de
conferência.

Esta consolidação junta as duas pontas: a árvore curada (402 arquivos, com os
geradores, os dados, as artes e os documentos) e os uploads que só `main`
tinha. Das 13 vias que se cruzavam, **12 eram idênticas byte a byte** — as
cotações de `Orçamentos/Sinalização/`. Só o `README.md` divergia, e a versão
curada é a que descreve a árvore inteira.

Nada foi descartado: `Identidadevisual/` e `conferencia/` continuam onde
estavam, ao lado de `referencias/identidade_visual_tse_2026/` e de
`data/oficiais/`.

---

## 2. A cadeia, na ordem que morde

```bash
python3 scripts/ring3_montagem.py                   # 1. escreve saidas/ring3_montagem.json
python3 scripts/sinalizacao_v2.py                   # 2. lê o JSON acima
python3 scripts/pranchas/gera_pranchas.py           # 3.
python3 scripts/pranchas/gera_internas.py           # 4.
python3 scripts/pranchas/gera_main.py               # 5.
CHROMIUM=<binário> python3 scripts/pranchas/gera_artes.py --render   # 6.
python3 scripts/pranchas/gera_plano_consolidado.py  # 7.
```

## 3. Os valores de controle, conferidos

| Passo | Esperado | Obtido |
|---|---|---|
| `ring3_montagem.py` | `larguras {'A': 12.87, 'B': 12.86, 'C': 12.87}` · `CCB: 179` · `compra 0 \| sobra 21` · `fita grossa 506.0 m` | **bate** |
| `sinalizacao_v2.py` | `blocos: [5, 5, 6]` · `secoes/porta: [18, 16, 17]` · `TOTAL 1139.57` | **bate** |
| `gera_main.py` | `21 pranchas` | **bate** |
| `gera_artes.py --render` | 18 peças · `nenhuma arte cortada` | **bate** |
| `gera_plano_consolidado.py` | `18 fichas` | **bate** |

Como `sinalizacao_v2.py` **grava** — ele falha em vez de gravar se as 51 seções
não aparecerem uma vez cada, se os aptos não somarem 16.794 ou se as 28 mesas
não fecharem —, a base do TSE bate junto.

### A regeneração não moveu um byte

Rodada a cadeia inteira sobre a árvore recém-consolidada, o `git status` voltou
**limpo**: os 21 HTMLs das pranchas, os 18 PNGs, o `canvas.json`, os JSONs e o
plano consolidado saíram idênticos aos versionados.

Os 18 **PDFs** apareceram como modificados, e não estavam: a diferença é de
**8 bytes em 13.222**, o `/CreationDate` e o `/ModDate` que o Chromium carimba
na hora de imprimir. Mesmo tamanho, mesmo `/Producer (Skia/PDF m141)`, e os
PNGs da mesma rodada byte a byte iguais. Foram restaurados para não versionar
carimbo de relógio como se fosse arte nova.

> Quem repetir isto e vir os 18 PDFs "modificados": confira o tamanho e o
> `CreationDate` antes de commitar. Dezoito binários trocados por um relógio
> poluem o histórico e escondem a próxima mudança de verdade.

---

## 4. O `CHROMIUM` do passo 6 não é detalhe

`gera_artes.py --render` sobe o Chromium pelo Playwright, e **a versão do
Playwright tem de casar com a build do navegador instalado**. Num ambiente onde
o `pip install playwright` trouxe a 1.63 e o navegador disponível era a build
1194, o passo 6 morreu em `Executable doesn't exist ... chromium_headless_shell-1243`.

O script já prevê isso: a variável de ambiente **`CHROMIUM`** aponta o binário
existente e o `launch` o usa como `executable_path`.

```bash
CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  python3 scripts/pranchas/gera_artes.py --render
```

Não troque isso por `playwright install`: o que falta é compatibilidade de
build, não navegador. E **não pule o passo 6** — a peça corta o que passa da
borda (`overflow: hidden`), e arte cortada não parece cortada: parece uma peça
com menos conteúdo. Quatro peças já foram para publicação com metade das 51
seções fora da arte antes de essa checagem existir.

---

## 5. O que esta verificação **não** resolve

As pendências do §6 da transferência viajam intactas. Em ordem de urgência:

1. **O prazo de entrega**, a única com hora marcada: arquivo até **18/09 às
   13:30** para a Saver (grátis) chegar em 28/09; Standard + € 35 chega 23/09;
   Express + € 38, 22/09. A eleição é **4/10**.
2. **Republicar** a Rota do Eleitor (`1PQjgzstbiNorfJgagXhB5`) e a Sinalização
   Hall 2 (`BcT5yzxRkSaUsbbHQQgjWF`) **nas mesmas URLs**. As duas páginas já
   estão regeneradas aqui com a paleta e os formatos novos; falta publicar.
   Publicar sem `url` cria um segundo artefato com o mesmo título.
3. **Confirmar as três cores contra o rolo de fita.** Os hexes foram lidos a
   olho da foto do estoque, não medidos.
4. **Vetor do logotipo** do TSE e **autorização de uso da marca** para posto no
   exterior. O logotipo destas peças é marcação de lugar: nenhuma peça deve ser
   impressa a partir dele.
5. **Cotar as quatro linhas que seguem premissa**: 3 banners PVC, 3 vinis, 2
   placas correx e a fixação.
6. **A fonte da campanha**, não identificada; as peças usam Archivo e Nunito
   Sans como substitutas.
7. **Medir em campo** o vão da S7 (1,27 m) e a posição das portas S4 · S5 · S6
   contra a planta cotada do RDS.
8. **O desvio da zona A**: a boca fica **2,91 m a oeste** do eixo da porta A —
   confirmado nesta rodada (`desvios {'A': 2.91, 'B': 0.0, 'C': 0.0}`). Ou vira
   trabalho de orientador, ou o Ring se desloca para leste.
9. **Sangria**: as artes são do tamanho exato da peça, sem sangria. Conferir
   com a gráfica antes de enviar.
