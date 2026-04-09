-- Basic CTE — WITH clause defines a named subquery
WITH dept_summary AS (
    SELECT
        department,
        COUNT(*)        AS headcount,
        AVG(salary)     AS avg_salary,
        MAX(salary)     AS max_salary
    FROM employees
    GROUP BY department
)
SELECT *
FROM dept_summary
WHERE headcount > 2
ORDER BY avg_salary DESC;
-- having can do this too


WITH
-- Step 1: clean and filter base data
active_employees AS (
    SELECT *
    FROM employees
    WHERE salary > 0
      AND hire_date >= '2019-01-01'
),
-- Step 2: aggregate by department
dept_stats AS (
    SELECT
        department,
        COUNT(*)            AS headcount,
        ROUND(AVG(salary), 2) AS avg_salary
    FROM active_employees
    GROUP BY department
),
-- Step 3: flag high-performing departments
flagged AS (
    SELECT *,
        CASE WHEN avg_salary > 70000 THEN 'high'
             WHEN avg_salary > 60000 THEN 'mid'
             ELSE 'low' END AS salary_band
    FROM dept_stats
)
SELECT * FROM flagged ORDER BY avg_salary DESC;


-- Walk the manager hierarchy starting from top-level (no manager)
WITH RECURSIVE org_chart AS (
    -- Base case: top-level employees (no manager)
    SELECT emp_id, name, manager_id, 0 AS level
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    -- Recursive case: join employees to their manager
    SELECT e.emp_id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.emp_id
)
SELECT
    LPAD('  ', level * 2, ' ') || name AS hierarchy,
    level
FROM org_chart
ORDER BY level, emp_id;

