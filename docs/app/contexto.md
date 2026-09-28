# App "Onde eu voto?" — contexto e decisões

Consulta de seção com rota até a mesa, para o eleitor (antes de sair de casa) e para a
equipe do P0 e das mesas (no dia, sem internet). Iniciado em 28/09/2026 na branch
`appeleicoes`; código em `app/`, scripts em `scripts/app_*.py`.

## 1. Por que existe

O P0 (calçada da Merrion Road) é o posto crítico da rota: quem chega sem o número da
seção não pode ser triado depois do portão, e três operadores atendem da ordem de
1.200 consultas no dia (premissa de ~90 s por atendimento; `docs/voluntarios/contexto.md`
§4). Cada consulta feita em casa pelo app é uma a menos na calçada. A peça P0-Consulta
já prevê um QR ("NÃO SABE SUA SEÇÃO? CONSULTE AQUI"); hoje aponta só para o e-Título,
que dá a seção mas não a fila, a porta nem a parede.

## 2. Decisões (28/09/2026)

| Decisão | Escolha | Por quê |
|---|---|---|
| Repositório | `dublineleicoesfinal`, branch `appeleicoes` com merge de volta | é onde vivem `decisoes.json` e `grupos_mesas.json`, que o app lê |
| Identificação do eleitor | **nome + data de nascimento** | só o nome não resolve homônimos (5 em 8.144 na lista de Berlim de 2022; ~10 esperados em 16.794) e deixa qualquer pessoa confirmar quem vota em Dublin |
| Hospedagem | **só GitHub Pages, sem servidor** | zero infraestrutura no dia; 50 consultas/s é trivial para CDN + cache no aparelho |
| Versão da equipe | **obrigatoriamente offline** | cobertura de dados na calçada não testada |
| Formato mobile | PWA instalável (site), não app de loja | prazo de 6 dias; funciona em Android e iPhone sem publicação em loja |

## 3. Como funciona

```
lista oficial (.xlsx / .csv / .pdf com texto)
   │  scripts/app_importar_eleitores.py   (confere contagem por seção contra saidas/dados.json)
   ▼
data/eleitores/eleitores.csv          ← dado pessoal; fica fora do git
   │  scripts/app_construir.py  +  data/decisoes.json  +  data/grupos_mesas.json
   ▼
app/dist/                             ← o que se publica
   dados/rotas.json           51 seções → mesa, letra, porta, parede, grupo, passos (público, sem dado pessoal)
   dados/indice_publico.json  hash(nome normalizado | nascimento) → seção        (eleitor)
   dados/equipe.enc           lista completa cifrada, AES-256-GCM               (equipe)
   dados/versao.json          carimbo da construção; muda o cache do service worker
```

**Eleitor.** O navegador normaliza o nome (maiúsculas, sem acento, sem apóstrofo, sem
DE/DA/DO/DOS/DAS/E), calcula PBKDF2-SHA256 de `NOME|AAAA-MM-DD` (50.000 iterações, sal
público) e procura o hash no índice. Cada eleitor está indexado duas vezes: pelo nome
completo e por "primeiro + último sobrenome", para tolerar quem omite nomes do meio.
Resultado: cartão com letra, porta e parede; seção e grupo de mesas; os seis passos no
vocabulário das peças P1–P7; mini-mapa esquemático; nota da preferencial S7.

**Equipe.** A página `equipe/` baixa o pacote cifrado e pede a senha do dia. A chave
sai de PBKDF2 (600.000 iterações) e o AES-GCM rejeita senha errada. Aberta, a lista fica
só em memória: busca por qualquer parte do nome, mostra homônimos com nascimento,
**título** e seção, e a mesma rota. "Fechar a lista" descarrega. O service worker guarda
tudo no aparelho na primeira visita; depois funciona sem rede.

**Data de nascimento.** Campo de texto `DD/MM/AAAA` com máscara, nas duas páginas:
obrigatório no eleitor; opcional na equipe, onde filtra a lista e separa homônimos
sem olhar a data de cada candidato. Aceita colar `23101967` ou `23.10.1967`.

**Paleta.** Identidade Eleições 2026 do TSE (`Identidadevisual/`): fundo amarelo
`#FCC537`, texto e botão em navy `#042B5A`, azul `#478BAD`/`#6486A7` em rótulos,
laranja `#EF9A3E` em erros, verde `#98BD31`/`#557372` em notas e na faixa da equipe.
As cores das portas A/B/C são as v2 das peças (`comum.js`, `COR_LETRA`) e não mudam.
Sem versão em inglês (decisão de 28/09).

