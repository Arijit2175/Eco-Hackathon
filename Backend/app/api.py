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
    pred = predict_rainfall_rf(df)
    return {"predicted_rainfall_mm": float(pred[0])}

