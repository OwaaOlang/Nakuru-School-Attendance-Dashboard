import streamlit as st
import pandas as pd

st.set_page_config(page_title="Nakuru School Attendance", layout="wide")

st.title("🏫 Nakuru School - Attendance Dashboard")
st.write("For the Principal: See overall attendance, by class, and last 30 days trend without opening Excel.")

# Load CSV
@st.cache_data
def load_data():
    df = pd.read_csv("attendance.csv", parse_dates=["date"])
    df["attendance_rate"] = (df["students_present"] / df["students_total"]) * 100
    return df

df = load_data()

# Sidebar - Date Range Slider
st.sidebar.header("Filter")
min_date = df["date"].min().date()
max_date = df["date"].max().date()

start_date, end_date = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filter data
filtered = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]

# --- TOP 3 METRICS ---
overall_rate = (filtered["students_present"].sum() / filtered["students_total"].sum()) * 100

by_class = filtered.groupby("class_name").agg(
    present=("students_present", "sum"),
    total=("students_total", "sum")
)
by_class["rate"] = (by_class["present"] / by_class["total"]) * 100
by_class = by_class.sort_values("rate", ascending=False)

best_class = by_class.index[0]
best_rate = by_class.iloc[0]["rate"]
worst_class = by_class.index[-1]
worst_rate = by_class.iloc[-1]["rate"]

col1, col2, col3 = st.columns(3)
col1.metric("Overall Attendance Rate", f"{overall_rate:.1f}%")
col2.metric("Best-Attending Class", f"{best_class}", f"{best_rate:.1f}%")
col3.metric("Worst-Attending Class", f"{worst_class}", f"{worst_rate:.1f}%")

# --- ATTENDANCE BY CLASS ---
st.subheader("Attendance by Class")
st.dataframe(by_class.reset_index()[["class_name", "present", "total", "rate"]].rename(
    columns={"class_name": "Class", "present": "Students Present", "total": "Students Total", "rate": "Rate (%)"}
))
st.bar_chart(by_class["rate"])

# --- LINE CHART: ONE LINE PER CLASS ---
st.subheader("Attendance Rate Over Time (One Line Per Class)")

# Daily rate per class
daily = filtered.groupby(["date", "class_name"])["attendance_rate"].mean().reset_index()
pivot = daily.pivot(index="date", columns="class_name", values="attendance_rate")

st.line_chart(pivot)

# Show if a class is declining
st.info("Tip for Principal: If a line keeps going down, that class is declining — check it early.")

# --- RAW DATA ---
with st.expander("See Raw Data"):
    st.dataframe(filtered)