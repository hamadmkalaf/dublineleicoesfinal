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
for (const c of v.titulos) { assert.equal(OEV.normalizaInscricao(c.entrada), c.normalizado, `título: ${c.entrada}`); assert.equal(OEV.tituloParcial(c.entrada), c.parcial, `parcial: ${c.entrada}`); n++; }
for (const c of v.hashes) { assert.equal(await OEV.hashPublico(c.chave, c.fator, indice), c.hash, `hash: ${c.chave}|${c.fator}`); n++; }

// consultaPublica sobre um índice v2 montado à mão: nome único, homônimo com título, chave curta
const h = (c, f = "") => OEV.hashPublico(c, f, indice);
const itens = {};
itens[await h("ANA CRISTINA EVARISTO")] = ["3313"];
itens[await h("ANA EVARISTO")] = ["3313"];
itens[await h("MARIA APARECIDA SILVA")] = "H";
itens[await h("MARIA APARECIDA SILVA", "1111")] = ["0511"];
itens[await h("MARIA APARECIDA SILVA", "2222")] = ["3862", "VT"];
itens[await h("MARIA APARECIDA SILVA", "7777")] = "P";
const idx = { ...indice, v: 2, fator: "nome", titulo: { digitos: "5-8", tamanho: 4 }, itens };
assert.deepEqual((await OEV.consultaPublica(idx, "Ana Cristina Evaristo")).estado, "ok");
assert.equal((await OEV.consultaPublica(idx, "ana evaristo")).secao, "3313");
assert.equal((await OEV.consultaPublica(idx, "Ana Cristina de Evaristo")).estado, "ok", "chave curta quando a completa não existe");
assert.equal((await OEV.consultaPublica(idx, "Maria Aparecida Silva")).estado, "homonimo");
assert.equal((await OEV.consultaPublica(idx, "Maria Aparecida Silva", "1111 1111 1111")).secao, "0511", "título completo: extrai os dígitos 5-8");
assert.equal((await OEV.consultaPublica(idx, "Maria Aparecida Silva", "1111")).secao, "0511", "só os 4 do meio");
const r = await OEV.consultaPublica(idx, "Maria Aparecida Silva", "2222");
assert.deepEqual([r.estado, r.secao, r.marca], ["ok", "3862", "VT"]);
assert.equal((await OEV.consultaPublica(idx, "Maria Aparecida Silva", "9999")).estado, "titulo_errado");
assert.equal((await OEV.consultaPublica(idx, "Maria Aparecida Silva", "7777")).estado, "sem_desempate");
assert.equal((await OEV.consultaPublica(idx, "Maria Aparecida Silva", "12")).estado, "titulo_invalido");
assert.equal((await OEV.consultaPublica(idx, "Fulano Inexistente")).estado, "nao_encontrado");
assert.equal((await OEV.consultaPublica(idx, "   ")).estado, "incompleto");
n += 12;

const t0 = performance.now();
for (let i = 0; i < 5; i++) await OEV.hashPublico("MARIA APARECIDA SILVA", "", indice);
console.log(`${n} vetores iguais em Python e JavaScript · hash público: ${((performance.now() - t0) / 5).toFixed(0)} ms cada`);
