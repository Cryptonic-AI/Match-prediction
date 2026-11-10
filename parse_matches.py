import requests

url = "https://v3.football.api-sports.io/fixtures"
# Fetching matches for tomorrow
querystring = {"date": "2026-11-12"}
headers = {
    'x-apisports-key': '7a0a9c3f5016f642729e3b5d1a2dae04'
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Match Predictions</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #f4f4f9; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #333; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .prediction { font-weight: bold; color: #2c3e50; }
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

outcomes = ['1', 'X', '2', '1X', '2X']

for match in data.get('response', []):
    time = match['fixture']['date'].replace('T', ' ')[:16]
    league = match['league']['name']
    home = match['teams']['home']['name']
    away = match['teams']['away']['name']
    
    # Simple logic placeholder for prediction
    prediction = "1X" if "FC" in home else "1"
    
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
