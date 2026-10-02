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

### 2c. v2 — título parcial (01/10/2026, branch `appeleicoes2`, página `/v2/`)

Pedido do usuário: blindar o app contra preocupações de segurança da informação. A tabela
importada e tudo o que se publica guardam **só 4 dígitos do título**; nome, seção e marcas de
turno continuam. Medição na lista real para escolher a janela:

| Janela do título | Valores distintos (de 16.794) | Colisões nome+4 dígitos entre homônimos (de 1.278 chaves) |
|---|---|---|
| 4 últimos (UF + verificadores) | 271 | 131 |
| 4 primeiros | 3.986 | 11 |
| **dígitos 5 a 8** | **8.151** | **0** |

Decisão: **dígitos 5 a 8** (`TITULO_JANELA` em `app_normaliza.py`, `tituloParcial` em `comum.js`).
- O importador grava `TITULO_5_8` em `data/eleitores/eleitores_v2.csv` (padrão); `--titulo-completo`
  volta ao formato v1. O PDF do TRE não é editado nem volta ao git.
- O build aceita os dois CSVs e reduz o título na leitura; o título completo não existe no índice,
  no pacote da equipe nem em `versao.json`. Se duas pessoas da mesma chave de nome tiverem os
  mesmos 4 dígitos, a entrada vira `"P"` e o app manda ao P0 (0 casos na lista real).
- O eleitor digita os 4 dígitos do meio **ou** o número completo; o app extrai os 4 no aparelho.
- A equipe vê `···· 5678 ····`; a lista cifrada não tem como reconstruir o título.
- O CSV v2 fica no git **cifrado**: `data/eleitores/eleitores_v2.csv.enc`, AES-256-GCM com
  chave PBKDF2 (600 mil iterações) da senha da equipe (`scripts/app_cifra_lista.py`). É o único
  arquivo de `data/eleitores/` que o `.gitignore` deixa entrar. Quem tem a senha reconstrói o
  app em qualquer máquina com `app_construir.py --lista …csv.enc --senha-equipe`. Decisão de
  01/10: o usuário pediu o CSV no repositório; em claro violaria a regra da lista nominal.
- Os PDFs que haviam sido commitados (`appeleicoes`, 29–30/09; `DUBLIN.pdf` em `main`) foram
  purgados do histórico em 01/10 com force-push; o pedido de limpeza de cache ao suporte do
  GitHub ficou com o usuário.
- Publicação em `gh-pages/v2/` (`app_publicar.sh --subpasta v2`); a v1 fica na raiz até ser
  removida. **Pendência:** remover a v1 depois de validar a v2, porque o pacote cifrado da v1 ainda
  tem os títulos completos.

### 2d. v3 — número no caderno, tempo de espera e área do administrador (01/10/2026, branch `appeleicoesv3`, página `/v3/`)

Pedido do usuário em 01/10; mudanças concentradas na área da equipe, mais uma área nova.

| Decisão | Escolha | Por quê |
|---|---|---|
| **Número no caderno** (equipe) — **RETIRADO DA PÁGINA em 02/10** | calculado no **build** (`numera_caderno` em `app_construir.py`): posição do nome na ordem alfabética dos eleitores da **mesma seção**; até 200 → a posição; acima de 200 → **posição − 200** (256º → 56). Vai no pacote da equipe como `c` (número) e `p` (posição); a página mostra "nº 56 no caderno (256º da seção)" | regra ditada pelo usuário. Calcular uma vez, em Python, deixa a regra testável e o JS só exibe |
| Ordem alfabética do caderno | `chave_caderno`: nome **impresso**, maiúsculas, sem acento, espaços simples, **partículas contam** (≠ `normaliza_nome`); empate → título parcial | é a ordem de uma lista impressa; **premissa**, conferir com um caderno real |
| Seção da ordenação | a da lista do TRE (por mesa, agregadas somadas) | é a única seção que a lista traz. **Por isso a função foi retirada da página em 02/10:** o usuário conferiu cadernos reais e eles são **um por seção, principal e agregada separados**; a lista do TRE não diz a que seção (principal ou agregada) cada eleitor pertence, então a posição calculada não encontra o eleitor no caderno. Os campos `p`/`c` continuam no pacote, sem uso na interface, até haver uma lista por seção ou outra solução |
| **Tempo de espera** | a equipe informa **só uma porcentagem** de quão cheia está cada zona A/B/C do Ring 3; o app converte: `pessoas = pct × 706`, `vazão = urnas da zona × 60 / 60 s`, `espera = pessoas / vazão + 3 min`, arredondado a 5 min (`estimaEspera` em `comum.js`; parâmetros em `config.json → fila`; urnas por zona em `rotas.json → zonas`) | pedido do usuário: "simplesmente colocar uma porcentagem". 706 é a lotação por zona da montagem do Ring 3. **Premissas:** 60 s por eleitor (`docs/contexto_geral.md`), 3 min de travessia |
| **Onde mora o estado vivo** | `fila.json` num **branch órfão `fila`** deste repositório: `{ativo, zonas: {A: {pct, em}, …}, atualizado}`. Equipe e admin **escrevem pela API do GitHub** (Contents API, com `sha` e 3 tentativas em conflito); o eleitor **lê** por `raw.githubusercontent.com` (cache quebrado por minuto; CDN pode atrasar até ~5 min) | decisão de 28/09 "só GitHub Pages, sem servidor" mantida: nenhuma infraestrutura nova. Não usa `gh-pages` porque cada gravação dispararia um build do Pages (limite brando de 10/hora) |
| **Chave de publicação** | fine-grained PAT com *Contents: read and write* **só neste repositório**, distribuída no briefing como a senha do dia. Fica no aparelho **cifrada** (AES-GCM, chave PBKDF2 de 100 mil iterações) com a senha do dia (equipe) ou a do admin (`guardaSegredo`/`leSegredo` em `comum.js`) | um site estático não tem como autenticar escrita sem um segredo no cliente. Vazamento → revogar no GitHub. **Risco aceito:** o PAT alcança todos os branches do repositório, inclusive `gh-pages`; para reduzir, mover `fila.json` para um repositório só dele (trocar `repo`, `branch`, `url_leitura` em `config.json` e reconstruir) |
| **Área do administrador** (`admin/`) | senha conferida contra **hash PBKDF2** em `config.json → admin` (sal e 200 mil iterações; a senha nunca fica em claro no git). Função **"Ativar status de fila"** grava `ativo` em `fila.json`; mostra a lotação publicada, zera lotações, guarda/apaga a chave de publicação e exibe os parâmetros da estimativa | pedido do usuário. O hash num site estático é só um portão de interface: quem baixa o `config.json` pode tentar senhas offline; o que protege a gravação é a chave de publicação, não a senha |
| **Eleitor** | quando `ativo` e a zona dele tem informação: bloco **"Tempo estimado de espera · fila X"** logo **abaixo da nota da preferencial**, com "cerca de N min", barra de lotação, hora da informação e a premissa. Informação com mais de 60 min ganha aviso laranja; `ativo: false`, zona sem dado ou sem rede → **nada aparece** | pedido do usuário (posição do bloco). Sem rede o app continua inteiro: a fila é o único dado que não fica no cache |

