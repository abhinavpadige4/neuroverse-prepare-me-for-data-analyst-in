"""
SQL Q1: Basic SELECT Operations
================================
Topic: SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, aliases

Interview Question:
Given a table 'employees' with columns (id, name, department, salary, hire_date),
write queries to:
  1. Select all columns from employees
  2. Select only name and salary
  3. Filter employees earning more than 50000
  4. Get distinct departments
  5. Order by salary descending, limit to top 5
  6. Use column aliases

This solution uses SQLite (in-memory) for portability and includes tests.
"""

import sqlite3
import unittest
from datetime import date


def setup_database(conn):
    """Create and populate the employees table for practice."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL,
            hire_date TEXT NOT NULL
        )
    """)
    cursor.execute("DELETE FROM employees")
    employees = [
        (1, "Alice Johnson", "Engineering", 95000, "2019-03-15"),
        (2, "Bob Smith", "Marketing", 62000, "2020-07-22"),
        (3, "Carol White", "Engineering", 88000, "2018-11-01"),
        (4, "David Brown", "Sales", 55000, "2021-01-10"),
        (5, "Eve Davis", "Marketing", 71000, "2019-09-05"),
        (6, "Frank Miller", "Engineering", 102000, "2017-06-18"),
        (7, "Grace Lee", "Sales", 48000, "2022-02-28"),
        (8, "Henry Wilson", "HR", 58000, "2020-04-12"),
        (9, "Ivy Chen", "Engineering", 91000, "2019-08-20"),
        (10, "Jack Taylor", "Marketing", 67000, "2021-05-30"),
        (11, "Karen Adams", "Sales", 52000, "2020-12-01"),
        (12, "Leo Martinez", "Engineering", 98000, "2018-02-14"),
    ]
    cursor.executemany(
        "INSERT INTO employees (id, name, department, salary, hire_date) VALUES (?, ?, ?, ?, ?)",
        employees
    )
    conn.commit()
    return cursor


def q1a_select_all(conn):
    """Q1a: Select all columns from employees."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    return cursor.fetchall()


def q1b_select_specific_columns(conn):
    """Q1b: Select only name and salary."""
    cursor = conn.cursor()
    cursor.execute("SELECT name, salary FROM employees")
    return cursor.fetchall()


def q1c_filter_salary(conn):
    """Q1c: Filter employees earning more than 50000."""
    cursor = conn.cursor()
    cursor.execute("SELECT name, salary FROM employees WHERE salary > 50000")
    return cursor.fetchall()


def q1d_distinct_departments(conn):
    """Q1d: Get distinct departments."""
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT department FROM employees")
    return cursor.fetchall()


def q1e_order_limit(conn):
    """Q1e: Order by salary descending, limit to top 5."""
    cursor = conn.cursor()
    cursor.execute("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 5")
    return cursor.fetchall()


def q1f_aliases(conn):
    """Q1f: Use column aliases for readability."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            name AS employee_name,
            department AS dept,
            salary AS annual_salary,
            hire_date AS start_date
        FROM employees
        WHERE salary > 60000
        ORDER BY annual_salary DESC
    """)
    return cursor.fetchall()


def q1g_multiple_conditions(conn):
    """Q1g: Multiple WHERE conditions with AND/OR."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, department, salary
        FROM employees
        WHERE department = 'Engineering' AND salary > 90000
    """)
    return cursor.fetchall()


def q1h_between_and_like(conn):
    """Q1h: Use BETWEEN and LIKE operators."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, salary
        FROM employees
        WHERE salary BETWEEN 60000 AND 80000
    """)
    between_results = cursor.fetchall()

    cursor.execute("""
        SELECT name, department
        FROM employees
        WHERE name LIKE '%son%'
    """)
    like_results = cursor.fetchall()

    return between_results, like_results


class TestBasicSelect(unittest.TestCase):
    """Tests for all Q1 basic SELECT exercises."""

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(":memory:")
        setup_database(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_q1a_select_all(self):
        results = q1a_select_all(self.conn)
        self.assertEqual(len(results), 12)
        self.assertEqual(results[0][0], 1)
        self.assertEqual(results[0][1], "Alice Johnson")

    def test_q1b_select_specific_columns(self):
        results = q1b_select_specific_columns(self.conn)
        self.assertEqual(len(results), 12)
        self.assertEqual(len(results[0]), 2)
        self.assertEqual(results[0][0], "Alice Johnson")
        self.assertEqual(results[0][1], 95000)

    def test_q1c_filter_salary(self):
        results = q1c_filter_salary(self.conn)
        self.assertEqual(len(results), 10)
        for row in results:
            self.assertGreater(row[1], 50000)

    def test_q1d_distinct_departments(self):
        results = q1d_distinct_departments(self.conn)
        departments = [r[0] for r in results]
        self.assertEqual(len(departments), len(set(departments)))
        self.assertIn("Engineering", departments)
        self.assertIn("Marketing", departments)
        self.assertIn("Sales", departments)
        self.assertIn("HR", departments)

    def test_q1e_order_limit(self):
        results = q1e_order_limit(self.conn)
        self.assertEqual(len(results), 5)
        salaries = [r[1] for r in results]
        self.assertEqual(salaries, sorted(salaries, reverse=True))
        self.assertEqual(results[0][0], "Frank Miller")
        self.assertEqual(results[0][1], 102000)

    def test_q1f_aliases(self):
        results = q1f_aliases(self.conn)
        self.assertGreater(len(results), 0)
        for row in results:
            self.assertGreater(row[2], 60000)

    def test_q1g_multiple_conditions(self):
        results = q1g_multiple_conditions(self.conn)
        self.assertEqual(len(results), 4)
        for row in results:
            self.assertEqual(row[1], "Engineering")
            self.assertGreater(row[2], 90000)

    def test_q1h_between_and_like(self):
        between_results, like_results = q1h_between_and_like(self.conn)
        self.assertEqual(len(between_results), 3)
        for row in between_results:
            self.assertGreaterEqual(row[1], 60000)
            self.assertLessEqual(row[1], 80000)
        self.assertGreater(len(like_results), 0)


def print_explanations():
    """Print detailed explanations for interview preparation."""
    explanations = [
        """Q1a - SELECT * FROM employees;
