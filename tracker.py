<!DOCTYPE html>
<html lang="el">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"/>
<meta name="theme-color" content="#2d9b6f"/>
<meta name="apple-mobile-web-app-capable" content="yes"/>
<meta name="mobile-web-app-capable" content="yes"/>
<meta name="apple-mobile-web-app-title" content="Guru Investor"/>
<title>Guru Investor OS</title>
<link rel="manifest" href="/manifest.json"/>
<link rel="icon" href="/icon-192.png"/>

<!-- Tabler Icons CDN -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.0.0/tabler-icons.min.css"/>

<style>
:root{
  --g:#1a6b4a;--gm:#2d9b6f;--gl:#e8f5ee;
  --gold:#7a5200;--goldl:#fdf7e3;
  --red:#9a1a1a;--redl:#fdf0ee;
  --blue:#0d3a8a;--bluel:#e6f0fb;
  --bg:#0f1a14;--surf:#17261d;--surf2:#1e3326;
  --border:#2a4035;--txt:#e8f2ec;--muted:#7aaa8a;
  --rad:14px;--radm:10px;
  --safe-bottom: env(safe-area-inset-bottom, 0px);
}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;}
html,body{height:100%;background:var(--bg);color:var(--txt);
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  overscroll-behavior:none;}

/* ── Layout ─────────────────────────────────────── */
.app{display:flex;flex-direction:column;height:100vh;max-width:430px;
  margin:0 auto;position:relative;}

/* ── Top bar ─────────────────────────────────────── */
.topbar{background:var(--surf);border-bottom:1px solid var(--border);
  padding:12px 16px 10px;display:flex;justify-content:space-between;
  align-items:center;flex-shrink:0;}
.topbar-title{font-size:16px;font-weight:600;letter-spacing:-.3px;}
.live-dot{width:7px;height:7px;border-radius:50%;background:#2d9b6f;
  display:inline-block;margin-right:6px;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.3;}}

/* ── Tabs ────────────────────────────────────────── */
.tabs{display:flex;background:var(--surf);border-bottom:1px solid var(--border);
  overflow-x:auto;scrollbar-width:none;flex-shrink:0;}
.tabs::-webkit-scrollbar{display:none;}
.tab-btn{flex:none;padding:9px 11px;font-size:10px;color:var(--muted);
  background:none;border:none;cursor:pointer;border-bottom:2px solid transparent;
  white-space:nowrap;font-family:inherit;transition:color .15s;}
.tab-btn i{font-size:16px;display:block;margin-bottom:2px;}
.tab-btn.on{color:var(--gm);border-bottom-color:var(--gm);}

/* ── Scroll area ─────────────────────────────────── */
.content{flex:1;overflow-y:auto;padding:12px;
  padding-bottom:calc(70px + var(--safe-bottom));}
.screen{display:none;}
.screen.on{display:block;}

/* ── Bottom nav ──────────────────────────────────── */
.bottom-nav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);
  width:100%;max-width:430px;background:var(--surf);
  border-top:1px solid var(--border);display:flex;
  padding-bottom:var(--safe-bottom);}
.nav-btn{flex:1;padding:10px 4px 8px;text-align:center;font-size:10px;
  color:var(--muted);background:none;border:none;cursor:pointer;
  font-family:inherit;transition:color .15s;}
.nav-btn i{font-size:22px;display:block;margin-bottom:2px;}
.nav-btn.on{color:var(--gm);}
.nav-badge{background:var(--red);color:#fff;font-size:9px;font-weight:700;
  border-radius:20px;padding:1px 5px;margin-left:2px;vertical-align:top;}

/* ── Cards ───────────────────────────────────────── */
.card{background:var(--surf);border:1px solid var(--border);
  border-radius:var(--rad);padding:13px;margin-bottom:10px;}
.stitle{font-size:10px;font-weight:600;color:var(--muted);
  text-transform:uppercase;letter-spacing:.6px;margin-bottom:9px;}

