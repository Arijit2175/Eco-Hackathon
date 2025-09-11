import os
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from app.config import MODEL_DIR, PROCESSED_PATH

def load_random_forest():
    return joblib.load(os.path.join(MODEL_DIR, "rainfall_rf.pkl"))

