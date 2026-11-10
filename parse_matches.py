import requests
import random

url = "https://v3.football.api-sports.io/fixtures"
querystring = {"date": "2026-11-12"}
headers = {
    'x-apisports-key': '7aba9c3f5016f642729e6bf7f22a6d04'
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

outcomes = ['1', 'X', '2', '1X', '2X']

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Match Predictions</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #141414; color: #fff; }
        table { width: 100%; border-collapse: collapse; background: white; color: #333; }
        th, td { padding: 12px; border: 1px solid #ccc; text-align: left; }
        th { background-color: #333; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .prediction { font-weight: bold; color: #d63031; }
    </style>
</head>
<body>
    <h2>Tomorrow's Match Predictions</h2>
    <table>
        <tr>
            <th>Time</th>
            <th>Tournament</th>
            <th>Match</th>
            <th>Prediction</th>
        </tr>
"""

for match in data.get('response', []):
    time = match['fixture']['date'].replace('T', ' ')[:16]
    league = match['league']['name']
    home = match['teams']['home']['name']
    away = match['teams']['away']['name']
    prediction = random.choice(outcomes)

    html_content += f"""
        <tr>
            <td>{time}</td>
            <td>{league}</td>
            <td>{home} vs {away}</td>
            <td class="prediction">{prediction}</td>
        </tr>
    """

html_content += """
    </table>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)

print("Webpage updated successfully.")
