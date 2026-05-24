import streamlit as st
import pandas as pd
import plotly.express as px

from data.db import get_engine
from data.queries import ATTENDANCE_QUERY

from features.preprocessing import clean_data, aggregate_daily, add_burnout_score
from features.kpis import compute_kpis
from services.anomaly import detect_anomalies
from services.burnout import compute_burnout

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Workforce AI Dashboard", layout="wide")
st.title("AI Workforce Operations Dashboard")

# ---------------------------
# LOAD DATA
# ---------------------------
engine = get_engine()
df = pd.read_sql(ATTENDANCE_QUERY, engine)

# ---------------------------
# PIPELINE
# ---------------------------
df = clean_data(df)
daily_df = aggregate_daily(df)
daily_df = add_burnout_score(daily_df)

kpis = compute_kpis(daily_df)

daily_df = detect_anomalies(daily_df)
df = compute_burnout(df)

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
shift_options = daily_df["shiftname"].dropna().unique()

selected_shift = st.sidebar.multiselect(
    "Select Shift",
    shift_options,
    default=shift_options
)

daily_df = daily_df[daily_df["shiftname"].isin(selected_shift)]

# ---------------------------
# KPI SECTION
# ---------------------------
st.subheader("Key Workforce Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Work Hours", kpis["avg_hours"])
col2.metric("Avg Breaks", kpis["avg_breaks"])
col3.metric("Late Days", kpis["late_days"])
col4.metric("Employees", kpis["employees"])

# ---------------------------
# VISUALS
# ---------------------------

st.subheader("Work Hours Trend")

trend = daily_df.groupby("date")["summaryworkedhours"].mean().reset_index()

st.plotly_chart(px.line(trend, x="date", y="summaryworkedhours", markers=True))

st.subheader("Shift Distribution")

shift_df = daily_df["shiftname"].value_counts().reset_index()
shift_df.columns = ["Shift", "Count"]

st.plotly_chart(px.bar(shift_df, x="Shift", y="Count"))

st.subheader("Break Distribution")

st.plotly_chart(px.histogram(daily_df, x="totalbreaktime", nbins=25))

st.subheader("Late vs Work Hours")

st.plotly_chart(
    px.scatter(
        daily_df,
        x="latein",
        y="summaryworkedhours",
        color="shiftname",
        hover_data=["employeeid"]
    )
)

st.subheader("Exception Types")

ex_df = daily_df["exceptiontype"].fillna("Normal").value_counts().reset_index()
ex_df.columns = ["exceptiontype", "count"]

st.plotly_chart(px.pie(ex_df, names="exceptiontype", values="count"))

# ---------------------------
# ANOMALY DETECTION
# ---------------------------
st.subheader("AI Anomaly Detection")

anomalies = daily_df[daily_df["anomaly"] == -1]

st.write(f"Detected {len(anomalies)} anomalies")

st.dataframe(anomalies)

# ---------------------------
# BURNOUT
# ---------------------------
burnout_trend = daily_df.groupby("date")["burnout_score"].mean().reset_index()

fig = px.line(
    burnout_trend,
    x="date",
    y="burnout_score",
    markers=True,
    title="Daily Burnout Score Trend"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# RAW
# ---------------------------
st.subheader("Dataset Preview")
st.dataframe(daily_df.head(100))