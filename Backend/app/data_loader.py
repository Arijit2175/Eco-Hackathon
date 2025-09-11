import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

RAW_PATH = os.path.join("data", "raw")
PROCESSED_PATH = os.path.join("data", "processed")

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

