import pandas as pd
from pathlib import Path

# Loading
df = pd.read_csv("data/raw/users.csv")
df_json = pd.read_json("data/raw/posts_20260406_220749.json")
df_parquet = pd.read_parquet("data/output/users_clean.parquet")  # from Day 1 bonus

df_emp = pd.read_csv("data/employees.csv")

# First inspection — always run these first
def basic_inspection(df):
    print("shape: ", df.shape  )                                        # (rows, columns)
    print("type: ", df.dtypes   )                                       # column types — spot problems here
    print("head:\n ", df.head(3) )                                      # first 3 rows
    print("tail:\n ", df.tail(4) )                                      # last 4 rows
    print("info: ", df.info()   )                                       # dtypes + non-null counts together
    print("describe: ", df.describe()  )                                # stats for numeric columns
    print("isnull to find missing values: ", df.isnull().sum())         # count missing values per column
    print("count duplicates: ", df.duplicated().sum() )                 # count duplicate rows
    print("column name to list: ", df.columns.tolist())                 # list all column names
    print("count frequency of values: ", df["salary"].value_counts())   # frequency of each value — spot garbage values


def cleaning(df):
    # Casting types
    df["age"]    = df["age"].astype(int)
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")  # bad values → NaN
    #df["date"]   = pd.to_datetime(df["date"], format="%Y-%m-%d")

    # Handling nulls
    #df.dropna(subset=["salary"])            # drop rows where salary is null
    #df["salary"].fillna(0)                  # fill nulls with 0
    df["salary"] = round(df["salary"].fillna(df["salary"].mean()), 2) # fill with mean

    # String cleaning
    df["name"] = df["name"].str.strip()     # remove whitespace
    df["name"] = df["name"].str.lower()     # normalize case
    df["name"] = df["name"].str.replace("  ", " ")  # fix double spaces

    # Dropping duplicates
    df = df.drop_duplicates()               # all columns
    df = df.drop_duplicates(subset=["id"])  # by specific column

    # Renaming columns
    df = df.rename(columns={"id": "emp_id", "name": "emp_name"})

    # add new columns
    print("before ", df.shape)
    df["unnecessary_col"] = df['age'] +9999
    df["another_col"] = 0
    print("added columns ",df.shape)

    # Dropping columns
    df = df.drop(columns=["unnecessary_col", "another_col"])

    # Filtering rows
    print("age >50\n",df[df["age"] > 50])                       # keep rows where age > 18
    print(df[df["salary"].notna()].count()  )                   # keep non-null salaries
    print("before filter out: ", df.shape)
    df = df[~df["emp_name"].str.contains("test", case=False)]   # remove test records
    print("after filter out: ", df.shape)
    return df


def aggregation(df):
    # Basic groupby
    print("salary mean by department: ", df.groupby("department")["salary"].mean())             # avg salary per dept
    print("salary sum by department", df.groupby("department")["salary"].sum())                 # total salary per dept
    print("employee count by department", df.groupby("department")["employee_id"].count())      # headcount per dept

    # Multiple aggregations at once — most useful pattern
    summary = df.groupby("department").agg(
        headcount  = ("employee_id", "count"),
        avg_salary = ("salary", "mean"),
        max_salary = ("salary", "max"),
        min_age    = ("age",    "min")
    ).reset_index()                                  # turn index back into column
    print("multiple aggregation\n", summary)

    # Groupby multiple columns ~pivot table
    print("group by multiple columns\n", df.groupby(["department", "city"])["salary"].mean().reset_index(name="average_salary"))

    # Filter groups — only keep departments with more than 5 people
    print("windows filter with lambda\n",df.groupby("department").filter(lambda g: len(g) > 10))

    # Apply custom function to each group
    def salary_range(g):
        return g["salary"].max() - g["salary"].min()

    print("replicate having with function\n",df.groupby("department").apply(salary_range))

