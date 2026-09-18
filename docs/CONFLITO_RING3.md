# Conflito aberto — o Ring 3 está de pé ou não?

> Escrito durante a transferência dos dois temas para este repositório, em
> 18/09/2026. Não é uma decisão: é o registro de uma contradição que os dois
> temas transferidos carregam e que **só o Posto pode resolver**.

---

## 1. A contradição, em um parágrafo

Os dois temas que este repositório reúne partem de premissas incompatíveis sobre
onde o eleitor espera.

- O tema dos **separadores de fila** parte de que o **Ring 3 não existe mais**: o
  RDS proibiu fila no terreno dele, não houve autorização de Brasília, e a fila
  passou a ser dimensionada **dentro do Hall 2**, uma por parede. É por isso que o
  desenho gasta 98 unifilas e 769 m de fita no piso do salão.
- O tema dos **voluntários** mantém o **Ring 3 como pátio de fila ao ar livre**,
  com 23 raias por zona, e apoia nele 5 dos seus 17 postos, mais o estágio do
  apron.

As duas coisas não podem ser verdade ao mesmo tempo.

## 2. A prova documental

| Evidência | O que diz | Data |
|---|---|---|
| `data/decisoes.json`, bloco `ring3` | *"abandonado em 15/09/2026 — o RDS proibiu fila no terreno e não houve autorização de Brasília; a fila passa a ser dimensionada dentro do Hall 2, uma por parede"* | 15/09 |
| `docs/separadores/CONFERENCIA_PRANCHETA_2026-09-15.md` | *"O Ring 3 não existe mais."* | 15/09 |
| `docs/separadores/contexto.md` §1 | *"o RDS proibiu fila no seu terreno e o Ring 3 foi abandonado em 15/09"* | 17–18/09 |
| `CLAUDE.md`, seção de geometria (vinda do tema de voluntários) | Ring 3 como pátio de fila de 44,0 × 35,0 m, 23 raias por zona | *"planta de 16/09"* |
| `docs/voluntarios/contexto.md` §2 e §5 | Postos R1–R5 no Ring; 888 m de fila; 926 m de barreira necessários | 15–18/09 |

**O registro de decisão é de 15/09 e é explícito.** A geometria do tema de
voluntários se declara de 16/09 — posterior — mas não menciona a proibição do RDS
em nenhum ponto, nem a contesta. A leitura mais provável, e que deve ser confirmada
com o Posto, é que **o tema dos voluntários não recebeu a decisão de 15/09**: foi
desenvolvido num branch próprio, em paralelo, e nunca leu o `decisoes.json`
atualizado. É exatamente a falha de processo que o próprio roteiro de transferência
dos separadores descreve como *"o sintoma mais caro"* do repositório de origem.

**Nenhum documento transferido registra uma reversão da decisão de 15/09.** Até que
apareça, a hipótese de trabalho é a do §3.1.

## 3. O que cai e o que sobrevive, em cada hipótese

### 3.1 Hipótese A — o Ring 3 está fora (é o que a decisão de 15/09 diz)

**Cai do tema de voluntários:**

- Os **5 postos do Ring**: R1 (corredor de chegada), R2 (bocas das zonas), R3
  (trecho de fundo), R4 (dentro das raias), R5 (cabeça de fila).
- Os **3 postos do apron**: A1 (cruzamento com a saída S8), A2 (portas S4/S5/S6),
  A3 (preferencial S7) — o apron continua existindo como faixa física, mas deixa de
  ser cabeça de fila, e o papel desses postos muda de conteúdo.
- Toda a **§5 do contexto de voluntários**: os 888 m de fila do Ring, a absorção de
  30–45 min de atraso, os ~926 m de barreira contra 200 m orçados, o protocolo de
  chuva para pátio descoberto, e o diagnóstico de que o apron é travessia e não
  estoque.
- A composição de **C1 e C2** muda: C1 aloca 1 pessoa em R3 e C2 acrescenta R5 e
  R2 — 6 das 15 posições do C2 estão no Ring.

