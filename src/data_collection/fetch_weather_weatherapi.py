import requests
import json
from datetime import datetime
import os

API_KEY = "6f9ad4092dd94fabbdf194842251806"
CITY = "Budapest"
URL = f"http://api.weatherapi.com/v1/current.json?key=6f9ad4092dd94fabbdf194842251806&q=Budapest&aqi=no"

def fetch_weather():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs("data", exist_ok=True)
        filename = f"data/weatherapi_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Weather data saved to {filename}")
    else:
        print(f"Error: {response.status_code} – {response.text}")

if __name__ == "__main__":
    fetch_weather()
