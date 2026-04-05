import csv, json
from pathlib import Path

with open("data/employees.csv", "r", encoding="utf-8") as f:
    records = list(csv.DictReader(f))

# Cast numeric fields (DictReader returns everything as string)
for r in records:
    r["employee_id"]    = int(r["employee_id"])
    r["salary"]         = int(r["salary"])
    r["age"]            = int(r["age"])
    r["performance_score"]= float(r["performance_score"])
    r["is_active"]      = bool(r["is_active"])


with open("data/output/employees.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)

print(f"Exported {len(records)} records to JSON")