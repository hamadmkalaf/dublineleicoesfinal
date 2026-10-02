// Confere que a criptografia em JavaScript puro de comum.js (usada quando a página está em http:// e o
// navegador não expõe crypto.subtle) dá byte a byte o mesmo resultado que o WebCrypto do Node:
// SHA-256, PBKDF2-HMAC-SHA256, AES-GCM, pacote da equipe, cofre e senha do admin.
//   node app/testes/cripto.test.mjs
import { createRequire } from "node:module";
import { createHash, pbkdf2Sync, randomBytes } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import assert from "node:assert/strict";
const aqui = path.dirname(fileURLToPath(import.meta.url));
const OEV = createRequire(import.meta.url)(path.join(aqui, "../public/comum.js"));
const enc = new TextEncoder();
const hex = (b) => Buffer.from(b).toString("hex");
let n = 0;

assert.equal(OEV.temWebCrypto(), true, "o Node tem crypto.subtle");

// ---- SHA-256: vetores conhecidos e comprimentos em torno do bloco ----
assert.equal(hex(OEV.sha256Puro(enc.encode("abc"))), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
assert.equal(hex(OEV.sha256Puro(new Uint8Array(0))), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
for (const tam of [1, 55, 56, 63, 64, 65, 119, 120, 128, 1000, 70000]) {
  const dados = randomBytes(tam);
  assert.equal(hex(OEV.sha256Puro(dados)), createHash("sha256").update(dados).digest("hex"), `sha256 de ${tam} bytes`);
  n++;
}

// ---- PBKDF2: os hashes do índice público (vetores do Python) pelo caminho puro ----
const v = JSON.parse(readFileSync(path.join(aqui, "vetores_nome.json"), "utf-8"));
const indice = { sal: "dublin-2026-onde-eu-voto", iteracoes: 50000, bytes: 12 };
OEV.usaWebCrypto(false);
assert.equal(OEV.temWebCrypto(), false);
let t0 = performance.now();
for (const c of v.hashes) { assert.equal(await OEV.hashPublico(c.chave, c.fator, indice), c.hash, `hash puro: ${c.chave}|${c.fator}`); n++; }
const msPuro = (performance.now() - t0) / v.hashes.length;
OEV.usaWebCrypto(true);

// PBKDF2 em geral: senhas/sais aleatórios, vários tamanhos de saída (1, 2 e 3 blocos de 32 bytes), senha longa (> 64 bytes)
for (const [senhaTam, salTam, it, bytes] of [[8, 16, 1, 32], [0, 1, 2, 12], [20, 32, 100, 40], [100, 8, 1000, 64], [64, 24, 333, 65], [65, 24, 10, 20]]) {
  const senha = randomBytes(senhaTam), sal = randomBytes(salTam);
  const esperado = pbkdf2Sync(senha, sal, it, bytes, "sha256");
  OEV.usaWebCrypto(false);
  const puro = await OEV.pbkdf2(senha, sal, it, bytes);
  OEV.usaWebCrypto(true);
  const nativo = await OEV.pbkdf2(senha, sal, it, bytes);
  assert.equal(hex(puro), esperado.toString("hex"), `pbkdf2 puro senha=${senhaTam} sal=${salTam} it=${it} bytes=${bytes}`);
  assert.equal(hex(nativo), esperado.toString("hex"), `pbkdf2 nativo senha=${senhaTam} sal=${salTam} it=${it} bytes=${bytes}`);
  n++;
}

// ---- AES-GCM: cifra num caminho, decifra no outro; chaves de 128/192/256 bits; tamanhos em torno do bloco ----
for (const kTam of [16, 24, 32]) {
  for (const tam of [0, 1, 15, 16, 17, 31, 32, 33, 100, 4097]) {
    const chave = randomBytes(kTam), iv = randomBytes(12), claro = randomBytes(tam);
    OEV.usaWebCrypto(true);
    const cNativo = await OEV.aesGcmCifra(chave, iv, claro);
    OEV.usaWebCrypto(false);
    const cPuro = await OEV.aesGcmCifra(chave, iv, claro);
    assert.equal(hex(cPuro), hex(cNativo), `aes-gcm cifra chave=${kTam} tam=${tam}`);
    assert.equal(hex(await OEV.aesGcmDecifra(chave, iv, cNativo)), hex(claro), `decifra puro chave=${kTam} tam=${tam}`);
    const estragado = Buffer.from(cNativo); estragado[estragado.length - 1] ^= 1;
    await assert.rejects(() => OEV.aesGcmDecifra(chave, iv, estragado), /senha errada|alterados/, "tag errada é rejeitada");
    OEV.usaWebCrypto(true);
    assert.equal(hex(await OEV.aesGcmDecifra(chave, iv, cPuro)), hex(claro), `decifra nativo o que o puro cifrou chave=${kTam} tam=${tam}`);
    n++;
  }
}

// ---- Cofre (localStorage simulado): guarda com um caminho, lê com o outro ----
const memoria = new Map();
globalThis.localStorage = { getItem: (k) => (memoria.has(k) ? memoria.get(k) : null), setItem: (k, v) => memoria.set(k, String(v)), removeItem: (k) => memoria.delete(k) };
OEV.usaWebCrypto(false);
t0 = performance.now();
await OEV.guardaSegredo("teste.cofre", "github_pat_exemplo_123", "senha do dia");
const msCofre = performance.now() - t0;
OEV.usaWebCrypto(true);
assert.equal(await OEV.leSegredo("teste.cofre", "senha do dia"), "github_pat_exemplo_123", "cofre: puro grava, nativo lê");
await assert.rejects(() => OEV.leSegredo("teste.cofre", "senha errada"));
await OEV.guardaSegredo("teste.cofre", "outro segredo", "s2");
OEV.usaWebCrypto(false);
assert.equal(await OEV.leSegredo("teste.cofre", "s2"), "outro segredo", "cofre: nativo grava, puro lê");
await assert.rejects(() => OEV.leSegredo("teste.cofre", "s3"));
assert.equal(await OEV.leSegredo("nada", "x"), "", "sem nada guardado: vazio");
OEV.usaWebCrypto(true);
n += 3;

// ---- Senha do administrador: mesmo veredito nos dois caminhos ----
const cfg = JSON.parse(readFileSync(path.join(aqui, "../public/dados/config.json"), "utf-8"));
if (cfg.admin && cfg.admin.hash) {
  for (const senha of ["senha errada", "br1sk3t2026"]) {
    OEV.usaWebCrypto(true); const a = await OEV.confereAdmin(cfg.admin, senha);
    OEV.usaWebCrypto(false); const b = await OEV.confereAdmin(cfg.admin, senha);
    OEV.usaWebCrypto(true);
    assert.equal(a, b, `confereAdmin("${senha}") igual nos dois caminhos`);
    n++;
  }
}

// ---- Pacote da equipe do dist com a amostra (se existir): decifra pelo caminho puro ----
const pacotePath = path.join(aqui, "../dist/dados/equipe.enc");
const versaoPath = path.join(aqui, "../dist/dados/versao.json");
let msEquipe = null;
if (existsSync(pacotePath) && existsSync(versaoPath) && JSON.parse(readFileSync(versaoPath, "utf-8")).amostra_sintetica) {
  const pacote = JSON.parse(readFileSync(pacotePath, "utf-8"));
  const senha = process.env.APP_SENHA_EQUIPE || "teste amostra";
  OEV.usaWebCrypto(true);
  const nativo = await OEV.decifraEquipe(pacote, senha);
  OEV.usaWebCrypto(false);
  t0 = performance.now();
  const puro = await OEV.decifraEquipe(pacote, senha);
  msEquipe = performance.now() - t0;
  await assert.rejects(() => OEV.decifraEquipe(pacote, "senha errada"));
  OEV.usaWebCrypto(true);
  assert.deepEqual(puro, nativo, "pacote da equipe: mesmo conteúdo nos dois caminhos");
  assert.ok(Array.isArray(puro.eleitores) && puro.eleitores.length > 100);
  n++;
} else {
  console.log("  (app/dist com a amostra não existe: pulei o pacote da equipe)");
}

// ---- sobeParaHTTPS: só age em http:// fora de localhost ----
globalThis.location = { protocol: "https:", hostname: "dublineleicoes2026.com.br", host: "dublineleicoes2026.com.br", pathname: "/", search: "", hash: "" };
assert.equal(OEV.sobeParaHTTPS(), false, "já em https: nada");
globalThis.location = { protocol: "http:", hostname: "localhost", host: "localhost:8765", pathname: "/", search: "", hash: "" };
assert.equal(OEV.sobeParaHTTPS(), false, "localhost: nada");
globalThis.location = { protocol: "http:", hostname: "127.0.0.1", host: "127.0.0.1:8765", pathname: "/equipe/", search: "", hash: "" };
assert.equal(OEV.sobeParaHTTPS("../dados/versao.json"), false, "127.0.0.1: nada");
let sondado = null;
globalThis.fetch = (url) => { sondado = url; return Promise.reject(new Error("sem rede")); };
globalThis.location = { protocol: "http:", hostname: "dublineleicoes2026.com.br", host: "dublineleicoes2026.com.br", pathname: "/equipe/", search: "?x=1", hash: "", replace: () => assert.fail("não redireciona se a sonda falha") };
assert.equal(OEV.sobeParaHTTPS("../dados/versao.json"), true, "http num domínio: sonda");
await new Promise((r) => setTimeout(r, 10));
assert.equal(sondado, "https://dublineleicoes2026.com.br/dados/versao.json");
let destino = null;
globalThis.fetch = () => Promise.resolve({ ok: true });
globalThis.location = { protocol: "http:", hostname: "dublineleicoes2026.com.br", host: "dublineleicoes2026.com.br", pathname: "/v3/", search: "?x=1", hash: "#a", replace: (u) => { destino = u; } };
OEV.sobeParaHTTPS();
await new Promise((r) => setTimeout(r, 10));
assert.equal(destino, "https://dublineleicoes2026.com.br/v3/?x=1#a", "sonda ok: redireciona para o mesmo endereço em https");
n += 5;

console.log(`${n} casos de criptografia iguais em JavaScript puro e WebCrypto · PBKDF2 50 mil iterações em JS puro: ${msPuro.toFixed(0)} ms · cofre (100 mil): ${msCofre.toFixed(0)} ms${msEquipe == null ? "" : ` · pacote da equipe (600 mil + AES-GCM): ${msEquipe.toFixed(0)} ms`}`);
