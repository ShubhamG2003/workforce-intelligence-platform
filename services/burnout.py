import pandas as pd

def compute_burnout(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["hour_deviation"] = df["summaryworkedhours"] - 8
    
    df["burnout_score"] = (
        df["summaryworkedhours"] * 4 +
        df["latein"] * 1.5 +
        (30 - df["totalbreaktime"]) * 2
    )

    def category(x):
        if x >= 50:
            return "High"
        elif x >= 35:
            return "Medium"
        return "Low"

    df["burnout_risk"] = df["burnout_score"].apply(category)

    return df
