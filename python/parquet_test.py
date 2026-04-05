import csv, json, pyarrow as pa, pyarrow.parquet as pq
from pathlib import Path

# Load your clean CSV into a list of dicts first
with open("data/output/users_clean.csv", "r") as f:
    records = list(csv.DictReader(f))

#pa used to create parquet table in memory, handle data schema
# Convert to pyarrow Table
table = pa.Table.from_pylist(records)

#file operations: read, write
# Write Parquet
pq.write_table(table, "data/output/users_clean.parquet")

# Read it back and inspect
t2 = pq.read_table("data/output/users_clean.parquet")
print(t2.schema)      # see inferred column types
print(t2.to_pydict()) # back to Python dict
