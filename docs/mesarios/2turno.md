# Mesários do 2º turno (25/10/2026) — expectativa de comparecimento

Planilha: `saidas/mesarios/2026.10.12_Mesarios_2turno_consolidado.xlsx`, com nomes, e-mails e
títulos de eleitor. Ela é gerada por `scripts/mesarios_2turno.py --grava`. Sem `--grava`, o script
só confere e imprime; sai com código 1 se alguma conferência falhar.

## As quatro abas

| Aba | O que mostra | Como se atualiza |
|---|---|---|
| **Expectativa** | Seção, nome e expectativa de cada mesário, mais um resumo por categoria | fórmula sobre "Mesários" |
| **Mesários** | Base completa: seção, função, nome, e-mail, título, presença no 1º turno, resposta do 2º turno, ID no formulário, expectativa | **é aqui que se edita**: coluna G, "Resposta 2º turno" |
| **Funções a preencher** | Seção, função, designado e sugestão de ação, em ordem de prioridade | fórmula sobre "Mesários"; não editar |
| **Por seção** | Aptos no BU, comparecimento efetivo, posição e faixa efetiva | valores dos BUs de 04/10 |

São 112 linhas em "Mesários": 28 urnas × 4 funções. Os 111 designados ocupam 111 delas; a 112ª é a
vaga sem designado desde o 1º turno (3862, 2º Mesário). Ela entra para aparecer em "Funções a
preencher".

## Regra de expectativa (Posto, 12/10)

| Presença no 1º turno | Resposta no 2º turno | Expectativa | Ação sugerida |
|---|---|---|---|
| qualquer | SIM | **Deve comparecer** | — |
| qualquer | NÃO | **Não deve comparecer** | Recrutar substituto |
| esteve | sem resposta | **Confirmar** | Contatar para confirmar presença |
| faltou | sem resposta | **Não deve comparecer** | Recrutar substituto |
| — (função vaga) | — | **Vago** | Recrutar mesário |

A ordem em "Funções a preencher" segue a posição da seção em "Por seção" (comparecimento efetivo do
1º turno). Dentro da seção, a ordem é Presidente > 1º Mesário > 1º Secretário > 2º Mesário. Essa
ordem de funções é uma premissa operacional.

## Números (12/10)

| Expectativa | Funções |
|---|---|
| Deve comparecer | **58** |
| Confirmar | **28** |
| Não deve comparecer | **25** (11 responderam NÃO + 14 faltaram ao 1º turno e não responderam) |
| Vago | 1 |
| **A preencher** | **54** |

## De onde vem cada dado

| Arquivo (em `saidas/mesarios/entrada/`) | O que vale |
|---|---|
| `2026.10.12_Mesarios_Secoes_Atualizadas.xlsx` | só a aba `Por secao`: aptos e comparecimento efetivo dos BUs, posição e faixa efetiva |
| `2026.10.12_Mesarios_Comparecimento_confirmado.xlsx` | aba `Mesarios`: seção, função, nome, e-mail, título e presença consolidada (lista Elo × boletins de identificação) |
| `2026.10.12_Confirmacao_2turno_Forms_1-75.xlsx` | as 72 respostas do formulário de confirmação |

O cruzamento do formulário com a lista funciona assim:

- O formulário é anônimo, então o casamento é pelo nome sem acento e em maiúsculas (59 respostas).
- O resto passa pela tabela `EQUIVALENCIAS` do script, conferida à mão (12 respostas, como "Rogetio
  Goes" → Rogério Linhares Goes). Não há nenhum casamento aproximado automático.
- Quem respondeu mais de uma vez fica com a **última** resposta. Lincoln Cubas Guedes respondeu NÃO
  e depois SIM.
- "Mariana Souza bode" (SIM) não corresponde a nenhum dos 111 designados e ficou de fora.

**Ajustes informados pelo Posto (12/10), fora do formulário** (`CONFIRMACOES_DIRETAS` e
`CORRECOES_PRESENCA` no script):

- Os Presidentes Maíra Fabiola Fabiani (3322), Jair de Assunção Correia Filho (3315) e Vanessa Rocha
  Barbosa Barbalho (3313) confirmaram por contato direto. Na planilha, o ID deles aparece como
  "contato direto".
- Jair constava como ausente no boletim de identificação do 1º turno; o Posto informou que ele
  compareceu, e a presença foi corrigida para SIM.

## Para atualizar

- **Uma confirmação nova:** mude a coluna G da aba "Mesários" (SIM / NÃO / vazio). As outras abas
  se recalculam.
- **Um export novo do formulário:**
  1. Substitua o arquivo em `entrada/`.
  2. Rode `python3 scripts/mesarios_2turno.py`.
  3. Se aparecer um nome sem correspondência, acrescente-o em `EQUIVALENCIAS`.
  4. Rode com `--grava`.

  Isso regrava a planilha a partir das fontes: mudanças feitas à mão na planilha se perdem. Por isso,
  confirmações por fora do formulário vão em `CONFIRMACOES_DIRETAS`.
