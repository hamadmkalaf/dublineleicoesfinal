/* Service worker do "Onde eu voto?": guarda o site inteiro e os dados no aparelho.
 * A VERSAO é trocada pelo build (scripts/app_construir.py); um build novo = cache novo.
 * Estratégia: cache primeiro, rede como reserva. Funciona sem internet depois da 1ª visita. */
const VERSAO = "2026-10-01T17:57:31+00:00";
const CACHE = `onde-eu-voto-${VERSAO}`;
const ARQUIVOS = [
  "./", "./index.html", "./equipe/", "./equipe/index.html", "./comum.js", "./estilo.css",
  "./manifest.webmanifest", "./icones/icone.svg", "./icones/icone-192.png", "./icones/icone-512.png",
  "./dados/config.json", "./dados/rotas.json", "./dados/indice_publico.json", "./dados/equipe.enc", "./dados/versao.json",
];

self.addEventListener("install", (ev) => {
  ev.waitUntil(caches.open(CACHE).then((c) => c.addAll(ARQUIVOS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (ev) => {
  ev.waitUntil(
    caches.keys().then((chaves) => Promise.all(chaves.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (ev) => {
  if (ev.request.method !== "GET") return;
  ev.respondWith(
    caches.match(ev.request, { ignoreSearch: true }).then((hit) => hit || fetch(ev.request).then((resp) => {
      if (resp.ok && new URL(ev.request.url).origin === self.location.origin) {
        const copia = resp.clone();
        caches.open(CACHE).then((c) => c.put(ev.request, copia));
      }
      return resp;
    }))
  );
});