def merge_join():
    # Setup — two DataFrames to join
    employees = pd.DataFrame({
        "id":         [1, 2, 3, 4],
        "name":       ["Alice", "Bob", "Charlie", "Diana"],
        "dept_id":    [10, 20, 10, 30]
    })

    departments = pd.DataFrame({
        "dept_id":          [10, 20, 40],
        "dept_name":        ["Engineering", "Marketing", "HR"],
        "department_id":    [10, 20, 40]
    })

    df1 = pd.DataFrame({
        "company_id": [1, 2, 3, 4, 1, 3, 1],
        "year":       [2023, 2023, 2023, 2023, 2024, 2024, 2025],
        "name":    ["xdd", "xpp", "xtd", "xgg", "xdd", "xtd", "xdd"], 
        "oil_import": [5000, 2000, 15000, 300, 7000, 8000, 6000]
    })

    df2 = pd.DataFrame({
        "company_id": [1, 2, 3, 4, 1, 2, 3, 4],
        "year":       [2023, 2023, 2023, 2023, 2024, 2024, 2024, 2024],
        "name":       ["xdd", "xpp", "xtd", "xgg", "xdd", "xpp", "xtd", "xgg"],
        "earnings":    [5000000, 600000, 10000000, 50000, 3000000, 50000000, 60000000, 8000000]
    })

    df_jan = pd.DataFrame({
        "province": ["Bangkok", "Nonthaburi", "Samut Prakan"],
        "month-year": ["jan-2026", "jan-2026", "jan-2026"],
        "total_users": [100000, 50000, 60000]
    })

    df_feb = pd.DataFrame({
        "province": ["Bangkok", "Nonthaburi", "Samut Prakan"],
        "month-year": ["feb-2026", "feb-2026", "feb-2026"],
        "total_users": [105000, 52000, 59000]
    })

    df_mar = pd.DataFrame({
        "province": ["Bangkok", "Nonthaburi", "Samut Prakan"],
        "month-year": ["mar-2026", "mar-2026", "mar-2026"],
        "total_users": [120000, 90000, 65000]
    })

    # Inner join — only matching rows (default)
    print("inner join\n", pd.merge(employees, departments, on="dept_id", how="inner"))
    # → Alice, Bob, Charlie (Diana's dept 30 has no match)

    # Left join — all employees, null if no dept match
    print("left join\n", pd.merge(employees, departments, on="dept_id", how="left"))
    # → all 4 employees, Diana gets NaN for dept_name

    # Right join — all departments, null if no employee match
    print("right join\n", pd.merge(employees, departments, on="dept_id", how="right"))
    # → Engineering, Marketing, HR — HR has no employees

    # Different column names on each side
    print("left join different names\n", pd.merge(employees, departments,
            left_on="dept_id", right_on="department_id", how="left"))

    # Merging on multiple keys
    print("inner join with multiple columns\n", pd.merge(df1, df2, on=["company_id", "year"], how="inner"))

    # Concat — stack DataFrames vertically (same columns)
    print("concat vertically\n", pd.concat([df_jan, df_feb, df_mar], ignore_index=True))    
    print("concat horizontally\n", pd.concat([df_jan, df_feb, df_mar], ignore_index=True, axis=1))  

def window_function(df):
    # rank within group — e.g. salary rank within each department
    df_dept = df.sort_values(["department", "salary"], ascending=[True, False])
    df_dept["row_number"] = df_dept.groupby("department").cumcount() + 1
    df_dept["dense_rank"] = df_dept.groupby("department")["salary"].rank(
        method="dense", ascending=False
    )
    df_dept["rank"] = df_dept.groupby("department")["salary"].rank(method="min", ascending=False)
    print(df_dept[['employee_id', 'department', 'salary', 'hire_date', 'age','row_number', 'rank', 'dense_rank']])

    # running total within group
    df_dept2 =df.sort_values(["department", "salary"], ascending=[True, True])
    df_dept2["running_salary"] = df_dept2.groupby("department")["salary"].cumsum()
    
    # lag — previous row's value (compare to prior period)
    df_dept2["prev_salary"] = df_dept2.groupby("department")["salary"].shift(1)
    
    # lead — next row's value
    df_dept2["next_salary"] = df_dept2.groupby("department")["salary"].shift(-1)
    
    # difference from previous row
    df_dept2["salary_change"] = df_dept2["salary"] - df_dept2["prev_salary"]
    print(df_dept2[['employee_id', 'name', 'department', 'salary', 'running_salary', 'prev_salary', 'next_salary', 'salary_change']])

    # rolling average — 3-month moving average per employee
    # min_periods > fill average value for the first two row with itself
    df_dept3 =df.sort_values(["department", "salary"], ascending=[True, True])

    df_dept3["salary_3m_avg"] = (
        df_dept3.groupby("department")["salary"]
        .transform(lambda x: x.rolling(3, min_periods=1).mean())
    )

    # percent of group total
    df_dept3["pct_of_dept"] = (
        df_dept3["salary"] / df_dept3.groupby("department")["salary"].transform("sum") * 100
    )

    df_dept3["total_pct_of_dept"] = df_dept3.groupby("department")["pct_of_dept"].cumsum()
    print(df_dept3[['employee_id', 'name', 'department', 'salary','salary_3m_avg','pct_of_dept', 'total_pct_of_dept']])
    


def create_file(df):
    # CSV
    df.to_csv("data/output/clean/transformed.csv", index=False)  # index=False — don't save row numbers

    # JSON
    df.to_json("data/output/clean/transformed.json", orient="records", indent=2)

    # Parquet — best for downstream Spark work
    df.to_parquet("data/output/clean/transformed.parquet", index=False)


    Path("data/output/clean/department").mkdir(parents=True, exist_ok=True)
    # Multiple files partitioned by column — real DE pattern
    for dept, group in df.groupby("department"):
        group.to_parquet(f"data/output/clean/department/dept_{dept}.parquet", index=False)

#basic_inspection(df)
#cleaned_df = cleaning(df)
#aggregation(df_emp)
#merge_join()
#window_function(df_emp)
create_file(df_emp)