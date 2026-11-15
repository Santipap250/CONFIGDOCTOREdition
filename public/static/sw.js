/* CONFIGDOCTOR Edition — bounded allowlist cache + network-first HTML.
 * Never cache application HTML, API responses, video, or arbitrary static files.
 */
const CACHE_NAME = 'obixconfigdoctor-v12-workspace';
const STATIC_ASSETS = [
  '/static/css/edition-tokens.css',
  '/static/css/components.css',
  '/static/css/edition-pages.css',
  '/static/css/workspace-nav.css',
  '/static/css/landing-premium.css',
  '/static/css/responsive.css',
  '/static/css/ui-enhance.css',
  '/static/img/configdoctor-logo.png',
  '/static/favicon.ico',
  '/static/android-chrome-192x192.png',
  '/static/img/pwa-maskable-512.png',
  '/static/manifest.json',
  '/static/offline.html'
];
const STATIC_ALLOWLIST = new Set(STATIC_ASSETS);
const MAX_ASSET_BYTES = 512 * 1024;

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

  if (!STATIC_ALLOWLIST.has(url.pathname) || url.search) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(async (cache) => {
      const cached = await cache.match(request);
      if (cached) return cached;

      const response = await fetch(request);
      const rawContentLength = response.headers.get('Content-Length');
      const contentLength = rawContentLength !== null && /^\d+$/.test(rawContentLength)
        ? Number(rawContentLength)
        : null;
      if (response && response.ok && response.type === 'basic' &&
          contentLength !== null && contentLength <= MAX_ASSET_BYTES) {
        await cache.put(request, response.clone());
      }
      return response;
    })
  );
});
