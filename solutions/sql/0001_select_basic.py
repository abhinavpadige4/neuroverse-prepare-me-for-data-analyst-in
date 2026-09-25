"""
SQL Q1: SELECT Basic - Filter and Project Columns
=====================================================
Problem:
    Given an 'employees' table, write a SQL query to select the name and
    department of all employees who earn more than 50000.

Table Schema:
    employees (
        id          INTEGER PRIMARY KEY,
        name        VARCHAR(100),
        department  VARCHAR(100),
        salary      DECIMAL(10,2),
        hire_date   DATE
    )

Difficulty: Easy
Topic: SELECT, WHERE, column projection
"""

import sqlite3
import os


def create_sample_database(db_path: str) -> None:
    """Create and populate a sample employees database for testing."""
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE employees (
            id          INTEGER PRIMARY KEY,
            name        VARCHAR(100),
            department  VARCHAR(100),
            salary      DECIMAL(10,2),
            hire_date   DATE
        )
    """)

    sample_data = [
        (1, 'Alice Johnson', 'Engineering', 85000.00, '2020-03-15'),
        (2, 'Bob Smith', 'Marketing', 45000.00, '2019-07-22'),
        (3, 'Carol Williams', 'Engineering', 92000.00, '2018-01-10'),
        (4, 'David Brown', 'Sales', 55000.00, '2021-05-01'),
        (5, 'Eva Martinez', 'Marketing', 38000.00, '2022-02-28'),
        (6, 'Frank Lee', 'Engineering', 78000.00, '2019-11-05'),
        (7, 'Grace Kim', 'Sales', 62000.00, '2020-09-18'),
        (8, 'Henry Davis', 'HR', 51000.00, '2021-01-12'),
        (9, 'Irene Chen', 'Engineering', 105000.00, '2017-06-30'),
        (10, 'Jack Wilson', 'Sales', 48000.00, '2022-08-14'),
    ]

    cursor.executemany(
        "INSERT INTO employees (id, name, department, salary, hire_date) VALUES (?, ?, ?, ?, ?)",
        sample_data
    )

    conn.commit()
    conn.close()


def get_sql_solution() -> str:
    """Return the SQL query that solves the problem."""
    return """
    SELECT name, department
    FROM employees
    WHERE salary > 50000
    ORDER BY name ASC;
    """.strip()


def execute_solution(db_path: str) -> list:
    """Execute the SQL solution and return results as list of tuples."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = get_sql_solution()
    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results


def verify_solution(db_path: str) -> bool:
    """Verify the solution produces correct results."""
    results = execute_solution(db_path)

    # Expected results: employees with salary > 50000, ordered by name
    expected = [
        ('Alice Johnson', 'Engineering'),
        ('Carol Williams', 'Engineering'),
        ('David Brown', 'Sales'),
        ('Frank Lee', 'Engineering'),
        ('Grace Kim', 'Sales'),
        ('Henry Davis', 'HR'),
        ('Irene Chen', 'Engineering'),
    ]

    assert results == expected, (
        f"Solution failed!\n"
        f"Expected: {expected}\n"
        f"Got:      {results}"
    )

    # Additional assertions for correctness
    assert len(results) == 7, f"Expected 7 rows, got {len(results)}"

    # Verify no salary <= 50000 leaked through
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for name, dept in results:
        cursor.execute(
            "SELECT salary FROM employees WHERE name = ? AND department = ?",
            (name, dept)
        )
        salary = cursor.fetchone()[0]
        assert salary > 50000, f"{name} has salary {salary}, should be > 50000"
    conn.close()

    # Verify ordering is alphabetical by name
    names = [row[0] for row in results]
    assert names == sorted(names), "Results not ordered by name ASC"

    return True


def print_solution():
    """Print formatted solution output."""
    print("=" * 60)
    print("SQL Q1: SELECT Basic - Filter and Project Columns")
    print("=" * 60)
    print()
    print("PROBLEM:")
    print("  Select name and department of employees earning > 50000.")
    print()
    print("SQL SOLUTION:")
    print("-" * 40)
    print(get_sql_solution())
    print("-" * 40)
    print()

    db_path = ":memory:"
    create_sample_database(db_path)
    results = execute_solution(db_path)

    print("RESULTS:")
    print(f"{'Name':<20} {'Department':<15}")
    print("-" * 35)
    for name, dept in results:
        print(f"{name:<20} {dept:<15}")
    print()
    print(f"Total rows returned: {len(results)}")
    print()

    passed = verify_solution(db_path)
    print(f"Verification: {'PASSED' if passed else 'FAILED'}")
    print()

    # Explain the query
    print("EXPLANATION:")
    print("  1. SELECT name, department - projects only the needed columns")
    print("  2. FROM employees - specifies the source table")
    print("  3. WHERE salary > 50000 - filters rows by salary condition")
    print("  4. ORDER BY name ASC - sorts results alphabetically by name")
    print()
    print("KEY CONCEPTS:")
    print("  - Column projection: selecting specific columns instead of SELECT *")
    print("  - WHERE clause: filters rows based on a boolean condition")
    print("  - ORDER BY: sorts the result set (ASC = ascending, DESC = descending)")
    print("  - Best practice: always specify columns explicitly rather than SELECT *")


if __name__ == "__main__":
    print_solution()
