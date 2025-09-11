import os
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from app.config import MODEL_DIR

rainfall_rf_model = joblib.load(os.path.join(MODEL_DIR, "rainfall_rf.pkl"))

def load_random_forest():
    return joblib.load(os.path.join(MODEL_DIR, "rainfall_rf.pkl"))


def load_lstm():
    return tf.keras.models.load_model(
        os.path.join(MODEL_DIR, "rainfall_lstm.h5"),
        compile=False  
    )

def predict_rainfall_rf(features: pd.DataFrame):
      """
    Predict rainfall using the preloaded Random Forest model.
    Features must match the order the model was trained on.
    """
      features = features[rainfall_rf_model.feature_names_in_]
      return rainfall_rf_model.predict(features)

def predict_temperature_lstm(sequence):
    """Predict temperature using trained LSTM model."""
    model_path = os.path.join(MODEL_DIR, "temperature_lstm.h5")
    scaler_path = os.path.join(MODEL_DIR, "temperature_scaler.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError("LSTM model not found, train it first with train_lstm.py")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError("Scaler not found, make sure training saved it.")

    model = load_model(model_path, compile=False)
    scaler = joblib.load(scaler_path)

    seq_scaled = scaler.transform(np.array(sequence).reshape(-1, 1))
    seq_scaled = seq_scaled.reshape(1, len(seq_scaled), 1)

    pred_scaled = model.predict(seq_scaled)
    pred = scaler.inverse_transform(pred_scaled)

    return float(pred[0][0])