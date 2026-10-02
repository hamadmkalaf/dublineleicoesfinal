# Decisões 21026_final — consolidado de 02/10/2026

`21026` é a data (2/10/26). Este branch junta **num lugar só** tudo o que foi
registrado depois de 24/09 nos dois repositórios e refaz, a partir disso, quatro
artefatos: **prancheta do Hall 2**, **montagem do Ring 3**, **plano de sinalização** e
**imagem do layout final**. Base: a rodada `23926v2`, a última consolidada.

## 1. Critério de corte

- **Entrou:** o que foi registrado **depois de 24/09**. A hora dos commits é UTC;
  Dublin está em UTC+1 (IST) em setembro. O roll-up da P4 (`a0a29b3`) tem carimbo
  24/09 23:26 UTC, que é **25/09 00:26 em Dublin** — entrou.
- **Já estava na base:** as duas decisões de 24/09 de seguir sem aguardar o RDS
  (`d2be0e6`, 24/09 13:34 UTC). São do próprio dia 24, mas já faziam parte da
  `23926v2`; os artefatos de 23/09 ainda as tratavam como pendência, então esta
  rodada as leva até eles.
- **Não é decisão:** cotações recebidas (são insumo) e passagens de sessão do app.
  Ficam registradas, mas não mudam desenho.

## 2. O que foi registrado depois de 24/09, e onde caiu

| Data | Registro | Origem | Prancheta | Ring 3 | Plano de sinalização | Layout final |
|---|---|---|---|---|---|---|
| 24/09 (25/09 em Dublin) | **P4-FimAvenidaB vira roll-up 1000 × 2000 mm** — a boca da pequena avenida não tem gradil, só unifila, que não aguenta o banner | `claude/sleepy-volta-4glyc7` | — | — | **aplicada**: ficha, medida, fixação; orçamento 11 fence banners + 4 pull-ups largos, 41 itens, € 1.232,72 sem IVA | não desenhada (ver §4) |
| 24/09 | Seguir sem o RDS: fita no piso do Hall 2 e os 4 painéis do gradil norte do Ring 3 | já na base | — | **aplicada**: aberturas viram decisão com risco assumido | **aplicada** na lista de pendências | — |
| 24–25/09 | Cotações: carrinho Helloprint de 24/09 (€ 2.694,68 sem IVA) substitui a referência de 18/09; Snap Leeson revista em 25/09 (€ 4.145,00 sem IVA, Basic) | `23926v2` (xlsx) | — | — | **registradas** nas pendências; **nenhum fornecedor escolhido** | — |
| 25/09 | Briefings: celulares e equipamentos, justificativa | `claude/laughing-brown-wmai9a` | — | — | — | — |
| 29/09 | Arquivo de impressão da P4 em roll-up: PDF vetorial com Montserrat TrueType, JPG 8000 × 16000 px | `eleicoes2026` · `claude/avenida-b-resolution-margins-2ozmlk` | — | — | **aplicada**: copiado em `Artes/impressao/` e citado na ficha | — |
| 30/09 | **Módulo da MRV, da parede para dentro:** mesa redonda com a urna (0,90) · vaga do eleitor de costas para a parede (0,90) · mesa-cavalete dos mesários 1,70 × 0,80 · passagem (0,60) = 4,10 m | `claude/happy-franklin-zys8pj` | **aplicada** | — | — | **aplicada** (urna junto à parede) |
| 30/09 | **Ponto de informação**: mesa-cavalete 1,70 × 0,80 m ao lado do recuo do R1 (x 11,55–13,25 · y 1,70–2,50 m) | idem | **aplicada** | — | — | **aplicada** |
| 30/09 | Sem setas nas avenidas — na planta detalhada para o eleitor | idem | — | — | — | **não aplicada** (ver §4) |
| 30/09 | Peças 9:16 de divulgação e a planta do Hall 2 em versão de sinalização | `claude/busy-archimedes-q689b1` | — | — | — | — |
| 01/10 | Mapa do Hall 2 em alta resolução (mesas desenhadas ampliadas, só apresentação) | `claude/gifted-maxwell-97iv30` | — | — | — | — |
| 01–02/10 | App "Onde eu voto?" v1→v3: consulta só por nome, título parcial, status de fila com 706 por zona, textos na direção do eleitor, sem número de porta S… ao eleitor | `appeleicoesv3` | — | nota no rodapé | — | — |