Trocar a senha do admin: `python3 -c "import hashlib,base64;print(base64.urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256',b'NOVA',b'dublin-2026-onde-eu-voto-admin',200000,32)).decode().rstrip('='))"`
e colar em `config.json → admin.hash`; reconstruir e republicar.

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

**Fila (v3).** `equipe/` tem o painel "Fila no Ring 3": três controles de 0 a 100% (A, B, C), cada um
já mostrando a espera estimada; "Publicar lotação" grava em `fila.json` (branch `fila`) com a chave de
publicação. `admin/` liga/desliga `ativo`. O eleitor lê `fila.json` ao abrir e de novo a cada consulta
(se a leitura anterior tem mais de 1 min), com limite de 4 s para não atrasar o resultado.

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
| Quem baixa `indice_publico.json` | tentar nomes contra os hashes, a ~30 ms por tentativa (PBKDF2 50k) | recuperar nomes em massa (30 mil chaves × espaço de nomes); recuperar títulos (o índice só conhece 4 dígitos do meio) |
| Quem baixa `equipe.enc` sem a senha | nada útil | decifrar (AES-256-GCM, chave de PBKDF2 600k sobre frase de seis palavras) |
| Quem tem a senha | tudo que a equipe vê: nome, 4 dígitos do meio do título, seção, marcas de turno | reconstruir o título completo (faltam 8 dígitos) |
| Quem acha um celular da equipe | o pacote cifrado no cache; a chave de publicação cifrada no `localStorage` | a lista, sem a senha; a chave, sem a senha; a página descarrega a lista ao fechar |
| Quem obtém a chave de publicação (v3) | alterar `fila.json` (lotações falsas, ligar/desligar o status) e, em tese, qualquer branch do repositório | nada sobre eleitores (o repositório só tem a lista cifrada). Remédio: revogar o PAT no GitHub |
| Quem baixa `config.json` (v3) | tentar senhas do admin offline contra o hash PBKDF2 (200 mil iterações) | gravar a fila: a senha do admin só abre a interface; gravar exige a chave de publicação |

Limites conhecidos: nome de casada, abreviações e apelidos não encontram (o app sempre
mostra o caminho de volta ao e-Título e ao P0); homônimo sem o título em mãos vai ao
e-Título ou ao P0; a consulta só por nome foi uma decisão consciente de 01/10, tomada porque
a lista não traz outro dado (§2a).

## 7. Testes

- v3 acrescenta: `numero_caderno` (regra dos 200), `chave_caderno`, `numera_caderno` com 256 eleitores
  (256º → 56), pacote da equipe com `p`/`c` ordenados por seção, `rotas.json → zonas`, `config.json`
  com `fila` e `admin` (hash confere, senha não está em claro); em JS, `estimaEspera`, `renderEspera`
  (desligado/zona sem dado/offline → vazio; informação velha), `textoCaderno`; ponta a ponta: bloco de
  espera abaixo da preferencial e sumindo com `ativo: false`, nº no caderno, painel da fila, admin
  (senha errada/certa, cofre da chave) e offline (24 verificações).
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

- **v3 / caderno:** a lista do TRE por mesa não separa principal de agregada; o caderno físico separa. Para
  voltar com o nº no caderno é preciso (a) uma relação por seção do Cartório, ou (b) cruzar o título/zona de
  origem com `data/decisoes.json` (origem_agregada) — a inscrição não traz a seção. Pensar depois.
- **v3:** criar o fine-grained PAT (só `dublineleicoesfinal`, *Contents: read and write*), guardar
  no aparelho do admin e distribuir à equipe no briefing; decidir se `fila.json` vai para um
  repositório só dele. Conferir a **regra dos 200** com um caderno real (o que acontece acima de
  400? a regra literal dá posição − 200; se o caderno reinicia a cada 200, trocar `numero_caderno`).
  Validar na véspera o ciclo equipe → `fila.json` → eleitor (latência do raw ~1–5 min).

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
