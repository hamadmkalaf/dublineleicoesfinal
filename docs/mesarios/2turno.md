# Mesários do 2º turno (25/10/2026) — quem volta e o que falta preencher

Consolidação de 12/10/2026. Planilha: `saidas/mesarios/2026.10.12_Mesarios_2turno_consolidado.xlsx`
(contém nomes, e-mails e títulos de eleitor). Gerada por `scripts/mesarios_2turno.py --grava`.
Sem `--grava`, o script só confere e imprime, e sai com código 1 se alguma conferência falhar.

## De onde vem cada coisa

| Arquivo (em `saidas/mesarios/entrada/`) | O que vale | O que está superado |
|---|---|---|
| `2026.10.12_Mesarios_Secoes_Atualizadas.xlsx` | `Por secao` colunas **M–W** (comparecimento efetivo dos 28 BUs de 04/10) e `Ranking` | presença sem consolidar (`0006/2026`, `-`) em todas as outras abas |
| `2026.10.12_Mesarios_Comparecimento_confirmado.xlsx` | `Resumo`, `Mesarios`, `Presenca por secao`, `Por secao` A–L, `Boletins`, `Divergências`, `Fora da lista` | `Por secao` M–O (substituídas pelas M–W do arquivo acima) |
| `2026.10.12_Confirmacao_2turno_Forms_1-75.xlsx` | as 72 respostas do formulário de 2º turno (IDs 1–75; faltam 40, 42 e 67 no export) | — |

As duas abas `Por secao` têm as mesmas linhas (seções 2–29, total 30, notas até 38), então as
colunas M–W entram no arquivo consolidado **com as fórmulas**, e o `Ranking` continua lendo
`'Por secao'!V`.

## Regras do cruzamento

- O formulário é anônimo: só traz o nome digitado. Casamento pelo nome sem acento e em maiúsculas
  (59 respostas); o resto passa pela tabela `EQUIVALENCIAS` do script, conferida à mão (12 respostas,
  por exemplo "Rogetio Goes" → Rogério Linhares Goes). **Nenhum casamento aproximado automático.**
- Quem respondeu mais de uma vez: **vale a última resposta.** Cinco pessoas responderam duas vezes;
  só uma mudou de resposta (NÃO e depois SIM). Essa pessoa foi ausente no 1º turno, então convém
  confirmar por contato.
- Uma resposta (SIM) não corresponde a nenhum dos 111 designados. Fica sinalizada na aba
  `Respostas 2º turno` para revisão manual, e não é sugerida para vaga.

## Números (retrato de 12/10)

| | |
|---|---|
| Designados do 1º turno | 111 (+1 função vaga desde o 1º turno: 3862, 2º Mesário) |
| Confirmados para o 2º turno | **55** (54 deles estiveram presentes no 1º turno) |
| Não voltam | 11 |
| Sem resposta | **45** (30 deles estiveram presentes no 1º turno) |
| Funções abertas, de 112 | 57 |
| Meta: 4 nas Alto/Médio, 3 nas Baixo | 91 funções |
| **Déficit para a meta** | **38**: 13 nas 7 urnas prioritárias + 25 nas 21 Baixo |
| … dos quais são designados sem resposta (contatar) | 31 |
| … dos quais exigem substituto (não volta ou vaga) | 7 |
| Urnas sem Presidente confirmado | **16 de 28** |
| Urnas com as 4 funções confirmadas | 2 (3142, 517) |

**Lotação integral** (4 funções) vale para as urnas de faixa efetiva Alto ou Médio, ou seja, com
comparecimento efetivo de pelo menos 329 em 04/10: **3315, 3322, 3313** (Alto) e **3311, 3302,
3179, 3306** (Médio). Cada uma das três urnas Alto tem hoje só 2 confirmados e nenhum Presidente
confirmado.

Duas premissas são operacionais, não regra legal. Ambas ficam editáveis:
- a **meta 3** nas urnas Baixo (célula amarela em `Vagas por urna`; constante `META_BAIXO` no script);
- a **ordem de prioridade** ao preencher: Presidente > 1º Mesário > 1º Secretário > 2º Mesário
  (`ORDEM_PRIORIDADE`).

## Abas novas da planilha consolidada

- **Resumo 2º turno**: os números acima. Os que dependem da lista de mesários são fórmulas.
- **Vagas por urna**: as 28 urnas na ordem do Ranking, com as 4 funções (nome + status), a meta, o
  déficit e um alerta. **São fórmulas sobre `Mesarios!P`**: quando chega uma confirmação nova, basta
  mudar a célula da pessoa em `Mesarios!P` e esta aba se atualiza.
- **Funções a preencher**: lista plana, com filtro, das funções não confirmadas, cada uma marcada
  como *Necessária* (falta para a meta) ou *Desejável*, com a ação a tomar. É um retrato: para
  atualizar, é preciso rodar o script de novo.
- **Respostas 2º turno**: cada resposta do formulário, com o designado correspondente, o tipo de
  casamento e as duplicadas e conflitos marcados.
- **Mesarios** ganhou as colunas P–R (resposta do 2º turno, ID no formulário e observação).

## Para atualizar com um novo export do formulário

1. Substitua `saidas/mesarios/entrada/2026.10.12_Confirmacao_2turno_Forms_1-75.xlsx`, ou ajuste
   `ARQ_FORMS` no script.
2. Rode `python3 scripts/mesarios_2turno.py`. Se aparecer um nome novo sem correspondência, decida à
   mão e acrescente a linha em `EQUIVALENCIAS`.
3. Rode com `--grava`.
