/* Onde eu voto? — código comum às páginas do eleitor, da equipe e do administrador (v3).
 *
 * A normalização de nomes reimplementa scripts/app_normaliza.py. Os dois têm de dar o
 * mesmo resultado: app/testes confere isso sobre vetores compartilhados. Mudou aqui, mude lá.
 */
"use strict";

const OEV = (() => {
  const PARTICULAS = new Set(["DE", "DA", "DO", "DOS", "DAS", "E"]);
  const COR_LETRA = { A: "#33507E", B: "#E8C63A", C: "#DE7343" };
  const COR_TEXTO_LETRA = { A: "#FFFFFF", B: "#3F3F3F", C: "#3F3F3F" };
  /* Parede do salão na perspectiva de quem entra pelas portas S4/S5/S6 (reserva para rotas sem parede_rotulo). */
  const ROTULO_PAREDE = { oeste: "da esquerda", norte: "do fundo", leste: "da direita" };
  const enc = new TextEncoder();

  function normalizaNome(texto) {
    if (texto == null) return "";
    let s = String(texto).normalize("NFKD").replace(/[\u0300-\u036f]/g, "");
    s = s.toUpperCase().replace(/['’`´]/g, "");
    s = s.replace(/[^A-Z0-9]+/g, " ");
    return s.split(" ").filter((p) => p && !PARTICULAS.has(p)).join(" ");
  }

  function chavesNome(texto) {
    const completo = normalizaNome(texto);
    if (!completo) return [];
    const chaves = [completo];
    const partes = completo.split(" ");
    if (partes.length >= 3) {
      const curta = `${partes[0]} ${partes[partes.length - 1]}`;
      if (curta !== completo) chaves.push(curta);
    }
    return chaves;
  }

  function normalizaData(valor) {
    if (!valor) return "";
    const s = String(valor).trim();
    let m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/);
    let a, me, d;
    if (m) [, a, me, d] = m;
    else {
      m = s.match(/^(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})/) || s.match(/^(\d{2})(\d{2})(\d{4})$/);
      if (!m) return "";
      [, d, me, a] = m;
    }
    const dt = new Date(Date.UTC(+a, +me - 1, +d));
    if (dt.getUTCFullYear() !== +a || dt.getUTCMonth() !== +me - 1 || dt.getUTCDate() !== +d) return "";
    return `${a}-${String(me).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
  }

  /* Título de eleitor -> 12 dígitos com zeros à esquerda (reimplementa normaliza_inscricao). */
  function normalizaInscricao(valor) {
    if (valor == null) return "";
    const d = String(valor).trim().replace(/\.0+$/, "").replace(/\D/g, "");
    return d ? d.padStart(12, "0") : "";
  }

  /* Título PARCIAL (v2): só os dígitos 5 a 8. Aceita os 4 dígitos ou o número completo de 8 a 12
     dígitos (extrai os 4 aqui, no aparelho). Reimplementa titulo_parcial. */
  const TITULO_JANELA = [5, 8];
  function tituloParcial(valor) {
    if (valor == null) return "";
    const d = String(valor).trim().replace(/\.0+$/, "").replace(/\D/g, "");
    if (d.length === 4) return d;
    if (d.length >= 8 && d.length <= 12) return d.padStart(12, "0").slice(TITULO_JANELA[0] - 1, TITULO_JANELA[1]);
    return "";
  }

  /* Máscara 0000 0000 0000 num <input type="text">: só dígitos, espaços inseridos ao digitar; aceita colar com pontos.
     Com 4 dígitos (só a parte do meio) fica "0000". */
  function mascaraTitulo(el) {
    const aplica = () => {
      const d = el.value.replace(/\D/g, "").slice(0, 12);
      const v = d.replace(/(\d{4})(?=\d)/g, "$1 ");
      if (v !== el.value) el.value = v;
    };
    el.addEventListener("input", aplica);
    el.addEventListener("blur", aplica);
    return el;
  }

  /* Máscara DD/MM/AAAA num <input type="text">: só dígitos, barras inseridas ao digitar; aceita colar 23101967 ou 23.10.1967. */
  function mascaraData(el) {
    const aplica = () => {
      const d = el.value.replace(/\D/g, "").slice(0, 8);
      let v = d;
      if (d.length > 4) v = `${d.slice(0, 2)}/${d.slice(2, 4)}/${d.slice(4)}`;
      else if (d.length > 2) v = `${d.slice(0, 2)}/${d.slice(2)}`;
      if (v !== el.value) el.value = v;
    };
    el.addEventListener("input", aplica);
    el.addEventListener("blur", aplica);
    return el;
  }

  function b64url(bytes) {
    let s = "";
    for (const b of new Uint8Array(bytes)) s += String.fromCharCode(b);
    return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  function b64bytes(s) {
    const bin = atob(s);
    const out = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  /* ---- Criptografia: WebCrypto quando existe; senão, JavaScript puro ----
     O navegador só expõe crypto.subtle em "contexto seguro" (https://, localhost ou arquivo local).
     Aberta por http:// num domínio de verdade, a página quebrava na consulta com
     "Cannot read properties of undefined (reading 'importKey')" (02/10/2026, dublineleicoes2026.com.br).
     Daqui para baixo: SHA-256, HMAC, PBKDF2 e AES-GCM em JavaScript puro, usados SÓ quando não há
     crypto.subtle. Dão byte a byte o mesmo resultado (app/testes/cripto.test.mjs confere contra o WebCrypto
     do Node). São mais lentos: ~1 s por hash do índice num celular médio, contra ~0,1 s no nativo. */
  const SUBTLE_NATIVO = typeof crypto !== "undefined" && crypto.subtle ? crypto.subtle : null;
  let subtle = SUBTLE_NATIVO;
  function temWebCrypto() { return !!subtle; }
  /* Para testes: força o caminho em JavaScript puro (false) ou volta ao nativo (true). */
  function usaWebCrypto(sim) { subtle = sim ? SUBTLE_NATIVO : null; return !!subtle; }

  function bytesDe(x) {
    if (x instanceof Uint8Array) return x;
    if (x instanceof ArrayBuffer) return new Uint8Array(x);
    if (ArrayBuffer.isView(x)) return new Uint8Array(x.buffer, x.byteOffset, x.byteLength);
    throw new TypeError("esperava bytes");
  }

  function bytesAleatorios(n) {
    if (typeof crypto !== "undefined" && crypto.getRandomValues) return crypto.getRandomValues(new Uint8Array(n));
    throw new Error("este navegador não gera números aleatórios seguros");
  }

  /* -- SHA-256 (FIPS 180-4), por blocos de 16 palavras de 32 bits -- */
  const K256 = new Uint32Array([
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
  ]);
  const H256_INICIAL = new Uint32Array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]);
  const W256 = new Uint32Array(64);

  /* Comprime um bloco (m: Uint32Array de 16 palavras, big-endian) sobre o estado h (8 palavras), no lugar. */
  function sha256Bloco(h, m) {
    const w = W256;
    for (let i = 0; i < 16; i++) w[i] = m[i];
    for (let i = 16; i < 64; i++) {
      const a = w[i - 15], b = w[i - 2];
      const s0 = ((a >>> 7) | (a << 25)) ^ ((a >>> 18) | (a << 14)) ^ (a >>> 3);
      const s1 = ((b >>> 17) | (b << 15)) ^ ((b >>> 19) | (b << 13)) ^ (b >>> 10);
      w[i] = (w[i - 16] + s0 + w[i - 7] + s1) | 0;
    }
    let a = h[0], b = h[1], c = h[2], d = h[3], e = h[4], f = h[5], g = h[6], k = h[7];
    for (let i = 0; i < 64; i++) {
      const S1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
      const ch = (e & f) ^ (~e & g);
      const t1 = (k + S1 + ch + K256[i] + w[i]) | 0;
      const S0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
      const maj = (a & b) ^ (a & c) ^ (b & c);
      const t2 = (S0 + maj) | 0;
      k = g; g = f; f = e; e = (d + t1) | 0; d = c; c = b; b = a; a = (t1 + t2) | 0;
    }
    h[0] = (h[0] + a) | 0; h[1] = (h[1] + b) | 0; h[2] = (h[2] + c) | 0; h[3] = (h[3] + d) | 0;
    h[4] = (h[4] + e) | 0; h[5] = (h[5] + f) | 0; h[6] = (h[6] + g) | 0; h[7] = (h[7] + k) | 0;
  }

  /* Bytes -> blocos de 16 palavras já com o padding do SHA-256 (0x80, zeros, tamanho em bits). */
  function sha256Blocos(bytes) {
    const n = bytes.length, total = ((n + 8) >> 6) + 1;
    const buf = new Uint8Array(total * 64);
    buf.set(bytes);
    buf[n] = 0x80;
    const bits = n * 8;
    buf[total * 64 - 4] = (bits >>> 24) & 0xff; buf[total * 64 - 3] = (bits >>> 16) & 0xff;
    buf[total * 64 - 2] = (bits >>> 8) & 0xff; buf[total * 64 - 1] = bits & 0xff;
    buf[total * 64 - 8] = Math.floor(bits / 0x100000000) & 0xff; // tamanhos acima de 512 MiB não acontecem aqui
    const dv = new DataView(buf.buffer);
    const blocos = [];
    for (let b = 0; b < total; b++) {
      const m = new Uint32Array(16);
      for (let i = 0; i < 16; i++) m[i] = dv.getUint32(b * 64 + i * 4);
      blocos.push(m);
    }
    return blocos;
  }

  function palavrasParaBytes(h) {
    const out = new Uint8Array(h.length * 4);
    for (let i = 0; i < h.length; i++) { out[4 * i] = h[i] >>> 24; out[4 * i + 1] = (h[i] >>> 16) & 0xff; out[4 * i + 2] = (h[i] >>> 8) & 0xff; out[4 * i + 3] = h[i] & 0xff; }
    return out;
  }

  function sha256Puro(bytes) {
    const h = new Uint32Array(H256_INICIAL);
    for (const m of sha256Blocos(bytesDe(bytes))) sha256Bloco(h, m);
    return palavrasParaBytes(h);
  }

  /* HMAC-SHA256 com os estados internos (ipad/opad) pré-computados: o PBKDF2 reaproveita. */
  function hmacSha256Estado(chave) {
    let k = bytesDe(chave);
    if (k.length > 64) k = sha256Puro(k);
    const ipad = new Uint32Array(16), opad = new Uint32Array(16);
    const kb = new Uint8Array(64); kb.set(k);
    for (let i = 0; i < 16; i++) {
      const w = (kb[4 * i] << 24) | (kb[4 * i + 1] << 16) | (kb[4 * i + 2] << 8) | kb[4 * i + 3];
      ipad[i] = w ^ 0x36363636; opad[i] = w ^ 0x5c5c5c5c;
    }
    const hi = new Uint32Array(H256_INICIAL), ho = new Uint32Array(H256_INICIAL);
    sha256Bloco(hi, ipad); sha256Bloco(ho, opad);
    return { hi, ho };
  }

  /* HMAC de uma mensagem qualquer (comprimento em bits inclui o bloco do pad: +512). */
  function hmacSha256(estado, mensagem) {
    const msg = bytesDe(mensagem);
    const h = new Uint32Array(estado.hi);
    const blocos = sha256Blocos(msg);
    // corrige o tamanho: o padding foi feito para `msg` sozinha; o HMAC tem 64 bytes de pad antes
    const ultimo = blocos[blocos.length - 1];
    const bits = (msg.length + 64) * 8;
    ultimo[14] = Math.floor(bits / 0x100000000) >>> 0; ultimo[15] = bits >>> 0;
    for (const m of blocos) sha256Bloco(h, m);
    return hmacExterno(estado, h);
  }

  const BLOCO_32 = new Uint32Array(16);
  /* Passo externo do HMAC sobre um resumo interno de 32 bytes (8 palavras); devolve 8 palavras. */
  function hmacExterno(estado, interno) {
    const m = BLOCO_32;
    for (let i = 0; i < 8; i++) m[i] = interno[i];
    m[8] = 0x80000000; for (let i = 9; i < 15; i++) m[i] = 0; m[15] = 768; // (64 + 32) bytes * 8 bits
    const h = new Uint32Array(estado.ho);
    sha256Bloco(h, m);
    return h;
  }

  /* PBKDF2-HMAC-SHA256 (RFC 8018) -> Uint8Array de `bytes`. */
  function pbkdf2Puro(senha, sal, iteracoes, bytes) {
    const estado = hmacSha256Estado(senha);
    const s = bytesDe(sal);
    const nBlocos = Math.ceil(bytes / 32);
    const out = new Uint8Array(nBlocos * 32);
    const m = new Uint32Array(16);
    for (let b = 1; b <= nBlocos; b++) {
      const salI = new Uint8Array(s.length + 4);
      salI.set(s); salI[s.length] = b >>> 24; salI[s.length + 1] = (b >>> 16) & 0xff; salI[s.length + 2] = (b >>> 8) & 0xff; salI[s.length + 3] = b & 0xff;
      let u = hmacSha256(estado, salI);
      const t = new Uint32Array(u);
      for (let i = 1; i < iteracoes; i++) {
        // HMAC(u): interno = SHA256(ipad-estado, u || pad), externo = SHA256(opad-estado, interno || pad)
        for (let j = 0; j < 8; j++) m[j] = u[j];
        m[8] = 0x80000000; for (let j = 9; j < 15; j++) m[j] = 0; m[15] = 768;
        const h = new Uint32Array(estado.hi);
        sha256Bloco(h, m);
        u = hmacExterno(estado, h);
        for (let j = 0; j < 8; j++) t[j] ^= u[j];
      }
      out.set(palavrasParaBytes(t), (b - 1) * 32);
    }
    return out.slice(0, bytes);
  }

  /* -- AES (FIPS 197), só cifra de bloco: é o que o GCM usa nos dois sentidos -- */
  const AES_SBOX = new Uint8Array(256);
  (function geraSbox() {
    let p = 1, q = 1;
    do {
      p = p ^ ((p << 1) & 0xff) ^ (p & 0x80 ? 0x1b : 0); // p *= 3
      q ^= q << 1; q ^= q << 2; q ^= q << 4; q &= 0xff; if (q & 0x80) q ^= 0x09; // q /= 3
      const x = q ^ ((q << 1) | (q >>> 7)) ^ ((q << 2) | (q >>> 6)) ^ ((q << 3) | (q >>> 5)) ^ ((q << 4) | (q >>> 4));
      AES_SBOX[p] = (x ^ 0x63) & 0xff;
    } while (p !== 1);
    AES_SBOX[0] = 0x63;
  })();

  function aesExpandeChave(chave) {
    const k = bytesDe(chave), nk = k.length / 4;
    if (![4, 6, 8].includes(nk)) throw new Error("chave AES de tamanho inválido");
    const nr = nk + 6, w = new Uint8Array(16 * (nr + 1));
    w.set(k);
    let rcon = 1;
    for (let i = nk; i < 4 * (nr + 1); i++) {
      let t0 = w[4 * (i - 1)], t1 = w[4 * (i - 1) + 1], t2 = w[4 * (i - 1) + 2], t3 = w[4 * (i - 1) + 3];
      if (i % nk === 0) {
        [t0, t1, t2, t3] = [AES_SBOX[t1] ^ rcon, AES_SBOX[t2], AES_SBOX[t3], AES_SBOX[t0]];
        rcon = (rcon << 1) ^ (rcon & 0x80 ? 0x11b : 0);
      } else if (nk > 6 && i % nk === 4) {
        [t0, t1, t2, t3] = [AES_SBOX[t0], AES_SBOX[t1], AES_SBOX[t2], AES_SBOX[t3]];
      }
      w[4 * i] = w[4 * (i - nk)] ^ t0; w[4 * i + 1] = w[4 * (i - nk) + 1] ^ t1;
      w[4 * i + 2] = w[4 * (i - nk) + 2] ^ t2; w[4 * i + 3] = w[4 * (i - nk) + 3] ^ t3;
    }
    return { w, nr };
  }

  const xtime = (b) => ((b << 1) ^ (b & 0x80 ? 0x1b : 0)) & 0xff;
  /* Cifra um bloco de 16 bytes (entrada `e`, saída `s`, podem ser o mesmo array). */
  function aesCifraBloco(ch, e, s) {
    const { w, nr } = ch;
    const st = new Uint8Array(16);
    for (let i = 0; i < 16; i++) st[i] = e[i] ^ w[i];
    for (let r = 1; r <= nr; r++) {
      for (let i = 0; i < 16; i++) st[i] = AES_SBOX[st[i]];
      // ShiftRows (estado por colunas: st[c*4 + linha])
      let t = st[1]; st[1] = st[5]; st[5] = st[9]; st[9] = st[13]; st[13] = t;
      t = st[2]; st[2] = st[10]; st[10] = t; t = st[6]; st[6] = st[14]; st[14] = t;
      t = st[15]; st[15] = st[11]; st[11] = st[7]; st[7] = st[3]; st[3] = t;
      if (r !== nr) {
        for (let c = 0; c < 16; c += 4) {
          const a0 = st[c], a1 = st[c + 1], a2 = st[c + 2], a3 = st[c + 3], x = a0 ^ a1 ^ a2 ^ a3;
          st[c] ^= x ^ xtime(a0 ^ a1); st[c + 1] ^= x ^ xtime(a1 ^ a2); st[c + 2] ^= x ^ xtime(a2 ^ a3); st[c + 3] ^= x ^ xtime(a3 ^ a0);
        }
      }
      for (let i = 0; i < 16; i++) st[i] ^= w[16 * r + i];
    }
    s.set(st);
  }

  /* -- GCM (NIST SP 800-38D), IV de 12 bytes, tag de 16, sem dados associados: o que o app usa -- */
  function gfMul(x, h) { // x, h: 4 palavras big-endian; devolve x·h em GF(2^128)
    let z0 = 0, z1 = 0, z2 = 0, z3 = 0, v0 = h[0], v1 = h[1], v2 = h[2], v3 = h[3];
    for (let i = 0; i < 128; i++) {
      if ((x[i >>> 5] >>> (31 - (i & 31))) & 1) { z0 ^= v0; z1 ^= v1; z2 ^= v2; z3 ^= v3; }
      const lsb = v3 & 1;
      v3 = (v3 >>> 1) | ((v2 & 1) << 31); v2 = (v2 >>> 1) | ((v1 & 1) << 31); v1 = (v1 >>> 1) | ((v0 & 1) << 31); v0 >>>= 1;
      if (lsb) v0 ^= 0xe1000000;
    }
    x[0] = z0 >>> 0; x[1] = z1 >>> 0; x[2] = z2 >>> 0; x[3] = z3 >>> 0;
  }

  function ghash(h, dados, comprimentoBits) {
    const y = new Uint32Array(4), n = dados.length;
    const bloco = new Uint8Array(16);
    for (let p = 0; p < n; p += 16) {
      bloco.fill(0); bloco.set(dados.subarray(p, Math.min(p + 16, n)));
      for (let i = 0; i < 4; i++) y[i] ^= (bloco[4 * i] << 24) | (bloco[4 * i + 1] << 16) | (bloco[4 * i + 2] << 8) | bloco[4 * i + 3];
      gfMul(y, h);
    }
    y[2] ^= Math.floor(comprimentoBits / 0x100000000) >>> 0; y[3] ^= comprimentoBits >>> 0; // len(A)=0 || len(C)
    gfMul(y, h);
    return palavrasParaBytes(y);
  }

  function gcmNucleo(chaveBytes, iv, entrada) {
    iv = bytesDe(iv);
    if (iv.length !== 12) throw new Error("GCM em JavaScript puro só com IV de 12 bytes");
    const ch = aesExpandeChave(chaveBytes);
    const hb = new Uint8Array(16); aesCifraBloco(ch, new Uint8Array(16), hb);
    const h = new Uint32Array(4);
    for (let i = 0; i < 4; i++) h[i] = ((hb[4 * i] << 24) | (hb[4 * i + 1] << 16) | (hb[4 * i + 2] << 8) | hb[4 * i + 3]) >>> 0;
    const j0 = new Uint8Array(16); j0.set(iv); j0[15] = 1;
    const ej0 = new Uint8Array(16); aesCifraBloco(ch, j0, ej0);
    const ctr = new Uint8Array(j0), ks = new Uint8Array(16), saida = new Uint8Array(entrada.length);
    for (let p = 0; p < entrada.length; p += 16) {
      for (let i = 15; i >= 12; i--) { ctr[i] = (ctr[i] + 1) & 0xff; if (ctr[i] !== 0) break; } // inc32
      aesCifraBloco(ch, ctr, ks);
      const fim = Math.min(p + 16, entrada.length);
      for (let i = p; i < fim; i++) saida[i] = entrada[i] ^ ks[i - p];
    }
    return { h, ej0, saida };
  }

  function tagGcm(h, ej0, cifrado) {
    const t = ghash(h, cifrado, cifrado.length * 8);
    for (let i = 0; i < 16; i++) t[i] ^= ej0[i];
    return t;
  }

  function aesGcmCifraPuro(chaveBytes, iv, claro) {
    const { h, ej0, saida } = gcmNucleo(chaveBytes, iv, bytesDe(claro));
    const out = new Uint8Array(saida.length + 16);
    out.set(saida); out.set(tagGcm(h, ej0, saida), saida.length);
    return out;
  }

  function aesGcmDecifraPuro(chaveBytes, iv, cifradoComTag) {
    const c = bytesDe(cifradoComTag);
    if (c.length < 16) throw new Error("dados cifrados curtos demais");
    const cifrado = c.subarray(0, c.length - 16), tag = c.subarray(c.length - 16);
    const { h, ej0, saida } = gcmNucleo(chaveBytes, iv, cifrado);
    const esperada = tagGcm(h, ej0, cifrado);
    let dif = 0;
    for (let i = 0; i < 16; i++) dif |= esperada[i] ^ tag[i];
    if (dif) throw new Error("não foi possível decifrar: senha errada ou dados alterados");
    return saida;
  }

  /* -- Fachada: o resto do código só chama estas quatro -- */
  async function pbkdf2(material, sal, iteracoes, bytes) {
    material = bytesDe(material); sal = bytesDe(sal);
    if (!subtle) return pbkdf2Puro(material, sal, iteracoes, bytes);
    const chave = await subtle.importKey("raw", material, "PBKDF2", false, ["deriveBits"]);
    return new Uint8Array(await subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt: sal, iterations: iteracoes }, chave, bytes * 8));
  }

  async function aesGcmCifra(chaveBytes, iv, claro) {
    if (!subtle) return aesGcmCifraPuro(chaveBytes, iv, claro);
    const k = await subtle.importKey("raw", bytesDe(chaveBytes), "AES-GCM", false, ["encrypt"]);
    return new Uint8Array(await subtle.encrypt({ name: "AES-GCM", iv: bytesDe(iv) }, k, bytesDe(claro)));
  }

  async function aesGcmDecifra(chaveBytes, iv, cifradoComTag) {
    if (!subtle) return aesGcmDecifraPuro(chaveBytes, iv, cifradoComTag);
    const k = await subtle.importKey("raw", bytesDe(chaveBytes), "AES-GCM", false, ["decrypt"]);
    return new Uint8Array(await subtle.decrypt({ name: "AES-GCM", iv: bytesDe(iv) }, k, bytesDe(cifradoComTag)));
  }

  /* Página aberta por http:// num domínio de verdade: tenta passar para https:// (onde há service worker,
     WebCrypto nativo e a consulta é mais rápida). Só redireciona se o https:// do mesmo endereço responde
     (sonda `arquivoSonda`, relativo à página); se não responde — certificado do GitHub Pages ainda não
     emitido, por exemplo — fica em http:// e a criptografia em JavaScript puro assume, sem erro ao eleitor.
     Devolve true se a sonda foi disparada. */
  function sobeParaHTTPS(arquivoSonda = "./dados/versao.json", limiteMs = 2500) {
    try {
      if (typeof location === "undefined" || location.protocol !== "http:") return false;
      if (/^(localhost|127\.|0\.0\.0\.0|\[::1\])/.test(location.hostname)) return false;
      const pagina = `https://${location.host}${location.pathname}`;
      const destino = `${pagina}${location.search}${location.hash}`;
      const sonda = new URL(arquivoSonda, pagina).href;
      const ctl = typeof AbortController !== "undefined" ? new AbortController() : null;
      const timer = ctl && setTimeout(() => ctl.abort(), limiteMs);
      fetch(sonda, { mode: "cors", cache: "no-store", signal: ctl ? ctl.signal : undefined })
        .then((r) => { if (r.ok) location.replace(destino); })
        .catch(() => {})
        .finally(() => { if (timer) clearTimeout(timer); });
      return true;
    } catch (e) {
      return false;
    }
  }

  /* Hash do índice público: só a chave do nome, ou "CHAVE|FATOR" quando há fator (o título, em homônimos).
     Tem de dar o mesmo resultado que hash_publico em app_normaliza.py. */
  async function hashPublico(chave, segundoFator, indice) {
    const material = segundoFator ? `${chave}|${segundoFator}` : chave;
    const bits = await pbkdf2(enc.encode(material), enc.encode(indice.sal), indice.iteracoes, indice.bytes);
    return b64url(bits);
  }

  /* Consulta pública (índice v2, só por nome): nome digitado [+ título] -> {estado, secao, marca}.
     estado: "incompleto"      nome vazio;
             "ok"              uma pessoa: secao (e marca de turno, se a lista não diz "OK");
             "homonimo"        mais de uma pessoa com esse nome: peça o título;
             "titulo_invalido" título digitado não tem 4 dígitos (os do meio) nem 8 a 12 (completo);
             "titulo_errado"   há homônimos, mas o título não casa com nenhum deles;
             "sem_desempate"   homônimos com o mesmo título parcial: o app não separa, manda ao P0;
             "nao_encontrado"  nenhuma chave do nome (completa ou primeiro+último) está no índice.
     Tenta primeiro o nome completo; se não há nada, tenta "primeiro + último", como o build indexa. */
  async function consultaPublica(indice, nomeDigitado, tituloDigitado = "") {
    const chaves = chavesNome(nomeDigitado);
    if (!chaves.length) return { estado: "incompleto" };
    const titulo = tituloParcial(tituloDigitado);
    if (String(tituloDigitado || "").trim() && !titulo) return { estado: "titulo_invalido" };
    for (const chave of chaves) {
      const v = indice.itens[await hashPublico(chave, "", indice)];
      if (!v) continue;
      if (v !== "H") return { estado: "ok", secao: v[0], marca: v[1] || "", chave };
      if (!titulo) return { estado: "homonimo", chave };
      const vt = indice.itens[await hashPublico(chave, titulo, indice)];
      if (vt === "P") return { estado: "sem_desempate", chave };
      if (vt && vt !== "H") return { estado: "ok", secao: vt[0], marca: vt[1] || "", chave };
      return { estado: "titulo_errado", chave };
    }
    return { estado: "nao_encontrado" };
  }

  /* Pacote da equipe: senha -> lista de eleitores em memória. Lança em senha errada. */
  async function decifraEquipe(pacote, senha) {
    const bits = await pbkdf2(enc.encode(senha), b64bytes(pacote.sal), pacote.iteracoes, 32);
    const claro = await aesGcmDecifra(bits, b64bytes(pacote.iv), b64bytes(pacote.dados));
    const ds = new DecompressionStream("deflate");
    const fluxo = new Blob([claro]).stream().pipeThrough(ds);
    const texto = await new Response(fluxo).text();
    return JSON.parse(texto);
  }

  /* Busca da equipe: cada palavra digitada tem de aparecer como prefixo de alguma palavra do nome.
     Homônimos saem lado a lado, ordenados por nome e título; o título de cada um é o que os distingue. */
  function buscaEquipe(eleitores, texto, limite = 30) {
    const termos = normalizaNome(texto).split(" ").filter(Boolean);
    if (!termos.length) return [];
    const achados = [];
    for (const e of eleitores) {
      const palavras = e.n.split(" ");
      if (termos.every((t) => palavras.some((p) => p.startsWith(t)))) {
        achados.push(e);
        if (achados.length >= limite * 4) break;
      }
    }
    achados.sort((a, b) => (a.n === b.n ? a.t.localeCompare(b.t) : a.n.localeCompare(b.n)));
    return achados.slice(0, limite);
  }

  /* Marcas de turno da lista do TRE ("OK", "VT", ...) para a equipe: vazio quando os dois turnos são OK. */
  function marcasTurno(e) {
    const m = [];
    if (e.t1 && e.t1 !== "OK") m.push(`1º turno: ${e.t1}`);
    if (e.t2 && e.t2 !== "OK") m.push(`2º turno: ${e.t2}`);
    return m.join(" · ");
  }

  async function carregaJSON(url) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(`${url}: HTTP ${r.status}`);
    return r.json();
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function formataData(iso) {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
    return m ? `${m[3]}/${m[2]}/${m[1]}` : iso || "";
  }

  /* 4 dígitos (título parcial, v2) -> "···· 1234 ····"; 12 dígitos -> "0000 0000 0000". */
  function formataTitulo(t) {
    if (!t) return "";
    if (String(t).length === 4) return `···· ${t} ····`;
    return String(t).replace(/(\d{4})(\d{4})(\d{4})/, "$1 $2 $3");
  }

  /* Título a mostrar à equipe: o completo (campo "tc", 12 dígitos, desde 02/10) quando o pacote o traz; senão o parcial. */
  function tituloEquipe(e) {
    return (e && (e.tc || e.t)) || "";
  }

  /* ---- Mini-mapa: Ring 3 + pátio de travessia + Hall 2, esquemático, com zona, porta e grupo em destaque ---- */
  function desenhaMapa(rota) {
    const s = 5; // px por metro
    const M = 14; // margem
    const TOPO = 9; // m de faixa acima do Hall, para o portão e a chegada
    const HALL_W = 50.3, HALL_D = 44.4, PATIO = 14, RING_W = 44, RING_D = 35, RING_X = (HALL_W - RING_W) / 2;
    const W = HALL_W * s + 2 * M, H = (TOPO + HALL_D + PATIO + RING_D) * s + 2 * M + 22;
    const X = (m) => M + m * s;
    const YH = (y) => M + TOPO * s + (HALL_D - y) * s; // y do salão cresce para o fundo (para cima no desenho)
    const ringTop = M + (TOPO + HALL_D + PATIO) * s;
    const cor = COR_LETRA[rota.letra], fraco = "#C9D6E3", texto = "#042B5A", suave = "#6486A7", amarelo = "#FCC537";
    const p = [];
    const marcador = (x, y, n) => p.push(`<g data-passo="${n}"><circle cx="${x}" cy="${y}" r="8.5" fill="${texto}" stroke="${amarelo}" stroke-width="1.5"/><text x="${x}" y="${y + 0.5}" text-anchor="middle" dominant-baseline="middle" font-size="10" font-weight="800" fill="${amarelo}">${n}</text></g>`);
    p.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Esquema do caminho até o grupo de mesas ${rota.grupo}, pela porta ${rota.letra}, com os seis passos marcados">`);
    p.push(`<defs><marker id="seta" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="${cor}"/></marker></defs>`);
    // portão na Merrion Road e caminho de chegada: desce ao lado do Hall 2 (o Hall fica à direita de quem desce)
    const xChegada = X(HALL_W) + 7;
    p.push(`<text x="${xChegada}" y="${M + 8}" text-anchor="end" font-size="9" font-weight="700" fill="${texto}">portão · Merrion Road ▼</text>`);
    p.push(`<path d="M ${xChegada} ${M + 14} L ${xChegada} ${ringTop - 6} L ${X(RING_X + RING_W - 1.5)} ${ringTop - 6} L ${X(RING_X + RING_W - 1.5)} ${ringTop}" stroke="${cor}" stroke-width="2" fill="none" stroke-dasharray="5 4"/>`);
    // Hall 2
    p.push(`<rect x="${X(0)}" y="${YH(HALL_D)}" width="${HALL_W * s}" height="${HALL_D * s}" fill="#FFFFFF" stroke="${texto}" stroke-width="1.5"/>`);
    p.push(`<text x="${X(HALL_W / 2)}" y="${YH(HALL_D / 2)}" text-anchor="middle" font-size="11" fill="${suave}">HALL 2</text>`);
    // paredes com mesas
    const paredes = {
      oeste: [X(0), YH(HALL_D), 6, HALL_D * s],
      norte: [X(0), YH(HALL_D), HALL_W * s, 6],
      leste: [X(HALL_W) - 6, YH(HALL_D), 6, HALL_D * s],
    };
    for (const [nome, [x, y, w, h]] of Object.entries(paredes)) {
      p.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${nome === rota.parede ? cor : fraco}"/>`);
    }
    // grupo em destaque (passos 4 e 5)
    const c = rota.coord_grupo;
    let p4 = null, p5 = null;
    if (c) {
      const ext = 4 * s;
      if (rota.parede === "oeste") p.push(`<rect x="${X(0)}" y="${YH(c + 2)}" width="10" height="${ext}" fill="${texto}"/>`);
      if (rota.parede === "leste") p.push(`<rect x="${X(HALL_W) - 10}" y="${YH(c + 2)}" width="10" height="${ext}" fill="${texto}"/>`);
      if (rota.parede === "norte") p.push(`<rect x="${X(c - 2)}" y="${YH(HALL_D)}" width="${ext}" height="10" fill="${texto}"/>`);
      const lx = rota.parede === "oeste" ? X(0) + 16 : rota.parede === "leste" ? X(HALL_W) - 16 : X(c);
      const ly = rota.parede === "norte" ? YH(HALL_D) + 22 : YH(c);
      p.push(`<text x="${lx}" y="${ly}" font-size="12" font-weight="700" fill="${texto}" text-anchor="${rota.parede === "leste" ? "end" : rota.parede === "norte" ? "middle" : "start"}" dominant-baseline="middle">${esc(rota.grupo)}</text>`);
      if (rota.parede === "oeste") { p4 = [X(0) + 42, ly]; p5 = [X(0) + 62, ly]; }
      else if (rota.parede === "leste") { p4 = [X(HALL_W) - 42, ly]; p5 = [X(HALL_W) - 62, ly]; }
      else { p4 = [X(c), ly + 20]; p5 = [X(c), ly + 40]; }
    }
    // portas na fachada de entrada: só a letra, nunca o número da prancheta
    const portas = { S2: [7.6, "saída", null], S4: [15.8, "A", "A"], S5: [22.0, "B", "B"], S6: [28.2, "C", "C"], S7: [33.0, "pref.", null], S8: [40.0, "saída", null] };
    for (const [id, [x, rot, letra]] of Object.entries(portas)) {
      const ativa = id === rota.porta;
      const fill = ativa ? cor : letra ? "#F4F7FA" : fraco;
      p.push(`<rect x="${X(x) - 6}" y="${YH(0) - 4}" width="12" height="8" fill="${fill}" stroke="${texto}" stroke-width="${ativa ? 1.5 : 0.5}"/>`);
      p.push(`<text x="${X(x)}" y="${YH(0) + 16}" text-anchor="middle" font-size="${ativa ? 12 : 8}" font-weight="${ativa ? 800 : 400}" fill="${texto}">${esc(rot)}</text>`);
    }
    // pátio de travessia: seta da frente da fila até a porta (passo 3)
    const zonaLarg = (RING_W - 3 - 2 * 1.2) / 3;
    const zonaX = { A: RING_X, B: RING_X + zonaLarg + 1.2, C: RING_X + 2 * (zonaLarg + 1.2) }; // A à esquerda, C à direita, no desenho
    const zx = zonaX[rota.letra];
    const portaX = portas[rota.porta][0];
    const x3a = X(zx + zonaLarg / 2), y3a = ringTop, x3b = X(portaX), y3b = YH(0) + 24;
    p.push(`<path d="M ${x3a} ${y3a} L ${x3b} ${y3b}" stroke="${cor}" stroke-width="2.5" fill="none" marker-end="url(#seta)"/>`);
    // Ring 3
    p.push(`<rect x="${X(RING_X)}" y="${ringTop}" width="${RING_W * s}" height="${RING_D * s}" fill="#FFFFFF" stroke="${texto}" stroke-width="1.5" stroke-dasharray="4 3"/>`);
    for (const [letra, x] of Object.entries(zonaX)) {
      const ativa = letra === rota.letra;
      p.push(`<rect x="${X(x)}" y="${ringTop}" width="${zonaLarg * s}" height="${(RING_D - 3) * s}" fill="${ativa ? cor : "#F4F7FA"}" fill-opacity="${ativa ? 0.9 : 1}" stroke="${fraco}"/>`);
      for (let i = 1; i < 6; i++) p.push(`<line x1="${X(x)}" x2="${X(x + zonaLarg)}" y1="${ringTop + i * ((RING_D - 3) * s) / 6}" y2="${ringTop + i * ((RING_D - 3) * s) / 6}" stroke="${ativa ? "#FFFFFF" : fraco}" stroke-opacity="0.6"/>`);
      p.push(`<text x="${X(x + zonaLarg / 2)}" y="${ringTop + (RING_D - 3) * s / 2}" text-anchor="middle" dominant-baseline="middle" font-size="26" font-weight="800" fill="${ativa ? COR_TEXTO_LETRA[letra] : "#9DB0C4"}">${letra}</text>`);
    }
    // corredor de chegada e trecho de fundo (passo 2)
    const xCorredor = X(RING_X + RING_W - 1.5), yFundo = ringTop + (RING_D - 1.5) * s;
    p.push(`<rect x="${X(RING_X + RING_W - 3)}" y="${ringTop}" width="${3 * s}" height="${RING_D * s}" fill="#EEF3F8"/>`);
    p.push(`<rect x="${X(RING_X)}" y="${ringTop + (RING_D - 3) * s}" width="${RING_W * s}" height="${3 * s}" fill="#EEF3F8"/>`);
    p.push(`<path d="M ${xCorredor} ${ringTop + 4} L ${xCorredor} ${yFundo} L ${x3a} ${yFundo} L ${x3a} ${ringTop + (RING_D - 3) * s - 2}" stroke="${texto}" stroke-width="1.5" fill="none" stroke-dasharray="3 3"/>`);
    p.push(`<text x="${xCorredor - 12}" y="${ringTop - 10}" text-anchor="end" font-size="9" fill="${texto}">Ring 3: você entra aqui ▶</text>`);
    // marcadores dos seis passos
    marcador(xChegada, YH(HALL_D / 2), 1);
    marcador(x3a, yFundo, 2);
    marcador((x3a + x3b) / 2, (y3a + y3b) / 2, 3);
    if (p4) marcador(p4[0], p4[1], 4);
    if (p5) marcador(p5[0], p5[1], 5);
    const saidaX = rota.letra === "C" ? portas.S8[0] : portas.S2[0];
    marcador(X(saidaX), YH(0) - 16, 6);
    p.push(`<text x="${X(HALL_W / 2)}" y="${H - 6}" text-anchor="middle" font-size="9" fill="${suave}">Esquema sem escala · os números são os passos acima</text>`);
    p.push(`</svg>`);
    return p.join("");
  }

  /* ---- Cartão de resultado + passos, comum às duas páginas ----
     Ênfase em PORTA e GRUPO DE MESAS (decisão de 02/10/2026). A seção específica do eleitor não aparece:
     a lista do TRE vem por mesa, com as seções agregadas somadas na principal, então a seção que o build
     conhece pode não ser a que está no título dele. Logo abaixo do grupo, uma nota manda conferir a seção
     no e-Título / site do TSE (texto em opcoes.notaSecao; link em opcoes.linkTSE). */
  function renderRota(rota, opcoes = {}) {
    const cor = COR_LETRA[rota.letra], corTexto = COR_TEXTO_LETRA[rota.letra];
    const extra = opcoes.cabecalhoExtra || "";
    const passos = rota.passos.map((p) => `<li><b>${esc(p.onde)}</b><span>${esc(p.texto)}</span></li>`).join("");
    const nota = opcoes.notaSecao == null
      ? "Confira a sua seção no e-Título ou no site do TSE antes de ir votar: ela está entre as seções deste grupo, mas é a do seu título que vale na mesa."
      : opcoes.notaSecao;
    const link = opcoes.linkTSE ? ` <a href="${esc(opcoes.linkTSE)}" target="_blank" rel="noopener">Consultar no TSE</a>` : "";
    return `
      <div class="cartao" style="--cor:${cor};--cor-texto:${corTexto}">
        ${extra}
        <div class="cartao-letra"><span class="letra">${rota.letra}</span>
          <div><div class="rotulo">sua fila e sua porta de entrada</div><div class="grande">Porta ${esc(rota.letra)}</div><div class="medio">parede ${esc(rota.parede_rotulo || ROTULO_PAREDE[rota.parede] || rota.parede)}</div></div></div>
        <div class="cartao-grupo"><div class="rotulo">seu grupo de mesas</div><div class="enorme">${esc(rota.grupo)}</div>
          <div class="rotulo">seções deste grupo</div><div class="medio">${rota.secoes_do_grupo.map(esc).join(" · ")}</div></div>
        ${nota ? `<p class="nota-secao" id="nota-secao">${esc(nota)}${link}</p>` : ""}
      </div>
      <ol class="passos">${passos}</ol>
      <div class="mapa">${desenhaMapa(rota)}</div>
      <p class="nota">Idoso, gestante, pessoa com deficiência ou com acompanhante: <b>entrada PREFERENCIAL</b>, a porta logo à direita da porta C, sem fila.</p>`;
  }

  function rotaDaSecao(rotas, secao) {
    const r = rotas.secoes[secao];
    return r ? { ...r, coord_grupo: r.coord_grupo } : null;
  }

  async function registraSW(caminho) {
    if (!("serviceWorker" in navigator)) return;
    try {
      const reg = await navigator.serviceWorker.register(caminho);
      reg.addEventListener("updatefound", () => {
        const novo = reg.installing;
        novo && novo.addEventListener("statechange", () => {
          if (novo.state === "installed" && navigator.serviceWorker.controller) {
            const aviso = document.getElementById("aviso-versao");
            if (aviso) aviso.hidden = false;
          }
        });
      });
    } catch (e) {
      console.warn("service worker não registrado:", e);
    }
  }

  /* ---- v3: número no caderno (vem do build, campo "c"; "p" é a posição alfabética na seção) ---- */
  function textoCaderno(e) {
    if (!e || e.c == null) return "";
    return e.p != null && e.p !== e.c ? `nº ${e.c} no caderno (${e.p}º da seção)` : `nº ${e.c} no caderno`;
  }

  /* ---- v3: estimativa de espera na fila do Ring 3 ----
     pct = quanto a zona está cheia (0–100), informado pela equipe. Modelo simples e declarado:
       pessoas na fila  = pct/100 × lotação da zona (706, montagem do Ring 3)
       vazão da zona    = urnas da zona × 60 / segundos por eleitor (premissa de config.json)
       espera           = pessoas / vazão + minutos de travessia do pátio
     Devolve {minutos (arredondado), minutosExatos, pessoas, vazaoPorMin}. */
  function estimaEspera(pct, zona, cfgFila) {
    const p = Math.max(0, Math.min(100, Number(pct) || 0));
    const lotacao = Number(cfgFila.lotacao_zona) || 706;
    const seg = Number(cfgFila.segundos_por_eleitor) || 60;
    const travessia = Number(cfgFila.minutos_travessia) || 0;
    const passo = Number(cfgFila.arredonda_min) || 5;
    const urnas = Number(zona && zona.urnas) || 9;
    const pessoas = Math.round((p / 100) * lotacao);
    const vazao = (urnas * 60) / seg; // pessoas por minuto
    const exatos = pessoas / vazao + travessia;
    const minutos = Math.max(passo, Math.round(exatos / passo) * passo);
    return { minutos, minutosExatos: exatos, pessoas, vazaoPorMin: vazao, pct: p };
  }

  function horaLocal(iso) {
    const d = new Date(iso);
    return isNaN(d) ? "" : d.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
  }

  function preenche(modelo, valores) {
    return String(modelo || "").replace(/\{(\w+)\}/g, (_, k) => (valores[k] == null ? "" : String(valores[k])));
  }

  /* Bloco que aparece ao eleitor abaixo da nota da preferencial, quando o admin ativou o status da fila.
     fila = conteúdo de fila.json; rota = rota da seção; rotas.zonas = urnas por zona (do build). */
  function renderEspera(fila, rota, rotas, cfgFila, agora = Date.now()) {
    if (!fila || !fila.ativo || !rota) return "";
    const z = fila.zonas && fila.zonas[rota.letra];
    if (!z || z.pct == null || !z.em) return "";
    const hora = horaLocal(z.em);
    const idade = (agora - new Date(z.em).getTime()) / 60000;
    const validade = Number(cfgFila.validade_min) || 60;
    const est = estimaEspera(z.pct, rotas.zonas && rotas.zonas[rota.letra], cfgFila);
    const velho = idade > validade;
    const cor = COR_LETRA[rota.letra];
    const corpo = est.pct <= 0
      ? `<div class="espera-grande">poucos minutos</div><p>${esc(preenche(cfgFila.sem_fila, { letra: rota.letra, hora }))}</p>`
      : `<div class="espera-grande">cerca de ${est.minutos} min</div>
         <div class="espera-barra" aria-hidden="true"><span style="width:${est.pct}%;background:${cor}"></span></div>
         <p>${esc(preenche(cfgFila.explicacao, { letra: rota.letra, pct: est.pct, hora, seg: cfgFila.segundos_por_eleitor || 60 }))}</p>`;
    return `<div class="espera${velho ? " velha" : ""}" id="espera" data-minutos="${est.minutos}" data-pct="${est.pct}">
      <div class="rotulo">${esc(cfgFila.rotulo || "Tempo estimado de espera")} · fila ${esc(rota.letra)}</div>
      ${corpo}
      ${velho ? `<p class="espera-aviso">${esc(preenche(cfgFila.desatualizado, { hora, validade }))}</p>` : ""}
    </div>`;
  }

  /* Lê o estado vivo da fila publicado (raw.githubusercontent.com). Cache do CDN quebrado por minuto;
     devolve null se não há rede, se a resposta não é JSON ou se demora mais que `limiteMs`. */
  async function leFilaPublica(cfgFila, limiteMs = 5000) {
    if (!cfgFila || !cfgFila.url_leitura) return null;
    const sep = cfgFila.url_leitura.includes("?") ? "&" : "?";
    const url = `${cfgFila.url_leitura}${sep}t=${Math.floor(Date.now() / 60000)}`;
    const ctl = typeof AbortController !== "undefined" ? new AbortController() : null;
    const timer = ctl && setTimeout(() => ctl.abort(), limiteMs);
    try {
      const r = await fetch(url, { cache: "no-store", signal: ctl ? ctl.signal : undefined });
      if (!r.ok) return null;
      return await r.json();
    } catch (e) {
      return null;
    } finally {
      if (timer) clearTimeout(timer);
    }
  }

  /* ---- v3: escrita de fila.json pela API do GitHub (branch próprio; ver docs/app/contexto.md §2d) ----
     O token é um fine-grained PAT com "Contents: read and write" SÓ neste repositório. */
  function filaVazia() {
    return { v: 1, ativo: false, zonas: { A: { pct: null, em: null }, B: { pct: null, em: null }, C: { pct: null, em: null } }, atualizado: null };
  }

  function urlConteudo(cfgFila) {
    return `https://api.github.com/repos/${cfgFila.repo}/contents/${cfgFila.arquivo}`;
  }

  function cabecalhosGitHub(token) {
    return { Accept: "application/vnd.github+json", Authorization: `Bearer ${token}`, "X-GitHub-Api-Version": "2022-11-28" };
  }

  function utf8ParaB64(texto) {
    return btoa(String.fromCharCode(...enc.encode(texto)));
  }

  function b64ParaUtf8(b64) {
    return new TextDecoder().decode(b64bytes(String(b64).replace(/\s/g, "")));
  }

  /* Lê fila.json com o sha (necessário para gravar). 404 -> {fila: vazia, sha: null}. */
  async function leFilaAPI(cfgFila, token) {
    const r = await fetch(`${urlConteudo(cfgFila)}?ref=${encodeURIComponent(cfgFila.branch)}&t=${Date.now()}`, { headers: cabecalhosGitHub(token), cache: "no-store" });
    if (r.status === 404) return { fila: filaVazia(), sha: null };
    if (r.status === 401) throw new Error("chave de publicação inválida ou vencida (401)");
    if (!r.ok) throw new Error(`GitHub respondeu HTTP ${r.status} ao ler ${cfgFila.arquivo}`);
    const j = await r.json();
    let fila;
    try { fila = JSON.parse(b64ParaUtf8(j.content)); } catch (e) { fila = filaVazia(); }
    return { fila: { ...filaVazia(), ...fila, zonas: { ...filaVazia().zonas, ...(fila.zonas || {}) } }, sha: j.sha };
  }

  /* Lê, aplica `mutador(fila)` e grava; repete até 3 vezes se outra pessoa gravou no meio (409/422). */
  async function publicaFila(cfgFila, token, mutador, mensagem = "fila: atualização pela equipe") {
    let erro = null;
    for (let tentativa = 0; tentativa < 3; tentativa++) {
      const { fila, sha } = await leFilaAPI(cfgFila, token);
      const nova = mutador(JSON.parse(JSON.stringify(fila))) || fila;
      nova.atualizado = new Date().toISOString();
      const corpo = { message: mensagem, content: utf8ParaB64(JSON.stringify(nova, null, 1) + "\n"), branch: cfgFila.branch };
      if (sha) corpo.sha = sha;
      const r = await fetch(urlConteudo(cfgFila), { method: "PUT", headers: { ...cabecalhosGitHub(token), "Content-Type": "application/json" }, body: JSON.stringify(corpo) });
      if (r.ok) return nova;
      if (r.status === 409 || r.status === 422) { erro = new Error(`conflito ao gravar (HTTP ${r.status}); tentando de novo`); continue; }
      if (r.status === 401) throw new Error("chave de publicação inválida ou vencida (401)");
      if (r.status === 403) throw new Error("a chave de publicação não tem permissão de escrita neste repositório (403)");
      if (r.status === 404) throw new Error(`repositório ou branch não encontrado (404): confira ${cfgFila.repo} / ${cfgFila.branch}`);
      throw new Error(`GitHub respondeu HTTP ${r.status} ao gravar`);
    }
    throw erro || new Error("não foi possível gravar a fila");
  }

  /* ---- v3: cofre local — guarda um segredo (a chave de publicação) cifrado com uma senha, no localStorage ---- */
  const ITERACOES_COFRE = 100000;
  function chaveCofre(senha, sal) {
    return pbkdf2(enc.encode(senha), sal, ITERACOES_COFRE, 32);
  }

  async function guardaSegredo(nome, texto, senha) {
    const sal = bytesAleatorios(16), iv = bytesAleatorios(12);
    const k = await chaveCofre(senha, sal);
    const cifrado = await aesGcmCifra(k, iv, enc.encode(texto));
    const b64 = (b) => btoa(String.fromCharCode(...new Uint8Array(b)));
    localStorage.setItem(nome, JSON.stringify({ v: 1, sal: b64(sal), iv: b64(iv), dados: b64(cifrado) }));
  }

  /* Devolve o segredo, "" se não há nada guardado, e lança se a senha não abre. */
  async function leSegredo(nome, senha) {
    const bruto = localStorage.getItem(nome);
    if (!bruto) return "";
    const c = JSON.parse(bruto);
    const k = await chaveCofre(senha, b64bytes(c.sal));
    const claro = await aesGcmDecifra(k, b64bytes(c.iv), b64bytes(c.dados));
    return new TextDecoder().decode(claro);
  }

  function apagaSegredo(nome) { localStorage.removeItem(nome); }

  /* ---- v3: senha do administrador — conferida contra o hash PBKDF2 de config.json ("admin") ---- */
  async function confereAdmin(cfgAdmin, senha) {
    if (!cfgAdmin || !cfgAdmin.hash) return false;
    const bits = await pbkdf2(enc.encode(senha), enc.encode(cfgAdmin.sal), cfgAdmin.iteracoes, 32);
    return b64url(bits) === cfgAdmin.hash;
  }

  return { normalizaNome, chavesNome, normalizaData, normalizaInscricao, tituloParcial, mascaraData, mascaraTitulo, hashPublico, consultaPublica,
           decifraEquipe, buscaEquipe, marcasTurno, carregaJSON, esc, formataData, formataTitulo, tituloEquipe, desenhaMapa, renderRota,
           rotaDaSecao, registraSW, COR_LETRA,
           textoCaderno, estimaEspera, renderEspera, horaLocal, preenche, leFilaPublica, filaVazia, leFilaAPI, publicaFila,
           guardaSegredo, leSegredo, apagaSegredo, confereAdmin,
           temWebCrypto, usaWebCrypto, sobeParaHTTPS, pbkdf2, aesGcmCifra, aesGcmDecifra, sha256Puro, bytesAleatorios };
})();

if (typeof module !== "undefined") module.exports = OEV;
