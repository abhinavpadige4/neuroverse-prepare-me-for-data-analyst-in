"""
Problem 0003 - SQL: Employees Per Department (INNER JOIN)
==========================================================
Day 2 - SQL Joins

Problem
-------
Given:
    departments(department_id, department_name)
    employees(employee_id, name, department_id, salary)

Write a SQL query to list each department and the number of employees in it
using an INNER JOIN.

Solution
--------
    SELECT d.department_id,
           d.department_name,
           COUNT(e.employee_id) AS employee_count
    FROM departments d
    INNER JOIN employees e ON e.department_id = d.department_id
    GROUP BY d.department_id, d.department_name
    ORDER BY employee_count DESC;

Notes
-----
- INNER JOIN keeps only rows with a match on both sides.
- Departments with zero employees will NOT appear. Use LEFT JOIN for that.
- COUNT(e.employee_id) is safer than COUNT(*) when using LEFT JOIN.

Complexity
----------
- Time:  O(n + m) with hash join, or O(n log n) with sort-merge join
- Space: O(min(n, m)) for the hash table
"""

import sqlite3

def setup_demo_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS departments;
        DROP TABLE IF EXISTS employees;
        CREATE TABLE departments (
            department_id   INTEGER PRIMARY KEY,
            department_name TEXT NOT NULL
        );
        CREATE TABLE employees (
            employee_id   INTEGER PRIMARY KEY,
            name          TEXT NOT NULL,
            department_id INTEGER,
            salary        REAL
        );
        INSERT INTO departments VALUES (1, 'Engineering'), (2, 'Sales'), (3, 'Marketing'), (4, 'Finance');
        INSERT INTO employees VALUES
            (1, 'Alice', 1, 185000),
            (2, 'Bob',   2, 120000),
            (3, 'Carol', 1, 195000),
            (4, 'Dave',  3,  95000),
            (5, 'Eve',   4, 160000),
            (6, 'Frank', 1, 210000),
            (7, 'Grace', 2, 110000),
            (8, 'Heidi', 4, 175000);
        """
    )

def dept_emp_count(conn: sqlite3.Connection):
    query = """
        SELECT d.department_id,
               d.department_name,
               COUNT(e.employee_id) AS employee_count
        FROM departments d
        INNER JOIN employees e ON e.department_id = d.department_id
        GROUP BY d.department_id, d.department_name
        ORDER BY employee_count DESC;
    """
    return conn.execute(query).fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup_demo_db(conn)
    for row in dept_emp_count(conn):
        print(row)
    conn.close()
