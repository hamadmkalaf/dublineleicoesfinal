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

// ---- v3: estimativa de espera, bloco ao eleitor, número no caderno ----
const cfgFila = { lotacao_zona: 706, segundos_por_eleitor: 60, minutos_travessia: 3, arredonda_min: 5, validade_min: 60,
  rotulo: "Tempo estimado de espera", explicacao: "fila {letra} {pct}% às {hora}, {seg} s", sem_fila: "Sem fila na {letra} às {hora}", desatualizado: "velha: {hora} há mais de {validade} min" };
const zonas = { A: { urnas: 9 }, B: { urnas: 9 }, C: { urnas: 10 } };
let e = OEV.estimaEspera(50, zonas.A, cfgFila);
assert.deepEqual([e.pessoas, e.vazaoPorMin, e.minutos], [353, 9, 40], "zona A meio cheia: 353 pessoas a 9/min = 39,2 + 3 ≈ 40 min");
assert.equal(OEV.estimaEspera(100, zonas.C, cfgFila).minutos, 75, "zona C lotada: 706 a 10/min = 70,6 + 3 ≈ 75");
assert.equal(OEV.estimaEspera(0, zonas.A, cfgFila).minutos, 5, "vazia: nunca abaixo do passo de arredondamento");
assert.equal(OEV.estimaEspera(150, zonas.A, cfgFila).pct, 100, "porcentagem é limitada a 0–100");
assert.equal(OEV.estimaEspera(50, zonas.A, { ...cfgFila, segundos_por_eleitor: 90 }).minutos, 60, "90 s por eleitor: 58,8 + 3 ≈ 60");
const rotaA = { letra: "A", secao: "3889" }, rotas = { zonas };
const agora = Date.parse("2026-10-04T10:00:00Z");
const fila = { ativo: true, zonas: { A: { pct: 50, em: "2026-10-04T09:50:00Z" }, B: { pct: null, em: null } } };
let html = OEV.renderEspera(fila, rotaA, rotas, cfgFila, agora);
assert.match(html, /cerca de 40 min/); assert.match(html, /fila A 50%/); assert.doesNotMatch(html, /velha/);
assert.equal(OEV.renderEspera({ ...fila, ativo: false }, rotaA, rotas, cfgFila, agora), "", "status desligado pelo admin: nada ao eleitor");
assert.equal(OEV.renderEspera(fila, { letra: "B" }, rotas, cfgFila, agora), "", "zona sem informação: nada");
assert.equal(OEV.renderEspera(null, rotaA, rotas, cfgFila, agora), "", "sem fila.json (offline): nada");
html = OEV.renderEspera({ ativo: true, zonas: { A: { pct: 0, em: "2026-10-04T09:50:00Z" } } }, rotaA, rotas, cfgFila, agora);
assert.match(html, /poucos minutos/); assert.match(html, /Sem fila na A/);
html = OEV.renderEspera({ ativo: true, zonas: { A: { pct: 80, em: "2026-10-04T08:00:00Z" } } }, rotaA, rotas, cfgFila, agora);
assert.match(html, /class="espera velha"/); assert.match(html, /há mais de 60 min/);
assert.equal(OEV.textoCaderno({ c: 56, p: 256 }), "nº 56 no caderno (256º da seção)");
assert.equal(OEV.textoCaderno({ c: 12, p: 12 }), "nº 12 no caderno");
assert.equal(OEV.textoCaderno({}), "", "pacote v2 sem o campo: nada");
assert.equal(OEV.preenche("{a}-{b}-{c}", { a: 1, b: "x" }), "1-x-");
n += 14;
console.log(`${n} vetores/casos ok`);
