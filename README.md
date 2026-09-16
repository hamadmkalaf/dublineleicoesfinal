# Eleições 2026 · Posto de Dublin

Repositório final do planejamento do posto de votação de Dublin (Irlanda) para
o 1º turno de **4 de outubro de 2026**, no **Royal Dublin Society, Hall 2 e
Ring 3** (Merrion Road, Ballsbridge, Dublin 4). Contém apenas as versões
finais e o que as reproduz. O repositório de trabalho anterior,
`hamadmkalaf/eleicoes2026`, fica como arquivo morto; o roteiro da transferência
está em [`transferencia/TRANSFERENCIA.md`](transferencia/TRANSFERENCIA.md).

## 1. O que está decidido

**As agregações.** 16.794 eleitores aptos, 51 seções, 28 urnas num único
local. 23 urnas somam duas seções (429 a 797 eleitores); 5 operam com uma só,
perto de 400. Três urnas críticas, todas de duas seções de Dublin: MRV 22
(3313 + 3889), MRV 24 (3322 + 3752) e MRV 23 (3315 + 3778). Um quarto do
eleitorado (4.213) mora fora de Dublin. Página: `saidas/dublin_agregacoes.html`
("Urnas de Dublin", https://claude.ai/artifact/8YfHrRWvw7j8rZEZ2PgKiv).

**As portas.** Decisão do Posto de 06/09/2026, confirmada em 13/09: entradas
S4 (A), S5 (B) e S6 (C) na fachada sul; saídas S2 e S8. Identidade das filas
por letra.

**A fila externa (Ring 3).** Cenário 3 adaptado: raias leste-oeste, vão entre
zonas de 1,20 m, um CCB de apoio intermediário por divisória, bordas rígidas
só onde a fila empurra. Fecha em **180 CCBs (360,0 m)** e 506,0 m de fita
grossa, dentro dos 200 CCBs do estoque da organizadora, sem compra. Lotação
2.118. Folha: `saidas/ring3_montagem.html` ("Montagem do Ring 3",
https://claude.ai/artifact/FcQs4H7fM3RcBxmyFywazV); planta:
`saidas/ring3_planta.svg`.

**Dentro do salão.** Sem checkpoint: fitas coloridas no piso levam da porta à
mesa (decisão de 14/09). Postes Tensa só nas filas de mesa. Cada entrada serve
uma parede inteira (A oeste, B norte, C leste; decisão de 15/09). Detalhe nas
páginas em `artefatos/`.

O contexto consolidado, com a cronologia das decisões, está em
[`contexto_eleicoes_dublin_2026.md`](contexto_eleicoes_dublin_2026.md).

## 2. O que está aberto

- [`PENDENCIAS.md`](PENDENCIAS.md): orçamento final, comunicação com
  eleitores e mesários, funcionamento da MRV, apresentação do projeto.
- **Quatro pendências técnicas da folha do Ring 3** (seção "Quatro coisas
  para fechar" em `saidas/ring3_montagem.html`): a ponta fixa da divisória
  ainda amarra em fita; medir uma CCB na entrega (largura real do painel); a
  boca real do fundo não dá 1,00 m; confirmar com o safety officer do RDS as
  duas premissas marcadas.
- **Decisão D9** (identificação no caderno físico), registrada em
  `artefatos/posto-de-dublin-2026/pecas/decisoes.html`: condiciona o ritmo
  das três urnas críticas (≤ 55 s por eleitor para fechar às 17h).

## 3. Como reproduzir

```bash
pip install pandas openpyxl
python3 scripts/mapa_agregacoes.py    # data/raw → saidas/Dublin_2026_agregacoes.xlsx + saidas/dados.json
python3 scripts/gera_pagina.py        # saidas/dados.json → saidas/dublin_agregacoes.html
python3 scripts/ring3_montagem.py     # geometria e materiais do Ring 3 → saidas/ring3_planta.svg
python3 scripts/gera_pagina_ring3.py  # template + números → saidas/ring3_montagem.html
```

Os scripts resolvem caminho pelo próprio arquivo e rodam de qualquer
diretório; não é preciso `cd scripts`. `parse_dados.py` roda sozinho e
imprime um resumo da carga.

**Verificação (16/09/2026, pandas 3.0.5):** os quatro rodam a partir de
`/tmp`; `dados.json`, `dublin_agregacoes.html`, `ring3_montagem.html` e
`ring3_planta.svg` são reproduzidos byte a byte. O `.xlsx` nunca é byte a
byte, porque o formato grava a data de criação; confira abas e totais, não
bytes. `ring3_montagem.py` imprime `CCB: 180` e `compra 0 | sobra 20`.
`mapa_agregacoes.py` falha em vez de gravar saída errada se as validações não
passarem: soma por seção = soma por urna = total do perfil (16.794 por três
caminhos), 51 seções, 28 urnas, e o total de cada urna igual ao
`QT_ELEITOR_ELEICAO_FEDERAL` que o TSE publica.

**Não renomeie os arquivos de `data/raw/`**: `parse_dados.py` os abre pelo
nome literal. Também não mova `scripts/` para um subdiretório: os caminhos
saem de `parent.parent`.

## 4. De onde vêm os dados

Os três arquivos em `data/raw/` vieram da pasta do Google Drive do usuário:

| Arquivo | Gerado em | Papel |
|---|---|---|
| `eleitorado_local_votacao_2026_ZZ.csv` | 13/08/2026 | Seção a seção no exterior: papel (Principal/Agregada), `NR_SECAO_PRINCIPAL`, `QT_ELEITOR_SECAO` |
| `Filtrado_Dublin.csv` | 14/07/2026 | Perfil do eleitorado de Dublin, com `NR_SECAO` × `NM_LOCAL_VOTACAO` × `QT_ELEITORES` |
| `mapa_agregacoes_TSE.png` | 13/08/2026 | Mapa oficial de pares principal → agregada |

Ambos os CSVs estão em **latin-1**, separados por `;`. O `Filtrado_Dublin.csv`
foi re-exportado com a linha inteira envolvida em aspas e as aspas internas
duplicadas; `scripts/parse_dados.py` trata isso. Não "normalize" os arquivos
para UTF-8: a carga quebra.

`NM_LOCAL_VOTACAO` no arquivo de perfil é o local de votação original do
eleitor e é usado como referência de onde ele reside.

**Erro conhecido no PNG do TSE:** o mapa lista a seção agregada 3752 sob a
principal 3222, que pertence ao Porto. A correta é a 3322. O CSV prevalece; o
caso está na aba `Inconsistencias` do `.xlsx`.

Os dois CSVs são dados abertos do TSE e não identificam eleitores: são
contagens por seção. O repositório é privado por outro motivo: reúne planta,
barreiras, staff e orçamento de um local de votação com data e hora públicas.

`referencias/` guarda o que veio de terceiros e não é gerado aqui: a planta do
RDS Hall 2, o material sobre a MRV, a agregação na versão do TSE, a proposta de
agregação e o rascunho à mão do plano de fluxo com duas entradas
(`plano-fluxos-rascunho-2-entradas.png`, superado pela decisão de três portas
mas único desenho manuscrito do projeto).

## 5. O que é `artefatos/`

Cópias de leitura das páginas publicadas no claude.ai (plantas do salão,
sinalização, rota do eleitor, pranchetas, simulador, barreiras e o painel
"Posto de Dublin 2026"). **A fonte de verdade de cada uma é o URL, não o
arquivo.** Os scripts que as geraram nunca foram commitados e não existem
mais; as páginas são o único registro. Índice, URLs, versões lidas e o que
foi classificado como histórico: [`artefatos/README.md`](artefatos/README.md).
Inventário completo dos 17 artefatos, com a decisão sobre cada um:
[`transferencia/manifesto-artefatos.tsv`](transferencia/manifesto-artefatos.tsv).

## Estrutura

```
README.md · PENDENCIAS.md · contexto_eleicoes_dublin_2026.md
data/raw/        fontes TSE (nomes intocados)
scripts/         parse_dados · mapa_agregacoes · gera_pagina · ring3_montagem · gera_pagina_ring3 · template
saidas/          xlsx · dados.json · dublin_agregacoes.html · ring3_montagem.html · ring3_planta.svg
referencias/     recebidos de terceiros
artefatos/       HTML exportado do claude.ai (ver README de lá)
transferencia/   roteiro e manifesto da migração
```
