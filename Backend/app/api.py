import uvicorn
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from app.models import predict_rainfall_rf, predict_temperature_lstm

