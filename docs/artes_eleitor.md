# Artes para o eleitor — 1º turno, 4 de outubro

Quatro peças quadradas de 1080 × 1080 para o feed, geradas por
`scripts/artes_eleitor.py` em `saidas/artes/`. Elas contam ao eleitor o que a
apresentação de 23/09 conta à equipe: **o percurso, e a letra que o atravessa.**

| # | Arquivo | O que resolve |
|---|---|---|
| 1 | `01-quando-e-onde` | Quando, onde, e o que levar. |
| 2 | `02-percurso` | O mapa simplificado do slide 9, em cinco passos. |
| 3 | `03-secao-porta` | As 51 seções, por porta. É a peça que faz o trabalho. |
| 4 | `04-no-dia` | Preferencial, documento, celular, saída. |

O SVG é o entregável — é vetor, escala para qualquer formato e se edita. O PNG
existe só para quem vai postar, e sai de `scripts/artes_png.py`.

```bash
python3 scripts/artes_eleitor.py            # escreve saidas/artes/
python3 scripts/artes_eleitor.py --confere  # só confere; código 1 se quebrar
python3 scripts/artes_png.py                # PNG 1080 × 1080, se houver Chromium
```

## De onde vem cada coisa

Nada aqui foi inventado. Tudo sai de fonte já versionada no repositório:

| Conteúdo | Fonte |
|---|---|
| Data, horário, local, 16.794 aptos, 51 seções, 28 urnas | `CLAUDE.md` · `saidas/dados.json` |
| O percurso em cinco passos | slide 9 do briefing de 23/09 |
| As 51 seções e a porta de cada uma | `mapa/sinalizacao/P1-Portao.dc.html` |
| Cores, tipografia, a regra da letra | `mapa/sinalizacao/Main.dc.html` |
| Portas da fachada sul (S4–S7) | `data/prancheta_hall2.json` |

A **conferência sai com código 1** se a tabela mestra deixar de ter 51 seções ou
se ela discordar das três bocas de zona (`P4-ZonaA/B/C`). Hoje fecha em
**18 A · 16 B · 17 C**. Rode antes de qualquer commit que toque nas peças de
sinalização — assim a arte pública não descola da placa que está no pátio.

## As três regras que as peças obedecem

1. **A letra identifica a fila; a cor é apoio.** Decisão de 17/09, em
   `Main.dc.html`. Em nenhuma peça a cor aparece sozinha: para um deuteranope, o
   amarelo de B e a abóbora de C só diferem em claridade.
2. **A cor da porta é a cor da fita comprada** — A `#33507E`, B `#E8C63A`,
   C `#DE7343`. A arte persegue a fita, não o contrário.
3. **Nunca rotular por número de mesa.** As mesas não têm número em peça nenhuma;
   o eleitor sabe a sua seção.

## Legendas sugeridas

**1 · Quando e onde**
> 🇧🇷 Eleições 2026 · 1º turno
> Domingo, 4 de outubro, das 8h às 17h (horário de Dublin), no RDS — Hall 2,
> Merrion Road, Ballsbridge, Dublin 4.
> Leve um documento oficial brasileiro com foto: e-Título, passaporte, RG, CNH ou
> carteira profissional.
> E descubra o número da sua seção **antes de sair de casa** — são quatro
> dígitos, e é o que organiza toda a fila. Se houver 2º turno, 25 de outubro.

**2 · O percurso**
> Da calçada até a urna, em cinco passos. Você entra pelo portão na Merrion Road,
> contorna o Hall 2 pela lateral leste, entra no pátio do Ring 3 pelo canto
> nordeste e procura a sua letra — C primeiro, B depois, A no fim. Da porta até a
> urna é sempre a mesma letra.
> Esquema, não está em escala.

**3 · A sua seção diz a sua letra**
> Procure os seus quatro dígitos. A letra ao lado é a sua fila, a sua porta e a
> sua parede — do pátio até a urna.
> As mesas não têm número: cada uma traz as seções que votam nela. Salve esta
> imagem e leve no celular.

**4 · No dia**
> Atendimento preferencial sem fila para idoso, gestante, lactante, pessoa com
> deficiência e quem os acompanha: pela porta à direita da C.
> A maior fila do dia é logo na abertura — se puder escolher, evite as duas
> primeiras horas. O celular fica na mesa dos celulares. E quem confere documento
> é o mesário, sempre: o voluntário orienta, não decide.

## O que falta antes de publicar

1. **O logotipo é marcação de lugar.** Como nas peças de sinalização, o lockup
   destas artes mostra onde a arte oficial entra e quanto espaço ocupa. **A arte
   em vetor tem de vir do TSE**, com a fonte da campanha e a autorização de uso da
   marca por posto no exterior. Não publicar sem trocar.
2. **A porta preferencial.** As artes dizem *"a porta à direita da C"* (S7), como
   o `CLAUDE.md` e o slide 9 do briefing de 23/09. A peça `P5-Preferencial`, de
   17/09, ainda diz *"qualquer porta"*. **As duas não podem ir para a rua juntas.**
   Quem decidir, decide para as duas.
3. **Documentos aceitos.** A lista da peça 1 é a regra geral do TSE para o voto no
   exterior, não uma instrução do Posto. Conferir com o Cartório antes de publicar.
4. **Horário.** As peças dizem *8h às 17h, horário de Dublin*. No exterior a
   votação segue o fuso local, e não o de Brasília — mas isso vale a confirmação
   por escrito, porque é a informação que mais custa se estiver errada.
5. **Inglês.** Parte do eleitorado lê melhor em inglês, e as peças 1 e 4 são as
   que mais se beneficiariam de uma versão. O gerador aceita outro dicionário de
   textos sem mudar o desenho.
