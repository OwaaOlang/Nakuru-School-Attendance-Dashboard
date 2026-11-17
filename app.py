import streamlit as st
import pandas as pd

st.set_page_config(page_title="Nakuru School Attendance", layout="wide")

st.title("🏫 Nakuru School - Attendance Dashboard")
st.write("For Teachers: Upload your own class CSV and see only YOUR class data. No code needed.")

# --- 1. FILE UPLOADER ---
st.sidebar.header("1. Upload Your Data")
uploaded_file = st.sidebar.file_uploader(
    "Drag your CSV here",
    type=["csv"],
    help="CSV must have columns: date, class_name, students_present, students_total"
)

# Load data: uploaded file if present, else default attendance.csv
@st.cache_data
def load_default():
    df = pd.read_csv("attendance.csv", parse_dates=["date"])
    return df

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, parse_dates=["date"])
        st.success(f"✅ Loaded your file: {uploaded_file.name} ({len(df)} rows)")
    except Exception as e:
        st.error(f"Could not read file: {e}")
        st.stop()
else:
    df = load_default()
    st.info("Showing sample data from attendance.csv. Upload your own CSV in the sidebar to replace it.")

# Validate columns
required = ["date", "class_name", "students_present", "students_total"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Your CSV is missing columns: {missing}. It must have: {required}")
    st.stop()

df["attendance_rate"] = (df["students_present"] / df["students_total"]) * 100

# --- 2. DROPDOWN: FILTER BY CLASS ---
st.sidebar.header("2. Filter by Class")
all_classes = sorted(df["class_name"].unique().tolist())
selected_class = st.sidebar.selectbox(
    "Select Class",
    options=["All Classes"] + all_classes
)

# --- 3. DATE RANGE PICKER ---
st.sidebar.header("3. Filter by Date")
min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handle if user picks only one date
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

# --- APPLY FILTERS ---
filtered = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]

if selected_class != "All Classes":
    filtered = filtered[filtered["class_name"] == selected_class]

if filtered.empty:
    st.warning("No data for this filter. Try a wider date range or another class.")
    st.stop()

# --- TOP 3 METRICS (on filtered view) ---
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
st.subheader(f"Attendance by Class - Showing: {selected_class} | {start_date} to {end_date}")
st.dataframe(by_class.reset_index()[["class_name", "present", "total", "rate"]].rename(
    columns={"class_name": "Class", "present": "Students Present", "total": "Students Total", "rate": "Rate (%)"}
))
st.bar_chart(by_class["rate"])

# --- LINE CHART: ONE LINE PER CLASS ---
st.subheader("Attendance Rate Over Time (One Line Per Class)")
daily = filtered.groupby(["date", "class_name"])["attendance_rate"].mean().reset_index()
pivot = daily.pivot(index="date", columns="class_name", values="attendance_rate")
st.line_chart(pivot)

# --- 4. DOWNLOAD BUTTON FOR FILTERED VIEW ---
st.subheader("Download Filtered View")
csv_data = filtered[["date", "class_name", "students_present", "students_total", "attendance_rate"]].to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered CSV",
    data=csv_data,
    file_name=f"filtered_attendance_{selected_class}_{start_date}_to_{end_date}.csv",
    mime="text/csv"
)

with st.expander("See Filtered Raw Data"):
    st.dataframe(filtered)