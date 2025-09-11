import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from app.data_loader import RAW_PATH, PROCESSED_PATH

def preprocess_data():
    file = os.path.join(RAW_PATH, "climate_data.csv")
    df = pd.read_csv(file, parse_dates=["date"])

    