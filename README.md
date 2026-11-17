# Nakuru School Attendance Dashboard

A Streamlit web app for a school principal in Nakuru to monitor student attendance without opening Excel.

## What it shows
- Overall attendance rate
- Best-attending class and worst-attending class
- Attendance by class (table + bar chart)
- Line chart of attendance rate over selected date range, one line per class

## How to run
```bash
pip install -r requirements.txt
streamlit run app.py

## Part B - Teacher Upload & Filters (Today's Exercise)

- **File Uploader:** A teacher can drag their own CSV in the sidebar. Dashboard updates immediately without touching code. If no file is uploaded, it shows the sample `attendance.csv`.
- **Class Dropdown:** Filter by class name. A teacher sees only their own class.
- **Date Range Picker:** Filter by start and end date.
- **Download Button:** Downloads ONLY the filtered view as CSV.

CSV format: `date, class_name, students_present, students_total`

Tested with two different uploaded files: `test_teacher_1A.csv` (high attendance) and `test_teacher_4B.csv` (low/declining).

## Pricing - What I Would Charge a School

**I would charge PER SCHOOL, not per teacher.**

Reason: A school has 1 principal + many teachers sharing the same dashboard. Charging per teacher punishes the school for adding teachers and makes teachers afraid to use it. Per-school pricing is simple, predictable, and encourages all teachers to upload.

**My price for a school in Nakuru:**
- **Build + Deploy (one-time): KES 45,000** (approx. UGX 1,250,000) — Includes setup, custom school name/logo, training for 1 principal + 5 teachers, and sample data.
- **Monthly Maintenance: KES 3,000 / month** (approx. UGX 85,000) — Hosting on Streamlit Cloud, bug fixes, small changes, WhatsApp support.
- **Yearly Option: KES 30,000 / year** if paid upfront (2 months free).

If a school wants extra features like SMS alerts to parents or login per teacher, that is charged separately as an add-on.
