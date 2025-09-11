import os
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from app.config import MODEL_DIR, PROCESSED_PATH

def load_random_forest():
    return joblib.load(os.path.join(MODEL_DIR, "rainfall_rf.pkl"))

def load_lstm():
    return tf.keras.models.load_model(os.path.join(MODEL_DIR, "rainfall_lstm.h5"))

def predict_rainfall_rf(features: pd.DataFrame):
    model = load_random_forest()
    return model.predict(features)

def predict_temperature_lstm(sequence):
    """Predict temperature using trained LSTM model."""
    model_path = os.path.join(MODEL_DIR, "temperature_lstm.h5")
    scaler_path = os.path.join(MODEL_DIR, "temperature_scaler.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError("LSTM model not found, train it first with train_lstm.py")

    model = load_model(model_path)
    scaler = joblib.load(scaler_path)

    seq_scaled = scaler.transform(np.array(sequence).reshape(-1, 1))
    seq_scaled = seq_scaled.reshape(1, len(seq_scaled), 1)

    pred_scaled = model.predict(seq_scaled)
    pred = scaler.inverse_transform(pred_scaled)
    return float(pred[0][0])