**Sobrevive:**

- **P0**, o posto crítico, e a sua criticidade — que só aumenta, porque sem pátio de
  fila externo o custo de alguém chegar sem saber a seção cresce.
- **H1, H2, H3** (dentro do salão) e **T1, T2** (coordenação e base).
- O princípio de projeto: *a sinalização atende o caso padrão; o voluntário atende a
  exceção* — que é aritmético e independe do Ring.
- *Voluntário orienta, não decide.*
- As três compensações de C1/C2, com a primeira reescrita: presença de fila dentro
  do salão, não no pátio.

**Consequência quantitativa que ninguém calculou ainda:** sem o Ring, os ~11.499
comparecentes esperam **dentro** do Hall 2, e o desenho dos separadores já reserva o
campo central para isso. Mas o dimensionamento de pessoal do tema de voluntários
nunca foi refeito contra essa geometria. **Os cenários C1–C4 precisam ser
recontados.**

### 3.2 Hipótese B — o Ring 3 voltou depois de 15/09

Então a decisão em `data/decisoes.json` está **vencida**, e com ela:

- o desenho dos separadores perde a sua razão de ser na forma atual (a reserva de
  fila no campo central do Hall 2 deixa de ser necessária nessa escala);
- `cenarios/paredes-abc-20260915.json` e a atribuição mesa → entrada precisam ser
  reconferidos, porque a versão anterior distribuía a carga **por cota do Ring 3**
  (A 3.642 / B 4.215 / C 3.642), e não "uma entrada por parede";
- as 98 unifilas e os 769 m de fita passam a ser um orçamento a revisar.

Nessa hipótese **o tema dos separadores é que precisa ser refeito**, não o de
voluntários.

## 4. Por que a transferência não resolveu isto

Três razões, na ordem em que pesam.

1. **Não é uma decisão técnica.** Depende de um fato externo — o que o RDS
   autoriza — e de uma autorização de Brasília. Nenhum dos dois está neste
   repositório.
2. **Resolver por edição de texto destruiria informação.** Apagar os postos R1–R5
   do tema de voluntários, ou apagar o bloco `ring3` do `decisoes.json`, faria o
   repositório parecer coerente sem que nada tivesse sido decidido — e a próxima
   sessão herdaria uma falsa coerência, que é pior do que um conflito declarado.
3. **Os dois roteiros de transferência mandaram trazer os dois temas inteiros**, e
   nenhum dos dois menciona o outro. A contradição só aparece quando os dois chegam
   ao mesmo repositório, que é o que acabou de acontecer.

## 5. O que fazer com isto

1. **Perguntar ao Posto qual das duas hipóteses vale.** É pergunta de uma linha, e
   bloqueia o recálculo dos cenários de efetivo.
2. Se valer a **hipótese A** — a mais provável —, encomendar o recálculo dos
   cenários C1–C4 contra a geometria confinada do Hall 2, reaproveitando P0, H1–H3
   e T1–T2 e descartando R1–R5 e a §5 do contexto de voluntários.
3. Se valer a **hipótese B**, reabrir `cenarios/paredes-abc-20260915.json` e a
   alocação de barreira antes de comprar qualquer coisa.
4. Em qualquer caso, **não comprar as 15 unifilas adicionais nem os 8 rolos de
   fita** antes da resposta, e antes da pendência bloqueante do §9 do contexto dos
   separadores (o RDS permite fita no piso?).

## 6. Fontes

- `data/decisoes.json` — bloco `ring3`
- `docs/separadores/CONFERENCIA_PRANCHETA_2026-09-15.md` — achado 1
- `docs/separadores/contexto.md` — §1, §2, §9
- `docs/voluntarios/contexto.md` — §2, §3, §5, §6
- `CLAUDE.md` — seção "Geometria do local"
- `docs/TRANSFERENCIA_REALIZADA.md` — como e de onde cada arquivo chegou
