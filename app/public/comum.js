/* Onde eu voto? — código comum às páginas do eleitor e da equipe.
 *
 * A normalização de nomes reimplementa scripts/app_normaliza.py. Os dois têm de dar o
 * mesmo resultado: app/testes confere isso sobre vetores compartilhados. Mudou aqui, mude lá.
 */
"use strict";

const OEV = (() => {
  const PARTICULAS = new Set(["DE", "DA", "DO", "DOS", "DAS", "E"]);
  const COR_LETRA = { A: "#33507E", B: "#E8C63A", C: "#DE7343" };
  const COR_TEXTO_LETRA = { A: "#FFFFFF", B: "#3F3F3F", C: "#3F3F3F" };
  const enc = new TextEncoder();

  function normalizaNome(texto) {
    if (texto == null) return "";
    let s = String(texto).normalize("NFKD").replace(/[̀-ͯ]/g, "");
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

  /* Máscara 0000 0000 0000 num <input type="text">: só dígitos, espaços inseridos ao digitar; aceita colar com pontos. */
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

  async function pbkdf2(material, sal, iteracoes, bytes) {
    const chave = await crypto.subtle.importKey("raw", material, "PBKDF2", false, ["deriveBits"]);
    return crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt: sal, iterations: iteracoes }, chave, bytes * 8);
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
             "titulo_invalido" título digitado não tem 12 dígitos;
             "titulo_errado"   há homônimos, mas o título não casa com nenhum deles;
             "nao_encontrado"  nenhuma chave do nome (completa ou primeiro+último) está no índice.
     Tenta primeiro o nome completo; se não há nada, tenta "primeiro + último", como o build indexa. */
  async function consultaPublica(indice, nomeDigitado, tituloDigitado = "") {
    const chaves = chavesNome(nomeDigitado);
    if (!chaves.length) return { estado: "incompleto" };
    const digitos = String(tituloDigitado || "").replace(/\D/g, "");
    if (String(tituloDigitado || "").trim() && digitos.length !== 12) return { estado: "titulo_invalido" };
    const titulo = digitos ? normalizaInscricao(digitos) : "";
    for (const chave of chaves) {
      const v = indice.itens[await hashPublico(chave, "", indice)];
      if (!v) continue;
      if (v !== "H") return { estado: "ok", secao: v[0], marca: v[1] || "", chave };
      if (!titulo) return { estado: "homonimo", chave };
      const vt = indice.itens[await hashPublico(chave, titulo, indice)];
      if (vt && vt !== "H") return { estado: "ok", secao: vt[0], marca: vt[1] || "", chave };
      return { estado: "titulo_errado", chave };
    }
    return { estado: "nao_encontrado" };
  }

  /* Pacote da equipe: senha -> lista de eleitores em memória. Lança em senha errada. */
  async function decifraEquipe(pacote, senha) {
    const bits = await pbkdf2(enc.encode(senha), b64bytes(pacote.sal), pacote.iteracoes, 32);
    const chave = await crypto.subtle.importKey("raw", bits, "AES-GCM", false, ["decrypt"]);
    const claro = await crypto.subtle.decrypt({ name: "AES-GCM", iv: b64bytes(pacote.iv) }, chave, b64bytes(pacote.dados));
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

  function formataTitulo(t) {
    return t ? t.replace(/(\d{4})(\d{4})(\d{4})/, "$1 $2 $3") : "";
  }

  /* ---- Mini-mapa: Ring 3 + apron + Hall 2, esquemático, com zona, porta e grupo em destaque ---- */
  function desenhaMapa(rota) {
    const s = 5; // px por metro
    const M = 14; // margem
    const HALL_W = 50.3, HALL_D = 44.4, APRON = 14, RING_W = 44, RING_D = 35, RING_X = (HALL_W - RING_W) / 2;
    const W = HALL_W * s + 2 * M, H = (HALL_D + APRON + RING_D) * s + 2 * M + 22;
    const X = (m) => M + m * s;
    const YH = (y) => M + (HALL_D - y) * s; // y do salão cresce para o norte
    const ringTop = M + (HALL_D + APRON) * s;
    const cor = COR_LETRA[rota.letra], fraco = "#C9D6E3", texto = "#042B5A", suave = "#6486A7";
    const p = [];
    p.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Esquema do caminho até a seção ${rota.secao}">`);
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
    // grupo em destaque
    const c = rota.coord_grupo;
    if (c) {
      const ext = 4 * s;
      if (rota.parede === "oeste") p.push(`<rect x="${X(0)}" y="${YH(c + 2)}" width="10" height="${ext}" fill="${texto}"/>`);
      if (rota.parede === "leste") p.push(`<rect x="${X(HALL_W) - 10}" y="${YH(c + 2)}" width="10" height="${ext}" fill="${texto}"/>`);
      if (rota.parede === "norte") p.push(`<rect x="${X(c - 2)}" y="${YH(HALL_D)}" width="${ext}" height="10" fill="${texto}"/>`);
      const lx = rota.parede === "oeste" ? X(0) + 16 : rota.parede === "leste" ? X(HALL_W) - 16 : X(c);
      const ly = rota.parede === "norte" ? YH(HALL_D) + 22 : YH(c);
      p.push(`<text x="${lx}" y="${ly}" font-size="12" font-weight="700" fill="${texto}" text-anchor="${rota.parede === "leste" ? "end" : rota.parede === "norte" ? "middle" : "start"}" dominant-baseline="middle">${esc(rota.grupo)}</text>`);
    }
    // portas na fachada sul: S2 saída, S4 A, S5 B, S6 C, S7 preferencial, S8 saída
    const portas = { S2: [7.6, "saída", null], S4: [15.8, "A", "A"], S5: [22.0, "B", "B"], S6: [28.2, "C", "C"], S7: [33.0, "pref.", null], S8: [40.0, "saída", null] };
    for (const [id, [x, rot, letra]] of Object.entries(portas)) {
      const ativa = id === rota.porta;
      const fill = ativa ? cor : letra ? "#F4F7FA" : fraco;
      p.push(`<rect x="${X(x) - 6}" y="${YH(0) - 4}" width="12" height="8" fill="${fill}" stroke="${texto}" stroke-width="${ativa ? 1.5 : 0.5}"/>`);
      p.push(`<text x="${X(x)}" y="${YH(0) + 16}" text-anchor="middle" font-size="${ativa ? 11 : 8}" font-weight="${ativa ? 800 : 400}" fill="${texto}">${id} ${esc(rot)}</text>`);
    }
    // apron: seta da cabeça da zona até a porta
    const zonaLarg = (RING_W - 3 - 2 * 1.2) / 3;
    const zonaX = { A: RING_X, B: RING_X + zonaLarg + 1.2, C: RING_X + 2 * (zonaLarg + 1.2) }; // A a oeste, C a leste
    const zx = zonaX[rota.letra];
    const portaX = portas[rota.porta][0];
    p.push(`<path d="M ${X(zx + zonaLarg / 2)} ${ringTop} L ${X(portaX)} ${YH(0) + 24}" stroke="${cor}" stroke-width="2.5" fill="none" marker-end="url(#seta)"/>`);
    p.push(`<defs><marker id="seta" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="${cor}"/></marker></defs>`);
    // Ring 3
    p.push(`<rect x="${X(RING_X)}" y="${ringTop}" width="${RING_W * s}" height="${RING_D * s}" fill="#FFFFFF" stroke="${texto}" stroke-width="1.5" stroke-dasharray="4 3"/>`);
    for (const [letra, x] of Object.entries(zonaX)) {
      const ativa = letra === rota.letra;
      p.push(`<rect x="${X(x)}" y="${ringTop}" width="${zonaLarg * s}" height="${(RING_D - 3) * s}" fill="${ativa ? cor : "#F4F7FA"}" fill-opacity="${ativa ? 0.9 : 1}" stroke="${fraco}"/>`);
      for (let i = 1; i < 6; i++) p.push(`<line x1="${X(x)}" x2="${X(x + zonaLarg)}" y1="${ringTop + i * ((RING_D - 3) * s) / 6}" y2="${ringTop + i * ((RING_D - 3) * s) / 6}" stroke="${ativa ? "#FFFFFF" : fraco}" stroke-opacity="0.6"/>`);
      p.push(`<text x="${X(x + zonaLarg / 2)}" y="${ringTop + (RING_D - 3) * s / 2}" text-anchor="middle" dominant-baseline="middle" font-size="26" font-weight="800" fill="${ativa ? COR_TEXTO_LETRA[letra] : "#9DB0C4"}">${letra}</text>`);
    }
    // corredor de chegada (leste) e trecho de fundo
    p.push(`<rect x="${X(RING_X + RING_W - 3)}" y="${ringTop}" width="${3 * s}" height="${RING_D * s}" fill="#EEF3F8"/>`);
    p.push(`<rect x="${X(RING_X)}" y="${ringTop + (RING_D - 3) * s}" width="${RING_W * s}" height="${3 * s}" fill="#EEF3F8"/>`);
    p.push(`<path d="M ${X(RING_X + RING_W - 1.5)} ${ringTop + 4} L ${X(RING_X + RING_W - 1.5)} ${ringTop + (RING_D - 1.5) * s} L ${X(zx + zonaLarg / 2)} ${ringTop + (RING_D - 1.5) * s} L ${X(zx + zonaLarg / 2)} ${ringTop + (RING_D - 3) * s - 2}" stroke="${texto}" stroke-width="1.5" fill="none" stroke-dasharray="3 3"/>`);
    p.push(`<text x="${X(RING_X + RING_W - 1.5)}" y="${ringTop - 4}" text-anchor="middle" font-size="9" fill="${texto}">entrada ▼</text>`);
    p.push(`<text x="${X(HALL_W / 2)}" y="${H - 6}" text-anchor="middle" font-size="9" fill="${suave}">Ring 3 (pátio de fila) · esquema sem escala · norte para cima</text>`);
    p.push(`</svg>`);
    return p.join("");
  }

  /* ---- Cartão de resultado + passos, comum às duas páginas ---- */
  function renderRota(rota, opcoes = {}) {
    const cor = COR_LETRA[rota.letra], corTexto = COR_TEXTO_LETRA[rota.letra];
    const extra = opcoes.cabecalhoExtra || "";
    const passos = rota.passos.map((p) => `<li><b>${esc(p.onde)}</b><span>${esc(p.texto)}</span></li>`).join("");
    return `
      <div class="cartao" style="--cor:${cor};--cor-texto:${corTexto}">
        ${extra}
        <div class="cartao-letra"><span class="letra">${rota.letra}</span>
          <div><div class="rotulo">sua fila e sua porta</div><div class="grande">Porta ${esc(rota.porta)} · parede ${esc(rota.parede)}</div></div></div>
        <div class="cartao-linha"><div><div class="rotulo">seção</div><div class="grande">${esc(rota.secao)}</div></div>
          <div><div class="rotulo">grupo de mesas</div><div class="grande">${esc(rota.grupo)}</div></div>
          <div><div class="rotulo">seções do grupo</div><div class="medio">${rota.secoes_do_grupo.map(esc).join(" · ")}</div></div></div>
      </div>
      <ol class="passos">${passos}</ol>
      <div class="mapa">${desenhaMapa(rota)}</div>
      <p class="nota">Idoso, gestante, pessoa com deficiência ou com acompanhante: <b>entrada preferencial S7</b>, sem fila, por qualquer porta.</p>`;
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

  return { normalizaNome, chavesNome, normalizaData, normalizaInscricao, mascaraData, mascaraTitulo, hashPublico, consultaPublica,
           decifraEquipe, buscaEquipe, marcasTurno, carregaJSON, esc, formataData, formataTitulo, desenhaMapa, renderRota,
           rotaDaSecao, registraSW, COR_LETRA };
})();

if (typeof module !== "undefined") module.exports = OEV;
