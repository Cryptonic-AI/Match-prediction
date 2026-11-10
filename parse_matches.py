import os
import random
from datetime import datetime, timedelta, timezone
import requests

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
API_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_KEY:
    raise SystemExit("❌ API_FOOTBALL_KEY environment variable is missing")

LEAGUE_ID = 39          # Premier League
SEASON = 2025           # 2025/2026 season

today = datetime.now(timezone.utc).date()
date_from = today.isoformat()
date_to   = (today + timedelta(days=7)).isoformat()

url = "https://v3.football.api-sports.io/fixtures"
params = {
    "league": LEAGUE_ID,
    "season": SEASON,
    "from": date_from,
    "to": date_to,
    "timezone": "UTC",
}
headers = {
    "x-apisports-key": API_KEY
}

# ------------------------------------------------------------------
# Fetch
# ------------------------------------------------------------------
print(f"Fetching fixtures {date_from} → {date_to} (season {SEASON}) …")
response = requests.get(url, headers=headers, params=params, timeout=30)

if response.status_code != 200:
    print(f"HTTP {response.status_code}")
    print(response.text)
    raise SystemExit("API request failed")

data = response.json()

errors = data.get("errors")
if errors:
    print("API returned errors:", errors)
    raise SystemExit("API key or request invalid")

matches = data.get("response", [])
print(f"Found {len(matches)} matches")

# ------------------------------------------------------------------
# Build HTML
# ------------------------------------------------------------------
outcomes = ["1", "X", "2", "1X", "12", "X2"]

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Match Predictions</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 24px;
            background: #141414;
            color: #eee;
        }}
        h1 {{
            margin-top: 0;
            font-size: 1.6rem;
        }}
        .meta {{
            color: #888;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #1e1e1e;
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid #333;
        }}
        th {{
            background: #2a2a2a;
            font-weight: 600;
            color: #ccc;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        .prediction {{
            font-weight: 700;
            color: #ff6b6b;
        }}
        .empty {{
            padding: 40px;
            text-align: center;
            color: #888;
        }}
    </style>
</head>
<body>
    <h1>Upcoming Match Predictions</h1>
    <div class="meta">
        Premier League · {date_from} → {date_to} · Generated {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
    </div>
"""

if not matches:
    html += '<div class="empty">No upcoming matches found in the selected period.</div>'
else:
    html += """
    <table>
        <thead>
            <tr>
                <th>Time (UTC)</th>
                <th>Tournament</th>
                <th>Match</th>
                <th>Prediction</th>
            </tr>
        </thead>
        <tbody>
"""
    for match in matches:
        dt = match["fixture"]["date"].replace("T", " ")[:16]
        league = match["league"]["name"]
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        prediction = random.choice(outcomes)

        html += f"""
            <tr>
                <td>{dt}</td>
                <td>{league}</td>
                <td>{home} vs {away}</td>
                <td class="prediction">{prediction}</td>
            </tr>
"""
    html += """
        </tbody>
    </table>
"""

html += """
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html updated successfully")