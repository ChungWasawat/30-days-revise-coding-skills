-- Keep only the most recent sale per employee per month
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY employee_id, sale_month
            ORDER BY sale_id DESC          -- latest insert wins
        ) AS rn
    FROM monthly_sales
)
SELECT * FROM ranked WHERE rn = 1;

-- Find employees whose salary changed vs a snapshot table
SELECT
    curr.emp_id,
    curr.name,
    prev.salary AS old_salary,
    curr.salary AS new_salary,
    curr.salary - prev.salary AS change
FROM employees curr
JOIN employees_snapshot prev ON curr.emp_id = prev.emp_id
WHERE curr.salary <> prev.salary;


WITH expected AS (
    SELECT generate_series(
        '2024-01-01'::date,
        '2024-05-01'::date,
        '1 month'::interval
    )::date AS sale_month
),
actuals AS (
    SELECT DISTINCT sale_month FROM monthly_sales WHERE employee_id = 4
)
SELECT e.sale_month AS missing_month
FROM expected e
LEFT JOIN actuals a ON e.sale_month = a.sale_month
WHERE a.sale_month IS NULL;