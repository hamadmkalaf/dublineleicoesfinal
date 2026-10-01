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

## 2. Decisões

### 2a. Replanejamento de 01/10/2026 — a lista real não tem data de nascimento

A relação do TRE-DF chegou em 29/09 (PDF, 470 páginas) com **seção, inscrição, nome e as
marcas de 1º e 2º turno**, e nada mais. O desenho de 28/09 (nome + nascimento) não construía.

| Decisão | Escolha | Por quê |
|---|---|---|
| Identificação do eleitor | **só o nome**; em homônimo, o app **avisa e pede o título** (12 dígitos) | decisão do usuário, 01/10; é o único dado além do nome que a lista traz |
| Homônimo na equipe | lista os dois (ou três) lado a lado, **cada um com o seu título** | a equipe pede o título ao eleitor e toca no nome certo |
| Chave curta "primeiro + último" | mantida; quando ambígua (1.279 chaves em 30.092) cai no mesmo fluxo do título | quem omite nomes do meio ainda encontra |
| Seção na lista | a lista vem **por mesa**: 28 seções principais, agregadas já somadas | a rota é a da mesa; o cartão mostra as seções da mesa e do grupo |
| Marcas de turno | guardadas (`TURNO1`, `TURNO2`); eleitor marcado diferente de "OK" no turno em construção recebe aviso e a equipe vê a marca em destaque | 74 eleitores não são "OK" no 1º turno (60 VT/VT + 14 VT/OK). **Premissa:** VT = voto em trânsito; confirmar com o Cartório |
| Leitura do PDF | `pdftotext -layout` (poppler-utils) + leitor de blocos; nomes longos quebram em duas linhas | `pdfplumber` não estava disponível; o layout do TRE é estável |
| Números de porta | nunca aparecem ao eleitor (S4, S7… confundem): só "porta A/B/C"; grupos de mesas A1…C6 ficam. Os seis passos têm texto ditado pelo usuário e são marcados no mini-mapa, com a linha tracejada de chegada ao lado do Hall 2 | pedido do usuário, 01/10 |
| Textos ao eleitor | na direção em que ele caminha: esquerda/direita do eleitor, sem leste/oeste, sem "apron", "boca" e "cabeça" ("pátio", "entrada da zona", "frente da fila"); parede da esquerda / do fundo / da direita | pedido do usuário, 01/10; os dados (`parede: oeste`) e as peças de sinalização mantêm o vocabulário técnico |

Medido na lista real: 16.794 eleitores, 0 inscrições repetidas, 24 nomes completos repetidos
(49 pessoas, nunca na mesma seção), contagem por mesa idêntica a `decisoes.json` nas 28 mesas.

**O que muda no modelo de ameaça.** Quem tem o link e sabe um nome completo descobre que a
pessoa vota em Dublin e em que seção (o e-Título já permite isso com nome + nascimento + nome
da mãe, que são dados mais fáceis de achar do que parece). O custo de PBKDF2 (50 mil
iterações, ~30 ms por tentativa) continua tornando a enumeração em massa impraticável; o
**título nunca aparece em claro** no índice público, só dentro do hash de desempate.

### 2b. Decisões de 28/09/2026 (mantidas, exceto a identificação)

| Decisão | Escolha | Por quê |
|---|---|---|
| Repositório | `dublineleicoesfinal`, branch `appeleicoes` com merge de volta | é onde vivem `decisoes.json` e `grupos_mesas.json`, que o app lê |
| Identificação do eleitor | ~~nome + data de nascimento~~ → **só nome, título desempata** (2a) | a lista real não tem nascimento |
| Hospedagem | **só GitHub Pages, sem servidor** | zero infraestrutura no dia; 50 consultas/s é trivial para CDN + cache no aparelho |
| Versão da equipe | **obrigatoriamente offline** | cobertura de dados na calçada não testada |
| Formato mobile | PWA instalável (site), não app de loja | prazo de 6 dias; funciona em Android e iPhone sem publicação em loja |

## 3. Como funciona

```
lista oficial (PDF do TRE com texto; .xlsx / .csv também servem)
   │  scripts/app_importar_eleitores.py   (pdftotext -layout; confere contagem por mesa contra data/decisoes.json)
   ▼
data/eleitores/eleitores.csv          ← dado pessoal; fica fora do git
   │  scripts/app_construir.py  +  data/decisoes.json  +  data/grupos_mesas.json  +  config.json (turno_n)
   ▼
app/dist/                             ← o que se publica
   dados/rotas.json           51 seções → mesa, letra, porta, parede, grupo, passos (público, sem dado pessoal)
   dados/indice_publico.json  v2: hash(nome) → [seção(, marca)] · "H" se homônimo · hash(nome|título) → [seção]
   dados/equipe.enc           lista completa (nome, título, seção, marcas) cifrada, AES-256-GCM   (equipe)
   dados/versao.json          carimbo da construção; muda o cache do service worker
```

