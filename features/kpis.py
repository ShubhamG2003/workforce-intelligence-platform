import pandas as pd

def compute_kpis(df: pd.DataFrame) -> dict:
    return {
        "avg_hours": round(df["summaryworkedhours"].mean(), 2),
        "avg_breaks": round(df["numberofbreaks"].mean(), 2),
        "employees": df["employeeid"].nunique(),
        "late_days": (df["latein"] > 0).sum()
    }