# As pranchas da proposta de sinalização

Geram o canvas de design publicado em
<https://claude.ai/artifact/Ek3FfeYnwvQLZEs4ZJ5Zzr> — 21 pranchas: o sistema
visual, as duas plantas de posicionamento e cada peça de sinalização em escala.

```bash
python3 scripts/pranchas/gera_pranchas.py    # peças externas (P0, P1, P2, P3, P4, P5) e a saída
python3 scripts/pranchas/gera_internas.py    # peças internas (P6) e as duas plantas
python3 scripts/pranchas/gera_main.py        # a prancha do sistema e o índice do canvas
```

Saída: `saidas/pranchas_sinalizacao/project/`, um `.dc.html` por prancha mais
`canvas.json`. Só biblioteca padrão.

**Escala: 1 px = 2 mm.** Um banner de 2,0 × 1,0 m sai 1000 × 500 px e uma letra
de 400 mm sai 200 px — o que se vê na tela é a proporção da peça impressa.

## De onde sai cada número

| O quê | Fonte |
|---|---|
| as 51 seções e a porta de cada uma | `saidas/sinalizacao_v2.json`, `mestra` |
| as seções de cada zona e de cada grupo de mesas | idem, `portas[].blocos` |
| a posição de cada x-banner no salão | idem, `pos_banner` |
| largura, boca e lotação de cada zona do Ring 3 | `saidas/ring3_montagem.json` |
| a geometria do salão | `data/prancheta_hall2.json` |
| a paleta e as regras | `docs/identidade_visual.md` |

Nenhuma seção é digitada nestes scripts: mudar o arranjo e rodar de novo
reescreve todas as listas. Se `ring3_montagem.json` não existir, rode antes
`python3 scripts/ring3_montagem.py`.

## O que estas pranchas não são

Não são arte final. O logotipo desenhado nelas é **marcação de lugar** — mostra
onde a arte oficial entra e quanto espaço ocupa. Antes da gráfica: vetor do
TSE, a fonte da campanha e a autorização de uso da marca
(`docs/identidade_visual.md` §4).
