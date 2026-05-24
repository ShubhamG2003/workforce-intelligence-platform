import pandas as pd

def time_to_hours(value):
    try:
        if pd.isna(value):
            return 0
        if isinstance(value, str):
            h, m = value.split(":")
            return int(h) + int(m) / 60
        return float(value)
    except:
        return 0