/* OBIXCONFIGDOCTOR — static-asset cache only.
 * Never cache application HTML or API responses: pages include per-session CSRF tokens.
 */
const CACHE_NAME = 'obixconfigdoctor-v6-static';
const STATIC_ASSETS = [
  '/static/css/landing-premium.css',
  '/static/img/hero-drone-premium.webp',
  '/static/img/configdoctor-logo.png',
  '/static/img/og-premium.webp',
  '/static/favicon.ico',
  '/static/manifest.json'
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
  if (url.origin !== self.location.origin || !url.pathname.startsWith('/static/')) return;

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
