/* 词斩背单词 - Service Worker (https 部署后自动启用离线缓存) */
const CACHE = 'cz-v1';
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(['./', './index.html']))
      .then(() => self.skipWaiting())
  );
});
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  const cdn = /cdn\.(bootcdn\.net|jsdelivr\.net|cdnjs\.cloudflare\.com)$/.test(url.host);
  if (url.origin !== location.origin && !cdn) return;
  if (e.request.mode === 'navigate') {
    // 网络优先：更新能到达；离线时回退缓存
    e.respondWith(
      fetch(e.request)
        .then(r => {
          const c = r.clone();
          caches.open(CACHE).then(cache => cache.put('./index.html', c));
          return r;
        })
        .catch(() => caches.match('./index.html'))
    );
    return;
  }
  e.respondWith(
    caches.open(CACHE).then(async c => {
      const hit = await c.match(e.request);
      const net = fetch(e.request)
        .then(r => { if (r.ok) c.put(e.request, r.clone()); return r; })
        .catch(() => null);
      return hit || net;
    })
  );
});
