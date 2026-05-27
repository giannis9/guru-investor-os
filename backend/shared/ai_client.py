"""Config — βάλε τα keys στα GitHub Secrets"""
import os

# AI (δωρεάν)
GROQ_API_KEY   = os.getenv("GROQ_API_KEY",  "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Market data (δωρεάν)
YOUTUBE_API_KEY    = os.getenv("YOUTUBE_API_KEY",    "")
FINNHUB_API_KEY    = os.getenv("FINNHUB_API_KEY",    "")
TRADING212_API_KEY = os.getenv("TRADING212_API_KEY", "")

# Notifications (δωρεάν)
FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY", "")

# Database (δωρεάν)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Gurus — YouTube Channel IDs
GURU_CHANNELS = {
    "Ben Felix":       "UC3Pfbn2JkHRRL7B-DNRMIpg",
    "The Plain Bagel": "UCfdmXVvNjkIkBHFkGMWPqYg",
    "Tom Nash":        "UCo9oq7LDkCjANi9G8HE5dRw",
    "Andrei Jikh":     "UCGy7SkBjcIAgTiwkXEtPnYg",
    "Giannis Andreou": "UCxxxxxxxxxxxxxxxxxxxxxxx",  # ← βάλε πραγματικό ID
}

# SEC 13F filers (CIK)
SEC_FILERS = {
    "Berkshire Hathaway": "0001067983",
    "ARK Invest":         "0001697748",
    "Pershing Square":    "0001336528",
}

# Το portfolio σου — target allocation
TARGET_ALLOCATION = {
    "VWCE": 0.35, "AMD":  0.20, "PLTR": 0.10,
    "MELI": 0.10, "RKLB": 0.10, "ASTS": 0.05,
    "LSE":  0.05, "CASH": 0.05,
}

# Watchlist για earnings alerts
WATCHLIST = ["AMD","PLTR","MELI","RKLB","ASTS","LSE","LITE","NVDA","MSFT","ASML"]
