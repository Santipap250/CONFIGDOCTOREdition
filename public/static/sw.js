/* CONFIGDOCTOR Edition — cache static assets and a standalone offline fallback only.
 * Never cache application HTML or API responses: pages include per-session CSRF tokens.
 */
const CACHE_NAME = 'obixconfigdoctor-v10-static';
const STATIC_ASSETS = [
  '/static/css/landing-premium.css',
  '/static/img/hero-drone-premium.webp',
  '/static/img/configdoctor-logo.png',
  '/static/img/og-premium.webp',
  '/static/favicon.ico',
  '/static/favicon.png',
  '/static/android-chrome-192x192.png',
  '/static/img/pwa-maskable-512.png',
  '/static/manifest.json',
  '/static/offline.html'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((key) => key.startsWith('obixconfigdoctor-') && key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  // HTML is always fetched from the network. If it fails, serve only the
  // static offline notice; do not persist personalized pages or CSRF tokens.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(async () => {
        const cache = await caches.open(CACHE_NAME);
        const offlinePage = await cache.match('/static/offline.html');
        if (!offlinePage) return Response.error();
        return new Response(await offlinePage.text(), {
          status: 503,
          statusText: 'Offline',
          headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' }
        });
      })
    );
    return;
  }

  if (!url.pathname.startsWith('/static/')) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(async (cache) => {
      const cached = await cache.match(request);
      if (cached) return cached;

      const response = await fetch(request);
      if (response && response.ok && response.type === 'basic') {
        cache.put(request, response.clone()).catch(() => {});
      }
      return response;
    })
  );
});
