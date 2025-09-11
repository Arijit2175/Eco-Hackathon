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

