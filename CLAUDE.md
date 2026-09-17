> ## ⚠ ESTE ARQUIVO ESTÁ DESATUALIZADO NUM PONTO — RING 3
>
> **O Ring 3 foi CONFIRMADO pelo Posto em 16/09/2026.** Tudo o que este
> documento diz sobre o Ring 3 ter sido abandonado, proibido pelo RDS ou "não
> existir mais" está **revertido**, e a fila externa no terreno do RDS voltou a
> ser o plano. A fila confinada dentro do Hall 2 é contingência.
>
> Com a confirmação, as larguras das zonas também mudaram: elas eram
> proporcionais às cotas do Ring 3 antigo (A 3.642 / B 4.215 / C 3.642) e
> passaram a sair do esperado por entrada de Paredes_ABC — **12,87 · 12,86 ·
> 12,87 m**, 179 CCBs, percurso máximo de 296 m.
>
> Esta branch é uma das origens da consolidação em `main` e não recebeu essa
> correção: ela vive em `main` (`data/decisoes.json`, bloco `ring3`;
> `scripts/ring3_montagem.py`; `docs/CONTEXTO_DO_PROJETO.md` §6.1). **Leia a
> `main` antes de usar qualquer número de Ring 3 deste arquivo.**

# Regras deste repositório

Este repositório é a **fonte única** do desenho do posto de Dublin para
4/10/2026. Ele nasceu de uma transferência que deixou para trás 26 branches e
quatro cópias divergentes do mesmo contexto (ver `TRANSFERENCIA.md` §9). As
regras abaixo existem para isso não se repetir.

## Antes de tocar no arranjo

**Leia `CONFERENCIA_PRANCHETA_2026-09-15.md`.** Os onze adendos são o porquê de
cada decisão, com números. Várias ideias que parecem novas já foram testadas e
descartadas ali — inverter paredes, redistribuir por aptos em vez de esperados,
usar o Ring 3. Propor de novo o que já foi medido e rejeitado custa uma sessão.

## Nunca

1. **Nunca edite `data/decisoes.json` à mão.** Ele é gerado: o passo 3
   (`gera_decisoes_base.py --grava`) escreve o bloco das mesas, o passo 4
   (`arranjo_paredes.py --grava`) escreve a camada de layout por cima. Uma
   edição manual sobrevive até a próxima rodada e depois some — ou, pior, fica
   e as conferências passam a mentir. Para mudar um número, mude o script.
2. **Nunca mexa na agregação de seções.** O par principal → agregada é do
   Cartório Eleitoral, está conferido contra
   `data/oficiais/secoes_agregadas_dublin_2026.pdf`, e os 109 mesários já
   foram nomeados por MRV em cima dele. Mudar a agregação invalida a nomeação.
3. **Nunca commite sem rodar as duas conferências**, se o commit toca em dados
   ou arranjo. As duas saem com código 1 se algo divergir:

   ```bash
   python3 scripts/confere_prancheta.py && python3 scripts/confere_arranjo.py
   ```

4. **Nunca guarde cenário antigo dentro de `cenarios/`.** O gerador lê aquela
   pasta como lista de alternativas válidas. Histórico vai para `historico/`.
5. **Nunca abra um branch novo por sessão sem mesclar de volta.** Um branch só,
   com merge de volta, é o que evita a divergência que motivou a transferência.

## O editor não é a cadeia

`saidas/editor.html` serve para estudar posição, não para decidir. O que sai
dele é um cenário; ele vira desenho quando é gravado em `cenarios/` e a cadeia
roda de novo (passo 4 em diante) e as duas conferências passam. Regerar o
editor (`python3 scripts/gera_editor.py`) depois de qualquer mudança em
`data/decisoes.json`, senão a página passa a mostrar número velho.

## A cadeia

Sete passos, sem rede, na ordem do `README.md`. A ordem 3 → 4 não é
negociável. Depois de qualquer mudança, rode a cadeia inteira e confira que os
arquivos gerados saem idênticos — ela é determinística, e deixou de ser é
sintoma de bug.

## O que está decidido e congelado

| Decisão | Quando | Onde vive |
|---|---|---|
| Base de comparecimento B — taxa de 2022 por condado | 06/09 | `scripts/comparecimento.py` |
| MRV do DJE como identidade da mesa | 06/09 | `data/decisoes.json`, campo `numeracao` |
| Numeração eleitor: 1 na mesa mais ao sul da oeste, sentido horário | 13/09 | `arranjo_paredes.numeracao_eleitor()` |
| Uma entrada por parede: A→oeste, B→norte, C→leste | 15/09 | `arranjo_paredes.ENTRADA` |
| Ring 3 abandonado | 15/09 | `data/decisoes.json`, bloco `ring3` |
| Portas: S4/S5/S6 entradas, S2/S8 saídas, S7 preferencial | 16/09 | `arranjo_paredes.PAPEIS_PORTA` |
| N2 e O2 desobstruídas, recuo de 3 m | 16/09 | `decisoes.zonas_protegidas` |
| Faixa de emergência de 3 m na fachada leste | 16/09 | idem |
| Sala de apoio entre O1 e a parede norte | 16/09 | idem |
| Serpenteado de ~20 pessoas à frente de cada vermelha | 16/09 | `decisoes.serpenteados` |
| Vão de 3,00 m na dupla, 1,50 entre unidades, 1,90 ao lado da vermelha | 16/09 | `arranjo_paredes`, constantes |

Mudar qualquer linha dessa tabela é decisão do Posto, não da sessão.

## Aviso sobre peças antigas

Qualquer peça gerada **antes de 15/09/2026** carrega a atribuição mesa →
entrada por cota do Ring 3 (A 3.642 / B 4.215 / C 3.642) e a numeração eleitor
antiga. Trazer uma dessas para cá sem regerar é trazer número errado.
