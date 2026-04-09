import csv


def fetch_all_posts(files) -> list:
    result = []
    # DictReader — row becomes a dict (column name as key)
    with open(f"{files}", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            result.append(row)

    return result

#from pathlib import Path
#data  = Path.cwd().parent / "data" / "users.csv"
#print(fetch_all_posts(data)[1:])