As regras do app de 01/10 dizem expressamente que **as peças de sinalização em `mapa/`
mantêm o vocabulário técnico** — por isso "sem pontos cardeais" e "sem S4/S5/S6" não
foram levados às quatro peças.

## 2a. Decisões de 24 e 25/09 que só existiam no artefato publicado

Achado na republicação de 02/10: o **plano de sinalização** publicado
(versão 1790325876-6caa, 25/09 08:44 UTC) tinha sido revisto **fora do repositório**,
e o repositório ficou na versão de 23/09 (v2). Republicar a cópia do repositório
apagaria estas decisões; elas foram trazidas para cá e a versão nova foi montada
sobre a de 25/09:

| Data | Decisão (texto da própria página) |
|---|---|
| 24/09 | **P1-Portão sai do plano** — sem ponto de fixação nas grades do portão. A tabela seção → porta passa a ter três pontos e seis cópias (P0 ×2, P2 ×3, P3 ×1). |
| 24/09 | **Os quatro vinis de porta (A, B, C, preferencial) viram window stickers 900 × 900 mm** — mudança do Posto. Preço ainda não cotado no Helloprint; a proposta Snap de 25/09 dá € 70 por adesivo laminado 900 × 900. |
| 24/09 | A peça do fim da avenida B vira roll-up e é **renomeada P6-Painel_FimAvenidaB** (a mesma decisão do branch `claude/sleepy-volta-4glyc7`). |
| 24/09 | P7-Saída: **medir o vão livre acima do batente** antes de fixar (foto de 24/09). |
| 25/09 | **O fence banner P5-Preferencial do apron sai do plano**: o adesivo de vidro da S7 passa a ser a única peça preferencial, com a **foto real do arquivo** entregue (2000 × 2000 px), em `mapa/assets/p5-preferencial.jpg`. |
| 25/09 | Fence banners de 12 para **8**; plano com **17 peças externas**, **38 itens**, **€ 1.138,20 sem IVA** (com o window sticker a preço de vinil, marcado com *). |
| 25/09 | Pendência nova: **exportar as artes que faltam**, P2-ParedeLeste (3 cópias) e P3-EntradaRing3 (1 cópia). |

`scripts/plano_consolidado.py` passou a reconhecer a página de 25/09 (`MARCA_25_09`):
as legendas das fichas seguem os nomes novos, as revisões de 22 a 24/09 não rodam sobre ela
(a página já as traz, com texto próprio) e `numeros()` não sobrescreve o orçamento escrito à
mão. As peças `P1-Portao.dc.html`, `P5-Preferencial.dc.html` e `P5-VinilPref.dc.html` continuam
em `mapa/sinalizacao/`, mas não estão mais no plano.

A prancheta e o Ring 3 publicados batiam com o repositório (o Ring 3 publicado só trazia
"24/09" onde o repositório já dizia "23/09 (v2)").

## 3. Os quatro artefatos

