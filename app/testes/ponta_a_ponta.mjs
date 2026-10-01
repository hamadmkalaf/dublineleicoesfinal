// Teste de ponta a ponta no Chromium: eleitor (só nome; título em homônimo), estimativa de espera (v3), equipe (nº no caderno,
// painel da fila), administrador e modo offline, sobre app/dist/ com a amostra.
// O estado vivo da fila é simulado por dist/dados/fila_teste.json (config.json do dist é apontado para ele).
//   APP_SENHA_EQUIPE="teste amostra" python3 scripts/app_construir.py --grava
//   NODE_PATH=/opt/node22/lib/node_modules node app/testes/ponta_a_ponta.mjs
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
const { chromium } = createRequire(import.meta.url)("playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url));
const dist = path.resolve(aqui, "../dist");
const capturas = path.join(aqui, "capturas");
mkdirSync(capturas, { recursive: true });
const PORTA = 8765, BASE = `http://127.0.0.1:${PORTA}/`;
const SENHA = process.env.APP_SENHA_EQUIPE || "teste amostra";
const SENHA_ADMIN = "br1sk3t2026";

// v3: aponta a leitura da fila para um arquivo local servido junto com o dist (sem tocar em app/public)
const cfgPath = path.join(dist, "dados/config.json");
const cfg = JSON.parse(readFileSync(cfgPath, "utf-8"));
cfg.fila.url_leitura = `${BASE}dados/fila_teste.json`;
writeFileSync(cfgPath, JSON.stringify(cfg, null, 2));
const escreveFila = (fila) => writeFileSync(path.join(dist, "dados/fila_teste.json"), JSON.stringify(fila));
escreveFila({ v: 1, ativo: true, zonas: { A: { pct: 50, em: new Date().toISOString() }, B: { pct: null, em: null }, C: { pct: 0, em: new Date().toISOString() } }, atualizado: new Date().toISOString() });

const servidor = spawn("python3", ["-m", "http.server", String(PORTA), "--bind", "127.0.0.1", "-d", dist], { stdio: "ignore" });
await new Promise((r) => setTimeout(r, 800));
const navegador = await chromium.launch();
const ctx = await navegador.newContext({ viewport: { width: 390, height: 844 }, locale: "pt-BR", serviceWorkers: "allow" });
const pagina = await ctx.newPage();
let ok = 0;
const passo = (msg) => { ok++; console.log("  ✓", msg); };

async function consulta(nome, titulo) {
  await pagina.fill("#nome", nome);
  if (titulo !== undefined) {
    await pagina.waitForSelector("#bloco-titulo:not([hidden])");
    await pagina.fill("#titulo", titulo);
  }
  await pagina.click("#botao");
  await pagina.waitForFunction(() => /^(Consultar|Confirmar)$/.test(document.querySelector("#botao").textContent));
  return pagina.locator("#resultado");
}

try {
  await pagina.goto(BASE);
  await pagina.waitForSelector("#botao:not([disabled])");
  // (a) eleitor fixo da amostra: seção 3889 -> letra A, porta S4, grupo A3
  let r = await consulta("Tizzani Viana D'Andrea Nery");
  assert.equal(await r.locator(".letra").textContent(), "A");
  assert.match(await r.textContent(), /Porta A · parede da esquerda/);
  assert.match(await r.textContent(), /3889/);
  assert.match(await r.textContent(), /grupo A3/i);
  assert.doesNotMatch(await r.textContent(), /\bS[0-9]\b/, "nenhum número de porta da prancheta no que o eleitor lê");
  assert.equal(await r.locator(".mapa [data-passo]").count(), 6, "os seis passos marcados no mapa");
  passo("eleitor: nome completo com apóstrofo → seção 3889, fila A, porta S4, grupo A3");
  // v3: estimativa de espera abaixo da nota da preferencial (status ativado, zona A 50% cheia)
  await pagina.waitForSelector("#espera");
  assert.match(await pagina.locator("#espera").textContent(), /cerca de 40 min/);
  assert.match(await pagina.locator("#espera").textContent(), /50%/);
  assert.ok(await pagina.evaluate(() => { const n = document.querySelector("#resultado .nota"), e = document.querySelector("#espera"); return !!(n && e && (n.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING)); }), "o bloco de espera vem depois da nota da preferencial");
  passo("eleitor v3: status de fila ativado → “cerca de 40 min” para a zona A a 50%, abaixo da preferencial");
  await pagina.screenshot({ path: path.join(capturas, "eleitor_resultado.png"), fullPage: true });
  // status desligado pelo administrador: o bloco some (a página relê a fila a cada consulta, com mais de 1 min; força relendo)
  escreveFila({ v: 1, ativo: false, zonas: { A: { pct: 50, em: new Date().toISOString() } }, atualizado: new Date().toISOString() });
  await pagina.reload(); await pagina.waitForSelector("#botao:not([disabled])");
  r = await consulta("Tizzani Viana D'Andrea Nery");
  await pagina.waitForFunction(() => document.querySelector("#resultado .letra"));
  assert.equal(await r.locator("#espera").count(), 0, "status desligado: nada sobre fila ao eleitor");
  passo("eleitor v3: status desligado → nenhuma estimativa aparece");
  escreveFila({ v: 1, ativo: true, zonas: { A: { pct: 50, em: new Date().toISOString() } }, atualizado: new Date().toISOString() });
  await pagina.reload(); await pagina.waitForSelector("#botao:not([disabled])");
  // nome sem os nomes do meio
  r = await consulta("tizzani nery");
  assert.equal(await r.locator(".letra").textContent(), "A");
  passo("eleitor: primeiro + último sobrenome também encontra");
  // (b) não encontrado
  r = await consulta("Fulano Inexistente");
  assert.match(await r.textContent(), /Não encontramos/);
  passo("eleitor: nome errado → não encontrado, com caminho para o e-Título e o P0");
  // (c) homônimo: pede o título; título errado; título certo
  r = await consulta("Maria Aparecida Silva");
  assert.equal(await pagina.locator("#bloco-titulo").isHidden(), false);
  assert.match(await pagina.locator("#aviso-homonimo").textContent(), /mais de um eleitor/);
  assert.equal((await r.textContent()).trim(), "");
  passo("eleitor: homônimo → avisa e pede o título, sem mostrar seção");
  await pagina.screenshot({ path: path.join(capturas, "eleitor_homonimo.png"), fullPage: true });
  await pagina.fill("#titulo", "9999");
  await pagina.click("#botao");
  await pagina.waitForFunction(() => document.querySelector("#resultado").textContent.includes("não correspondem"));
  passo("eleitor: homônimo com dígitos errados → avisa e manda ao e-Título/P0");
  await pagina.fill("#titulo", "22");
  await pagina.click("#botao");
  await pagina.waitForFunction(() => document.querySelector("#resultado").textContent.includes("4 dígitos do meio"));
  passo("eleitor: título incompleto → pede os 4 dígitos do meio ou o número completo");
  await pagina.fill("#titulo", "333333333333");
  await pagina.click("#botao");
  await pagina.waitForFunction(() => document.querySelector("#resultado .letra"));
  assert.match(await pagina.locator("#resultado").textContent(), /3862/);
  assert.equal(await pagina.locator("#bloco-titulo").isHidden(), true);
  passo("eleitor: homônimo com o título completo → seção 3862 (o app extrai os dígitos 5-8 no aparelho)");
  r = await consulta("Maria Aparecida Silva");
  await pagina.fill("#titulo", "2222");
  await pagina.click("#botao");
  await pagina.waitForFunction(() => document.querySelector("#resultado .letra"));
  assert.match(await pagina.locator("#resultado").textContent(), /3313/);
  passo("eleitor: homônimo só com os 4 dígitos do meio → seção 3313");
  // (d) marca VT no 1º turno
  r = await consulta("Ana VT Teste");
  assert.match(await r.locator("#aviso-marca").textContent(), /VT/);
  assert.match(await r.textContent(), /3315/);
  passo("eleitor: marcado VT no turno → aviso em destaque, e ainda assim mostra a rota");
  // (e) equipe
  await pagina.goto(BASE + "equipe/");
  await pagina.waitForSelector("#botao-senha:not([disabled])");
  await pagina.fill("#senha", "senha errada");
  await pagina.click("#botao-senha");
  await pagina.waitForFunction(() => document.querySelector("#estado-lista").textContent.includes("incorreta"));
  passo("equipe: senha errada não abre a lista");
  await pagina.fill("#senha", SENHA);
  await pagina.click("#botao-senha");
  await pagina.waitForSelector("#aberto:not([hidden])");
  await pagina.fill("#busca", "maria aparecida silva");
  await pagina.waitForFunction(() => document.querySelectorAll("#lista li").length === 3);
  const lista = await pagina.locator("#lista").textContent();
  assert.match(lista, /···· 1111 ····/); assert.match(lista, /···· 2222 ····/); assert.match(lista, /···· 3333 ····/);
  assert.doesNotMatch(lista, /1111 1111 1111|nasc/);
  passo("equipe: três homônimas listadas, cada uma só com os 4 dígitos do meio do título e a sua seção");
  await pagina.click("#lista li:nth-child(2)");
  await pagina.waitForFunction(() => document.querySelector("#resultado .cartao-eleitor"));
  assert.match(await pagina.locator("#resultado").textContent(), /···· 2222 ····/);
  passo("equipe: tocar numa homônima abre a rota dela");
  await pagina.fill("#busca", "ana vt");
  await pagina.waitForFunction(() => document.querySelector("#resultado .cartao-eleitor"));
  assert.match(await pagina.locator("#resultado .marca-turno").textContent(), /1º turno: VT/);
  passo("equipe: marca VT aparece em destaque no cartão");
  await pagina.fill("#busca", "tizzani");
  await pagina.waitForFunction(() => document.querySelector("#resultado .cartao-eleitor") && document.querySelector("#resultado").textContent.includes("···· 5678 ····"));
  assert.match(await pagina.locator("#resultado").textContent(), /3889/);
  passo("equipe: busca por parte do nome → título ···· 5678 ···· e a rota");
  // v3: número no caderno no cartão e na lista
  assert.match(await pagina.locator("#resultado .badge-caderno").textContent(), /nº \d+ no caderno/);
  assert.match(await pagina.locator("#lista .badge-caderno").first().textContent(), /nº \d+/);
  const caderno = await pagina.evaluate(async () => {
    const t = document.querySelector("#resultado .badge-caderno").textContent; return t;
  });
  passo(`equipe v3: ${caderno} aparece no cartão do eleitor`);
  // v3: painel da fila com as três zonas; a lotação publicada foi lida; sem chave de publicação pede a chave
  await pagina.waitForSelector("#zonas-fila .zona-fila[data-letra=C]");
  assert.equal(await pagina.locator("#zonas-fila input[type=range]").count(), 3);
  await pagina.waitForFunction(() => document.querySelector("#pct-A-v").textContent === "50%");
  assert.match(await pagina.locator("#pct-A-m").textContent(), /40 min/);
  assert.match(await pagina.locator("#estado-publicado").textContent(), /ATIVADO/);
  await pagina.click("#publicar-fila");
  await pagina.waitForFunction(() => document.querySelector("#estado-fila").textContent.includes("chave de publicação"));
  assert.equal(await pagina.locator("#cofre-equipe").isHidden(), false);
  passo("equipe v3: painel da fila lê a lotação publicada (A 50% ≈ 40 min) e pede a chave antes de publicar");
  await pagina.screenshot({ path: path.join(capturas, "equipe_resultado.png"), fullPage: true });
  // (e2) administrador
  await pagina.goto(BASE + "admin/");
  await pagina.waitForSelector("#botao-senha:not([disabled])");
  await pagina.fill("#senha", "senha errada");
  await pagina.click("#botao-senha");
  await pagina.waitForFunction(() => document.querySelector("#estado-senha").textContent.includes("incorreta"));
  passo("admin: senha errada não entra");
  await pagina.fill("#senha", SENHA_ADMIN);
  await pagina.click("#botao-senha");
  await pagina.waitForSelector("#aberto:not([hidden])");
  await pagina.waitForFunction(() => document.querySelector("#ativo").checked === true);
  assert.match(await pagina.locator("#zonas").textContent(), /50% cheia/);
  assert.match(await pagina.locator("#estado-chave").textContent(), /Nenhuma chave/);
  await pagina.click("#gravar");
  await pagina.waitForFunction(() => document.querySelector("#estado-gravar").textContent.includes("chave de publicação"));
  passo("admin: entra com a senha, lê o status (ativado, A 50%) e exige a chave de publicação para gravar");
  // cofre: guarda a chave cifrada com a senha do admin; só reabre com a mesma senha
  await pagina.fill("#chave", "github_pat_TESTE_000000");
  await pagina.click("#guardar-chave");
  await pagina.waitForFunction(() => document.querySelector("#estado-chave").textContent.includes("guardada"));
  const cofre = await pagina.evaluate(() => localStorage.getItem("oev.chave_publicacao.admin"));
  assert.ok(cofre && !cofre.includes("github_pat_TESTE"), "a chave não fica em claro no aparelho");
  assert.equal(await pagina.evaluate(() => OEV.leSegredo("oev.chave_publicacao.admin", "outra senha").then(() => "abriu", () => "fechado")), "fechado");
  assert.equal(await pagina.evaluate(() => OEV.leSegredo("oev.chave_publicacao.admin", "br1sk3t2026")), "github_pat_TESTE_000000");
  passo("admin: chave de publicação guardada cifrada (AES-GCM) com a senha do administrador");
  await pagina.screenshot({ path: path.join(capturas, "admin.png"), fullPage: true });
  await pagina.click("#apagar-chave");
  // (f) offline: espera o service worker e repete com a rede desligada
  await pagina.goto(BASE);
  await pagina.waitForFunction(() => navigator.serviceWorker.controller !== null, null, { timeout: 15000 }).catch(async () => {
    await pagina.reload(); await pagina.waitForFunction(() => navigator.serviceWorker.controller !== null, null, { timeout: 15000 });
  });
  await ctx.setOffline(true);
  await pagina.reload();
  await pagina.waitForSelector("#botao:not([disabled])");
  r = await consulta("Tizzani Viana D'Andrea Nery");
  assert.equal(await r.locator(".letra").textContent(), "A");
  passo("offline: página do eleitor responde do cache");
  await pagina.goto(BASE + "equipe/");
  await pagina.waitForSelector("#botao-senha:not([disabled])");
  await pagina.fill("#senha", SENHA);
  await pagina.click("#botao-senha");
  await pagina.waitForSelector("#aberto:not([hidden])");
  await pagina.fill("#busca", "tizzani");
  await pagina.waitForFunction(() => document.querySelector("#resultado .cartao-eleitor"));
  passo("offline: equipe decifra a lista e encontra o eleitor sem rede");
  assert.match(await pagina.locator("#estado-publicado").textContent(), /Sem internet/);
  passo("offline v3: painel da fila avisa que não leu a lotação e a busca segue funcionando");
  await ctx.setOffline(false);
  // tamanho e tempo
  const tempo = await pagina.evaluate(async () => {
    const idx = await (await fetch("../dados/indice_publico.json")).json();
    const t0 = performance.now(); await OEV.hashPublico("MARIA APARECIDA SILVA", "", idx); return performance.now() - t0;
  });
  console.log(`  · hash público no navegador: ${tempo.toFixed(0)} ms`);
  assert.ok(tempo < 300);
  console.log(`${ok} verificações ok`);
} finally {
  await navegador.close();
  servidor.kill();
}
