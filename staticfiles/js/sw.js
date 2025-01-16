// Basic service worker
self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
  event.respondWith(fetch(event.request));
});

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(function(registration) {
      console.log('ServiceWorker registration successful with scope: ', registration.scope);
    })
    .catch(function(error) {
      console.error('ServiceWorker registration failed: ', error);
    });
}