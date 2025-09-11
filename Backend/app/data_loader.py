import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

RAW_PATH = os.path.join("data", "raw")
PROCESSED_PATH = os.path.join("data", "processed")

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

def generate_synthetic_climate_data(days: int = 365):
    """
    Generate synthetic climate data:
    - rainfall (mm)
    - temperature (°C)
    - pollution (AQI)
    - flood_risk (0/1)
    """
    start_date = datetime.today() - timedelta(days=days)
    dates = [start_date + timedelta(days=i) for i in range(days)]

    rainfall = np.random.gamma(2, 5, days)  
    temperature = np.random.normal(30, 5, days)  
    pollution = np.random.normal(100, 30, days)

    flood_risk = ((rainfall > 15) & (pollution > 120)).astype(int)

    df = pd.DataFrame({
        "date": dates,
        "rainfall_mm": rainfall,
        "temperature_c": temperature,
        "pollution_aqi": pollution,
        "flood_risk": flood_risk
    })

    raw_file = os.path.join(RAW_PATH, "climate_data.csv")
    df.to_csv(raw_file, index=False)

    return df

def load_data(processed: bool = False):
    """
    Load data from raw or processed folder.
    """
    path = PROCESSED_PATH if processed else RAW_PATH
    file = os.path.join(path, "climate_data.csv")

    if not os.path.exists(file):
        raise FileNotFoundError("Dataset not found. Run generate_synthetic_climate_data() first.")

    return pd.read_csv(file, parse_dates=["date"])