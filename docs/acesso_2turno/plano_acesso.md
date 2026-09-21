# Plano de acesso ao RDS no 2º turno — 25/10/2026, dia da Maratona de Dublin

**Estado:** proposta de 21/09/2026, a validar com a Garda e o RDS. Vale só se
houver 2º turno.

**Fonte:** plano de trânsito enviado pela chefia de polícia da região após a
reunião de setembro de 2026 (texto integral no anexo A). Data e ondas de largada
da maratona confirmadas na organização da prova: domingo 25/10/2026, largadas
às 8h45, 9h05, 9h25 e 9h45.

**Geração:** `python3 scripts/acesso_2turno.py --grava` produz o KML para o
Google My Maps, o esquema SVG/PNG, a página `mapa/acesso_2turno.html`, o JSON e a
lista de links do Google Maps. Sem `--grava`, só confere (sai com código 1 se
alguma rota de veículo tocar via fechada).

---

## 1. O problema em uma frase

A Merrion Road, que no 1º turno é a porta do RDS para tudo — eleitor a pé,
carro, táxi, ônibus, entrega —, é o **percurso da maratona a partir das 10h** e
fica fechada, provavelmente até o meio da tarde. O RDS passa a ter **uma só via
de veículos, a Anglesea Road**, e todo eleitor que vem do leste (DART, Sandymount,
Ballsbridge) precisa **cruzar o percurso** para chegar.

A votação vai das 8h às 17h. O regime de maratona cobre **cerca de seis das nove
horas** e, pelo perfil de chegada do 1º turno, dois terços ou mais dos 11.499
eleitores esperados (premissa: comparecimento igual ao do 1º turno).

## 2. O que a Garda decidiu, e o que isso faz com o RDS

| Via | Decisão da Garda | Consequência |
|---|---|---|
| Nutley Lane, Merrion Road inbound, Shelbourne Road, Haddington Road, Northumberland Road | fechadas a partir das 10h | O portão da Merrion Road deixa de servir veículos. A calçada continua aberta a pedestres. |
| Merrion Road | só outbound, a partir da Serpentine Avenue | Quem está ao sul da Serpentine Avenue pode sair para o sul. Ninguém entra por ela. |
| Anglesea Road | aberta ao tráfego do RDS; **proibido sair para a Merrion Road** | A única via de veículos do RDS. Entra e sai por Donnybrook. |
| Stillorgan Road (N11) | aberta ao tráfego geral o dia todo | Corredor de carro a partir do sul. Corredores nas faixas de ônibus: lentidão. |
| Donnybrook Road, Morehampton Road, Leeson Street Upper | abertas | Corredor de carro a partir do centro, do norte e do oeste. |
| Sandford Road (saída de Ranelagh) | desviada pela Eglinton Road para a Stillorgan Road | Não afeta o RDS; converge para Donnybrook. |
| Rock Road inbound | desviada nos Merrion Gates pela Strand Road, para Irishtown/Ringsend ou East Link | **Quem vier pela costa não chega ao RDS.** A rota do sul é a N11. |

A frase que manda no plano: *"Anglesea Road will remain open to R.D.S. traffic
but traffic will not be allowed exit Anglesea onto Merrion Road."*

## 3. O plano

### 3.1 Princípio

Mudar **como se chega ao P0**, não o que acontece depois dele. Ring 3, as três
zonas, as portas S4–S7, a rota P0–P7 e a sinalização do 1º turno ficam como
estão. O plano acrescenta uma segunda porta (Anglesea Gate), um posto (G1) e dois
pedidos à Garda (as travessias).

### 3.2 Portões

| Portão | 1º turno | 2º turno (10h → reabertura) |
|---|---|---|
| Merrion Road (P1) | tudo | **só pedestres**, pela calçada do lado do RDS. P0 continua no gradil. |
| Anglesea Gate | não usado pelo público | **todos os veículos**: mesários, táxi, preferencial, ambulância, entregas. Posto novo G1. |
| Simmonscourt Road | não usado | saída opcional para o sul pela Merrion outbound (rota V4), **só se a Garda confirmar**. |

### 3.3 Rotas recomendadas

Links prontos do Google Maps em `saidas/acesso_2turno_links.md`.

