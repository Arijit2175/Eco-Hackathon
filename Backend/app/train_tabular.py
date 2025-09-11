import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from app.config import PROCESSED_PATH, MODEL_DIR

def train_random_forest():
    df = pd.read_csv(PROCESSED_PATH)

    if "temp_humidity_index" not in df.columns:
        df["temp_humidity_index"] = df["temperature_c"] * df["humidity"] / 100

    feature_cols = ["temperature_c", "humidity", "wind_speed", "pressure", "temp_humidity_index"]
    X = df[feature_cols]
    y = df["rainfall_mm"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "rainfall_rf.pkl"))

    print("✅ Random Forest model trained and saved.")

if __name__ == "__main__":
    train_random_forest()