Purpose: Retrieve all data. Use in exploration, avoid in production for performance.
""",
        """Q1b - SELECT name, salary FROM employees;
Purpose: Select specific columns. Always prefer over SELECT * in production.
""",
        """Q1c - SELECT name, salary FROM employees WHERE salary > 50000;
Purpose: Filter rows. WHERE clause reduces result set before further processing.
""",
        """Q1d - SELECT DISTINCT department FROM employees;
Purpose: Remove duplicates. DISTINCT applies to entire row unless specified.
""",
        """Q1e - SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 5;
Purpose: Sort and paginate. DESC = descending. LIMIT for top-N queries.
""",
        """Q1f - SELECT name AS employee_name, ... FROM employees WHERE ...;
Purpose: Aliases improve readability. AS keyword renames output columns.
""",
        """Q1g - SELECT ... WHERE department = 'Engineering' AND salary > 90000;
Purpose: Multiple conditions. AND requires all true; OR requires at least one.
""",
        """Q1h - SELECT ... WHERE salary BETWEEN 60000 AND 80000;
       SELECT ... WHERE name LIKE '%son%';
Purpose: BETWEEN is inclusive range. LIKE uses % (any chars) and _ (single char).
""",
    ]
    for i, exp in enumerate(explanations, 1):
        print(f"{'='*60}")
        print(exp)


if __name__ == "__main__":
    print("=" * 60)
    print("SQL Q1: Basic SELECT Operations - Solutions")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    setup_database(conn)

    print("\n--- Q1a: Select All ---")
    for row in q1a_select_all(conn):
        print(row)

    print("\n--- Q1b: Select Specific Columns ---")
    for row in q1b_select_specific_columns(conn):
        print(row)

    print("\n--- Q1c: Filter Salary > 50000 ---")
    for row in q1c_filter_salary(conn):
        print(row)

    print("\n--- Q1d: Distinct Departments ---")
    for row in q1d_distinct_departments(conn):
        print(row)

    print("\n--- Q1e: Top 5 by Salary ---")
    for row in q1e_order_limit(conn):
        print(row)

    print("\n--- Q1f: With Aliases ---")
    for row in q1f_aliases(conn):
        print(row)

    print("\n--- Q1g: Multiple Conditions ---")
    for row in q1g_multiple_conditions(conn):
        print(row)

    print("\n--- Q1h: BETWEEN and LIKE ---")
    between, like = q1h_between_and_like(conn)
    print("BETWEEN 60000-80000:")
    for row in between:
        print(row)
    print("LIKE '%son%':")
    for row in like:
        print(row)

    conn.close()

    print("\n" + "=" * 60)
    print("Running Tests...")
    print("=" * 60)
    unittest.main(argv=["__main__"], exit=False, verbosity=2)

    print("\n" + "=" * 60)
    print("Interview Explanations")
    print("=" * 60)
    print_explanations()
