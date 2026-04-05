from pathlib import Path

print("parent", Path(__file__).parent)
print("resolve parent", Path(__file__).resolve().parent)

# Building paths
p = Path("data") / "employees.csv"   # joins safely on any OS -join path with string

# Checking existence
print('exist? ',p.exists())
print('file? ',p.is_file())
print('dir? ',p.is_dir())

# Creating directories
Path("data/output").mkdir(parents=True, exist_ok=True)

print("----- name | suffix | stem | parent -----")
# Listing files
for f in Path("data").glob("*.csv"):    # all CSVs in folder
    print("glob ", f.name, f.suffix, f.stem, f.parent)

print("----- name | suffix | stem | parent -----")
for f in Path("data").rglob("*.csv"):    # all CSVs in folder
    print("rglob ", f.name, f.suffix, f.stem, f.parent)

# Reading & writing text
t = Path("data/output") / "test.txt"
t.write_text("hello, hi", encoding="utf-8")
print(t.read_text(encoding="utf-8"))


# File metadata
print(t.stat().st_size )                        # file size in bytes