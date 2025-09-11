import os

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
ONECALL_URL = "https://api.openweathermap.org/data/2.5/onecall"
AIR_POLLUTION_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

if not OPENWEATHER_API_KEY:
    raise ValueError("Missing OpenWeather API key. Set OPENWEATHER_API_KEY env variable.")
