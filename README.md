# dublineleicoesfinal

Repositório para planejamento das eleições de Dublin — 1º turno de 04/10/2026,
RDS Ballsbridge, Hall 2. Destino da migração descrita em
[`TRANSFERENCIA.md`](https://github.com/hamadmkalaf/eleicoes2026/blob/main/TRANSFERENCIA.md)
do repositório `hamadmkalaf/eleicoes2026`, que ainda carrega a análise das
agregações, os scripts e as demais saídas.

## O que já está aqui

**O arranjo congelado.** A atribuição de seção/porta e a posição das 28 mesas
no Hall 2 são dado versionado em `congelado/`, no arranjo
`paredes-abc-20260915`. Cada entrada serve uma parede inteira — A/S4 a oeste
(9 mesas, 3.834 esperados), B/S5 ao norte (9 mesas, 3.832), C/S6 a leste
(10 mesas, 3.833). 51 seções, 16.794 aptos.

```bash
python3 scripts/verifica_congelamento.py
```

Os mesmos arquivos, byte a byte, estão em `hamadmkalaf/eleicoes2026`. O que
está congelado, como conferir e como mudar: **[CONGELAMENTO.md](CONGELAMENTO.md)**.

**Os artefatos.** `artefatos/` guarda 34 arquivos exportados do claude.ai em
17/09/2026, byte a byte, com `CHECKSUMS.sha256`. Inclui o bundle de 17 arquivos
do painel `Posto de Dublin 2026`, que carrega o registro de decisões e as
instruções de fluxo — duas peças que não existem como artefato solto. Leia
**[artefatos/README.md](artefatos/README.md)** antes de usar qualquer uma: ele
diz qual gerador cada página tem (quase nenhuma tem), e marca o documento de
instruções de fluxo como superado no ponto da atribuição de porta.

**`Identidadevisual/`** — referências de identidade visual para a sinalização.

## O que ainda não está

Os dados do TSE em `data/raw/`, os scripts de análise, as saídas e as
referências recebidas do local — passos 2 a 4 do roteiro de transferência. E os
onze scripts e documentos que os artefatos citam mas que nunca foram
commitados, sem os quais nenhuma das páginas de `artefatos/` pode ser regerada;
a lista está em [artefatos/README.md](artefatos/README.md).
