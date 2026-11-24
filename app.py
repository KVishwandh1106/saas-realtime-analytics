from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

st.set_page_config(page_title="SaaS Analytics Dashboard", page_icon="📊", layout="wide")
st.title("📊 SaaS Usage Analytics Dashboard")
st.caption("Synthetic demonstration dataset • Batch analytics prototype")

users_path = DATA / "user_events_clean.csv"
clicks_path = DATA / "click_events_clean.csv"
if not users_path.exists() or not clicks_path.exists():
    st.warning("Cleaned data not found. Run `python scripts/etl.py` first.")
    st.stop()

users = pd.read_csv(users_path, parse_dates=["event_timestamp"])
clicks = pd.read_csv(clicks_path, parse_dates=["event_timestamp"])

min_date = users["event_timestamp"].min().date()
max_date = users["event_timestamp"].max().date()
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

plan_options = sorted(users["subscription_plan"].dropna().unique())
selected_plans = st.sidebar.multiselect("Subscription plan", plan_options, default=plan_options)
country_options = sorted(users["country"].dropna().unique())
selected_countries = st.sidebar.multiselect("Country", country_options, default=country_options)

filtered = users[
    users["event_timestamp"].dt.date.between(start_date, end_date)
    & users["subscription_plan"].isin(selected_plans)
    & users["country"].isin(selected_countries)
]
filtered_clicks = clicks[clicks["event_timestamp"].dt.date.between(start_date, end_date)]

total_events = len(filtered)
unique_users = filtered["user_id"].nunique()
total_sessions = filtered["session_id"].nunique()
total_clicks = len(filtered_clicks)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Events", f"{total_events:,}")
c2.metric("Unique users", f"{unique_users:,}")
c3.metric("Sessions", f"{total_sessions:,}")
c4.metric("Clicks", f"{total_clicks:,}")

st.subheader("Events over time")
daily = filtered.assign(event_date=filtered["event_timestamp"].dt.date).groupby("event_date").size().reset_index(name="events")
if not daily.empty:
    st.plotly_chart(px.line(daily, x="event_date", y="events", markers=True, title="Daily events"), use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Event mix")
    event_mix = filtered["event_name"].value_counts().reset_index()
    event_mix.columns = ["event_name", "count"]
    if not event_mix.empty:
        st.plotly_chart(px.bar(event_mix, x="event_name", y="count", title="Events by type"), use_container_width=True)
with right:
    st.subheader("Click activity")
    click_mix = filtered_clicks["button_name"].value_counts().reset_index()
    click_mix.columns = ["button_name", "count"]
    if not click_mix.empty:
        st.plotly_chart(px.bar(click_mix, x="button_name", y="count", title="Clicks by button"), use_container_width=True)

st.subheader("Activity by device")
device_mix = filtered["device_type"].value_counts().reset_index()
device_mix.columns = ["device_type", "count"]
if not device_mix.empty:
    st.plotly_chart(px.pie(device_mix, names="device_type", values="count", title="Events by device"), use_container_width=True)

st.subheader("Activity by subscription plan")
plan_mix = filtered["subscription_plan"].value_counts().reset_index()
plan_mix.columns = ["subscription_plan", "count"]
if not plan_mix.empty:
    st.plotly_chart(px.bar(plan_mix, x="subscription_plan", y="count", title="Events by plan"), use_container_width=True)

st.subheader("Recent user events")
st.dataframe(filtered.sort_values("event_timestamp", ascending=False).head(100), use_container_width=True)

st.info("This dashboard uses synthetic sample records and local batch processing. It is not connected to a live event stream.")
