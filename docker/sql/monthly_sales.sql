
# ddl
CREATE TABLE IF NOT EXISTS monthly_sales (
    sale_id     SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(emp_id),
    sale_month  DATE,
    amount      NUMERIC(10,2)
);

# dml
INSERT INTO monthly_sales (employee_id, sale_month, amount) VALUES
    (4, '2024-01-01', 12000), (4, '2024-02-01', 15000), (4, '2024-03-01', 11000),
    (5, '2024-01-01',  9000), (5, '2024-02-01',  8500), (5, '2024-03-01', 10000),
    (6, '2024-01-01',  7000), (6, '2024-02-01',  9500), (6, '2024-03-01',  8000),
    (10,'2024-01-01', 11000), (10,'2024-02-01', 13000), (10,'2024-03-01', 12500);