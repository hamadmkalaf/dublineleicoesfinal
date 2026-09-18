# Mapas, plantas e artefatos

## O que está versionado aqui

| Arquivo | O que é |
|---|---|
| `voluntarios_postos.html` | Os 17 postos marcados sobre a rota e sobre a planta do salão, com seletor dos quatro cenários de efetivo. Não referencia nenhum arquivo do repositório. Busca as fontes tipográficas no Google Fonts: **sem internet ele abre e funciona, com outra tipografia**. Se for usado no dia, onde pode não haver rede, vale embutir as fontes. |

## O que ainda não está versionado — e devia estar

Os desenhos abaixo sustentam a geometria descrita no `CLAUDE.md` e as posições de
todos os postos, e **não estavam em repositório nenhum** quando os dois temas foram
transferidos. Estão publicados como artefatos, o que **não é versionamento**: o
repositório versiona o arquivo; a publicação é outra coisa, e pode mudar ou sair do
ar sem deixar rastro.

**Guardar o fonte de cada um**, e não só a URL.

| O quê | URL | Destino | Estado |
|---|---|---|---|
| **Rota do Eleitor** | https://claude.ai/artifact/1PQjgzstbiNorfJgagXhB5 | `mapa/rota_do_eleitor.html` | **lido na íntegra.** Define os pontos P0–P7, a tabela mestra seção → porta e o plano de sinalização. É a origem dos códigos de posto. |
| **Prancheta do Hall 2 pelas seções** | https://claude.ai/artifact/Szv5egKpHy3umh4udAybvr | `mapa/prancheta_hall2.html` | **lido na íntegra.** Coordenadas reais das portas e das 28 mesas; a planta do salão no `voluntarios_postos.html` foi gerada delas. |
| **Ring 3** | https://claude.ai/artifact/FcQs4H7fM3RcBxmyFywazV | `mapa/ring3.html` | ⚠ **não foi lido na íntegra.** Conferir contra a §5 de `docs/voluntarios/contexto.md` — e ver `docs/CONFLITO_RING3.md` antes, porque o Ring pode não existir mais. |
| **Sinalização interna** | https://claude.ai/artifact/BcT5yzxRkSaUsbbHQQgjWF | `mapa/sinalizacao_interna.html` | ⚠ **não foi lido na íntegra.** |
| **Sinalização (cores, grupos e peças)** | https://claude.ai/artifact/Ek3FfeYnwvQLZEs4ZJ5Zzr | `mapa/sinalizacao.html` | Fonte das seis cores de rolo e da convenção de rotular por grupo e seção. O tema dos separadores depende dele. |
| **Escala de Voluntários** | https://claude.ai/artifact/YaFNHUua2Hkqu7dtR7tf7A | — | Publicação do `voluntarios_postos.html`, que já está versionado aqui. |
| **Plantas em imagem** do Ring 3 e do Hall 2 | — | `plantas/` | A geometria do `CLAUDE.md` é prosa escrita a partir delas. Sem as imagens, a descrição perde a fonte. |
| **Caderno nominal de seções** (51 seções × nome do eleitor, do Cartório) | — | `data/` | Insumo do posto P0. **Pode não existir** — ver pendência 3 de `docs/voluntarios/contexto.md`. Obtê-la é a melhoria de maior retorno por euro gasto. |

### Por que isto importa

Dos quatro desenhos que sustentam o tema de voluntários, **dois foram lidos na
íntegra** — a Rota do Eleitor e a prancheta do Hall 2. A geometria do Ring 3 e os
pontos de sinalização interna vieram das descrições contidas no artefato da Rota do
Eleitor. **Se os artefatos dedicados divergirem, os postos R2, R4 e R5 são os que se
mexem.**

Há ainda dois achados do tema dos separadores que são **correções ao plano de
sinalização** e precisam ser levados a ele:

1. O x-banner da parede leste está em **x = 45,70** no `sinalizacao_v2.json` e devia
   estar em **42,70** — a 45,70 ele fica atrás das mesas, dentro da faixa protegida
   das saídas de emergência L1–L4.
2. Nos três grupos de alto comparecimento (A3, B2, C5), os **4,60 m** caem dentro do
   serpenteado; nesses três o banner recua para **8,60 m**.

O desenho dos separadores já aplica as duas correções. O plano de sinalização,
ainda não.
