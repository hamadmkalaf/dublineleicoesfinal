#!/usr/bin/env node
// Exporta as peças de mapa/sinalizacao/ em PDF vetorial no tamanho de impressão,
// com o nome que a gráfica recebe: <posição>_<modelo>_<largura>x<altura>mm.pdf
//
//   node scripts/exporta_artes.mjs            escreve em saidas/artes_sinalizacao/
//   node scripts/exporta_artes.mjs --png      além do PDF, um PNG de conferência a 150 dpi
//
// O canvas de cada peça está em px a 2 mm/px (1040 × 410 px = 2080 × 820 mm), e é
// isso que este script amarra: a página do PDF sai no tamanho real em mm e o corpo
// da peça é escalado por CSS, então texto e SVG continuam vetor e a Montserrat vai
// embutida (subconjunto) no arquivo. A fonte precisa estar instalada no sistema:
// sem ela o Chromium cai numa substituta e a medida das peças muda.
//
// Peças de vinil recortado (P5-Vinil*) saem sem o fundo cinza-azulado (#DDE4E2):
// ele representa o vidro da porta no desenho, não é impresso. O que se recorta é
// o que fica.

import { createRequire } from "node:module";
import { execSync } from "node:child_process";
import { readFileSync, writeFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const RAIZ = join(dirname(fileURLToPath(import.meta.url)), "..");
const PECAS = join(RAIZ, "mapa", "sinalizacao");
const SAIDA = join(RAIZ, "saidas", "artes_sinalizacao");
const MM_POR_PX = 2;           // escala do canvas das peças
const PX_CSS_POR_MM = 96 / 25.4;
const DPI_PNG = 150;

// Fonte: mapa/plano_sinalizacao.html (fichas "Modelo" e "Quantidade") e canvas.json.
// A ordem é a em que o eleitor encontra as peças.
const PLANO = [
  ["P0-Consulta",     "construction-fence", 2080,  820, 2,  "P0 · descubra sua seção (QR do TSE) · calçada da Merrion Road, uma de cada lado do portão"],
  ["P0-Mestra",       "construction-fence", 2080,  820, 2,  "P0 · tabela mestra seção → porta · calçada, ao lado de cada P0-Consulta"],
  ["P1-Portao",       "construction-fence", 2080,  820, 1,  "P1 · portão de eleitores"],
  ["P2-ParedeLeste",  "pvc-banner",         2000, 1000, 3,  "P2 · lateral leste do Hall 2, nas portas de serviço"],
  ["P3-EntradaRing",  "construction-fence", 2080,  820, 1,  "P3 · entrada do Ring 3, na CCB"],
  ["P4-ZonaC",        "construction-fence", 2080,  820, 1,  "P4 · boca da zona C do Ring 3"],
  ["P4-ZonaB",        "construction-fence", 2080,  820, 1,  "P4 · boca da zona B do Ring 3"],
  ["P4-ZonaA",        "construction-fence", 2080,  820, 1,  "P4 · boca da zona A do Ring 3"],
  ["P5-VinilA",       "cut-vinyl",          1200,  700, 1,  "P5 · letra A no vidro da porta S4"],
  ["P5-VinilB",       "cut-vinyl",          1200,  700, 1,  "P5 · letra B no vidro da porta S5"],
  ["P5-VinilC",       "cut-vinyl",          1200,  700, 1,  "P5 · letra C no vidro da porta S6"],
  ["P5-Preferencial", "construction-fence", 2080,  820, 1,  "P5 · entrada preferencial, no gradil do apron"],
  ["P5-VinilPref",    "cut-vinyl",          1200,  700, 1,  "P5 · preferencial no vidro da porta S7"],
  ["P6-PainelA",      "roll-up",            1000, 2000, 1,  "P6 · painel da porta A, atrás da S4"],
  ["P6-PainelB",      "roll-up",            1000, 2000, 1,  "P6 · painel da porta B, atrás da S5"],
  ["P6-PainelC",      "roll-up",            1000, 2000, 1,  "P6 · painel da porta C, atrás da S6"],
  ["P4-FimAvenidaB",  "construction-fence", 2080,  820, 1,  "P4 · fim da avenida B, na boca da pequena avenida da parede norte"],
  ...["A1","A2","A3","A4","A5","B1","B2","B3","B4","B5","C1","C2","C3","C4","C5","C6"].map(g =>
    [`P6-Bloco${g}`,   "roll-up",             850, 2000, 1,  `P6 · placa do grupo ${g}, na boca do corredor do par`]),
  ["P7-Saida",        "correx-sign-A2",      594,  420, 2,  "P7 · saídas S2 e S8"],
];

function playwright() {
  const req = createRequire(import.meta.url);
  try { return req("playwright"); } catch {}
  const global = execSync("npm root -g", { encoding: "utf8" }).trim();
  return createRequire(join(global, "x"))("playwright");
}

function corpo(nome, modelo) {
  const t = readFileSync(join(PECAS, `${nome}.dc.html`), "utf8");
  const ini = t.indexOf("<div", t.indexOf("</helmet>"));
  const fim = t.lastIndexOf("</x-dc>");
  if (ini < 0 || fim < 0) throw new Error(`${nome}: estrutura inesperada`);
  let html = t.slice(ini, fim).trim();
  const m = html.match(/^<div style="width: ([\d.]+)px; height: ([\d.]+)px;/);
  if (!m) throw new Error(`${nome}: o corpo não declara largura e altura`);
  if (modelo === "cut-vinyl") {
    // o fundo do vidro fica de fora do arquivo de recorte
    html = html.replace(/^(<div style="[^"]*?)background: #DDE4E2;\s*/, "$1");
  }
  return { html, px: [Number(m[1]), Number(m[2])] };
}

function pagina(html, larg, alt, pxL, pxA) {
  const k = (larg * PX_CSS_POR_MM) / pxL;
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
@page { size: ${larg}mm ${alt}mm; margin: 0; }
html, body { margin: 0; padding: 0; background: #FFFFFF; }
body { width: ${larg}mm; height: ${alt}mm; overflow: hidden; }
#arte { width: ${pxL}px; height: ${pxA}px; transform: scale(${k}); transform-origin: top left; }
</style></head><body><div id="arte">${html}</div></body></html>`;
}

async function main() {
  const png = process.argv.includes("--png");
  mkdirSync(SAIDA, { recursive: true });
  const { chromium } = playwright();
  const browser = await chromium.launch();
  const manifesto = [];
  for (const [nome, modelo, larg, alt, qtd, onde] of PLANO) {
    const { html, px } = corpo(nome, modelo);
    const [pxL, pxA] = px;
    if (Math.round(pxL * MM_POR_PX) !== larg || Math.round(pxA * MM_POR_PX) !== alt)
      throw new Error(`${nome}: canvas ${pxL}×${pxA} px não bate com ${larg}×${alt} mm a ${MM_POR_PX} mm/px`);
    const arquivo = `${nome}_${modelo}_${larg}x${alt}mm`;
    const doc = pagina(html, larg, alt, pxL, pxA);
    const ctx = await browser.newContext({ viewport: { width: pxL, height: pxA }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    await page.setContent(doc, { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    // Montserrat é fonte de sistema aqui: se estiver instalada, a medida do texto não
    // muda entre "Montserrat, serif" e "Montserrat, sans-serif"; se não, cai na substituta.
    const temFonte = await page.evaluate(() => {
      const c = document.createElement("canvas").getContext("2d");
      const larg = f => { c.font = `800 100px ${f}`; return c.measureText("SUA SEÇÃO 0513 EL").width; };
      return larg("Montserrat, serif") === larg("Montserrat, sans-serif") && larg("Montserrat, serif") !== larg("serif");
    });
    if (!temFonte) throw new Error(`${nome}: Montserrat não está instalada no sistema — o Chromium usaria uma substituta`);
    const pdf = join(SAIDA, `${arquivo}.pdf`);
    await page.pdf({ path: pdf, width: `${larg}mm`, height: `${alt}mm`, printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    const item = { arquivo: `${arquivo}.pdf`, peca: nome, modelo, largura_mm: larg, altura_mm: alt, quantidade: qtd, onde, bytes: statSync(pdf).size };
    if (png) {
      const fator = (DPI_PNG / 25.4) * MM_POR_PX;   // px de imagem por px de canvas
      const ctx2 = await browser.newContext({ viewport: { width: pxL, height: pxA }, deviceScaleFactor: fator });
      const p2 = await ctx2.newPage();
      await p2.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#fff}</style></head><body>${html}</body></html>`, { waitUntil: "load" });
      await p2.evaluate(() => document.fonts.ready);
      await p2.screenshot({ path: join(SAIDA, `${arquivo}.png`), clip: { x: 0, y: 0, width: pxL, height: pxA } });
      await ctx2.close();
      item.png = `${arquivo}.png`;
    }
    await ctx.close();
    manifesto.push(item);
    console.log(`${item.arquivo.padEnd(52)} ${String(item.bytes).padStart(8)} B  ×${qtd}`);
  }
  await browser.close();
  writeFileSync(join(SAIDA, "manifesto.json"), JSON.stringify({
    gerado_em: new Date().toISOString().slice(0, 10),
    nota: "PDF vetorial no tamanho final de impressão (sem sangria), Montserrat embutida. Nome = posição no plano _ modelo _ largura x altura mm. Quantidade é quantas cópias a gráfica imprime daquele arquivo.",
    escala: `${MM_POR_PX} mm por px de canvas`,
    total_arquivos: manifesto.length,
    total_pecas: manifesto.reduce((s, i) => s + i.quantidade, 0),
    artes: manifesto,
  }, null, 1) + "\n");
}

main().catch(e => { console.error(e.message); process.exit(1); });