| Cód. | Modo | Rota | Observação |
|---|---|---|---|
| V1 | carro, do sul | N11 → Donnybrook → Anglesea Road → Anglesea Gate | Nunca pela Rock Road: o desvio dos Merrion Gates não chega ao RDS. |
| V2 | carro, do centro/norte/oeste | Leeson St Upper → Morehampton → Donnybrook → Anglesea Road → Anglesea Gate | Não tentar Merrion, Shelbourne, Northumberland. |
| V3 | saída de carro | Anglesea Gate → Anglesea Road → Donnybrook | Única saída garantida. |
| V4 | saída alternativa para o sul | Simmonscourt → Merrion outbound → Merrion Gates → Rock Road | A confirmar com a Garda. |
| A1 | a pé, DART Sandymount | Serpentine Ave (≈750 m) → travessia 1 → calçada do RDS para o norte (≈250 m) → P1 | ≈1,0 km, 13 min. Cruza o percurso. |
| A2 | a pé, DART Lansdowne Road | Lansdowne Rd e Shelbourne Rd (≈450 m) → travessia 2 em Ballsbridge → calçada do RDS para o sul (≈250 m) → P1 | ≈700 m, 9 min. Cruza o percurso. |
| A3 | a pé, ônibus em Donnybrook | Anglesea Road → Anglesea Gate → rota interna → Ring 3 | ≈750 m, 10 min. **Não cruza o percurso.** Rota interna a confirmar com o RDS. |
| T1 | táxi, preferencial, mobilidade reduzida | destino "RDS Anglesea Road Gate"; embarque e desembarque dentro do portão | Nunca pedir "RDS": o aplicativo tenta a Merrion Road. |

Distâncias e tempos são estimativas de mapa, não medidas.

### 3.4 O dia, hora a hora

| Janela | Regime | O que vale |
|---|---|---|
| 07:00–10:00 | Normal | Como no 1º turno. Mesários, seguranças e entregas já dentro. A Garda pode conar antes das 10h (premissa a confirmar). |
| 10:00–10:45 | Maratona, sem corredores | Fechamentos em vigor, Merrion Road vazia. Trocar a sinalização de chegada, abrir o G1. Primeiros corredores (elite) por volta das 10h45. |
| 10:45–14:30 | Maratona, pico | Fluxo contínuo. Travessias só nos pontos controlados, com espera. Todo veículo pela Anglesea. |
| 14:30–16:00 | Maratona, cauda | Fluxo esparso. Fechamentos seguem até a Garda reabrir. Últimos corredores por volta das 15h40. |
| 16:00–17:00 | Reabertura progressiva (a confirmar) | Tratar como maratona até confirmação no rádio. Última hora: pico de chegada tardia; quem está na fila às 17h vota. |
| 17:00–18:30 | Normal | Saída de eleitores, mesários e material. |

Horas dos corredores: **estimativa** a partir das ondas e da posição do RDS
perto do km 40 (a organização coloca a marca de 25 milhas no RDS). A Garda não
informou hora de reabertura.

### 3.5 Sete diferenças operacionais em relação ao 1º turno

1. **Veículos só pelo Anglesea Gate**, saída sempre por Donnybrook.
2. **Posto novo G1 no Anglesea Gate**, 2 pessoas: recebe quem chega de carro,
   táxi e de Donnybrook, aponta a rota interna até o Ring 3 e cobre o
   preferencial. Em C1 (9 pessoas) sai de um dos 3 operadores do P0 mais o T1 em
   rodízio; de C2 em diante, +2 na fila de preenchimento. **Não foi editado em
   `docs/voluntarios/lista_postos.md`**: é proposta para o Posto decidir.
3. **Rota interna Anglesea Gate → Ring 3.** A entrada do Ring 3 é pelo canto
   nordeste; quem entra pelo oeste precisa de caminho sinalizado dentro do RDS.
4. **Fila da calçada capada.** A calçada da Merrion Road vira zona de
   espectadores e a Garda não aceitará fila na via. O Ring 3 tem lotação 2.118:
   puxar a fila para dentro, P0 encostado no gradil.
5. **Duas travessias controladas** a pedir à Garda: Merrion Rd × Serpentine Ave
   e Ballsbridge. Sem elas, quem vem de DART fica do lado errado do percurso.
6. **Comunicação:** "venha de DART" e "de carro, só Anglesea Road Gate". A
   campanha "descubra sua seção antes de sair de casa" vale ainda mais.
7. **Entregas antes das 10h**, ou pela Anglesea com margem.

## 4. Efeitos de segunda e terceira ordem

- **Deslocamento da chegada para depois das 16h.** Se a comunicação for "evite
  a maratona", parte do eleitorado chega na última hora, quando o Hall 2 já
  opera no limite. Melhor mensagem: "venha de DART, a qualquer hora".
- **O DART absorve o público da maratona.** Sandymount e Lansdowne Road são
  estações de espectadores; trens cheios entre 10h e 15h. Não há como medir
  daqui; é risco a registrar, não a resolver.
- **Donnybrook como funil.** V1, V2, V3, A3 e T1 passam por um só cruzamento.
  Um acidente ali isola o RDS de veículos. Não há alternativa dentro do plano da
  Garda; V4 é a única válvula, e depende de confirmação.
