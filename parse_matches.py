import requests

url = "https://v3.football.api-sports.io/fixtures"
querystring = {"date": "2026-11-11"}
headers = {
    'x-apisports-key': '7a0a9c3f5016f642729e3b5d1a2dae04'
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

for match in data.get('response', []):
    home = match['teams']['home']['name']
    away = match['teams']['away']['name']
    time = match['fixture']['date']
    print(f"{time} - {home} vs {away}")

