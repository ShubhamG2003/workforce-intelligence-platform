from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd

FEATURES = ["summaryworkedhours", "latein", "numberofbreaks", "totalbreaktime"]

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    X = df[FEATURES].fillna(0)

    X_scaled = StandardScaler().fit_transform(X)

    model = IsolationForest(contamination=0.08, random_state=42)
    df = df.copy()
    df["anomaly"] = model.fit_predict(X_scaled)

    return df