**Eleitor.** O navegador normaliza o nome (maiúsculas, sem acento, sem apóstrofo, sem
DE/DA/DO/DOS/DAS/E), calcula PBKDF2-SHA256 do nome (50.000 iterações, sal público) e procura o
hash no índice. Cada eleitor está indexado pelo nome completo e por "primeiro + último
sobrenome", para tolerar quem omite nomes do meio; o app tenta a chave completa e depois a
curta. Se o hash aponta `"H"`, há homônimos: a página avisa, abre o campo do **título** (12
dígitos, com máscara) e consulta `hash(NOME|TITULO)`. Título errado → mensagem com caminho
para o e-Título e o P0. Resultado: cartão com letra, porta e parede; seção e grupo de mesas;
os seis passos do caminho (portão → Ring 3 → pátio → parede → mesa → saída), com os
textos ditados em 01/10, só "porta A/B/C" e esquerda/direita na direção em que o eleitor
caminha; mini-mapa esquemático com a linha tracejada de chegada e os seis passos numerados;
nota da preferencial (a porta à direita da porta C). Se a lista marca o eleitor diferente de "OK" no turno em construção (ex.: VT), um aviso
laranja aparece acima do cartão, e o cartão aparece mesmo assim.

**Equipe.** A página `equipe/` baixa o pacote cifrado e pede a senha do dia. A chave
sai de PBKDF2 (600.000 iterações) e o AES-GCM rejeita senha errada. Aberta, a lista fica
só em memória: busca por qualquer parte do nome; homônimos saem lado a lado, cada um com
**título**, seção e marca de turno (badge laranja quando não é OK); tocar num nome abre a
rota dele. "Fechar a lista" descarrega. O service worker guarda tudo no aparelho na primeira
visita; depois funciona sem rede.

**Título de eleitor.** Só aparece no eleitor quando há homônimo; nunca é guardado nem enviado
(a consulta é local, no aparelho). Na equipe é o dado que separa homônimos, no lugar da data.

**Paleta.** Identidade Eleições 2026 do TSE (`Identidadevisual/`): fundo amarelo
`#FCC537`, texto e botão em navy `#042B5A`, azul `#478BAD`/`#6486A7` em rótulos,
laranja `#EF9A3E` em erros, verde `#98BD31`/`#557372` em notas e na faixa da equipe.
As cores das portas A/B/C são as v2 das peças (`comum.js`, `COR_LETRA`) e não mudam.
Sem versão em inglês (decisão de 28/09).

**Rótulos.** Por grupo de mesas (A1…C6) e por seção, nunca por número de mesa: regra do
plano de sinalização. As letras A/B/C e as cores são as v2 das peças (A `#33507E`,
B `#E8C63A`, C `#DE7343`).

## 4. Formato da lista nominal (a que chegou em 29/09/2026)

"Relação de eleitores por local de votação", TRE-DF, Eleições 2026 – Exterior, PDF com
texto (ReportLab), 470 páginas. Colunas: `SEÇÃO · INSCRIÇÃO · NOME DO ELEITOR · 1º TURNO ·
2º TURNO`. Um registro por bloco separado por linha em branco; nomes longos quebram em duas
linhas (a primeira parte **antes** e a segunda **depois** da linha do registro). Cabeçalho e
rodapé de página repetem a cada ~36 registros.

- O importador lê com `pdftotext -layout` (poppler-utils) e junta as linhas quebradas.
  Planilhas `.xlsx`/`.csv` continuam aceitas, reconhecidas pelo nome das colunas.
- A seção é a **da mesa** (principal): as 23 agregadas já vêm somadas. A conferência é por
  mesa contra `data/decisoes.json` e sai com código 1 se qualquer mesa diferir.
- Saída canônica: `NUM_INSCRICAO;NOM_ELEITOR;DAT_NASC;NUM_SECAO;NOM_MAE;NUM_LOCAL;TURNO1;TURNO2`
  (nascimento, mãe e local vazios na lista do TRE).
- PDF escaneado (imagem) não serve: pedir de novo em planilha. OCR está fora do escopo.

