"""
Problem 0001 - SQL: Top 10 Highest Paid Employees
=================================================
Day 1 - SQL Fundamentals (SELECT, ORDER BY, LIMIT)

Problem
-------
Given an `employees` table with columns (employee_id, name, department, salary),
write a SQL query to select the top 10 highest paid employees.

Solution
--------
    SELECT employee_id, name, department, salary
    FROM employees
    ORDER BY salary DESC
    LIMIT 10;

Notes
-----
- ORDER BY ... DESC sorts descending (highest first).
- LIMIT n returns only the first n rows after sorting.
- If ties exist at the boundary, LIMIT may arbitrarily drop some tied rows.
  Use RANK() or DENSE_RANK() if you need to keep all ties.

Complexity
----------
- Time:  O(n log n)  -- sorting dominates
- Space: O(1)        -- streaming sort in most engines

Equivalent with window function (keeps ties):
    SELECT employee_id, name, department, salary
    FROM (
        SELECT *, RANK() OVER (ORDER BY salary DESC) AS rnk
        FROM employees
    ) ranked
    WHERE rnk <= 10;
"""

import sqlite3

def setup_demo_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS employees;
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            department  TEXT NOT NULL,
            salary      REAL NOT NULL
        );
        INSERT INTO employees (name, department, salary) VALUES
            ('Alice',   'Engineering', 185000),
            ('Bob',     'Sales',       120000),
            ('Carol',   'Engineering', 195000),
            ('Dave',    'Marketing',   95000),
            ('Eve',     'Finance',     160000),
            ('Frank',   'Engineering', 210000),
            ('Grace',   'Sales',       110000),
            ('Heidi',   'Finance',     175000),
            ('Ivan',    'Marketing',   88000),
            ('Judy',    'Engineering', 205000),
            ('Kevin',   'Sales',       130000),
            ('Laura',   'Finance',     155000);
        """
    )

def top_10_highest_paid(conn: sqlite3.Connection):
    query = """
        SELECT employee_id, name, department, salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 10;
    """
    return conn.execute(query).fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup_demo_db(conn)
    for row in top_10_highest_paid(conn):
        print(row)
    conn.close()
