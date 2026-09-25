"""
Problem 0005 - SQL: Employees Above Average Salary
===================================================
Day 2 - Subqueries

Problem
-------
Given an `employees` table with columns (employee_id, name, department, salary),
write a SQL query to list all employees whose salary is strictly above the
overall average salary.

Solution
--------
    SELECT employee_id, name, department, salary
    FROM employees
    WHERE salary > (SELECT AVG(salary) FROM employees)
    ORDER BY salary DESC;

Variant: above their own department's average
    SELECT employee_id, name, department, salary
    FROM employees e
    WHERE salary > (
        SELECT AVG(salary)
        FROM employees
        WHERE department = e.department
    )
    ORDER BY department, salary DESC;

Notes
-----
- The subquery is executed once (correlated subqueries execute per row).
- Correlated subqueries can be rewritten with window functions for clarity:
        SELECT *
        FROM (
            SELECT *, AVG(salary) OVER (PARTITION BY department) AS dept_avg
            FROM employees
        ) t
        WHERE salary > dept_avg;

Complexity
----------
- Time:  O(n) for the non-correlated version
- Time:  O(n * d) for the correlated version (d = distinct departments)
- Space: O(1)
"""

import sqlite3

def setup_demo_db(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS employees;
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            name        TEXT,
            department  TEXT,
            salary      REAL
        );
        INSERT INTO employees VALUES
            (1, 'Alice',   'Engineering', 185000),
            (2, 'Bob',     'Sales',       120000),
            (3, 'Carol',   'Engineering', 195000),
            (4, 'Dave',    'Marketing',    95000),
            (5, 'Eve',     'Finance',     160000),
            (6, 'Frank',   'Engineering', 210000),
            (7, 'Grace',   'Sales',       110000),
            (8, 'Heidi',   'Finance',     175000);
    """)

def above_average(conn):
    query = """
        SELECT employee_id, name, department, salary
        FROM employees
        WHERE salary > (SELECT AVG(salary) FROM employees)
        ORDER BY salary DESC;
    """
    return conn.execute(query).fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup_demo_db(conn)
    for row in above_average(conn):
        print(row)
    conn.close()
