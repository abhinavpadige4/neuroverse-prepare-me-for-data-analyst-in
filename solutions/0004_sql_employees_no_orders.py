"""
Problem 0004 - SQL: Employees With No Orders (LEFT JOIN + IS NULL)
==================================================================
Day 2 - SQL Joins & Subqueries

Problem
-------
Given:
    employees(employee_id, name, department_id)
    orders(order_id, employee_id, order_date, total)

Write a SQL query to find employees who have NOT placed any orders,
using a LEFT JOIN and IS NULL.

Solution
--------
    SELECT e.employee_id, e.name, e.department_id
    FROM employees e
    LEFT JOIN orders o ON o.employee_id = e.employee_id
    WHERE o.order_id IS NULL;

Alternative (using NOT IN / NOT EXISTS):
    SELECT employee_id, name, department_id
    FROM employees
    WHERE employee_id NOT IN (SELECT DISTINCT employee_id FROM orders);

    SELECT employee_id, name, department_id
    FROM employees e
    WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.employee_id = e.employee_id);

Notes
-----
- LEFT JOIN keeps all rows from the left table; unmatched right rows become NULL.
- Filtering on the right table's columns with IS NULL identifies non-matches.
- NOT EXISTS is generally the most efficient for large tables.

Complexity
----------
- Time:  O(n + m) with hash anti-join
- Space: O(min(n, m))
"""

import sqlite3

def setup_demo_db(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS employees;
        DROP TABLE IF EXISTS orders;
        CREATE TABLE employees (
            employee_id   INTEGER PRIMARY KEY,
            name          TEXT NOT NULL,
            department_id INTEGER
        );
        CREATE TABLE orders (
            order_id    INTEGER PRIMARY KEY,
            employee_id INTEGER,
            order_date  TEXT,
            total       REAL
        );
        INSERT INTO employees VALUES
            (1, 'Alice', 1), (2, 'Bob', 2), (3, 'Carol', 1),
            (4, 'Dave', 3), (5, 'Eve', 4);
        INSERT INTO orders VALUES
            (101, 1, '2026-09-01', 120.00),
            (102, 3, '2026-09-02',  88.00),
            (103, 1, '2026-09-03',  45.00);
    """)

def employees_no_orders(conn):
    query = """
        SELECT e.employee_id, e.name, e.department_id
        FROM employees e
        LEFT JOIN orders o ON o.employee_id = e.employee_id
        WHERE o.order_id IS NULL;
    """
    return conn.execute(query).fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup_demo_db(conn)
    for row in employees_no_orders(conn):
        print(row)
    conn.close()
