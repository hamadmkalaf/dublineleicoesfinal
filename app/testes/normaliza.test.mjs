// Confere que comum.js reproduz a normalização e o hash do Python (vetores_nome.json).
//   node app/testes/normaliza.test.mjs
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import assert from "node:assert/strict";
const aqui = path.dirname(fileURLToPath(import.meta.url));
const OEV = createRequire(import.meta.url)(path.join(aqui, "../public/comum.js"));
const v = JSON.parse(readFileSync(path.join(aqui, "vetores_nome.json"), "utf-8"));
const indice = { sal: "dublin-2026-onde-eu-voto", iteracoes: 50000, bytes: 12 };
let n = 0;
for (const c of v.nomes) { assert.equal(OEV.normalizaNome(c.entrada), c.normalizado, `nome: ${c.entrada}`); assert.deepEqual(OEV.chavesNome(c.entrada), c.chaves, `chaves: ${c.entrada}`); n++; }
for (const c of v.datas) { assert.equal(OEV.normalizaData(c.entrada), c.normalizada, `data: ${c.entrada}`); n++; }
for (const c of v.hashes) { assert.equal(await OEV.hashPublico(c.chave, c.fator, indice), c.hash, `hash: ${c.chave}`); n++; }
const t0 = performance.now();
for (let i = 0; i < 5; i++) await OEV.hashPublico("MARIA APARECIDA SILVA", "1970-05-05", indice);
console.log(`${n} vetores iguais em Python e JavaScript · hash público: ${((performance.now() - t0) / 5).toFixed(0)} ms cada`);
