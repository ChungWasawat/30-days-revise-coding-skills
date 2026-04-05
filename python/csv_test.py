import csv

# python read files starting from current dir where python file is executed
file_path = "data/"

def basic_read():
    # Basic read
    with open(f"{file_path}employees.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:          # row is a plain list
            print(row)

def dict_read():
    # DictReader — row becomes a dict (column name as key)
    with open(f"{file_path}employees.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row["name"], row["hire_date"])   # access by column name

def basic_write():
    # Basic write
    # w -replace existing with new one
    with open(f"{file_path}raw/users.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "age"])     # header
        writer.writerow(["Alice", 30])

def dict_write():
    # DictWriter — write from dicts
    with open(f"{file_path}raw/users.csv", "a", newline="", encoding="utf-8") as f:
        fieldnames = ["id","name", "age", "salary"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        #writer.writeheader() # no need for append
        writer.writerow({"id":101,"name": "Eddy", "age": 50, "salary": 15000})

#basic_read()
#dict_read()
#basic_write()
dict_write()
