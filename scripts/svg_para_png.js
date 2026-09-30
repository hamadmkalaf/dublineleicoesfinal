// Rasteriza um SVG com o Chromium do Playwright: node svg_para_png.js in.svg out.png [escala]
const fs = require('fs');
let playwright;
try { playwright = require('playwright'); }
catch (e) { playwright = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright'); }
(async () => {
  const [svg, png, escala = '2'] = process.argv.slice(2);
  const m = fs.readFileSync(svg, 'utf8').match(/width="(\d+)" height="(\d+)"/);
  const b = await playwright.chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: +m[1], height: +m[2] }, deviceScaleFactor: +escala });
  await p.goto('file://' + require('path').resolve(svg));
  await p.screenshot({ path: png });
  await b.close();
})();
