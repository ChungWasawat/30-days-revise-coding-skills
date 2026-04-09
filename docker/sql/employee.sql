# ddl

CREATE TABLE IF NOT EXISTS employees (
    emp_id      SERIAL PRIMARY KEY,
    name        VARCHAR(100),
    department  VARCHAR(50),
    city        VARCHAR(50),
    salary      NUMERIC(10,2),
    hire_date   DATE,
    manager_id  INTEGER
); 


# dml
INSERT INTO employees (name, department, city, salary, hire_date, manager_id) VALUES
    ('Alice',   'Engineering', 'Bangkok',   95000, '2020-01-15', NULL),
    ('Bob',     'Engineering', 'Bangkok',   82000, '2021-03-10', 1),
    ('Charlie', 'Engineering', 'Chiang Mai',78000, '2022-06-01', 1),
    ('Diana',   'Marketing',   'Bangkok',   70000, '2019-08-20', NULL),
    ('Eve',     'Marketing',   'Bangkok',   65000, '2022-01-05', 4),
    ('Frank',   'Marketing',   'Chiang Mai',60000, '2023-02-14', 4),
    ('Grace',   'HR',          'Bangkok',   55000, '2021-11-30', NULL),
    ('Henry',   'HR',          'Bangkok',   52000, '2022-09-15', 7),
    ('Iris',    'Engineering', 'Bangkok',   91000, '2020-07-22', 1),
    ('Jack',    'Marketing',   'Chiang Mai',68000, '2021-05-18', 4);