- **Espectadores no gradil do RDS.** O P0 e a tabela mestra dividem a calçada
  com o público da prova. Risco de o P0 ficar invisível; mitigação é o G1 e a
  campanha prévia.
- **Mesários que moram ao sul da cidade** e chegam às 7h não sentem nada; os
  substitutos chamados durante o dia sentem tudo. Instruir por escrito: "Anglesea
  Road Gate, via N11 ou Donnybrook".
- **Interior do país (4.213 aptos)**: quem vem de Cork, Galway, Limerick chega
  pela M50 → N11 (V1) ou pela M50 → N7/N4 → centro (V2). Nenhuma rota pela
  costa. Se vierem de ônibus fretado, o desembarque é no Anglesea Gate e o
  estacionamento do ônibus é problema do RDS (a confirmar).

## 5. Pedidos a terceiros

| A quem | Pedido | Bloqueia? |
|---|---|---|
| Garda | Travessias controladas 1 (Merrion Rd × Serpentine Ave) e 2 (Ballsbridge), com horário | **Sim**: sem elas, A1 e A2 não funcionam |
| Garda | Hora prevista de reabertura da Merrion Road | Não, mas muda a janela 16h–17h |
| Garda | Saída da Simmonscourt Road para a Merrion outbound (V4) | Não |
| Garda | Ponto de contato no dia (rádio/telefone) | Não |
| RDS | Anglesea Gate aberto e operado 7h–18h30 | **Sim** |
| RDS | Rota interna sinalizável Anglesea Gate → Ring 3 | **Sim** para A3 e T1 |
| RDS | Estacionamento Anglesea/Simmonscourt para mesários; se o RDS recebe operação da maratona no mesmo dia | Não |
| Dublin Bus / TFI | Desvios das linhas 4, 7, 7A e 18 e paradas alternativas em Donnybrook | Não |

## 6. Premissas rotuladas

- Comparecimento e perfil horário de chegada iguais aos do 1º turno.
- Corredores no RDS entre 10h45 e 15h40 (cálculo a partir das ondas de largada;
  não confirmado pela Garda).
- Reabertura entre 15h30 e 16h30 (prática de anos anteriores; não confirmada).
- Coordenadas do mapa com precisão de 30–60 m: servem para o esquema e para
  posicionar as camadas no Google My Maps, não para medir.
- O Google Maps não conhece os fechamentos com antecedência; os links abrem a
  rota que o plano quer, mas o aplicativo pode sugerir outra.

## 7. Como usar o Google Maps

O plano marcado sobre o print de satélite do Google Maps está em
`mapa/acesso_2turno_print.png` (desenho de `scripts/acesso_2turno_print.py`;
posições em pixel lidas à mão sobre esse print, precisão de uns 20 px ≈ 50 m).

1. Abrir <https://www.google.com/maps/d/> e criar um mapa.
2. Importar `mapa/acesso_2turno.kml`. Cada pasta vira uma camada: percurso,
   vias, rotas, pontos.
3. Arrastar os pontos que estiverem fora do lugar.
4. Compartilhar o link público na comunicação com os eleitores.
5. Os links de rota em `saidas/acesso_2turno_links.md` abrem direto no
   aplicativo, com origem, destino e pontos de passagem preenchidos.

---

## Anexo A — texto integral enviado pela polícia

> The participants will enter the Dublin 4 area at Milltown Bridge and will
> proceed along Milltown Road, Clonskeagh Road, Roebuck Road and Fosters Avenue
> before taking a left and travelling along the inbound bus lane on the N11.
> Participants will utilise the UCD Flyover before going along the outbound bus
> lane, heading inbound. Participants will turn right down Nutley Lane and then
> left along the Merrion Road heading inbound to City Centre once more.
> Participants will continue from Merrion Road to Pembroke Road and
> Northumberland Road.
>
> Outbound traffic on Sandford Road from Ranelagh will be directed down Eglinton
> Road and right onto Stillorgan Road. The Stillorgan Road shall remain open to
> all traffic at all times. Donnybrook Road, Morehampton Road and Leeson Street
> Upper will remain open to traffic for the duration of the race and Anglesea
> Road will remain open to R.D.S. Traffic but traffic will not be allowed exit
> Anglesea onto Merrion Road.
>
> Nutley Lane, Merrion Road (inbound), Shelbourne Road, Haddington Road and
> Northumberland Road will be closed from 10:00am. Merrion Road will be open for
> outbound traffic only from Serpentine Avenue. All in bound traffic on the Rock
> Road will be diverted at the Merrion Gates via Strand Road and all North City
> bound traffic will proceed towards Ringsend Road via Irishtown or alternatively
> towards the East Link Bridge via Sean Moore Road.
