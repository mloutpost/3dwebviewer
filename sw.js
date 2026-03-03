// Service Worker to intercept and block unwanted Cadwork viewer API calls
const BLOCKED_PATTERNS = [
  '/api/v1/userdata',
  '/api/v1/secure-hello',
  'maps.googleapis.com/maps/api/timezone',
  'survey-module.azurewebsites.net',
  'survey-module-staging.azurewebsites.net',
  'survey-module-next.azurewebsites.net',
  'survey-module-manual.azurewebsites.net'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
  const url = event.request.url;
  
  // Check if this request should be blocked
  const shouldBlock = BLOCKED_PATTERNS.some(pattern => url.includes(pattern));
  
  if (!shouldBlock) return;

  event.respondWith(
    new Response(JSON.stringify({ blocked: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })
  );
});
