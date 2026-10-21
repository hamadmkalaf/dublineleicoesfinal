// Gera os PNG (1080 × 1350) do carrossel "conflito com maratona/instagram/cards.html".
// Uso: node scripts/instagram_cards_render.js
// Requer Playwright com Chromium; as fontes vêm do Google Fonts, então precisa de rede.
const path = require('path');
const { chromium } = require('playwright');

const pasta = path.join(__dirname, '..', 'conflito com maratona', 'instagram');

(async () => {
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage({ viewport: { width: 1200, height: 1400 }, deviceScaleFactor: 1 });
  await pagina.goto('file://' + path.join(pasta, 'cards.html'));
  await pagina.evaluate(() => document.fonts.ready);
  const cards = await pagina.$$('section.card');
  for (let i = 0; i < cards.length; i++) {
    const saida = path.join(pasta, `card${i + 1}.png`);
    await cards[i].screenshot({ path: saida });
    console.log(saida);
  }
  await navegador.close();
})();