/* ── Portfolio hero ──────────────────────────────── */
.hero{background:linear-gradient(135deg,#0a2018 0%,#1a4a35 100%);
  border:1px solid #2d6b4a;border-radius:var(--rad);padding:16px;margin-bottom:10px;}
.hero-label{font-size:12px;color:#9fcfb3;margin-bottom:6px;}
.hero-value{font-size:34px;font-weight:700;color:#fff;margin-bottom:6px;
  letter-spacing:-1px;}
.hero-change{font-size:13px;color:#5ee8a3;}

/* ── Metrics grid ────────────────────────────────── */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;}
.met{background:var(--surf2);border-radius:var(--radm);padding:10px 12px;}
.met-lbl{font-size:10px;color:var(--muted);margin-bottom:3px;}
.met-val{font-size:19px;font-weight:600;}
.green{color:#5ee8a3;} .red{color:#f08080;}
.gold{color:#e8c060;}  .blue{color:#80b0f0;}

/* ── Chip ────────────────────────────────────────── */
.chip{display:inline-block;font-size:10px;padding:2px 7px;
  border-radius:20px;font-weight:600;}
.cg{background:rgba(45,155,111,.2);color:#5ee8a3;}
.cr{background:rgba(192,80,80,.2);color:#f08080;}
.cgold{background:rgba(184,134,11,.2);color:#e8c060;}
.cb{background:rgba(64,128,208,.2);color:#80b0f0;}
.cgray{background:var(--surf2);color:var(--muted);border:1px solid var(--border);}

/* ── Holding row ─────────────────────────────────── */
.h-row{display:flex;align-items:center;justify-content:space-between;
  padding:9px 0;border-bottom:1px solid var(--border);}
.h-row:last-child{border-bottom:none;}
.h-ticker{font-size:14px;font-weight:600;}
.h-name{font-size:11px;color:var(--muted);}
.h-val{font-size:14px;font-weight:600;text-align:right;}
.h-pct{font-size:11px;text-align:right;}

/* ── Signal box ──────────────────────────────────── */
.sb{border-radius:var(--radm);padding:11px 13px;margin-bottom:9px;border:1px solid;}
.sb-buy{background:rgba(45,155,111,.12);border-color:#2d9b6f;}
.sb-sell{background:rgba(192,80,80,.12);border-color:#c05050;}
.sb-hold{background:rgba(184,134,11,.12);border-color:#b88020;}
.sb-info{background:rgba(64,128,208,.12);border-color:#4080d0;}
.sb-title{font-size:13px;font-weight:600;margin-bottom:4px;}
.sb-buy .sb-title{color:#5ee8a3;} .sb-sell .sb-title{color:#f08080;}
.sb-hold .sb-title{color:#e8c060;} .sb-info .sb-title{color:#80b0f0;}
.sb-desc{font-size:12px;line-height:1.5;color:var(--muted);}

/* ── Progress bar ────────────────────────────────── */
.prog-wrap{margin-bottom:8px;}
.prog-hd{display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px;}
.prog-track{height:6px;background:var(--surf2);border-radius:3px;overflow:hidden;}
.prog-fill{height:100%;border-radius:3px;background:var(--gm);
  transition:width .6s ease;}

/* ── Bar ─────────────────────────────────────────── */
.bar-wrap{margin-bottom:7px;}
.bar-hd{display:flex;justify-content:space-between;font-size:11px;
  margin-bottom:2px;color:var(--muted);}
.bar-track{height:4px;background:var(--surf2);border-radius:2px;overflow:hidden;}
.bar-fill{height:100%;border-radius:2px;}

/* ── Notification item ───────────────────────────── */
.notif{display:flex;gap:10px;padding:10px 0;
  border-bottom:1px solid var(--border);}
.notif:last-child{border-bottom:none;}
.n-icon{width:34px;height:34px;border-radius:10px;display:flex;
  align-items:center;justify-content:center;font-size:16px;flex-shrink:0;}
.ni-b{background:rgba(45,155,111,.2);}
.ni-s{background:rgba(192,80,80,.2);}
.ni-w{background:rgba(184,134,11,.2);}
.ni-i{background:rgba(64,128,208,.2);}
.n-title{font-size:13px;font-weight:600;color:var(--txt);margin-bottom:2px;}
.n-desc{font-size:12px;color:var(--muted);line-height:1.4;}
.n-time{font-size:10px;color:var(--muted);margin-top:3px;}

/* ── Feed item ───────────────────────────────────── */
.feed-item{background:var(--surf);border:1px solid var(--border);
  border-radius:var(--rad);padding:11px;margin-bottom:8px;}
.feed-head{display:flex;align-items:center;gap:9px;margin-bottom:7px;}
.av{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;}
.feed-body{font-size:12px;color:var(--muted);line-height:1.45;margin-bottom:7px;}
.feed-tags{display:flex;flex-wrap:wrap;gap:4px;}

/* ── Sector card ─────────────────────────────────── */
.sector-card{background:var(--surf);border:1px solid var(--border);
  border-radius:var(--rad);padding:11px;margin-bottom:8px;}
.sec-hd{display:flex;justify-content:space-between;align-items:flex-start;
  margin-bottom:5px;}
.sec-name{font-size:14px;font-weight:600;}
.sec-why{font-size:11px;color:var(--muted);line-height:1.4;margin-bottom:7px;}
.sec-picks{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:7px;}

/* ── Button ──────────────────────────────────────── */
.btn{display:inline-flex;align-items:center;gap:5px;padding:8px 13px;
  border-radius:var(--radm);font-size:12px;cursor:pointer;
  border:1px solid var(--border);background:var(--surf);color:var(--txt);
  font-family:inherit;transition:background .15s;width:100%;
  justify-content:center;margin-top:6px;}
.btn:active{background:var(--surf2);}
.btn-p{background:var(--g);color:#fff;border-color:var(--g);}
.btn-p:active{background:var(--gm);}

/* ── Goal inputs ─────────────────────────────────── */
.inp-lbl{font-size:12px;color:var(--muted);margin-top:10px;
  margin-bottom:3px;display:block;}
.inp{width:100%;padding:9px 11px;border:1px solid var(--border);
  border-radius:var(--radm);background:var(--surf2);color:var(--txt);
  font-size:14px;font-family:inherit;outline:none;}
.inp:focus{border-color:var(--gm);}
select.inp option{background:var(--surf);}

/* ── Code block ──────────────────────────────────── */
.code{background:var(--surf2);border:1px solid var(--border);
  border-radius:var(--radm);padding:10px;font-family:monospace;
  font-size:10px;color:var(--muted);line-height:1.6;overflow-x:auto;
  margin-bottom:8px;white-space:pre;}

/* ── Install banner ──────────────────────────────── */
.install-banner{background:linear-gradient(135deg,#0a2018,#1a4a35);
  border:1px solid var(--gm);border-radius:var(--rad);padding:13px;
  margin-bottom:10px;display:none;}
.install-banner.show{display:flex;gap:10px;align-items:center;}

/* ── Toast ───────────────────────────────────────── */
.toast{position:fixed;bottom:80px;left:50%;transform:translateX(-50%);
  background:var(--surf);border:1px solid var(--border);border-radius:var(--rad);
  padding:10px 16px;font-size:13px;z-index:999;display:none;
  max-width:320px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.4);}
.toast.show{display:block;animation:fadeInUp .3s ease;}
@keyframes fadeInUp{from{opacity:0;transform:translateX(-50%) translateY(10px);}
  to{opacity:1;transform:translateX(-50%) translateY(0);}}
</style>
</head>
<body>

<div class="app">
  <!-- Top bar -->
  <div class="topbar">
    <div class="topbar-title"><span class="live-dot"></span>Guru Investor OS</div>
    <div style="display:flex;align-items:center;gap:8px;">
      <span class="chip cg" id="aiStatus">Groq AI</span>
      <button onclick="showNotifPrompt()" style="background:none;border:none;cursor:pointer;color:var(--muted);font-size:22px;">
        <i class="ti ti-bell"></i>
      </button>
    </div>
  </div>

  <!-- Sub-tabs (hidden on mobile nav, shown on some screens) -->
  <div class="tabs" id="subtabs" style="display:none;"></div>

  <!-- Main content -->
  <div class="content">

    <!-- Install banner for Android -->
    <div class="install-banner" id="installBanner">
      <i class="ti ti-device-mobile" style="font-size:28px;color:var(--gm);flex-shrink:0;"></i>
      <div style="flex:1;">
        <div style="font-size:13px;font-weight:600;margin-bottom:2px;">Εγκατάστασε στο Android</div>
        <div style="font-size:11px;color:var(--muted);">Chrome → 3 τελείες → "Εγκατάσταση εφαρμογής"</div>
      </div>
      <button onclick="installApp()" class="btn btn-p" style="width:auto;margin:0;padding:6px 12px;">Εγκ/ση</button>
    </div>

    <!-- ── DASHBOARD ─────────────────────────────── -->
    <div class="screen on" id="sc-home">
      <div class="hero">
        <div class="hero-label">Σύνολο χαρτοφυλακίου</div>
        <div class="hero-value">€1,247.50</div>
        <div class="hero-change">▲ +€26.40 σήμερα (+2.2%)</div>
      </div>

      <div class="g2">
        <div class="met"><div class="met-lbl">Συνολική απόδοση</div>
          <div class="met-val green">+31.4%</div></div>
        <div class="met"><div class="met-lbl">Guru Score</div>
          <div class="met-val gold">78/100</div></div>
        <div class="met"><div class="met-lbl">Θέσεις</div>
          <div class="met-val blue">14</div></div>
        <div class="met"><div class="met-lbl">Στόχος</div>
          <div class="met-val green">€3,000</div></div>
      </div>

      <!-- Goal progress -->
      <div class="card">
        <div class="stitle">Πρόοδος στόχου</div>
        <div class="prog-wrap">
          <div class="prog-hd"><span>€1,247 → €3,000</span>
            <span style="font-weight:600;color:var(--gm);">42%</span></div>
          <div class="prog-track"><div class="prog-fill" style="width:42%;"></div></div>
        </div>
        <div style="font-size:11px;color:var(--muted);margin-top:4px;">
          Εκτίμηση: ~14 μήνες με €100/μήνα + 15% ετήσια απόδοση
        </div>
      </div>

      <!-- AI insight -->
      <div class="sb sb-info">
        <div class="sb-title"><i class="ti ti-sparkles"></i> AI Signal — Τώρα</div>
        <div class="sb-desc">AMD earnings αύριο — 72% πιθανότητα beat. Μην πουλάς πριν. RKLB -6% χωρίς news = dip buying ευκαιρία κάτω από $22.</div>
      </div>

      <!-- Top movers -->
      <div class="card">
        <div class="stitle">Top Movers σήμερα</div>
        <div class="h-row">
          <div><div class="h-ticker">RKLB</div><div class="h-name">Rocket Lab</div></div>
          <div><div class="h-val">€212</div><div class="h-pct red">-6.1% · DIP</div></div>
        </div>
        <div class="h-row">
          <div><div class="h-ticker">PLTR</div><div class="h-name">Palantir</div></div>
          <div><div class="h-val">€156</div><div class="h-pct green">+4.3%</div></div>
        </div>
        <div class="h-row">
          <div><div class="h-ticker">AMD</div><div class="h-name">AMD · Earnings αύριο</div></div>
          <div><div class="h-val">€310</div><div class="h-pct green">+1.8%</div></div>
        </div>
        <div class="h-row">
          <div><div class="h-ticker">MELI</div><div class="h-name">MercadoLibre</div></div>
          <div><div class="h-val">€125</div><div class="h-pct green">+0.9%</div></div>
        </div>
      </div>
    </div>

    <!-- ── PORTFOLIO ───────────────────────────────── -->
    <div class="screen" id="sc-portfolio">
      <div class="card">
        <div class="stitle">Holdings — Trading 212</div>
        <div class="h-row">
          <div><div class="h-ticker">AMD</div><div class="h-name">25% · AI/Tech</div></div>
          <div><div class="h-val">€310</div><div class="h-pct green">+22.1%</div></div>
        </div>
        <div class="h-row">
          <div><div class="h-ticker">RKLB</div><div class="h-name">17% · Space</div></div>
          <div><div class="h-val">€212</div><div class="h-pct green">+41.2%</div></div>
        </div>
        <div class="h-row">
          <div><div class="h-ticker">VWCE</div><div class="h-name">18% · ETF Core</div></div>
          <div><div class="h-val">€226</div><div class="h-pct green">+12.0%</div></div>
        </div>
        <div class="h-row">
          <div><div class="h-ticker">PLTR</div><div class="h-name">13% · AI Gov</div></div>
          <div><div class="h-val">€156</div><div class="h-pct green">+88.4%</div></div>
        </div>
        <div class="h-row">
          <div><div class="h-ticker">MELI</div><div class="h-name">10% · Fintech</div></div>
          <div><div class="h-val">€125</div><div class="h-pct green">+14.8%</div></div>
        </div>
        <div class="h-row">
          <div><div class="h-ticker">ASTS</div><div class="h-name">7% · Space</div></div>
          <div><div class="h-val">€93</div><div class="h-pct red">-8.3%</div></div>
        </div>
        <div class="h-row">
          <div><div class="h-ticker">LSE</div><div class="h-name">5% · Finance</div></div>
          <div><div class="h-val">€63</div><div class="h-pct green">+5.2%</div></div>
        </div>
        <div class="h-row">
          <div><div class="h-ticker">CASH</div><div class="h-name">Ρευστό</div></div>
          <div><div class="h-val">€63</div><div class="h-pct" style="color:var(--muted);">5%</div></div>
        </div>
      </div>

      <div class="sb sb-hold">
        <div class="sb-title">⚠ Rebalancing Κυριακής</div>
        <div class="sb-desc">RKLB 17% vs target 10% → Trim €87. VWCE 18% vs target 35% → Αγόρασε €212. AMD εντός target.</div>
      </div>
      <button class="btn btn-p" onclick="showToast('Rebalancing πλάνο στάλθηκε στο AI agent!')">
        <i class="ti ti-refresh"></i> Εκτέλεσε Rebalancing
      </button>
    </div>

    <!-- ── SIGNALS (NOTIFICATIONS) ────────────────── -->
    <div class="screen" id="sc-signals">
      <div class="card">
        <div class="stitle" style="display:flex;justify-content:space-between;">
          <span>Live Signals</span><span class="chip cr">3 Urgent</span>
        </div>

        <div class="notif">
          <div class="n-icon ni-b"><i class="ti ti-trending-up" style="color:#5ee8a3;"></i></div>
          <div>
            <div class="n-title">ΑΓΟΡΑ — RKLB</div>
            <div class="n-desc">-6% χωρίς bad news. Cathie Wood αύξησε θέση. Dip buying κάτω από $22 — thesis intact.</div>
            <div class="n-time">12 λεπτά · YouTube Scanner</div>
          </div>
        </div>

        <div class="notif">
          <div class="n-icon ni-w"><i class="ti ti-alert-triangle" style="color:#e8c060;"></i></div>
          <div>
            <div class="n-title">EARNINGS — AMD αύριο</div>
            <div class="n-desc">Beat probability 72%. EPS estimate $0.68. Μην πουλάς πριν ανακοίνωση. After Market.</div>
            <div class="n-time">07:00 · Earnings Agent</div>
          </div>
        </div>

        <div class="notif">
          <div class="n-icon ni-s"><i class="ti ti-trending-down" style="color:#f08080;"></i></div>
          <div>
            <div class="n-title">ΠΟΥΛΑ — FlyExclusive</div>
            <div class="n-desc">Δεν ταιριάζει στο Space PIE. Πούλα και βάλε τα σε RKLB ή VWCE.</div>
            <div class="n-time">Χτες · Risk Agent</div>
          </div>
        </div>

        <div class="notif">
          <div class="n-icon ni-i"><i class="ti ti-file-text" style="color:#80b0f0;"></i></div>
          <div>
            <div class="n-title">13F — Berkshire Hathaway</div>
            <div class="n-desc">Buffett αύξησε θέση σε AAPL +2.1M μετοχές. Αμετάβλητη η θέση σε OXY.</div>
            <div class="n-time">Πριν 3 ώρες · SEC Tracker</div>
          </div>
        </div>

        <div class="notif">
          <div class="n-icon ni-b"><i class="ti ti-sparkles" style="color:#5ee8a3;"></i></div>
          <div>
            <div class="n-title">Tom Nash — Νέο βίντεο</div>
            <div class="n-desc">MSFT ανέφερε ως "10% υποτιμημένο". DCF target $460. Αγορά κάτω από $415.</div>
            <div class="n-time">Πριν 4 ώρες · YouTube Scanner</div>
          </div>
        </div>
      </div>

      <button class="btn btn-p" onclick="requestNotifications()">
        <i class="ti ti-bell"></i> Ενεργοποίησε Push Notifications
      </button>
    </div>

    <!-- ── GURU FEED ───────────────────────────────── -->
    <div class="screen" id="sc-feed">
      <div class="feed-item">
        <div class="feed-head">
          <div class="av" style="background:rgba(64,128,208,.2);color:#80b0f0;">TN</div>
          <div>
            <div style="font-size:13px;font-weight:600;">Tom Nash</div>
            <div style="font-size:10px;color:var(--muted);">Πριν 4 ώρες · YouTube</div>
          </div>
          <span class="chip cg" style="margin-left:auto;">ΑΓΟΡΑ</span>
        </div>
        <div class="feed-body">DCF ανάλυση MSFT: Azure AI + Copilot ωθούν τα έσοδα. Fair value $460 vs τρέχουσα $415. "10% margin of safety υπάρχει τώρα."</div>
        <div class="feed-tags">
          <span class="chip cg">MSFT</span>
          <span class="chip cgray">DCF</span>
          <span class="chip cgray">YouTube</span>
        </div>
      </div>

      <div class="feed-item">
        <div class="feed-head">
          <div class="av" style="background:rgba(192,80,80,.2);color:#f08080;">CW</div>
          <div>
            <div style="font-size:13px;font-weight:600;">Cathie Wood</div>
            <div style="font-size:10px;color:var(--muted);">Πριν 6 ώρες · ARK</div>
          </div>
          <span class="chip cg" style="margin-left:auto;">ΑΓΟΡΑ</span>
        </div>
        <div class="feed-body">ARK αύξησε RKLB κατά 2.3M μετοχές. "Space economy θα φτάσει $1T. Rocket Lab η μόνη εταιρεία με ολοκληρωμένο launch + manufacturing."</div>
        <div class="feed-tags">
          <span class="chip cg">RKLB</span>
          <span class="chip cp">Space</span>
          <span class="chip cgray">ARK</span>
        </div>
      </div>

      <div class="feed-item">
        <div class="feed-head">
          <div class="av" style="background:rgba(184,134,11,.2);color:#e8c060;">WB</div>
          <div>
            <div style="font-size:13px;font-weight:600;">Warren Buffett</div>
            <div style="font-size:10px;color:var(--muted);">Πριν 3 ώρες · SEC 13F</div>
          </div>
          <span class="chip cg" style="margin-left:auto;">ΑΓΟΡΑ</span>
        </div>
        <div class="feed-body">Berkshire αύξησε AAPL +2.1M μετοχές. OXY αμετάβλητη. Νέα θέση σε Domino's Pizza — consumer resilience play.</div>
        <div class="feed-tags">
          <span class="chip cg">AAPL</span>
          <span class="chip cgold">OXY</span>
          <span class="chip cgray">13F</span>
        </div>
      </div>

      <div class="feed-item">
        <div class="feed-head">
          <div class="av" style="background:rgba(45,155,111,.2);color:#5ee8a3;">HM</div>
          <div>
            <div style="font-size:13px;font-weight:600;">Howard Marks</div>
            <div style="font-size:10px;color:var(--muted);">Σήμερα 09:00 · Memo</div>
          </div>
          <span class="chip cgold" style="margin-left:auto;">ΚΡΑΤΑ</span>
        </div>
        <div class="feed-body">"On Bubble Watch" — Προειδοποίηση για tech valuations. "Όταν όλοι είναι bullish, ο κίνδυνος είναι υψηλότερος." Προτείνει defensive + quality value.</div>
        <div class="feed-tags">
          <span class="chip cgold">BRK.B</span>
          <span class="chip cgold">Defensive</span>
          <span class="chip cgray">Memo</span>
        </div>
      </div>
    </div>

    <!-- ── SECTORS ─────────────────────────────────── -->
    <div class="screen" id="sc-sectors">
      <div class="sector-card">
        <div class="sec-hd">
          <div><div class="sec-name">AI / Τεχνητή Νοημοσύνη</div>
            <div style="font-size:11px;color:var(--muted);">Cathie Wood · Tom Nash · Ben Felix</div></div>
          <span class="chip cg">HOT</span>
        </div>
        <div class="sec-why">Ο σημαντικότερος megatrend. NVDA, MSFT, GOOGL, AMD, PLTR.</div>
        <div class="sec-picks">
          <span class="chip cg">NVDA</span><span class="chip cg">MSFT</span>
          <span class="chip cg">AMD</span><span class="chip cg">PLTR</span><span class="chip cg">GOOGL</span>
        </div>
        <div class="bar-wrap">
          <div class="bar-hd"><span>Guru consensus</span><span>90/100</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:90%;background:#2d9b6f;"></div></div>
        </div>
        <button class="btn" onclick="showToast('AI sector analysis loading...')">Top AI picks ↗</button>
      </div>

      <div class="sector-card">
        <div class="sec-hd">
          <div><div class="sec-name">Semiconductors</div>
            <div style="font-size:11px;color:var(--muted);">Cathie Wood · Tom Nash · Giannis</div></div>
          <span class="chip cg">HOT</span>
        </div>
        <div class="sec-why">AI χρειάζεται chips. TSMC κάνει τα πάντα. ASML αναντικατάστατη.</div>
        <div class="sec-picks">
          <span class="chip cg">TSM</span><span class="chip cg">ASML</span>
          <span class="chip cg">AMD</span><span class="chip cg">NVDA</span>
        </div>
        <div class="bar-wrap">
          <div class="bar-hd"><span>Guru consensus</span><span>85/100</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:85%;background:#2d9b6f;"></div></div>
        </div>
        <button class="btn" onclick="showToast('Semiconductor analysis loading...')">Top Chip picks ↗</button>
      </div>

      <div class="sector-card">
        <div class="sec-hd">
          <div><div class="sec-name">Value Investing</div>
            <div style="font-size:11px;color:var(--muted);">Buffett · Howard Marks · Ben Felix</div></div>
          <span class="chip cgold">Stable</span>
        </div>
        <div class="sec-why">BRK.B, AAPL, AMZN — χαμηλό ρίσκο, σταθερή απόδοση.</div>
        <div class="sec-picks">
          <span class="chip cg">BRK.B</span><span class="chip cg">AAPL</span>
          <span class="chip cg">AMZN</span><span class="chip cg">GOOGL</span>
        </div>
        <div class="bar-wrap">
          <div class="bar-hd"><span>Guru consensus</span><span>88/100</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:88%;background:#2d9b6f;"></div></div>
        </div>
        <button class="btn" onclick="showToast('Value picks loading...')">Top Value picks ↗</button>
      </div>

      <div class="sector-card">
        <div class="sec-hd">
          <div><div class="sec-name">ETFs — Core</div>
            <div style="font-size:11px;color:var(--muted);">Ben Felix · Plain Bagel</div></div>
          <span class="chip cb">Base</span>
        </div>
        <div class="sec-why">Ben Felix: "80% active funds χάνουν από index." VWCE ως θεμέλιο.</div>
        <div class="sec-picks">
          <span class="chip cg">VWCE</span><span class="chip cg">VUAA</span>
          <span class="chip cg">CSPX</span><span class="chip cgold">QQQ</span>
        </div>
        <div class="bar-wrap">
          <div class="bar-hd"><span>Guru consensus</span><span>95/100</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:95%;background:#2d9b6f;"></div></div>
        </div>
        <button class="btn" onclick="showToast('ETF analysis loading...')">Top ETF picks ↗</button>
      </div>

      <div class="sector-card">
        <div class="sec-hd">
          <div><div class="sec-name">Space & Aerospace</div>
            <div style="font-size:11px;color:var(--muted);">Cathie Wood · Giannis Andreou</div></div>
          <span class="chip cp">Έχεις</span>
        </div>
        <div class="sec-why">10ετής megatrend. $1T economy. Υψηλό ρίσκο, τεράστιο potential.</div>
        <div class="sec-picks">
          <span class="chip cg">RKLB</span><span class="chip cgold">ASTS</span>
          <span class="chip cgold">LUNR</span>
        </div>
        <div class="bar-wrap">
          <div class="bar-hd"><span>Guru consensus</span><span>72/100</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:72%;background:#b88020;"></div></div>
        </div>
        <button class="btn" onclick="showToast('Space analysis loading...')">Top Space picks ↗</button>
      </div>
    </div>

    <!-- ── GOAL ───────────────────────────────────── -->
    <div class="screen" id="sc-goal">
      <div class="card">
        <div class="stitle">Ορίσε τον στόχο σου</div>
        <label class="inp-lbl">Έχω τώρα (€)</label>
        <input class="inp" type="number" id="g-start" value="1247" oninput="calcGoal()"/>
        <label class="inp-lbl">Θέλω να φτάσω (€)</label>
        <input class="inp" type="number" id="g-goal" value="3000" oninput="calcGoal()"/>
        <label class="inp-lbl">Προσθέτω κάθε μήνα (€)</label>
        <input class="inp" type="number" id="g-monthly" value="100" oninput="calcGoal()"/>
        <label class="inp-lbl">Ανοχή ρίσκου</label>
        <select class="inp" id="g-risk" onchange="calcGoal()">
          <option value="8">Συντηρητικό (8%/χρόνο)</option>
          <option value="15" selected>Μέτριο (15%/χρόνο)</option>
          <option value="30">Aggressive (30%/χρόνο)</option>
          <option value="50">Πολύ Aggressive (50%/χρόνο)</option>
        </select>
      </div>

      <div class="g2" id="goalMetrics"></div>
      <div id="goalSignal"></div>

      <div class="card">
        <div class="stitle">Πρόοδος</div>
        <div class="prog-wrap">
          <div class="prog-hd">
            <span id="gProgLabel">€1,247 → €3,000</span>
            <span id="gProgPct" style="font-weight:600;color:var(--gm);">42%</span>
          </div>
          <div class="prog-track">
            <div class="prog-fill" id="gProgFill" style="width:42%;"></div>
          </div>
        </div>
        <div id="gTimeline" style="margin-top:8px;"></div>
      </div>

      <div class="card" id="guruGoalCard">
        <div class="stitle">Guru αξιολόγηση</div>
        <div id="guruGoalBars"></div>
      </div>

      <button class="btn btn-p" id="goalAIBtn">AI πλάνο ↗</button>
    </div>

  </div><!-- /content -->

  <!-- Bottom navigation -->
  <div class="bottom-nav">
    <button class="nav-btn on" id="nav-home" onclick="switchNav('home')">
      <i class="ti ti-home"></i>Home
    </button>
    <button class="nav-btn" id="nav-portfolio" onclick="switchNav('portfolio')">
      <i class="ti ti-chart-pie"></i>Portfolio
    </button>
    <button class="nav-btn" id="nav-signals" onclick="switchNav('signals')">
      <i class="ti ti-bell"></i>Signals<span class="nav-badge">3</span>
    </button>
    <button class="nav-btn" id="nav-feed" onclick="switchNav('feed')">
      <i class="ti ti-rss"></i>Feed
    </button>
    <button class="nav-btn" id="nav-sectors" onclick="switchNav('sectors')">
      <i class="ti ti-layout-grid"></i>Sectors
    </button>
    <button class="nav-btn" id="nav-goal" onclick="switchNav('goal')">
      <i class="ti ti-target"></i>Στόχος
    </button>
  </div>
</div><!-- /app -->

<div class="toast" id="toast"></div>

<!-- Firebase SDK for push notifications -->
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-messaging-compat.js"></script>

<script>
// ── Navigation ────────────────────────────────────
function switchNav(name) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('on'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('on'));
  document.getElementById('sc-' + name).classList.add('on');
  document.getElementById('nav-' + name).classList.add('on');
  // scroll top
  document.querySelector('.content').scrollTop = 0;
}

// ── Toast ─────────────────────────────────────────
function showToast(msg, duration = 2500) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), duration);
}

// ── PWA Install (Android) ─────────────────────────
let deferredPrompt = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  document.getElementById('installBanner').classList.add('show');
});
async function installApp() {
  if (!deferredPrompt) {
    showToast('Chrome → ⋮ → "Εγκατάσταση εφαρμογής"');
    return;
  }
  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  if (outcome === 'accepted') {
    showToast('Εγκαταστάθηκε! ✓');
    document.getElementById('installBanner').classList.remove('show');
  }
  deferredPrompt = null;
}
window.addEventListener('appinstalled', () => {
  document.getElementById('installBanner').classList.remove('show');
});

// ── Service Worker registration ───────────────────
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').then(reg => {
    console.log('[SW] Registered:', reg.scope);
  }).catch(err => console.error('[SW] Error:', err));
}

// ── Push Notifications ────────────────────────────
// ΒΑΛΕ ΤΑ ΔΙΚΑ ΣΟΥ Firebase keys εδώ:
const FIREBASE_CONFIG = {
  apiKey:            "YOUR_API_KEY",
  authDomain:        "YOUR_PROJECT.firebaseapp.com",
  projectId:         "YOUR_PROJECT_ID",
  storageBucket:     "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId:             "YOUR_APP_ID",
};
const VAPID_KEY = "YOUR_VAPID_KEY";   // Firebase → Project Settings → Cloud Messaging

let messaging = null;
try {
  firebase.initializeApp(FIREBASE_CONFIG);
  messaging = firebase.messaging();
} catch(e) { console.log('[FCM] Config not set yet'); }

async function requestNotifications() {
  if (!messaging) {
    showToast('Βάλε πρώτα τα Firebase keys στο index.html');
    return;
  }
  try {
    const permission = await Notification.requestPermission();
    if (permission !== 'granted') {
      showToast('Δεν δόθηκε άδεια notifications');
      return;
    }
    const token = await messaging.getToken({ vapidKey: VAPID_KEY });
    console.log('[FCM] Token:', token);
    // Αποθήκευσε το token στο Supabase
    showToast('Push notifications ενεργοποιήθηκαν! ✓');
  } catch(e) {
    showToast('Σφάλμα: ' + e.message);
  }
}

function showNotifPrompt() {
  switchNav('signals');
}

// ── Goal Calculator ───────────────────────────────
function calcGoal() {
  const start   = parseFloat(document.getElementById('g-start').value)   || 1247;
  const goal    = parseFloat(document.getElementById('g-goal').value)    || 3000;
  const monthly = parseFloat(document.getElementById('g-monthly').value) || 100;
  const rate    = parseFloat(document.getElementById('g-risk').value)    || 15;

  const mr = Math.pow(1 + rate/100, 1/12) - 1;
  let val = start, months = 0;
  while (val < goal && months < 360) {
    val = val * (1 + mr) + monthly;
    months++;
  }
  const yrs  = (months / 12).toFixed(1);
  const pct  = Math.round(start / goal * 100);
  const ti   = Math.round(start + monthly * months);
  const prof = Math.round(goal - ti);
  const color = months <= 24 ? '#5ee8a3' : months <= 60 ? '#e8c060' : '#f08080';

  document.getElementById('goalMetrics').innerHTML = `
    <div class="met"><div class="met-lbl">Χρόνος στόχου</div>
      <div class="met-val" style="color:${color};">${months > 120 ? '10+ χρ' : months > 24 ? yrs+' χρ' : months+' μήνες'}</div></div>
    <div class="met"><div class="met-lbl">Μηνιαία απόδοση</div>
      <div class="met-val green">${(mr*100).toFixed(1)}%</div></div>
    <div class="met"><div class="met-lbl">Σύνολο επένδυσης</div>
      <div class="met-val blue">€${ti.toLocaleString()}</div></div>
    <div class="met"><div class="met-lbl">Κέρδος αγοράς</div>
      <div class="met-val green">€${Math.max(0,prof).toLocaleString()}</div></div>`;

  const ok = months <= 36;
  document.getElementById('goalSignal').innerHTML = `
    <div class="sb ${ok ? 'sb-buy' : months<=60 ? 'sb-hold' : 'sb-sell'}">
      <div class="sb-title">${ok ? '✓ Εφικτός στόχος' : months<=60 ? '⚠ Φιλόδοξος' : '⚠ Πολύ aggressive'}</div>
      <div class="sb-desc">${months} μήνες με ${rate}%/χρόνο + €${monthly}/μήνα.
        ${ok ? 'Gurus λένε: ξεκίνα ΑΜΕΣΩΣ.' : 'Σκέψου να αυξήσεις μηνιαία συνεισφορά.'}</div>
    </div>`;

  document.getElementById('gProgLabel').textContent = `€${start.toLocaleString()} → €${goal.toLocaleString()}`;
  document.getElementById('gProgPct').textContent  = pct + '%';
  document.getElementById('gProgFill').style.width = Math.min(100,pct) + '%';
  document.getElementById('gProgFill').style.background = color;

  // Milestones
  const milestones = [];
  let v2 = start;
  for (let m = 1; m <= Math.min(months, 36); m++) {
    v2 = v2 * (1+mr) + monthly;
    if (m % Math.max(1,Math.floor(months/4)) === 0 || m === months) {
      milestones.push({m, v: Math.round(v2)});
    }
  }
  document.getElementById('gTimeline').innerHTML = milestones.map(p => `
    <div class="bar-wrap">
      <div class="bar-hd"><span>Μήνας ${p.m}</span>
        <span style="font-weight:600;color:${color};">€${p.v.toLocaleString()}</span></div>
      <div class="bar-track"><div class="bar-fill" style="width:${Math.min(100,Math.round(p.v/goal*100))}%;background:${color};"></div></div>
    </div>`).join('');

  // Guru bars
  const gurus = [
    {n:'Warren Buffett', s: Math.max(20, 95-months*0.5)},
    {n:'Ben Felix',      s: Math.max(20, 90-months*0.4)},
    {n:'Howard Marks',   s: Math.max(20, 88-months*0.4)},
    {n:'Tom Nash',       s: Math.max(30, 75+months*0.1)},
    {n:'Cathie Wood',    s: Math.max(40, 65+months*0.15)},
  ];
  document.getElementById('guruGoalBars').innerHTML = gurus.map(g => {
    const v   = Math.round(g.s);
    const col = v>=70 ? '#2d9b6f' : v>=50 ? '#b88020' : '#c05050';
    const lbl = v>=70 ? 'Εγκρίνει' : v>=50 ? 'Επιφυλακτικός' : 'Αντιτίθεται';
    return `<div class="bar-wrap">
      <div class="bar-hd"><span>${g.n}</span>
        <span style="color:${col};font-weight:600;">${lbl}</span></div>
      <div class="bar-track"><div class="bar-fill" style="width:${v}%;background:${col};"></div></div>
    </div>`;
  }).join('');

  document.getElementById('goalAIBtn').onclick = () => {
    showToast(`Στέλνω στο AI: €${Math.round(start)} → €${Math.round(goal)} σε ${months} μήνες...`);
  };
}

// Init
calcGoal();
</script>
</body>
</html>
