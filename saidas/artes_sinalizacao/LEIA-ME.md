# Artes de sinalização — arquivos para a gráfica

Gerados em 23/09/2026 de `mapa/sinalizacao/` por `node scripts/exporta_artes.mjs` e
`python3 scripts/compacta_artes.py`. PDF vetorial, **tamanho final em mm, sem sangria**,
Montserrat embutida (subconjunto). Nome = posição no plano _ modelo _ largura x altura mm.
Os vinis (`cut-vinyl`) saem **sem o fundo cinza do vidro**: o que está no arquivo é o que se recorta.
Todos os 34 arquivos estão no zip `artes_sinalizacao.zip` desta pasta.

| Arquivo | Qtd | Onde |
|---|---:|---|
| `P0-Consulta_construction-fence_2080x820mm.pdf` | 2 | P0 · descubra sua seção (QR do TSE) · calçada da Merrion Road, uma de cada lado do portão |
| `P0-Mestra_construction-fence_2080x820mm.pdf` | 2 | P0 · tabela mestra seção → porta · calçada, ao lado de cada P0-Consulta |
| `P1-Portao_construction-fence_2080x820mm.pdf` | 1 | P1 · portão de eleitores |
| `P2-ParedeLeste_pvc-banner_2000x1000mm.pdf` | 3 | P2 · lateral leste do Hall 2, nas portas de serviço |
| `P3-EntradaRing_construction-fence_2080x820mm.pdf` | 1 | P3 · entrada do Ring 3, na CCB |
| `P4-ZonaC_construction-fence_2080x820mm.pdf` | 1 | P4 · boca da zona C do Ring 3 |
| `P4-ZonaB_construction-fence_2080x820mm.pdf` | 1 | P4 · boca da zona B do Ring 3 |
| `P4-ZonaA_construction-fence_2080x820mm.pdf` | 1 | P4 · boca da zona A do Ring 3 |
| `P5-VinilA_cut-vinyl_1200x700mm.pdf` | 1 | P5 · letra A no vidro da porta S4 |
| `P5-VinilB_cut-vinyl_1200x700mm.pdf` | 1 | P5 · letra B no vidro da porta S5 |
| `P5-VinilC_cut-vinyl_1200x700mm.pdf` | 1 | P5 · letra C no vidro da porta S6 |
| `P5-Preferencial_construction-fence_2080x820mm.pdf` | 1 | P5 · entrada preferencial, no gradil do apron |
| `P5-VinilPref_cut-vinyl_1200x700mm.pdf` | 1 | P5 · preferencial no vidro da porta S7 |
| `P6-PainelA_roll-up_1000x2000mm.pdf` | 1 | P6 · painel da porta A, atrás da S4 |
| `P6-PainelB_roll-up_1000x2000mm.pdf` | 1 | P6 · painel da porta B, atrás da S5 |
| `P6-PainelC_roll-up_1000x2000mm.pdf` | 1 | P6 · painel da porta C, atrás da S6 |
| `P4-FimAvenidaB_construction-fence_2080x820mm.pdf` | 1 | P4 · fim da avenida B, na boca da pequena avenida da parede norte |
| `P6-BlocoA1_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo A1, na boca do corredor do par |
| `P6-BlocoA2_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo A2, na boca do corredor do par |
| `P6-BlocoA3_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo A3, na boca do corredor do par |
| `P6-BlocoA4_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo A4, na boca do corredor do par |
| `P6-BlocoA5_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo A5, na boca do corredor do par |
| `P6-BlocoB1_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo B1, na boca do corredor do par |
| `P6-BlocoB2_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo B2, na boca do corredor do par |
| `P6-BlocoB3_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo B3, na boca do corredor do par |
| `P6-BlocoB4_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo B4, na boca do corredor do par |
| `P6-BlocoB5_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo B5, na boca do corredor do par |
| `P6-BlocoC1_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo C1, na boca do corredor do par |
| `P6-BlocoC2_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo C2, na boca do corredor do par |
| `P6-BlocoC3_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo C3, na boca do corredor do par |
| `P6-BlocoC4_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo C4, na boca do corredor do par |
| `P6-BlocoC5_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo C5, na boca do corredor do par |
| `P6-BlocoC6_roll-up_850x2000mm.pdf` | 1 | P6 · placa do grupo C6, na boca do corredor do par |
| `P7-Saida_correx-sign-A2_594x420mm.pdf` | 2 | P7 · saídas S2 e S8 |

Total: 34 arquivos, 39 peças impressas.

Antes de subir na gráfica: confirmar se ela pede sangria (aqui é zero; as bordas são campo
de cor e podem ser estendidas) e, para o vinil recortado, se quer o texto em curvas (a
fonte vai embutida; o Illustrator converte com *Criar contornos*).
