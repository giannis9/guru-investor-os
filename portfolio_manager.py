"""
Portfolio Manager Agent v3
- Διαβάζει settings.json για portfolio + στόχο
- Αναλύει κάθε θέση (buy/sell/hold)
- Tracks progress προς τον στόχο σε £
- Στέλνει push notifications
"""
import os, asyncio, aiohttp, json
from datetime import datetime
from pathlib import Path

GROQ_KEY    = os.getenv("GROQ_API_KEY", "")
FINNHUB_KEY = os.getenv("FINNHUB_API_KEY", "")
FCM_KEY     = os.getenv("FCM_SERVER_KEY", "")


def load_settings():
    path = Path(__file__).parent / "settings.json"
    with open(path) as f:
        return json.load(f)


async def ask_groq(session, prompt, max_tokens=800):
    if not GROQ_KEY:
        print("[GROQ] No key — set GROQ_API_KEY secret"); return ""
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    body = {"model": "llama-3.3-70b-versatile", "max_tokens": max_tokens,
            "temperature": 0.1,
            "messages": [{"role": "user", "content": prompt}]}
    try:
        async with session.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers, json=body,
            timeout=aiohttp.ClientTimeout(total=40)
        ) as r:
            if r.status != 200:
                print(f"[GROQ] {r.status}: {await r.text()}"); return ""
            d = await r.json()
            return d["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[GROQ] Exception: {e}"); return ""


async def get_price(session, ticker):
    if not FINNHUB_KEY: return None
    try:
        async with session.get(
            f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}",
            timeout=aiohttp.ClientTimeout(total=10)
        ) as r:
            if r.status != 200: return None
            d = await r.json()
            return d.get("c") or d.get("pc")
    except:
        return None


async def send_push(title, body, urgency="medium"):
    color = {"critical":"#c05050","high":"#2d9b6f","medium":"#b8860b"}.get(urgency,"#888")
    if not FCM_KEY:
        print(f"  [{urgency.upper()}] {title}: {body}"); return
    payload = {
        "to": "/topics/guru_alerts",
        "priority": "high" if urgency in ("critical","high") else "normal",
        "notification": {"title": title, "body": body, "sound": "default"},
        "android": {"notification": {"color": color, "channel_id": "guru_alerts"}},
    }
    async with aiohttp.ClientSession() as s:
        async with s.post(
            "https://fcm.googleapis.com/fcm/send",
            headers={"Authorization": f"key={FCM_KEY}", "Content-Type": "application/json"},
            json=payload
        ) as r:
            ok = (await r.json()).get("success", 0) > 0
            print(f"  [PUSH {'OK' if ok else 'FAIL'}] {title}")