| Artefato | Arquivo | Gerador | O que mudou |
|---|---|---|---|
| Prancheta do Hall 2 | `mapa/prancheta_hall2.html` (= `saidas/prancheta_por_secao.html`) | `scripts/gera_prancheta_por_secao.py` | Cada MRV desenhada com as quatro partes de 30/09, rótulo sobre a mesa-cavalete; ponto de informação; **alta carga em roxo** e **entradas nas cores de rolo** (azul A, amarelo B, vermelho C), que a prancheta ainda não seguia desde 22/09; texto "Ring 3 abandonado", superado em 18/09, corrigido. Nenhuma mesa se moveu. |
| Montagem do Ring 3 | `mapa/ring3_montagem.html` | `scripts/ring3_montagem.py` + `gera_pagina_ring3.py` em `eleicoes2026`, branch `21026_final` | Aberturas da face norte: de "confirmar com o RDS" para **decisão de 24/09, risco assumido**. 202 CCBs, 2 a contratar, 558,0 m de fita, lotação 2.105 — sem mudança. |
| Plano de sinalização | `mapa/plano_sinalizacao.html` | `scripts/plano_consolidado.py` (`revisao_24_09_rollup`, `revisao_02_10`) | P4 em roll-up; arquivo de impressão; pendências do RDS; cotações; prazo da gráfica reescrito (as datas de 18/09 passaram). |
| Layout final | `saidas/separadores_definitivo.svg` / `.png` | `scripts/separadores_fila.py --grava` + `scripts/svg_para_png.js` (escala 3) | Urna junto à parede em cada módulo; ponto de informação; carimbo da versão. **O PNG de 23/09 estava cortado embaixo** (portas S2–S8 e rodapé fora): este sai inteiro. Barreira, fita e contas (96 unifilas, 802 m, 11 rolos) não mudam. |

Fonte única das constantes de 30/09: `U_URNA` e `PONTO_INFO` em
`scripts/separadores_fila.py`; `planta_hall2_detalhada.py` e a prancheta leem dali.

**Republicados em 02/10, nas mesmas URLs:** prancheta (versão 7), Ring 3 (versão 5)
e plano de sinalização (versão 17, sobre a de 25/09 — ver §2a). O layout final não tem
artefato publicado. `mapa/artefatos.json` traz as versões e o sha256 das cópias.

## 4. O que não foi aplicado, e por quê

1. **"Sem setas nas avenidas"** (30/09) foi feito na planta detalhada voltada ao
   eleitor. O layout final é peça de montagem para a equipe, e as setas dizem o
   sentido do fluxo a quem cola a fita. Manter foi escolha desta rodada; se o Posto
   quiser a regra também aqui, são três linhas em `svg_plano()`.
2. **A posição da P4 em roll-up no chão** não foi desenhada no layout. A peça é
   autoportante "na boca da pequena avenida", mas nenhum registro diz em que ponto
   exato da faixa de 1,80 × 25,50 m ela fica; posto no eixo da avenida B, o cassete
   de 1,0 m bloquearia um terço da boca de 3,0 m. **A decidir no local.**
3. **Fornecedor da gráfica.** Há duas cotações e nenhuma escolha registrada.

## 5. Achados desta rodada

- **O ponto de informação fica no caminho da saída S2.** No layout, a mesa-cavalete
  (x 11,55–13,25, y 1,70–2,50) encosta no vão da S2 (x 13,25–14,45), para onde converge
  o fluxo de quem já votou na parede oeste e na metade oeste da norte. Quem para para
  perguntar fica no fluxo de saída. Não movi: é decisão de 30/09; vale conferir no local.
- **A conferência do app quebrava neste branch.** `app_construir.py` lia a P0-Mestra
  no formato anterior a 21/09 (uma letra por linha); com a tabela agrupada por porta
  da `23926v2` ele reprovava as 51 seções. Corrigido para ler os dois formatos.
- **706 por zona (app) contra 2.105 no total (folha do Ring 3):** a raia de cima da B
  perde 13 lugares. Diferença abaixo de 1%; registrada no rodapé da folha.
- O texto "As dezesseis placas de grupo. ao contrário. já estavam…" no orçamento do
  plano já vinha assim da `23926v2` (pontuação perdida por uma revisão antiga); não foi
  tocado para não quebrar a idempotência das revisões anteriores.

## 6. Como conferir

```bash
for s in confere_arranjo grupos_mesas artes_sinalizacao tabela_mestra paleta \
         separadores_fila plano_consolidado mapa_publico planta_hall2_detalhada \
         mapa_hall_alta zonas_balanceadas app_construir; do python3 scripts/$s.py; done
python3 scripts/gera_prancheta_por_secao.py && cp saidas/prancheta_por_secao.html mapa/prancheta_hall2.html
```

Todos saem com código 0 neste branch. Em `hamadmkalaf/eleicoes2026`, branch
`21026_final`: `python3 scripts/ring3_montagem.py && python3 scripts/gera_pagina_ring3.py`.
