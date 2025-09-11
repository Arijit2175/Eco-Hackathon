import uvicorn
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from app.models import predict_rainfall_rf, predict_temperature_lstm

app = FastAPI(title="Eco Hackathon Weather API")

class RainfallRequest(BaseModel):
    features: dict  

class TemperatureRequest(BaseModel):
    sequence: list  

@app.get("/")
def root():
    return {"message": "🌍 Eco Hackathon Weather API is running!"}

@app.post("/predict/rainfall_rf")
def predict_rainfall(data: RainfallRequest):
    df = pd.DataFrame([data.features])
    df["temp_humidity_index"] = df["temperature_c"] * df["humidity"] / 100
    pred = predict_rainfall_rf(df)
    return {"predicted_rainfall_mm": float(pred[0])}

@app.post("/predict/temperature_lstm")
def predict_temperature(data: TemperatureRequest):
    pred = predict_temperature_lstm(data.sequence)
    return {"predicted_temperature_c": pred}

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)