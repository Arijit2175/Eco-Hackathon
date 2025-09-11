import uvicorn
import pandas as pd
from fastapi import FastAPI, Body
from pydantic import BaseModel
from app.models import predict_rainfall_rf, predict_temperature_lstm

app = FastAPI(title="Eco Hackathon Weather API")

class WeatherRequest(BaseModel):
    features: dict          
    sequence: list          

@app.get("/")
def root():
    return {"message": "🌍 Eco Hackathon Weather API is running!"}

@app.post("/predict")
def predict_weather(data: WeatherRequest):
    df = pd.DataFrame([data.features])
    df["temp_humidity_index"] = df["temperature_c"] * df["humidity"] / 100
    rainfall_pred = predict_rainfall_rf(df)

    temp_pred = predict_temperature_lstm(data.sequence)

    return {
        "predicted_rainfall_mm": float(rainfall_pred[0]),
        "predicted_temperature_c": temp_pred
    }

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
