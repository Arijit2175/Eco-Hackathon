import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from app.config import OPENWEATHER_API_KEY

RAW_PATH = os.path.join("data", "raw")
PROCESSED_PATH = os.path.join("data", "processed")

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

def fetch_weather_data(lat: float, lon: float, city: str):
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    current_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": "metric"}

    res_current = requests.get(current_url, params=params)
    res_current.raise_for_status()
    current_json = res_current.json()

    res_forecast = requests.get(forecast_url, params=params)
    res_forecast.raise_for_status()
    forecast_json = res_forecast.json()

    records = []

    main = current_json["main"]
    wind = current_json.get("wind", {})
    rain = current_json.get("rain", {}).get("1h", 0)
    records.append({
        "city": city,
        "date": datetime.utcfromtimestamp(current_json["dt"]).strftime("%Y-%m-%d %H:%M:%S"),
        "temperature_c": main.get("temp"),
        "humidity": main.get("humidity"),
        "wind_speed": wind.get("speed"),
        "pressure": main.get("pressure"),
        "rainfall_mm": rain,
    })

    for entry in forecast_json.get("list", []):
        main = entry["main"]
        wind = entry.get("wind", {})
        rain = entry.get("rain", {}).get("3h", 0)
        records.append({
            "city": city,
            "date": datetime.utcfromtimestamp(entry["dt"]).strftime("%Y-%m-%d %H:%M:%S"),
            "temperature_c": main.get("temp"),
            "humidity": main.get("humidity"),
            "wind_speed": wind.get("speed"),
            "pressure": main.get("pressure"),
            "rainfall_mm": rain,
        })

    return pd.DataFrame(records)

def fetch_multiple_cities():
    """Ask user for city inputs and fetch data for each."""
    cities = {}
    while True:
        city = input("Enter city name (or press Enter to stop): ").strip()
        if not city:
            break
        try:
            geo_url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {"q": city, "limit": 1, "appid": OPENWEATHER_API_KEY}
            res = requests.get(geo_url, params=params)
            res.raise_for_status()
            geo = res.json()
            if not geo:
                print(f"⚠️ Could not find coordinates for {city}, skipping.")
                continue
            lat, lon = geo[0]["lat"], geo[0]["lon"]
            cities[city] = (lat, lon)
        except Exception as e:
            print(f"❌ Error with {city}: {e}")

    if not cities:
        print("⚠️ No valid cities provided.")
        return

    all_dfs = []
    for city, (lat, lon) in cities.items():
        print(f"🌍 Fetching data for {city}...")
        df_city = fetch_weather_data(lat, lon, city)
        all_dfs.append(df_city)

    df_all = pd.concat(all_dfs, ignore_index=True)

    raw_file = os.path.join(RAW_PATH, "climate_data.csv")
    df_all.to_csv(raw_file, index=False)
    print(f"✅ Saved {len(df_all)} rows from {len(cities)} cities to {raw_file}")

    return df_all


if __name__ == "__main__":
    fetch_multiple_cities()
