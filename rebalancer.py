import os, asyncio, aiohttp, json

GROQ_KEY = os.getenv("GROQ_API_KEY", "")

PORTFOLIO = {
    "total_value": 1247.50,
    "cash": 62.50,
    "positions": [
        {"ticker": "AMD",  "value": 310.0, "pnl_pct": 22.1},
        {"ticker": "RKLB", "value": 212.0, "pnl_pct": 41.2},
        {"ticker": "PLTR", "value": 156.0, "pnl_pct": 88.4},
        {"ticker": "MELI", "value": 125.0, "pnl_pct": 14.8},
        {"ticker": "ASTS", "value":  93.0, "pnl_pct": -8.3},
        {"ticker": "LSE",  "value":  62.5, "pnl_pct":  5.2},
        {"ticker": "VWCE", "value": 226.5, "pnl_pct": 12.0},
    ]
}

TARGET = {
    "VWCE": 0.35, "AMD": 0.20, "PLTR": 0.10,
    "MELI": 0.10, "RKLB": 0.10, "ASTS": 0.05,
    "LSE": 0.05,  "CASH": 0.05,
}

async def ask_groq(session, prompt):
    if not GROQ_KEY:
        print("No GROQ_API_KEY set!")
        return ""
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}]
    }
    async with session.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers, json=body
    ) as r:
        if r.status != 200:
            print(f"Groq error: {r.status} - {await r.text()}")
            return ""
        d = await r.json()
        return d["choices"][0]["message"]["content"].strip()

async def main():
    total = PORTFOLIO["total_value"]
    current = {p["ticker"]: round(p["value"] / total, 4)
               for p in PORTFOLIO["positions"]}
    current["CASH"] = round(PORTFOLIO["cash"] / total, 4)

    trades = []
    for ticker in set(list(current.keys()) + list(TARGET.keys())):
        if ticker == "CASH":
            continue
        curr_pct   = current.get(ticker, 0.0)
        target_pct = TARGET.get(ticker, 0.0)
        diff       = curr_pct - target_pct
        amount     = abs(diff) * total
        if abs(diff) < 0.05 or amount < 10:
            continue
        trades.append({
            "ticker": ticker,
            "action": "SELL" if diff > 0 else "BUY",
            "amount_eur": round(amount, 2),
            "curr_pct": round(curr_pct * 100, 1),
            "target_pct": round(target_pct * 100, 1),
        })

    print(f"\n{'='*40}")
    print(f"Portfolio: EUR {total:,.2f}")
    print(f"Trades needed: {len(trades)}")
    print(f"{'='*40}")
    for t in sorted(trades, key=lambda x: x["amount_eur"], reverse=True):
        icon = "🔴 SELL" if t["action"] == "SELL" else "🟢 BUY"
        print(f"  {icon} EUR {t['amount_eur']:6.0f}  {t['ticker']:<6} "
              f"({t['curr_pct']}% -> {t['target_pct']}%)")

    if not trades:
        print("Portfolio balanced - no trades needed!")
        return

    async with aiohttp.ClientSession() as session:
        prompt = f"""Rebalancing report στα Ελληνικά.
Portfolio EUR {total:,.0f}.
Κινήσεις απαραίτητες: {json.dumps(trades, ensure_ascii=False)}
Γράψε 3 προτάσεις: ποιες κινήσεις χρειάζονται, ποια η σημαντικότερη και γιατί."""
        print("\nGroq AI Analysis:")
        print("-" * 40)
        analysis = await ask_groq(session, prompt)
        print(analysis)

asyncio.run(main())
