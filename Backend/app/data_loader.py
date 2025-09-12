import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from app.config import OPENWEATHER_API_KEY

RAW_PATH = os.path.join("data", "raw")
PROCESSED_PATH = os.path.join("data", "processed")

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

def fetch_weather_data(lat: float, lon: float, city: str = None):
    """Fetch last 5 days of hourly weather data for a single city."""
    base_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
    all_records = []

    for days_back in range(1, 6):
        dt = int((datetime.utcnow() - timedelta(days=days_back)).timestamp())
        params = {
            "lat": lat,
            "lon": lon,
            "dt": dt,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }

        res = requests.get(base_url, params=params)
        res.raise_for_status()
        data = res.json()

        for hour in data.get("hourly", []):
            date = datetime.fromtimestamp(hour["dt"]).strftime("%Y-%m-%d %H:%M:%S")
            temp = hour.get("temp")
            humidity = hour.get("humidity")
            pressure = hour.get("pressure")
            wind_speed = hour.get("wind_speed")
            rain = hour.get("rain", {}).get("1h", 0)

            all_records.append({
                "city": city if city else f"{lat},{lon}",
                "date": date,
                "temperature_c": temp,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "rainfall_mm": rain,
                "pressure": pressure,
            })

    return pd.DataFrame(all_records)


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
