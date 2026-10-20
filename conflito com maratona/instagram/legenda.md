# Carrossel "Eleição e maratona no mesmo dia" — legenda e fontes

Seis cards de 1080 × 1350 (`card1.png` a `card6.png`), gerados de `cards.html` com
`node scripts/instagram_cards_render.js`. Identidade das peças de `mapa/sinalizacao/`
(Archivo + Nunito Sans, amarelo e ardósia do TSE, `#VOTONADEMOCRACIA`).

## Legenda sugerida

> No domingo, 25 de outubro, o 2º turno das Eleições 2026 acontece no RDS, em Ballsbridge, das 8h às 17h, no mesmo dia da Maratona de Dublin. Vias serão fechadas e várias linhas de ônibus terão o trajeto alterado.
>
> As orientações abaixo foram obtidas pela Embaixada junto à Garda e à Dublin Bus:
>
> A Merrion Road fica aberta só até as 9h30. Se puder, vote pela manhã. Depois desse horário, chegue pela Donnybrook Road e entre pelo portão da Anglesea Road.
>
> De carro, a Garda orienta: N11 (Stillorgan Road) → Donnybrook Road → Anglesea Road. Quem vem do norte deve seguir pela Strand Road até Booterstown e retornar pela N11 no sentido centro. Não será possível sair da Anglesea Road para a Merrion Road.
>
> De ônibus, segundo a Dublin Bus: as linhas 4, 7 e 7A não passarão pela Merrion Road. Até as 11h, Donnybrook é servida só por ônibus vindos do sul (E1 e 14). A partir das 11h, voltam ao trajeto completo as linhas E1, E2, 11, 11B, 14 e 39A. Desça nas paradas 774, 758 ou 759 e siga a pé até o portão da Anglesea Road (cerca de 11 a 13 minutos). Não haverá DART ao sul de Grand Canal Dock.
>
> As informações estão sujeitas a alteração no dia.
>
> #VotoNaDemocracia #Eleições2026

## De onde vem cada informação

| Card | Afirmação | Fonte |
|---|---|---|
| 2 | Merrion Road aberta até 9h30 | Garda, como relatada no e-mail da Embaixada à Dublin Bus de 16/10. **Ver ressalva 1.** |
| 2, 3 | Depois, entrada pelo portão da Anglesea Road, via Donnybrook | Garda, 25/9 (`RE_ (External)Re_ .eml`); plano informado à Dublin Bus em 16/10. **Ver ressalva 2.** |
| 3 | N11 → Donnybrook Road → Anglesea Road; N11, Donnybrook e Anglesea abertas | Garda, 18/9 (`File.eml`) e 25/9 |
| 3 | Do norte: Strand Road → Booterstown → N11 sentido centro | Garda, 25/9 |
| 3 | Não se sai da Anglesea para a Merrion Road | Garda, 18/9 |
| 3 | Estacionamento: Simmonscourt, Anglesea, Clyde, Elgin Road | Garda, 25/9 |
| 4 | 4, 7 e 7A desviadas pela Strand Road desde 8h | Dublin Bus, documento de desvios e mapas anexos ao e-mail de 16/10 (`emails_dublinbus_16a19-10/`) |
| 4 | Sem DART ao sul de Grand Canal Dock, 24–26/10 | Irish Rail, 28/9 (`divergencias_garda_dublinbus.md` 4.1) |
| 5 | Até 11h, Donnybrook só com ônibus do sul; E1 termina em Sussex Road | Dublin Bus, e-mails de 16/10 e 19/10 |
| 5 | 14 até 11h: Dundrum ↔ Adelaide Road pela Donnybrook Road, com parada em Donnybrook | Dublin Bus, mapa "Route 14 Diversion 25th Oct"; paradas confirmadas (decisão de 20/10) |
| 6 | A partir das 11h, trajeto completo norte–sul; ônibus passam por Leeson e Hatch Street | Dublin Bus, e-mails de 19/10 |
| 6 | 39A termina na 771; 11 e 11B pela Donnybrook a partir das 11h | Dublin Bus, documento de desvios |
| 5, 6 | Paradas 774, 758, 759 | Prefeitura repassando a Dublin Bus, 7/10 |
| 6 | 11–13 min a pé até o portão | Medição OSRM (`ranking_linhas_rds.md` §2); premissa de 4,8 km/h |

## Decisões de 20/10/2026

As quatro ressalvas da primeira versão foram resolvidas assim:

1. **"Vote pela manhã" × ônibus:** manter a distinção. A manhã é recomendada para quem vai de
   carro ou a pé; quem depende de ônibus vindo do norte, do centro ou do oeste é orientado para
   depois das 11h (cards 2 e 5).
2. **Horário da Merrion Road:** fica **9h30**, como informado pela Garda. O 9h25 do organizador e
   o 10h do e-mail da Garda de 18/9 não entram nos cards.
3. **Portão:** o **RDS confirmou o portão da Anglesea Road.**
4. **Linhas 14 e 44:** a **14 está confirmada** em Donnybrook; a **44 foi retirada** dos cards e
   da legenda.