## 5. Publicar

1. `python3 scripts/app_importar_eleitores.py "data/eleitores/Lista de eleitores_Dublin.pdf" --grava`
   e depois `python3 scripts/app_construir.py --lista data/eleitores/eleitores.csv --grava --senha-equipe "..."`.
   Sem `--senha-equipe` o script sorteia uma frase de seis palavras e a imprime uma vez.
   O build da lista real leva uns 4 minutos (33 mil hashes PBKDF2, em paralelo).
2. Publicar **só `app/dist/`** no GitHub Pages: branch `gh-pages` deste repositório, ou
   um repositório público só com essa pasta se o plano da conta não permitir Pages em
   repositório privado. `app/dist/` não contém dado pessoal legível.
3. Distribuir a senha da equipe no briefing, fora de e-mail em massa. Trocar a senha =
   reconstruir e republicar; o service worker baixa o pacote novo pela mudança em
   `versao.json` (o build grava o carimbo em `sw.js`).
4. Pôr o link/QR na peça P0-Consulta e na campanha "descubra sua seção antes de sair de casa".
5. 2º turno (25/10): trocar `turno`, `turno_n` e `data` em `app/public/dados/config.json` e
   reconstruir — a marca de turno que gera aviso passa a ser a do 2º turno.

## 6. Modelo de ameaça, em uma tabela

| Quem | Consegue | Não consegue |
|---|---|---|
| Qualquer pessoa com o link | saber se um nome completo que conhece vota em Dublin, e em que seção; em homônimo, só com o título | listar eleitores; obter títulos |
| Quem baixa `indice_publico.json` | tentar nomes contra os hashes, a ~30 ms por tentativa (PBKDF2 50k) | recuperar nomes em massa (30 mil chaves × espaço de nomes); recuperar títulos (10¹² por nome) |
| Quem baixa `equipe.enc` sem a senha | nada útil | decifrar (AES-256-GCM, chave de PBKDF2 600k sobre frase de seis palavras) |
| Quem tem a senha | tudo que a equipe vê: nome, título, seção, marcas de turno | — (por isso a senha é do dia e se troca reconstruindo) |
| Quem acha um celular da equipe | o pacote cifrado no cache | a lista, sem a senha; a página descarrega a lista ao fechar |

Limites conhecidos: nome de casada, abreviações e apelidos não encontram (o app sempre
mostra o caminho de volta ao e-Título e ao P0); homônimo sem o título em mãos vai ao
e-Título ou ao P0; a consulta só por nome foi uma decisão consciente de 01/10, tomada porque
a lista não traz outro dado (§2a).

## 7. Testes

- `python3 -m pytest -q app/testes` (10): normalização, hash só nome × nome|título, leitor
  do PDF do TRE (nome quebrado, marcas VT, cabeçalho no meio), vetores Python × JS iguais
  (inclui `consultaPublica` sobre um índice v2 montado à mão), build confere a amostra e
  rejeita seção estranha, rotas batem com `decisoes.json`, índice v2 da amostra.
- `app/testes/ponta_a_ponta.mjs` (Chromium, 15): eleitor com apóstrofo, nome curto, não
  encontrado, homônimo → título errado / incompleto / certo, marca VT, equipe com senha
  errada e certa, três homônimas com título, marca VT na equipe, e as duas páginas **offline**.
- Importador validado sobre a lista real de 29/09: 16.794 registros, 62 nomes quebrados
  juntados, 28 mesas com contagem idêntica a `decisoes.json`.

## 8. Pendências

- Confirmar com o Cartório o significado da marca **VT** (premissa: voto em trânsito) e se
  os 74 eleitores marcados no 1º turno votam em Dublin ou não. O texto do aviso está em
  `config.json` (`aviso_marca`) e muda sem reconstruir o índice.
- GitHub Pages: branch `gh-pages` deste repositório (decisão de 01/10); conferir se o plano
  da conta serve Pages em repositório privado. Se não, repositório público só com `app/dist/`.
- Quem constrói e publica na véspera; quem guarda a senha da equipe. Trocar a senha =
  reconstruir e republicar.
- Teste da página da equipe sem sinal, na calçada, na véspera.
- Dispositivo dedicado no P0 (tablet) ou celulares dos voluntários?
- A lista nominal **não pode voltar ao git**: o PDF chegou commitado em 29/09 e foi removido
  do HEAD em 01/10 (continua no histórico do branch; purgar exige reescrever o histórico).
