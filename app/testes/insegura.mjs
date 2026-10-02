// Ponta a ponta em CONTEXTO INSEGURO: a página servida por http:// num endereço que não é localhost, como
// http://dublineleicoes2026.com.br/ antes de o HTTPS valer. Aí o Chromium não expõe crypto.subtle, e em 02/10
// a consulta quebrava com "Cannot read properties of undefined (reading 'importKey')". Este teste confere
// que eleitor, equipe e administrador funcionam mesmo assim, pela criptografia em JavaScript puro de comum.js.
// Usa app/dist/ com a amostra. O endereço vem de um IP da máquina (nunca 127.0.0.1, que conta como seguro).
//   APP_SENHA_EQUIPE="teste amostra" python3 scripts/app_construir.py --grava
//   NODE_PATH=/opt/node22/lib/node_modules node app/testes/insegura.mjs
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import { networkInterfaces } from "node:os";
import { fileURLToPath } from "node:url";
import { mkdirSync } from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
const { chromium } = createRequire(import.meta.url)("playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url));
const dist = process.env.APP_DIST || path.resolve(aqui, "../dist");
const capturas = path.join(aqui, "capturas");
mkdirSync(capturas, { recursive: true });
const SENHA = process.env.APP_SENHA_EQUIPE || "teste amostra";
const SENHA_ADMIN = "br1sk3t2026";
const PORTA = 8766;

const ip = Object.values(networkInterfaces()).flat().find((i) => i && i.family === "IPv4" && !i.internal)?.address;
if (!ip) { console.log("sem IP externo nesta máquina: não dá para simular um contexto inseguro"); process.exit(0); }
const BASE = `http://${ip}:${PORTA}/`;

const servidor = spawn("python3", ["-m", "http.server", String(PORTA), "--bind", "0.0.0.0", "-d", dist], { stdio: "ignore" });
await new Promise((r) => setTimeout(r, 800));
const navegador = await chromium.launch();
const ctx = await navegador.newContext({ viewport: { width: 390, height: 844 }, locale: "pt-BR" });
const pagina = await ctx.newPage();
const erros = [];
pagina.on("pageerror", (e) => erros.push(String(e)));
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
  const ctxSeguro = await pagina.evaluate(() => ({ seguro: window.isSecureContext, subtle: !!(window.crypto && window.crypto.subtle), nativo: OEV.temWebCrypto() }));
  assert.deepEqual(ctxSeguro, { seguro: false, subtle: false, nativo: false }, `a página em ${BASE} tem de ser um contexto inseguro, sem crypto.subtle`);
  passo(`contexto inseguro reproduzido em ${BASE}: sem crypto.subtle, comum.js usa JavaScript puro`);

  // eleitor: nome único (com acento, diferente de como está na lista), homônimo com título
  let t0 = Date.now();
  let r = await consulta("Tizzani Viana D'Andrea Néry");
  assert.doesNotMatch(await r.textContent(), /Erro na consulta|importKey/, "o erro de 02/10 não pode voltar");
  assert.equal(await r.locator(".letra").textContent(), "A");
  assert.match(await r.textContent(), /grupo A3/i);
  passo(`consulta por nome em http:// funciona (${Date.now() - t0} ms, PBKDF2 em JavaScript puro)`);
  await pagina.screenshot({ path: path.join(capturas, "insegura_eleitor.png"), fullPage: true });

  r = await consulta("Maria Aparecida Silva");
  assert.ok(!(await pagina.locator("#bloco-titulo").isHidden()), "homônimo pede o título");
  passo("homônimo em http://: pede o título");

  // equipe: senha do dia abre o pacote (600 mil iterações + AES-GCM em JavaScript puro)
  await pagina.goto(`${BASE}equipe/`);
  await pagina.waitForSelector("#botao-senha:not([disabled])");
  await pagina.fill("#senha", SENHA);
  t0 = Date.now();
  await pagina.click("#botao-senha");
  await pagina.waitForSelector("#aberto:not([hidden])", { timeout: 60000 });
  passo(`equipe em http://: pacote decifrado em JavaScript puro (${Date.now() - t0} ms)`);
  await pagina.fill("#busca", "tizzani");
  await pagina.waitForFunction(() => document.querySelectorAll("#lista li").length >= 1);
  assert.match(await pagina.locator("#resultado").textContent(), /Porta A/);
  passo("equipe em http://: busca e cartão do eleitor");
  await pagina.screenshot({ path: path.join(capturas, "insegura_equipe.png"), fullPage: true });

  // administrador: senha conferida pelo PBKDF2 puro; cofre grava e lê a chave
  await pagina.goto(`${BASE}admin/`);
  await pagina.waitForSelector("#botao-senha:not([disabled])");
  await pagina.fill("#senha", SENHA_ADMIN);
  await pagina.click("#botao-senha");
  await pagina.waitForSelector("#aberto:not([hidden])", { timeout: 60000 });
  await pagina.fill("#chave", "github_pat_teste_insegura");
  await pagina.click("#guardar-chave");
  await pagina.waitForFunction(() => /Chave guardada/.test(document.querySelector("#estado-chave").textContent));
  passo("administrador em http://: senha conferida e chave guardada no cofre em JavaScript puro");
  await pagina.reload();
  await pagina.waitForSelector("#botao-senha:not([disabled])");
  await pagina.fill("#senha", SENHA_ADMIN);
  await pagina.click("#botao-senha");
  await pagina.waitForSelector("#aberto:not([hidden])", { timeout: 60000 });
  assert.match(await pagina.locator("#estado-chave").textContent(), /Chave guardada/);
  passo("administrador em http://: cofre reaberto depois de recarregar");

  const graves = erros.filter((e) => !/fila\.json|raw\.githubusercontent|net::ERR|Failed to fetch/.test(e));
  assert.deepEqual(graves, [], "sem erros de página");
  console.log(`${ok} passos ok em contexto inseguro (${BASE})`);
} catch (e) {
  await pagina.screenshot({ path: path.join(capturas, "insegura_falha.png"), fullPage: true }).catch(() => {});
  console.error("FALHOU:", e.message, "\nerros de página:", erros);
  process.exitCode = 1;
} finally {
  await navegador.close();
  servidor.kill();
}
