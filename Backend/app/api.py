import os
import pandas as pd
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, conlist
from app.models import predict_rainfall_rf, predict_temperature_lstm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("eco_hackathon_api")

app = FastAPI(title="🌍 Eco Hackathon Weather API")

class RainfallFeatures(BaseModel):
    temperature_c: float = Field(..., example=31.2)
    humidity: float = Field(..., example=55)
    wind_speed: float = Field(..., example=5.3)
    pressure: float = Field(..., example=1012)

class WeatherRequest(BaseModel):
    rainfall_features: RainfallFeatures
    temperature_sequence: conlist(float, min_length=1)  

@app.get("/")
def root():
    return {"message": "🌍 Eco Hackathon Weather API is running!"}

@app.post("/predict")
def predict_weather(data: WeatherRequest):
    try:
        df = pd.DataFrame([data.rainfall_features.dict()])
        df["temp_humidity_index"] = df["temperature_c"] * df["humidity"] / 100
        rainfall_pred = predict_rainfall_rf(df)

        temperature_pred = predict_temperature_lstm(data.temperature_sequence)

        response = {
            "predicted_rainfall_mm": float(rainfall_pred[0]),
            "predicted_temperature_c": temperature_pred
        }

        logger.info(f"Prediction successful: {response}")
        return response

    except KeyError as e:
        logger.error(f"Missing feature: {e}")
        raise HTTPException(status_code=400, detail=f"Missing feature: {e}")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
