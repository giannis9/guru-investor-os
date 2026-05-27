"""
Stock Discovery Agent v3
- Διαβάζει settings.json
- Βρίσκει νέες μετοχές από gurus βάσει στόχου
- Αξιολογεί fit με το υπάρχον portfolio
- Δίνει: τιμή αγοράς, target, stop-loss, πότε να πουλήσεις
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


async def ask_groq_json(session, prompt, max_tokens=1200):
    if not GROQ_KEY:
        print("[GROQ] No key"); return {}
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    body = {
        "model": "llama-3.3-70b-versatile",
        "max_tokens": max_tokens,
        "temperature": 0.1,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    try:
        async with session.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers, json=body,
            timeout=aiohttp.ClientTimeout(total=60)
        ) as r:
            if r.status != 200:
                print(f"[GROQ] {r.status}: {await r.text()}"); return {}
            d = await r.json()
            raw = d["choices"][0]["message"]["content"].strip()
            return json.loads(raw)
    except Exception as e:
        print(f"[GROQ] Exception: {e}"); return {}


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
    cfg       = load_settings()
    goal_cfg  = cfg["goal"]
    port_cfg  = cfg["portfolio"]
    gurus     = cfg.get("gurus", [])

    target    = goal_cfg["target_gbp"]
    months    = goal_cfg["months"]
    monthly   = goal_cfg["monthly_contribution_gbp"]
    risk      = goal_cfg["risk_level"]

    existing  = [p["ticker"] for p in port_cfg["positions"]]
    total_val = sum(p["value_gbp"] for p in port_cfg["positions"])
    progress  = (total_val / target) * 100

    print(f"\n{'='*55}")
    print(f"  STOCK DISCOVERY — {datetime.utcnow().strftime('%a %d %b %Y')}")
    print(f"  Goal: £{target:,.0f} in {months}m | Risk: {risk}")
    print(f"  Portfolio: £{total_val:,.2f} ({progress:.1f}% of goal)")
    print(f"{'='*55}")
    print(f"\n  Existing positions ({len(existing)}): {', '.join(existing)}")
    print(f"\n  Asking Groq AI for new opportunities...")

    async with aiohttp.ClientSession() as session:

        prompt = f"""You are an expert investment advisor. Find the best NEW stock opportunities for this investor.

INVESTOR PROFILE:
- Goal: £{target:,.0f} in {months} months
- Current portfolio value: £{total_val:,.2f} ({progress:.1f}% of goal)
- Monthly contribution: £{monthly}/month
- Risk tolerance: {risk}
- Currency: GBP (British Pounds)

ALREADY OWNS (do NOT suggest these):
{existing}

GURU SOURCES TO CONSIDER:
{', '.join(gurus)}

Find stocks that these gurus currently recommend or have recently mentioned positively.

RETURN JSON with exactly this structure:
{{
  "market_context": "2-3 sentences in Greek about current market conditions",
  "goal_analysis": "Is the goal realistic? What annual return is needed? (in Greek)",
  "picks": [
    {{
      "ticker": "MSFT",
      "name": "Microsoft",
      "current_price_gbp": 312.50,
      "buy_below_gbp": 320.00,
      "target_gbp": 400.00,
      "stop_loss_gbp": 265.00,
      "upside_pct": 28,
      "timeframe_months": 18,
      "suggested_allocation_gbp": 50,
      "gurus": ["Tom Nash", "Bill Ackman"],
      "why_now_greek": "Γιατί να αγοράσεις τώρα (2 προτάσεις)",
      "when_to_sell_greek": "Πότε να πουλήσεις (1 πρόταση)",
      "when_to_buy_more_greek": "Πότε να αγοράσεις περισσότερο (1 πρόταση)",
      "risk": "low|medium|high",
      "fits_goal": true,
      "sector": "Technology"
    }}
  ],
  "portfolio_advice_greek": "Συμβουλή για το συνολικό portfolio (3 προτάσεις)",
  "this_week_action_greek": "Μία συγκεκριμένη ενέργεια αυτή την εβδομάδα με £"
}}

Rules:
- Suggest exactly 6 stocks
- Prices in GBP (British Pounds £)
- Prioritize stocks that fit the {risk} risk profile
- Consider the {months}-month timeframe
- suggested_allocation_gbp should be realistic for someone with £{monthly}/month to invest
- Focus on stocks that gurus have specifically mentioned recently"""

        result = await ask_groq_json(session, prompt, max_tokens=1500)

        if not result:
            print("  No result from Groq AI")
            return

        # ── Display results ────────────────────────────────
        print(f"\n{'─'*55}")
        print(f"  MARKET: {result.get('market_context','')}")
        print(f"\n  GOAL: {result.get('goal_analysis','')}")

        picks = result.get("picks", [])
        print(f"\n{'─'*55}")
        print(f"  TOP {len(picks)} STOCK PICKS THIS WEEK")
        print(f"{'─'*55}")

        for i, p in enumerate(picks, 1):
            ticker   = p.get("ticker","")
            name     = p.get("name","")
            buy_at   = p.get("buy_below_gbp", 0)
            target   = p.get("target_gbp", 0)
            sl       = p.get("stop_loss_gbp", 0)
            upside   = p.get("upside_pct", 0)
            tf       = p.get("timeframe_months", 0)
            alloc    = p.get("suggested_allocation_gbp", 0)
            gurus_s  = ", ".join(p.get("gurus", []))
            why      = p.get("why_now_greek","")
            sell     = p.get("when_to_sell_greek","")
            buy_more = p.get("when_to_buy_more_greek","")
            risk_lvl = p.get("risk","medium")
            sector   = p.get("sector","")
            risk_icon = {"low":"🟢","medium":"🟡","high":"🔴"}.get(risk_lvl,"🟡")

            print(f"""
  #{i} {ticker} — {name} ({sector}) {risk_icon}
  ┌─ Αγορά κάτω από: £{buy_at:.2f}
  ├─ Target:          £{target:.2f} (+{upside}% σε {tf} μήνες)
  ├─ Stop-loss:       £{sl:.2f}
  ├─ Suggested:       £{alloc:.0f} allocation
  ├─ Gurus:           {gurus_s}
  ├─ Γιατί τώρα:      {why}
  ├─ Πότε να πουλήσεις: {sell}
  └─ Πότε αγόρασε περισσότερο: {buy_more}""")

        advice = result.get("portfolio_advice_greek","")
        action = result.get("this_week_action_greek","")
        print(f"\n{'─'*55}")
        print(f"  PORTFOLIO ADVICE: {advice}")
        print(f"\n  THIS WEEK → {action}")

        # ── Push notifications ─────────────────────────────
        print(f"\n  Sending notifications...")

        for pick in picks[:3]:
            ticker = pick.get("ticker","")
            upside = pick.get("upside_pct",0)
            buy_at = pick.get("buy_below_gbp",0)
            target = pick.get("target_gbp",0)
            gurus_s = ", ".join(pick.get("gurus",[])[:2])
            why    = pick.get("why_now_greek","")[:70]
            await send_push(
                f"🟢 Νέα ευκαιρία — {ticker} (+{upside}%)",
                f"{gurus_s} | Αγορά: £{buy_at:.2f} → Target: £{target:.2f} | {why}",
                urgency="high"
            )
            await asyncio.sleep(0.8)

        tickers_list = [p["ticker"] for p in picks]
        await send_push(
            "📈 Weekly Picks",
            f"{', '.join(tickers_list)} | {action[:80]}",
            urgency="medium"
        )

    print(f"\n{'='*55}")
    print("  Stock Discovery done.")
    print(f"{'='*55}\n")


asyncio.run(main())
