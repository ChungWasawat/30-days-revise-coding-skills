-- EXPLAIN — shows the execution plan without running the query
EXPLAIN
SELECT * FROM employees WHERE department = 'Engineering';

-- EXPLAIN ANALYZE — actually runs the query and shows real timings
EXPLAIN ANALYZE
SELECT e.name, AVG(s.amount)
FROM employees e
JOIN monthly_sales s ON e.emp_id = s.employee_id
GROUP BY e.name;

--Seq Scan        — full table scan, no index used (bad on large tables)
--Index Scan      — using an index (good)
--Hash Join       — joining via hash table (good for large tables)
--Nested Loop     — row-by-row join (bad on large tables, ok on small)
--Sort            — sorting in memory (check if index could eliminate this)

--Rows=1000       — estimated rows (if wildly off, run ANALYZE to update stats)
--actual rows=987 — real rows (close to estimate = good planner)
--cost=0.00..8.50 — startup cost..total cost (lower is better)

-- Add index on frequently filtered column
CREATE INDEX idx_employees_dept ON employees(department);

-- Composite index for multi-column filters
CREATE INDEX idx_employees_dept_city ON employees(department, city);

-- Index on foreign key — always do this
CREATE INDEX idx_sales_employee_id ON monthly_sales(employee_id);

-- Check EXPLAIN before and after adding index
EXPLAIN ANALYZE
SELECT * FROM employees WHERE department = 'Engineering' AND city = 'Bangkok';


-- BAD — function on indexed column kills the index
WHERE UPPER(department) = 'ENGINEERING'

-- GOOD — store normalized, query normalized
WHERE department = 'Engineering'

-- BAD — SELECT * pulls all columns even if you need two
EXPLAIN ANALYZE
SELECT * FROM employees e JOIN monthly_sales s ON e.emp_id = s.employee_id

-- GOOD — select only what you need
EXPLAIN ANALYZE
SELECT e.name, s.amount FROM employees e JOIN monthly_sales s ON e.emp_id = s.employee_id

-- BAD — correlated subquery runs once per row
EXPLAIN ANALYZE
SELECT name,
    (SELECT AVG(salary) FROM employees e2
     WHERE e2.department = e1.department)
FROM employees e1;

-- GOOD — window function runs once
EXPLAIN ANALYZE
SELECT name,
    AVG(salary) OVER (PARTITION BY department)
FROM employees;

-- upsert instead of select then insert
INSERT INTO users (id, name) VALUES (1, 'Alice')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
-- insert if not conflict id, update if conflict
-- EXCLUDED.name = Alice; EXCLUDED from temporary row