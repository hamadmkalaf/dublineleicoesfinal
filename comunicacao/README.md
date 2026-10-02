# Comunicação — peças para redes sociais

Peças de divulgação no **mesmo design do briefing de 23/09**
(`Apresentações/2026.9.23_Equipe Embaixada_Briefing.pptx`): fundo creme `#F2EFE2`,
barra superior azul-marinho `#042B5A`, rótulo em verde `#5F882E` em caixa alta, título em
azul-marinho, texto em cinza `#6B6B6B`, cartões brancos com borda `#E4DFCC`, tudo em
Montserrat. O logo "Eleições 2026 · #VotoNaDemocracia" é o mesmo da apresentação.

| Peça | Fonte | Saída |
|---|---|---|
| "Onde eu vou votar?" (Instagram, 4:5) | `onde_eu_voto_instagram.html` | `onde_eu_voto_instagram.png` (2160×2700, 2×) |

A fonte é o HTML; o PNG é gerado a partir dele. Para regenerar com o Chromium do
Playwright (a `headless_shell` dá a viewport exata; o `chrome` desconta a barra da janela):

```sh
/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell \
  --no-sandbox --hide-scrollbars --window-size=1080,1350 --force-device-scale-factor=2 \
  --screenshot=comunicacao/onde_eu_voto_instagram.png file://$PWD/comunicacao/onde_eu_voto_instagram.html
```

O HTML carrega a Montserrat do Google Fonts; sem rede, embuta os `.ttf` em `@font-face`
antes de renderizar.
