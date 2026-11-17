import pandas as pd
import random
from datetime import date, timedelta

random.seed(42)
classes = {
    "Form 1A": 45,
    "Form 2A": 42,
    "Form 3A": 40,
    "Form 4A": 38,
    "Form 4B": 36,
}
# 8 weeks, Mon-Fri, starting Monday
start = date(2026, 9, 7)
rows = []
for week in range(8):
    for day in range(5):
        d = start + timedelta(days=week*7 + day)
        for cls, total in classes.items():
            # Make Form 4B slowly declining so principal can spot it
            base = 92 if cls != "Form 4B" else 92 - week*2
            rate = max(70, min(98, base + random.randint(-4, 3)))
            present = int(total * rate / 100)
            rows.append([d, cls, present, total])

pd.DataFrame(rows, columns=["date","class_name","students_present","students_total"]).to_csv("attendance.csv", index=False)
print("Done! attendance.csv created with", len(rows), "rows")
