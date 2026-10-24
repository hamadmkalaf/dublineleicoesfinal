// Gera icone-192.png e icone-512.png a partir de icone.svg com o Chromium do Playwright.
//   NODE_PATH=/opt/node22/lib/node_modules node app/testes/gera_icones.mjs
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright"); // usa NODE_PATH se não houver node_modules local
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
const pasta = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../public/icones");
const svg = readFileSync(path.join(pasta, "icone.svg"), "utf-8");
const navegador = await chromium.launch();
for (const tam of [192, 512]) {
  const pagina = await navegador.newPage({ viewport: { width: tam, height: tam } });
  await pagina.setContent(`<html><body style="margin:0">${svg.replace("<svg ", `<svg width="${tam}" height="${tam}" `)}</body></html>`);
  await pagina.screenshot({ path: path.join(pasta, `icone-${tam}.png`), omitBackground: true });
  await pagina.close();
}
await navegador.close();
console.log("ícones gerados em", pasta);
