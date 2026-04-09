# rank, dense_rank, row_number, percent_rank
SELECT
    name,
    department,
    salary,
    -- rank within department by salary (gaps on ties)
    RANK()       OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
    -- dense rank (no gaps on ties — preferred in DE)
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank,
    -- row number (unique, arbitrary order for ties)
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,
    -- percentile — what % of dept earns less than this person
    PERCENT_RANK() OVER (PARTITION BY department ORDER BY salary)   AS pct_rank,
    -- ntile - divide rows by partition into n groups
    NTILE(3) OVER (PARTITION BY department ORDER BY salary) as n3_tile
FROM employees;

SELECT
    name,
    department,
    salary,
    -- dept average alongside every row
    ROUND(AVG(salary) OVER (PARTITION BY department), 2)  AS dept_avg,
    -- salary vs dept average
    ROUND(salary - AVG(salary) OVER (PARTITION BY department), 2) AS vs_avg,
    -- running total within department ordered by hire date
    -- unbounded [preceding -since first row/ following -until last row]
    -- n [preceding/ following]
    -- current -current processing row
    SUM(salary) OVER (
        PARTITION BY department
        ORDER BY hire_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,
    -- each person's % of their dept total salary
    ROUND(
        salary / SUM(salary) OVER (PARTITION BY department) * 100, 2
    ) AS pct_of_dept
FROM employees;

SELECT
    employee_id,
    sale_month,
    amount,
    -- previous month's sales
    LAG(amount, 1)  OVER (PARTITION BY employee_id ORDER BY sale_month) AS prev_month,
    -- next month's sales
    LEAD(amount, 1) OVER (PARTITION BY employee_id ORDER BY sale_month) AS next_month,
    -- month over month change
    amount - LAG(amount, 1) OVER (PARTITION BY employee_id ORDER BY sale_month) AS mom_change,
    -- 3-month rolling average
    ROUND(AVG(amount) OVER (
        PARTITION BY employee_id
        ORDER BY sale_month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_3m_avg
FROM monthly_sales
ORDER BY employee_id, sale_month;

SELECT
    name,
    department,
    salary,
    -- highest earner's name in each department
    FIRST_VALUE(name) OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS top_earner_in_dept
FROM employees;