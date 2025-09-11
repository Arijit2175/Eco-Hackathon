import uvicorn
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, conlist
from app.models import predict_rainfall_rf, predict_temperature_lstm

app = FastAPI(title="🌍 Eco Hackathon Weather API")

class WeatherRequest(BaseModel):
    features: dict              
    temperature_sequence: conlist(float, min_length=1)  

@app.get("/")
def root():
    return {"message": "Eco Hackathon Weather API is running!"}

@app.post("/predict")
def predict_weather(data: WeatherRequest):
    features = data.features.copy()
    features["pressure"] = features.pop("pressure_hpa", None)
    features["wind_speed"] = features.pop("wind_speed_kph", None)
    df = pd.DataFrame([features])
    df["temp_humidity_index"] = df["temperature_c"] * df["humidity"] / 100
    
    rainfall_pred = predict_rainfall_rf(df)[0]        
    temperature_pred = predict_temperature_lstm(data.temperature_sequence)  

    flood_risk = "Low"
    if rainfall_pred > 100:
        flood_risk = "High"
    elif rainfall_pred > 50:
        flood_risk = "Moderate"

    heatwave_risk = "Low"
    if temperature_pred > 40:
        heatwave_risk = "High"
    elif temperature_pred > 35:
        heatwave_risk = "Moderate"

    drought_risk = "Low"
    if rainfall_pred < 10:
        drought_risk = "High"
    elif rainfall_pred < 25:
        drought_risk = "Moderate"

    return {
        "predicted_rainfall_mm": float(rainfall_pred),
        "predicted_temperature_c": float(temperature_pred),
        "flood_risk": flood_risk,
        "heatwave_risk": heatwave_risk,
        "drought_risk": drought_risk
    }

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
