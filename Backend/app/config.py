import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
ONECALL_URL = "https://api.openweathermap.org/data/2.5/onecall"
AIR_POLLUTION_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

if not OPENWEATHER_API_KEY:
    raise ValueError("Missing OpenWeather API key. Set OPENWEATHER_API_KEY env variable.")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_PATH = os.path.join(DATA_DIR, "raw", "climate_data_raw.csv")
PROCESSED_PATH = os.path.join(DATA_DIR, "processed", "climate_data_processed.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
