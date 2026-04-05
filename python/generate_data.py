# generate_data.py — run this first to create sample data
import csv, random, pathlib

pathlib.Path("data/raw").mkdir(parents=True, exist_ok=True)

with open("data/raw/users.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id","name","age","salary"])
    writer.writeheader()
    for i in range(1, 101):
        writer.writerow({
            "id": i,
            "name": random.choice(["Alice","Bob","Charlie","Diana","Eve"]),
            "age": random.randint(20, 60),
            "salary": random.choice([50000, 75000, None, 120000, "N/A"])  # intentional mess
        })