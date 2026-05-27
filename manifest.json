"""Firebase FCM — Android push notifications (δωρεάν)"""
import os, asyncio, aiohttp
from datetime import datetime

FCM_KEY   = os.getenv("FCM_SERVER_KEY", "")
FCM_TOPIC = "guru_alerts"   # όλοι subscribe εδώ


async def _send(title: str, body: str, data: dict, urgency: str = "medium") -> bool:
    if not FCM_KEY:
        print(f"[NOTIFY] [{urgency.upper()}] {title}: {body}")
        return True

    high = urgency in ("critical", "high")
    color = {"critical": "#c05050", "high": "#2d9b6f",
             "medium": "#b8860b"}.get(urgency, "#888888")

    payload = {
        "to": f"/topics/{FCM_TOPIC}",
        "priority": "high" if high else "normal",
        "notification": {"title": title, "body": body, "sound": "default"},
        "data": {**data, "urgency": urgency,
                 "ts": datetime.utcnow().isoformat()},
        "android": {
            "priority": "high" if high else "normal",
            "notification": {"color": color, "channel_id": "guru_alerts",
                             "click_action": "OPEN_ALERT"},
        },
    }
    headers = {"Authorization": f"key={FCM_KEY}",
               "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as s:
        async with s.post("https://fcm.googleapis.com/fcm/send",
                          headers=headers, json=payload) as r:
            result = await r.json()
            ok = result.get("success", 0) > 0
            if not ok: print(f"[FCM] Error: {result}")
            return ok


async def buy(ticker: str, reason: str, source: str = "", potential: str = ""):
    body = reason + (f" | Potential: {potential}" if potential else "")
    return await _send(f"ΑΓΟΡΑ — {ticker}", body,
                       {"type": "BUY", "ticker": ticker, "source": source},
                       urgency="high")

async def sell(ticker: str, reason: str, urgency: str = "critical"):
    return await _send(f"ΠΟΥΛΑ — {ticker}", reason,
                       {"type": "SELL", "ticker": ticker},
                       urgency=urgency)

async def info(title: str, body: str, data: dict = {}):
    return await _send(title, body, {"type": "INFO", **data}, urgency="medium")
