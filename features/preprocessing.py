import pandas as pd
from utils.time_utils import time_to_hours

TIME_COLS = [
    "summaryworkedhours",
    "latein",
    "totalbreaktime",
    "numberofbreaks"
]

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"].dt.weekday < 5]
    df["date"] = df["date"].dt.date

    for col in TIME_COLS:
        if col in df.columns:
            df[col] = df[col].apply(time_to_hours)

    return df


def aggregate_daily(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["employeeid", "date"])
        .agg({
            "summaryworkedhours": "max",
            "latein": "max",
            "numberofbreaks": "max",
            "totalbreaktime": "max",
            "shiftname": "first",
            "exceptiontype": "first"
        })
        .reset_index()
    )

def add_burnout_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["burnout_score"] = (
        df["summaryworkedhours"] * 4 +
        df["latein"] * 1.5 +
        (10 - df["totalbreaktime"]) * 2
    )

    return df