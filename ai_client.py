// Service Worker — offline support + push notifications για Android
const CACHE = "guru-investor-v1";
const STATIC = ["/", "/index.html", "/manifest.json"];

// ── Install: cache static assets ──────────────────────────────
self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(STATIC))
  );
  self.skipWaiting();
});

// ── Activate: cleanup old caches ──────────────────────────────
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// ── Fetch: serve from cache, fallback to network ──────────────
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then((cached) => {
      const network = fetch(e.request).then((res) => {
        if (res && res.status === 200) {
          const clone = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, clone));
        }
        return res;
      });
      return cached || network;
    })
  );
});

// ── Push Notifications (Firebase FCM) ─────────────────────────
self.addEventListener("push", (e) => {
  if (!e.data) return;
  const data = e.data.json();
  const { title, body } = data.notification || {};
  const { type, ticker, urgency } = data.data || {};

  // Εικονίδιο και χρώμα ανά urgency
  const icons = {
    BUY:  "/icon-buy.png",
    SELL: "/icon-sell.png",
    INFO: "/icon-info.png",
  };
  const badges = { BUY: "🟢", SELL: "🔴", INFO: "📊" };
  const tag    = ticker ? `${type}-${ticker}` : "guru-info";

  e.waitUntil(
    self.registration.showNotification(title || "Guru Investor", {
      body:    body || "",
      icon:    icons[type] || "/icon-192.png",
      badge:   "/icon-badge.png",
      tag,
      renotify: true,
      vibrate: urgency === "critical" ? [200, 100, 200, 100, 200] : [200, 100, 200],
      data:    { url: `/?tab=signals&ticker=${ticker || ""}`, type, ticker, urgency },
      actions: [
        { action: "open",    title: "Άνοιξε" },
        { action: "dismiss", title: "Απόρριψη" },
      ],
    })
  );
});

// ── Notification click ─────────────────────────────────────────
self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  if (e.action === "dismiss") return;
  const url = e.notification.data?.url || "/";
  e.waitUntil(
    clients.matchAll({ type: "window" }).then((wins) => {
      const existing = wins.find((w) => w.url.includes(self.location.origin));
      if (existing) { existing.focus(); existing.navigate(url); }
      else           clients.openWindow(url);
    })
  );
});
