// Teste de ponta a ponta no Chromium: eleitor, equipe e modo offline, sobre app/dist/ com a amostra.
//   APP_SENHA_EQUIPE="teste amostra" python3 scripts/app_construir.py --grava
//   NODE_PATH=/opt/node22/lib/node_modules node app/testes/ponta_a_ponta.mjs
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";
import assert from "node:assert/strict";
const { chromium } = createRequire(import.meta.url)("playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url));
const dist = path.resolve(aqui, "../dist");
const capturas = path.join(aqui, "capturas");
const PORTA = 8765, BASE = `http://127.0.0.1:${PORTA}/`;
const SENHA = process.env.APP_SENHA_EQUIPE || "teste amostra";

const servidor = spawn("python3", ["-m", "http.server", String(PORTA), "--bind", "127.0.0.1", "-d", dist], { stdio: "ignore" });
await new Promise((r) => setTimeout(r, 800));
const navegador = await chromium.launch();
const ctx = await navegador.newContext({ viewport: { width: 390, height: 844 }, locale: "pt-BR", serviceWorkers: "allow" });
const pagina = await ctx.newPage();
let ok = 0;
const passo = (msg) => { ok++; console.log("  ✓", msg); };

async function consulta(nome, data) {
  await pagina.fill("#nome", nome);
  await pagina.fill("#fator", data);
  await pagina.click("#botao");
  await pagina.waitForFunction(() => document.querySelector("#resultado").textContent.trim().length > 0);
  await pagina.waitForFunction(() => document.querySelector("#botao").textContent === "Consultar");
  return pagina.locator("#resultado");
}

try {
  await pagina.goto(BASE);
  await pagina.waitForSelector("#botao:not([disabled])");
  // (a) eleitor fixo da amostra: seção 3889 -> letra A, porta S4, grupo A3
  let r = await consulta("Tizzani Viana D'Andrea Nery", "1975-03-16");
  assert.equal(await r.locator(".letra").textContent(), "A");
  assert.match(await r.textContent(), /Porta S4 · parede oeste/);
  assert.match(await r.textContent(), /3889/);
  assert.match(await r.textContent(), /grupo A3/i);
  passo("eleitor: nome completo com apóstrofo → seção 3889, fila A, porta S4, grupo A3");
  await pagina.screenshot({ path: path.join(capturas, "eleitor_resultado.png"), fullPage: true });
  // nome sem os nomes do meio
  r = await consulta("tizzani nery", "16/03/1975".split("/").reverse().join("-"));
  assert.equal(await r.locator(".letra").textContent(), "A");
  passo("eleitor: primeiro + último sobrenome também encontra");
  // (b) não encontrado
  r = await consulta("Fulano Inexistente", "1975-03-16");
  assert.match(await r.textContent(), /Não encontramos/);
  passo("eleitor: nome errado → não encontrado, com caminho para o e-Título e o P0");
  // homônimo com mesma data
  r = await consulta("Joao Carlos Souza", "1988-08-08");
  assert.match(await r.textContent(), /mais de um eleitor/);
  passo("eleitor: homônimo com a mesma data → manda ao P0");
  // (c) equipe
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
  passo("equipe: três homônimas listadas com data e título");
  await pagina.fill("#busca", "tizzani");
  await pagina.waitForFunction(() => document.querySelector("#resultado .cartao-eleitor"));
  assert.match(await pagina.locator("#resultado").textContent(), /1234 5678 9012/);
  assert.match(await pagina.locator("#resultado").textContent(), /3889/);
  passo("equipe: busca por parte do nome → título 1234 5678 9012 e a rota");
  await pagina.screenshot({ path: path.join(capturas, "equipe_resultado.png"), fullPage: true });
  // (d) offline: espera o service worker e repete com a rede desligada
  await pagina.goto(BASE);
  await pagina.waitForFunction(() => navigator.serviceWorker.controller !== null, null, { timeout: 15000 }).catch(async () => {
    await pagina.reload(); await pagina.waitForFunction(() => navigator.serviceWorker.controller !== null, null, { timeout: 15000 });
  });
  await ctx.setOffline(true);
  await pagina.reload();
  await pagina.waitForSelector("#botao:not([disabled])");
  r = await consulta("Tizzani Viana D'Andrea Nery", "1975-03-16");
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
  await ctx.setOffline(false);
  // tamanho e tempo
  const tempo = await pagina.evaluate(async () => {
    const idx = await (await fetch("../dados/indice_publico.json")).json();
    const t0 = performance.now(); await OEV.hashPublico("MARIA APARECIDA SILVA", "1970-05-05", idx); return performance.now() - t0;
  });
  console.log(`  · hash público no navegador: ${tempo.toFixed(0)} ms`);
  assert.ok(tempo < 300);
  console.log(`${ok} verificações ok`);
} finally {
  await navegador.close();
  servidor.kill();
}
