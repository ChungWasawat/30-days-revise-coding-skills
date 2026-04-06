import os
from pathlib import Path

# --- Paths ---
print("current working dir: ", os.getcwd())     # current working directory
print("joined path: ", os.path.join("data", "raw", "users.csv"))    # safe path joining (like pathlib /)
print("file exist?: ",os.path.exists("data/raw/file.csv"))          # check existence
print("file?: ", os.path.isfile("file.csv"))                  
print("dir?: ", os.path.isdir("data/"))
print("basename: ", os.path.basename("/data/raw/users.csv") )       # → "users.csv"
print("dirname: ", os.path.dirname("/data/raw/users.csv"))          # → "/data/raw"
print("split name: ", os.path.splitext("file.csv") )                  # → ("file", ".csv")
print("absolute path: ", os.path.abspath("data/output"))            # → full absolute path

# --- Directories ---
try: 
    print("completed: ",os.mkdir("data/output"))                    # create one dir (fails if exists)
except FileExistsError: 
    print("fail to create dir")
print("create nested dir: ", os.makedirs("data/output/clean", exist_ok=True))   # create nested dirs safely
print("list dir: ", os.listdir("data/")  )                          # list everything in folder
# test file
Path('data/output/file.txt').touch()
print("renamed: ", os.rename("data/output/file.txt", "data/output/test2.txt") ) # rename/move a file
print("removed complete", os.remove("data/output/test2.txt"))       # delete a file

# --- Walking directories (very useful in DE) ---
for dirpath, dirnames, filenames in os.walk("data/"):
    for fname in filenames:
        if fname.endswith(".csv"):
            full_path = os.path.join(dirpath, fname)
            size = os.stat(full_path).st_size
            print(f"{full_path} — {size} bytes")

# --- Environment variables (critical in DE / Docker) ---
os.environ["MY_VAR"] = "hello"                  # set
os.getenv("DB_PASSWORD", default="xdd1234")     # same as .get()

# situation for environment
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
print(f"Would connect to: {DB_HOST}:{DB_PORT}")
