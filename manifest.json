name: Guru Investor OS

on:
  schedule:
    - cron: '*/15 * * * *'   # YouTube — κάθε 15 λεπτά
    - cron: '0 7 * * *'      # Earnings — κάθε μέρα 07:00
    - cron: '0 8 * * 0'      # Rebalancer — κάθε Κυριακή
    - cron: '0 */6 * * *'    # SEC 13F — κάθε 6 ώρες
  workflow_dispatch:
    inputs:
      module:
        type: choice
        default: youtube
        options: [youtube, sec, rebalancer, earnings, all]

env:
  PYTHONUNBUFFERED: "1"

jobs:

  youtube:
    name: YouTube Scanner
    runs-on: ubuntu-latest
    if: |
      (github.event_name == 'schedule' && contains(github.event.schedule, '*/15')) ||
      (github.event_name == 'workflow_dispatch' && contains(fromJSON('["youtube","all"]'), github.event.inputs.module))
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11', cache: pip }
      - run: pip install aiohttp youtube-transcript-api
      - uses: actions/cache@v4
        with:
          path: /tmp/yt_seen.json
          key: yt-${{ github.run_id }}
          restore-keys: yt-
      - run: python backend/youtube-scanner/scanner.py
        env:
          GROQ_API_KEY:    ${{ secrets.GROQ_API_KEY }}
          GEMINI_API_KEY:  ${{ secrets.GEMINI_API_KEY }}
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
          FCM_SERVER_KEY:  ${{ secrets.FCM_SERVER_KEY }}
          SUPABASE_URL:    ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY:    ${{ secrets.SUPABASE_KEY }}
      - uses: actions/cache@v4
        with:
          path: /tmp/yt_seen.json
          key: yt-${{ github.run_id }}

  sec:
    name: SEC 13F Tracker
    runs-on: ubuntu-latest
    if: |
      (github.event_name == 'schedule' && contains(github.event.schedule, '0 */6')) ||
      (github.event_name == 'workflow_dispatch' && contains(fromJSON('["sec","all"]'), github.event.inputs.module))
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11', cache: pip }
      - run: pip install aiohttp
      - uses: actions/cache@v4
        with:
          path: /tmp/sec_*.json
          key: sec-${{ github.run_id }}
          restore-keys: sec-
      - run: python backend/sec-tracker/tracker.py
        env:
          GROQ_API_KEY:   ${{ secrets.GROQ_API_KEY }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          FCM_SERVER_KEY: ${{ secrets.FCM_SERVER_KEY }}
      - uses: actions/cache@v4
        with:
          path: /tmp/sec_*.json
          key: sec-${{ github.run_id }}

  rebalancer:
    name: Sunday Rebalancer
    runs-on: ubuntu-latest
    if: |
      (github.event_name == 'schedule' && contains(github.event.schedule, '0 8 * * 0')) ||
      (github.event_name == 'workflow_dispatch' && contains(fromJSON('["rebalancer","all"]'), github.event.inputs.module))
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11', cache: pip }
      - run: pip install aiohttp
      - run: python backend/rebalancer/rebalancer.py
        env:
          GROQ_API_KEY:        ${{ secrets.GROQ_API_KEY }}
          GEMINI_API_KEY:      ${{ secrets.GEMINI_API_KEY }}
          TRADING212_API_KEY:  ${{ secrets.TRADING212_API_KEY }}
          FCM_SERVER_KEY:      ${{ secrets.FCM_SERVER_KEY }}

  earnings:
    name: Daily Earnings Preview
    runs-on: ubuntu-latest
    if: |
      (github.event_name == 'schedule' && contains(github.event.schedule, '0 7 * * *')) ||
      (github.event_name == 'workflow_dispatch' && contains(fromJSON('["earnings","all"]'), github.event.inputs.module))
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11', cache: pip }
      - run: pip install aiohttp
      - run: python backend/earnings-preview/earnings.py
        env:
          GROQ_API_KEY:    ${{ secrets.GROQ_API_KEY }}
          GEMINI_API_KEY:  ${{ secrets.GEMINI_API_KEY }}
          FINNHUB_API_KEY: ${{ secrets.FINNHUB_API_KEY }}
          FCM_SERVER_KEY:  ${{ secrets.FCM_SERVER_KEY }}
