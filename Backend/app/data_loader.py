import os
import requests
import pandas as pd
from datetime import datetime
from app.config import OPENWEATHER_API_KEY

RAW_PATH = os.path.join("data", "raw")
PROCESSED_PATH = os.path.join("data", "processed")

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

def fetch_weather_data(lat: float, lon: float):
    """
    Fetch 5-day forecast data (3-hour steps) + current weather.
    Works with free OpenWeather API.
    """
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    current_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    res = requests.get(forecast_url, params=params)
    res.raise_for_status()
    forecast_json = res.json()

    res_current = requests.get(current_url, params=params)
    res_current.raise_for_status()
    current_json = res_current.json()

    records = []
    for entry in forecast_json.get("list", []):
        date = datetime.fromtimestamp(entry["dt"]).strftime("%Y-%m-%d %H:%M:%S")
        main = entry["main"]
        wind = entry.get("wind", {})
        rain = entry.get("rain", {}).get("3h", 0)

        records.append({
            "date": date,
            "temperature_c": main.get("temp"),
            "humidity": main.get("humidity"),
            "wind_speed": wind.get("speed"),
            "rainfall_mm": rain,
            "pressure": main.get("pressure"),
        })

    df = pd.DataFrame(records)

    raw_file = os.path.join(RAW_PATH, "climate_data.csv")
    df.to_csv(raw_file, index=False)

    return df
