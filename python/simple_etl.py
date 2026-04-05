from pathlib import Path
import csv

INPUT  = Path("data/raw/users.csv")
# prepare output file
OUTPUT = Path("data/output/users_clean.csv")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

cleaned = []

with open(INPUT, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # 1. skip rows with missing/invalid salary
        try:
            salary = int(row["salary"])
        except (ValueError, TypeError):
            continue                        # drop bad rows

        # 2. cast types
        cleaned.append({
            "id":     int(row["id"]),
            "name":   row["name"].strip(),
            "age":    int(row["age"]),
            "salary": salary
        })

# 3. write output
with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id","name","age","salary"])
    writer.writeheader()
    writer.writerows(cleaned)

print(f"Done. {len(cleaned)} clean rows written to {OUTPUT}")