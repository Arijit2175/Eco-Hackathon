import os
import pandas as pd
from app.data_loader import RAW_PATH, PROCESSED_PATH

def preprocess_data():
    raw_file = os.path.join(RAW_PATH, "climate_data.csv")
    df = pd.read_csv(raw_file)

    if "rain.1h" in df.columns:
        df["rainfall_mm"] = df["rain.1h"].fillna(0)
    elif "rain" in df.columns:
        df["rainfall_mm"] = df["rain"].fillna(0)
    else:
        df["rainfall_mm"] = 0  

    df = df.ffill().bfill()

    df["temp_humidity_index"] = df["temperature_c"] * df["humidity"] / 100

    df = df[["rainfall_mm", "temperature_c", "humidity", "wind_speed", "pressure", "temp_humidity_index"]]

    processed_file = os.path.join(PROCESSED_PATH, "climate_data_processed.csv")
    df.to_csv(processed_file, index=False)

    return df

if __name__ == "__main__":
    df = preprocess_data()
    print("✅ Preprocessing complete. Processed data saved.")
    print(df.head())