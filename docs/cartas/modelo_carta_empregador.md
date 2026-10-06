# Modelo de carta aos empregadores de voluntários

Carta em **inglês** (os empregadores são irlandeses), uma por voluntário, com os
campos entre `{{chaves}}` preenchidos a partir da planilha de envio (fluxo, próxima
etapa). Tudo fora do bloco "Texto da carta" é nota interna e não vai na carta.

## Campos

| Campo | Conteúdo | Observação |
|---|---|---|
| `{{data_carta}}` | data de envio, ex.: 7 October 2026 | |
| `{{nome_voluntario}}` | nome completo | exatamente como o empregador o conhece |
| `{{cargo}}` | função na empresa | opcional; remover a frase se vazio |
| `{{nome_destinatario}}` | RH ou gestor direto | se desconhecido: "Human Resources Department" |
| `{{empresa}}` | razão social | |
| `{{endereco_empresa}}` | endereço postal | |
| `variante` | A (mesário nomeado) ou B (apoio) | escolhe o parágrafo 3 |
| `{{pronome_poss}}` | his / her / their | **vem do voluntário, nunca inferido do nome** |

## Duas variantes do segundo parágrafo

O art. 98 da Lei 9.504/1997 dá a dispensa pelo dobro dos dias a quem foi **nomeado**
para a mesa receptora ou **requisitado** para auxiliá-la. Por isso o parágrafo muda
conforme o voluntário (campo `variante` na planilha):

- **A — mesário nomeado:** afirma o direito, direto.
- **B — apoio não nomeado:** só por analogia, sem afirmar direito.

Consentimento dos voluntários: já obtido (informado em 07/10/2026).

## Pontos ainda abertos

1. Papel timbrado de quem (consulado, comissão eleitoral, outro) e `{{contato}}`.
2. Se mesários nomeados já têm a declaração da Justiça Eleitoral, vale citá-la na
   variante A ("a declaration is available on request").

---

## Texto da carta

**{{data_carta}}**

{{nome_destinatario}}
{{empresa}}
{{endereco_empresa}}

**Re: Voluntary service by {{nome_voluntario}} at the 2026 Brazilian Presidential Elections, Dublin**

Dear {{nome_destinatario}},

I am writing as the administrator of the 2026 Brazilian Presidential Elections in
Ireland, to let you know that your employee, {{nome_voluntario}}, took part in the
organisation of the first round of voting held in Dublin on Sunday, 4 October 2026.

On that day, between 06:30 and 18:00, {{nome_voluntario}} served as a polling station
worker. This was strictly voluntary work: it was unpaid, and it was carried out on
{{pronome_poss}} own time, on a Sunday, in support of an election in which the Brazilian
community in Ireland exercises its right to vote. We are very grateful for
{{pronome_poss}} commitment.

**[Variante A — mesário nomeado]**
{{nome_voluntario}} was formally appointed to serve at the polling station. Under
Brazilian electoral law (Law No. 9,504/1997, Article 98), citizens appointed to
polling stations are entitled to two days of leave, with no loss of pay, for each day
worked. We understand that Brazilian law creates no obligation for employers in
Ireland, and we do not suggest otherwise. We would, however, be grateful if you could
consider, as a courtesy, granting {{nome_voluntario}} additional time off in
recognition of the service {{pronome_poss}} performed.

**[Variante B — apoio não nomeado]**
In Brazil, citizens who serve at polling stations on election day are entitled to two
days of leave, with no loss of pay, for each day worked (Law No. 9,504/1997, Article
98). Although {{nome_voluntario}} served in a support role, we understand that Brazilian
law creates no obligation for employers in Ireland, and we do not suggest otherwise. We
would, however, be grateful if you could consider, as a courtesy, granting
{{nome_voluntario}} some additional time off in recognition of the service
{{pronome_poss}} performed.

Should you require any confirmation of the dates and hours described above, please do
not hesitate to contact us at {{contato}}.

Thank you for your time and consideration.

Yours sincerely,

&nbsp;

**Eduardo de Mattos Hosannah**
Administrator, 2026 Brazilian Presidential Elections in Ireland
{{contato}}
