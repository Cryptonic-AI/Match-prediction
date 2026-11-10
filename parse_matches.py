import os
import random
from datetime import datetime, timedelta, timezone
import requests

API_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_KEY:
    raise SystemExit("❌ API_FOOTBALL_KEY environment variable is missing")

# Get today + next 2 days (covers "upcoming / tomorrow")
today = datetime.now(timezone.utc).date()
dates = [
    today.isoformat(),
    (today + timedelta(days=1)).isoformat(),
    (today + timedelta(days=2)).isoformat(),
]

headers = {"x-apisports-key": API_KEY}
all_matches = []

print("Fetching upcoming matches across all tournaments...")

for d in dates:
    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "date": d,
        "timezone": "UTC",
    }
    response = requests.get(url, headers=headers, params=params, timeout=30)

    if response.status_code != 200:
        print(f"HTTP error on {d}: {response.status_code}")
        continue

    data = response.json()
    errors = data.get("errors")
    if errors:
        print(f"API error on {d}: {errors}")
        continue

    matches = data.get("response", [])
    print(f"  {d}: found {len(matches)} matches")
    all_matches.extend(matches)

# Remove duplicates just in case
seen = set()
unique_matches = []
for m in all_matches:
    fid = m["fixture"]["id"]
    if fid not in seen:
        seen.add(fid)
        unique_matches.append(m)

print(f"Total unique matches: {len(unique_matches)}")

# Sort by kick-off time
unique_matches.sort(key=lambda x: x["fixture"]["date"])

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
        h1 {{ margin-top: 0; font-size: 1.6rem; }}
        .meta {{ color: #888; font-size: 0.9rem; margin-bottom: 20px; }}
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
        th {{ background: #2a2a2a; font-weight: 600; color: #ccc; }}
        tr:last-child td {{ border-bottom: none; }}
        .prediction {{ font-weight: 700; color: #ff6b6b; }}
        .empty {{ padding: 40px; text-align: center; color: #888; }}
        .league {{ color: #aaa; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <h1>Upcoming Match Predictions</h1>
    <div class="meta">
        All available tournaments · {dates[0]} → {dates[-1]} · 
        Generated {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
    </div>
"""

if not unique_matches:
    html += '<div class="empty">No upcoming matches found (free plan limitation or no fixtures scheduled).</div>'
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
    for match in unique_matches:
        dt = match["fixture"]["date"].replace("T", " ")[:16]
        league = match["league"]["name"]
        country = match["league"].get("country", "")
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        prediction = random.choice(outcomes)

        league_display = f"{league}" + (f" ({country})" if country else "")

        html += f"""
            <tr>
                <td>{dt}</td>
                <td class="league">{league_display}</td>
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