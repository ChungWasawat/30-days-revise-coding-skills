
-- partition by range
-- Create a partitioned table
CREATE TABLE sales_partitioned (
    sale_id     SERIAL,
    employee_id INTEGER,
    sale_month  DATE NOT NULL,
    amount      NUMERIC(10,2)
) PARTITION BY RANGE (sale_month);

-- Create partitions per quarter
-- partition of helps to inherit the parent's schema
CREATE TABLE sales_2024_q1
    PARTITION OF sales_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE sales_2024_q2
    PARTITION OF sales_partitioned
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Insert data — Postgres automatically routes to correct partition
INSERT INTO sales_partitioned (employee_id, sale_month, amount)
VALUES (4, '2024-02-15', 15000);   -- goes to Q1

-- Query with partition pruning — only scans Q1 partition
SELECT * FROM sales_partitioned
WHERE sale_month BETWEEN '2024-01-01' AND '2024-03-31';


-- partition by list
CREATE TABLE employees_partitioned (
    emp_id     SERIAL,
    name       VARCHAR(100),
    department VARCHAR(50) NOT NULL,
    salary     NUMERIC(10,2)
) PARTITION BY LIST (department);

CREATE TABLE employees_engineering
    PARTITION OF employees_partitioned
    FOR VALUES IN ('Engineering');

CREATE TABLE employees_marketing
    PARTITION OF employees_partitioned
    FOR VALUES IN ('Marketing');

CREATE TABLE employees_other
    PARTITION OF employees_partitioned
    FOR VALUES IN ('HR', 'Finance', 'Legal');

--test
create table monthly_sales_partition(
    sale_id     SERIAL,
    employee_id INTEGER REFERENCES employees(emp_id),
    sale_month  DATE not null,
    amount      NUMERIC(10,2)
) partition by range(sale_month)

CREATE TABLE monthly_sales_2024_q1
    PARTITION OF monthly_sales_partition
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE monthly_sales_2024_q2
    PARTITION OF monthly_sales_partition
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- sale id is shared between child partitioned table
INSERT INTO monthly_sales_partition (employee_id, sale_month, amount)
VALUES (12, '2024-02-15', 10000);   -- goes to Q1