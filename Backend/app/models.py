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

def predict_rainfall_lstm(sequence: np.ndarray):
    model = load_lstm()
    seq = np.expand_dims(sequence, axis=0)  
    return model.predict(seq).flatten()[0]