async def main():
    cfg        = load_settings()
    goal_cfg   = cfg["goal"]
    port_cfg   = cfg["portfolio"]
    alert_cfg  = cfg["alerts"]

    target     = goal_cfg["target_gbp"]
    months     = goal_cfg["months"]
    monthly    = goal_cfg["monthly_contribution_gbp"]
    risk       = goal_cfg["risk_level"]
    positions  = port_cfg["positions"]
    cash       = port_cfg.get("cash_gbp", 0)
    currency   = "£"

    # Calculate totals
    total      = sum(p["value_gbp"] for p in positions) + cash
    needed     = target - total
    progress   = (total / target) * 100
    on_track_val = total + monthly * months  # simple projection

    print(f"\n{'='*55}")
    print(f"  PORTFOLIO MANAGER — {datetime.utcnow().strftime('%a %d %b %Y %H:%M')} UTC")
    print(f"{'='*55}")
    print(f"  Total:    {currency}{total:,.2f}")
    print(f"  Goal:     {currency}{target:,.2f} in {months} months")
    print(f"  Progress: {progress:.1f}%")
    print(f"  Needed:   {currency}{needed:,.2f}")
    print(f"  Monthly DCA: {currency}{monthly}/month")
    print(f"  Projected: {currency}{on_track_val:,.2f} (DCA only, no growth)")

    # Sort positions by value
    positions_sorted = sorted(positions, key=lambda x: x["value_gbp"], reverse=True)

    signals = []

    async with aiohttp.ClientSession() as session:

        # ── Price updates ──────────────────────────────────
        print(f"\n  {'TICKER':<8} {'VALUE':>10} {'WEIGHT':>8}  SIGNAL")
        print(f"  {'─'*50}")

        for pos in positions_sorted:
            ticker = pos["ticker"]
            value  = pos["value_gbp"]
            weight = (value / total * 100) if total else 0
            sig    = ""

            # Stop loss check
            avg = pos.get("avg_cost_gbp", 0)
            if avg and avg > 0:
                curr = pos.get("current_price_gbp", avg)
                pnl  = (curr - avg) / avg * 100
                if pnl <= alert_cfg["stop_loss_pct"]:
                    sig = f"🔴 STOP-LOSS ({pnl:.1f}%)"
                    signals.append({"ticker": ticker, "type": "SELL", "urgency": "critical",
                                    "reason": f"Down {pnl:.1f}% — below stop-loss"})
                elif pnl >= alert_cfg["profit_take_pct"]:
                    sig = f"💰 TAKE PROFIT (+{pnl:.1f}%)"
                    signals.append({"ticker": ticker, "type": "SELL_PARTIAL", "urgency": "high",
                                    "reason": f"Up {pnl:.1f}% — consider taking 25-50% profit"})

            # Overweight check
            if weight > alert_cfg["overweight_limit_pct"]:
                sig = sig or f"⚠ OVERWEIGHT ({weight:.1f}%)"
                signals.append({"ticker": ticker, "type": "TRIM", "urgency": "medium",
                                "reason": f"Overweight at {weight:.1f}% of portfolio"})

            print(f"  {ticker:<8} {currency}{value:>8.2f}   {weight:>5.1f}%  {sig}")

        print(f"  {'─'*50}")
        print(f"  {'TOTAL':<8} {currency}{total:>8.2f}  100.0%")
        if cash:
            print(f"  {'CASH':<8} {currency}{cash:>8.2f}")

        # ── AI Analysis ────────────────────────────────────
        top10 = [{"ticker": p["ticker"], "name": p["name"],
                  "value_gbp": p["value_gbp"],
                  "weight_pct": round(p["value_gbp"]/total*100, 1)}
                 for p in positions_sorted[:10]]

        all_tickers = [p["ticker"] for p in positions_sorted]

        prompt = f"""Είσαι AI portfolio manager. Αναλύσε αυτό το χαρτοφυλάκιο και δώσε συγκεκριμένες συμβουλές.

ΧΑΡΤΟΦΥΛΑΚΙΟ (σε British Pounds £):
Σύνολο: £{total:,.2f}
Top 10 θέσεις: {json.dumps(top10, ensure_ascii=False)}
Όλες οι θέσεις: {all_tickers}
Cash: £{cash:,.2f}

ΣΤΟΧΟΣ: £{target:,.0f} σε {months} μήνες
ΠΡΟΟΔΟΣ: {progress:.1f}%
ΜΗΝΙΑΙΑ ΕΠΕΝΔΥΣΗ: £{monthly}/μήνα
RISK LEVEL: {risk}

SIGNALS που εντοπίστηκαν: {json.dumps(signals, ensure_ascii=False)}

Δώσε ανάλυση στα Ελληνικά:

1. ΣΥΝΟΨΗ ΧΑΡΤΟΦΥΛΑΚΙΟΥ (1-2 προτάσεις — ποιοι κλάδοι κυριαρχούν, ποια η γενική κατάσταση)

2. ΑΜΕΣΕΣ ΚΙΝΗΣΕΙΣ (top 3 — τι να κάνεις ΤΩΡΑ με συγκεκριμένα £):
   - π.χ. "Πούλα £X από PLTR γιατί..."
   - π.χ. "Αγόρασε £X σε VUSA γιατί..."

3. ΑΝΑΛΥΣΗ ΚΙΝΔΥΝΟΥ (ποιες θέσεις είναι risky, ποιες stable)

4. ΠΡΟΟΔΟΣ ΣΤΟΧΟΥ (είσαι on track; αν όχι τι χρειάζεται)

5. ΣΥΣΤΑΣΗ ΕΒΔΟΜΑΔΑΣ (1 συγκεκριμένη ενέργεια)

Χωρίς markdown, με αριθμούς σε £."""

        print(f"\n{'─'*55}")
        print("  GROQ AI ANALYSIS")
        print(f"{'─'*55}")
        analysis = await ask_groq(session, prompt, max_tokens=900)
        print(analysis)

        # ── Push Notifications ─────────────────────────────
        print(f"\n  Sending notifications...")

        # Critical signals
        for sig in signals:
            if sig["urgency"] == "critical":
                await send_push(
                    f"🔴 ΠΟΥΛΑ — {sig['ticker']}",
                    sig["reason"],
                    urgency="critical"
                )
                await asyncio.sleep(0.8)

        # High priority
        for sig in [s for s in signals if s["urgency"] == "high"]:
            await send_push(
                f"💰 Profit Taking — {sig['ticker']}",
                sig["reason"],
                urgency="high"
            )
            await asyncio.sleep(0.8)

        # Daily summary
        on_track = on_track_val >= target * 0.9
        status   = "✅ On track" if on_track else f"⚠ Χρειάζεσαι +£{needed/months:.0f}/μήνα"
        await send_push(
            f"📊 Daily Report — £{total:,.0f} / £{target:,.0f}",
            f"{progress:.0f}% προς στόχο. {status}. {len(signals)} signals σήμερα.",
            urgency="medium"
        )

    print(f"\n{'='*55}")
    print("  Portfolio Manager done.")
    print(f"{'='*55}\n")


asyncio.run(main())
