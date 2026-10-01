// Teste de ponta a ponta no Chromium: eleitor (só nome; título em homônimo), equipe e modo offline, sobre app/dist/ com a amostra.
//   APP_SENHA_EQUIPE="teste amostra" python3 scripts/app_construir.py --grava
//   NODE_PATH=/opt/node22/lib/node_modules node app/testes/ponta_a_ponta.mjs
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { mkdirSync } from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
const { chromium } = createRequire(import.meta.url)("playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url));
const dist = path.resolve(aqui, "../dist");
const capturas = path.join(aqui, "capturas");
mkdirSync(capturas, { recursive: true });
const PORTA = 8765, BASE = `http://127.0.0.1:${PORTA}/`;
const SENHA = process.env.APP_SENHA_EQUIPE || "teste amostra";

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
  assert.match(await r.textContent(), /Porta S4 · parede da esquerda/);
  assert.match(await r.textContent(), /3889/);
  assert.match(await r.textContent(), /grupo A3/i);
  passo("eleitor: nome completo com apóstrofo → seção 3889, fila A, porta S4, grupo A3");
  await pagina.screenshot({ path: path.join(capturas, "eleitor_resultado.png"), fullPage: true });
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
  await pagina.fill("#titulo", "9999 9999 9999");
  await pagina.click("#botao");
  await pagina.waitForFunction(() => document.querySelector("#resultado").textContent.includes("não corresponde"));
  passo("eleitor: homônimo com título errado → avisa e manda ao e-Título/P0");
  await pagina.fill("#titulo", "2222");
  await pagina.click("#botao");
  await pagina.waitForFunction(() => document.querySelector("#resultado").textContent.includes("12 dígitos"));
  passo("eleitor: título incompleto → pede os 12 dígitos");
  await pagina.fill("#titulo", "333333333333");
  await pagina.click("#botao");
  await pagina.waitForFunction(() => document.querySelector("#resultado .letra"));
  assert.match(await pagina.locator("#resultado").textContent(), /3862/);
  assert.equal(await pagina.locator("#bloco-titulo").isHidden(), true);
  passo("eleitor: homônimo com título certo → seção 3862 (a Maria da seção 3862, não as outras duas)");
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
  assert.match(lista, /1111 1111 1111/); assert.match(lista, /2222 2222 2222/); assert.match(lista, /3333 3333 3333/);
  assert.doesNotMatch(lista, /nasc/);
  passo("equipe: três homônimas listadas, cada uma com o seu título e a sua seção");
  await pagina.click("#lista li:nth-child(2)");
  await pagina.waitForFunction(() => document.querySelector("#resultado .cartao-eleitor"));
  assert.match(await pagina.locator("#resultado").textContent(), /2222 2222 2222/);
  passo("equipe: tocar numa homônima abre a rota dela");
  await pagina.fill("#busca", "ana vt");
  await pagina.waitForFunction(() => document.querySelector("#resultado .cartao-eleitor"));
  assert.match(await pagina.locator("#resultado .marca-turno").textContent(), /1º turno: VT/);
  passo("equipe: marca VT aparece em destaque no cartão");
  await pagina.fill("#busca", "tizzani");
  await pagina.waitForFunction(() => document.querySelector("#resultado .cartao-eleitor") && document.querySelector("#resultado").textContent.includes("1234 5678 9012"));
  assert.match(await pagina.locator("#resultado").textContent(), /3889/);
  passo("equipe: busca por parte do nome → título 1234 5678 9012 e a rota");
  await pagina.screenshot({ path: path.join(capturas, "equipe_resultado.png"), fullPage: true });
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
