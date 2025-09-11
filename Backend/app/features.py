import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from app.data_loader import RAW_PATH, PROCESSED_PATH

def preprocess_data():
    file = os.path.join(RAW_PATH, "climate_data.csv")
    df = pd.read_csv(file, parse_dates=["date"])

    df = df.fillna(method="ffill").fillna(method="bfill")

    scaler = StandardScaler()
    df[["rainfall_mm", "temperature_c", "pollution_aqi"]] = scaler.fit_transform(
        df[["rainfall_mm", "temperature_c", "pollution_aqi"]]
    )

    