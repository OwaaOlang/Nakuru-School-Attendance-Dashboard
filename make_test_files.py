import pandas as pd

# Test File 1: Only Form 1A - High attendance
pd.DataFrame([
    ["2026-10-05", "Form 1A", 44, 45],
    ["2026-10-06", "Form 1A", 43, 45],
    ["2026-10-07", "Form 1A", 45, 45],
], columns=["date","class_name","students_present","students_total"]).to_csv("test_teacher_1A.csv", index=False)

# Test File 2: Only Form 4B - Low / Declining
pd.DataFrame([
    ["2026-10-05", "Form 4B", 28, 36],
    ["2026-10-06", "Form 4B", 27, 36],
    ["2026-10-07", "Form 4B", 26, 36],
], columns=["date","class_name","students_present","students_total"]).to_csv("test_teacher_4B.csv", index=False)

print("Created test_teacher_1A.csv and test_teacher_4B.csv")
