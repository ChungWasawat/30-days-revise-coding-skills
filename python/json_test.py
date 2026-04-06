import json
from pathlib import Path

# Parse JSON string → Python dict
data = json.loads('{"name": "Alice", "age": 30}')
print("infile data: ",data)

# dump -> file(None), dumps -> string
# Python dict → JSON string
json_str = json.dumps(data, indent=2)
print("dict to json: ", json_str)

# Read JSON file → Python dict
with open("data/raw/example.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print("example\n ",data)                    # return list of dict like in the file

# Write Python dict → JSON file
with open("data/output/op.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=5, ensure_ascii=False)   # ensure_ascii=False for Thai text

# Handling nested structures
records = data["items"]                         # list of dicts
for record in records:
    print(record.get("product_id", "N/A"))      # .get() avoids KeyError on missing keys

# Common real-world issue — non-serializable types
from datetime import datetime
try:
    json.dumps({"ts": datetime.now()})          # ❌ TypeError
except TypeError:
    print("json doesn't accept datetime type")

config_file = Path("data/output/op.json")
with config_file.open("w", encoding="utf-8") as f:
    json.dump({"ts": str(datetime.now())}, f, indent=4)
