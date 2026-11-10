import requests
import random

url = "https://v3.football.api-sports.io/fixtures"
querystring = {"date": "2026-11-11"}
headers = {
    'x-apisports-key': '7a0a9c3f5016f642729e3b5d1a2dae04'
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

print(f"{'Time':<20} | {'Match':<30} | {'Prediction':<10}")
print("-" * 65)

outcomes = ['1', 'X', '2', '1X', '2X']

for match in data.get('response', []):
    home = match['teams']['home']['name'][:14]
    away = match['teams']['away']['name'][:14]
    time = match['fixture']['date'].replace('T', ' ')[:16]
    
    # Simplified prediction logic for demonstration
    prediction = random.choice(outcomes)
    
    print(f"{time:<20} | {home} vs {away:<14} | {prediction:<10}")