**Rótulos.** Por grupo de mesas (A1…C6) e por seção, nunca por número de mesa: regra do
plano de sinalização. As letras A/B/C e as cores são as v2 das peças (A `#33507E`,
B `#E8C63A`, C `#DE7343`).

## 4. Formato da lista nominal (o que pedir ao Cartório)

Uma linha por eleitor, com inscrição, nome, data de nascimento e seção. O importador
aceita `.xlsx`, `.csv` (TSE, latin-1 ou UTF-8) e `.pdf` com texto; reconhece as colunas
pelo nome (`NUM_INSCRICAO`/`Título`, `NOM_ELEITOR`/`Nome`, `DAT_NASC`/`Data de
nascimento`, `NUM_SECAO`/`Seção`, `NOM_MAE`, `NUM_LOCAL`), como na lista de Berlim de 2022.

- Sem data de nascimento na lista, o build troca o segundo fator para o **nome da mãe**
  e o app troca o rótulo do campo. Sem nenhum dos dois, o build para.
- PDF escaneado (imagem) não serve: pedir de novo em planilha. OCR está fora do escopo.
- A seção da lista é a **original**; a agregação vem de `decisoes.json`.
- O importador compara a contagem por seção com `saidas/dados.json` e marca desvio > 2%.

## 5. Publicar

1. `python3 scripts/app_construir.py --lista data/eleitores/eleitores.csv --grava --senha-equipe "..."`.
   Sem `--senha-equipe` o script sorteia uma frase de seis palavras e a imprime uma vez.
2. Publicar **só `app/dist/`** no GitHub Pages: branch `gh-pages` deste repositório, ou
   um repositório público só com essa pasta se o plano da conta não permitir Pages em
   repositório privado. `app/dist/` não contém dado pessoal legível.
3. Distribuir a senha da equipe no briefing, fora de e-mail em massa. Trocar a senha =
   reconstruir e republicar; o service worker baixa o pacote novo pela mudança em
   `versao.json` (o build grava o carimbo em `sw.js`).
4. Pôr o link/QR na peça P0-Consulta e na campanha "descubra sua seção antes de sair de casa".
5. 2º turno (25/10): trocar `app/public/dados/config.json` e reconstruir.

## 6. Modelo de ameaça, em uma tabela

| Quem | Consegue | Não consegue |
|---|---|---|
| Qualquer pessoa com o link | consultar um eleitor de quem sabe nome completo e data de nascimento | listar eleitores; saber se "Fulano" vota em Dublin sem a data; obter título |
| Quem baixa `indice_publico.json` | tentar nome×data contra os hashes, a ~10 ms por tentativa (PBKDF2 50k) | recuperar nomes em massa: 17 mil chaves × espaço de nomes × 25 mil datas |
| Quem baixa `equipe.enc` sem a senha | nada útil | decifrar (AES-256-GCM, chave de PBKDF2 600k sobre frase de seis palavras) |
| Quem tem a senha | tudo que a equipe vê: nome, nascimento, título, seção | — (por isso a senha é do dia e se troca reconstruindo) |
| Quem acha um celular da equipe | o pacote cifrado no cache | a lista, sem a senha; a página descarrega a lista ao fechar |

Limites conhecidos: nome de casada, abreviações e apelidos não encontram (o app sempre
mostra o caminho de volta ao e-Título e ao P0); homônimo com a mesma data e seções
diferentes manda ao P0; alguém que já conheça nome e data de uma pessoa descobre a seção
dela, o que o e-Título já permite hoje.

## 7. Testes

- `python3 -m pytest -q app/testes`: normalização, vetores Python × JS iguais, build
  confere a amostra e rejeita seção estranha, rotas batem com `decisoes.json`.
- `app/testes/ponta_a_ponta.mjs` (Chromium): eleitor com apóstrofo, nome curto, não
  encontrado, homônimo, equipe com senha errada e certa, e as duas páginas **offline**.
- Importador validado localmente sobre a lista de Berlim (8.144 linhas de `Berlim`
  reconhecidas; nada gravado). O leitor de PDF só foi exercitado no código: não havia
  PDF de lista nominal para testar.

## 8. Pendências

- Chegada da lista (formato acima) e quem a recebe.
- GitHub Pages: plano da conta × repositório privado.
- Quem constrói e publica na véspera; quem guarda a senha da equipe.
- Teste da página da equipe sem sinal, na calçada, na véspera.
- Dispositivo dedicado no P0 (tablet) ou celulares dos voluntários?
