import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from app.config import PROCESSED_PATH, MODEL_DIR

def train_lstm(seq_len=5):
    df = pd.read_csv(PROCESSED_PATH)
    features = ["temperature_c", "humidity", "wind_speed", "pressure", "temp_humidity_index"]
    target = "rain"

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(df[features])
    y = df[target].values

    X_seq, y_seq = [], []
    for i in range(len(X_scaled) - seq_len):
        X_seq.append(X_scaled[i:i+seq_len])
        y_seq.append(y[i+seq_len])
    X_seq, y_seq = np.array(X_seq), np.array(y_seq)

    model = Sequential([
        LSTM(64, input_shape=(seq_len, len(features))),
        Dense(1)
    ])
    model.compile(optimizer=Adam(0.001), loss="mse")
    model.fit(X_seq, y_seq, epochs=10, batch_size=16, verbose=1)

    os.makedirs(MODEL_DIR, exist_ok=True)
    model.save(os.path.join(MODEL_DIR, "rainfall_lstm.h5"))

    print("✅ LSTM model trained and saved.")

if __name__ == "__main__":
    train_lstm()