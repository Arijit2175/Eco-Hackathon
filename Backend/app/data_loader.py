import os
import requests
import pandas as pd
from datetime import datetime
from app.config import OPENWEATHER_API_KEY, ONECALL_URL, AIR_POLLUTION_URL

RAW_PATH = os.path.join("data", "raw")
os.makedirs(RAW_PATH, exist_ok=True)

def fetch_weather_data(lat: float, lon: float, days: int = 7):
    """
    Fetch weather + pollution data for given coordinates.
    Uses OpenWeather OneCall + Air Pollution API.
    """

    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,alerts",
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    res = requests.get(ONECALL_URL, params=params)
    weather_json = res.json()

    records = []
    for day in weather_json.get("daily", []):
        date = datetime.fromtimestamp(day["dt"]).strftime("%Y-%m-%d")
        temp = day["temp"]["day"]
        humidity = day["humidity"]
        wind = day["wind_speed"]
        rainfall = day.get("rain", 0) 
        pressure = day["pressure"]

        records.append({
            "date": date,
            "temperature_c": temp,
            "humidity": humidity,
            "wind_speed": wind,
            "rainfall_mm": rainfall,
            "pressure": pressure,
        })

    params_pollution = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
    }
    res_poll = requests.get(AIR_POLLUTION_URL, params=params_pollution)
    pollution_json = res_poll.json()
    aqi = pollution_json["list"][0]["main"]["aqi"] if "list" in pollution_json else None

    for rec in records:
        rec["pollution_aqi"] = aqi

    df = pd.DataFrame(records)

    file = os.path.join(RAW_PATH, "climate_data.csv")
    df.to_csv(file, index=False)

    return df
