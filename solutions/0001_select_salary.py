"""
Data Analyst Interview Prep - Day 1: SQL Fundamentals
Problem 0001: Select all columns from employees where salary > 50000, ordered by last_name.

This solution demonstrates:
- Basic SELECT * query
- WHERE clause filtering
- ORDER BY sorting
- Connection to SQLite for live execution
"""

import sqlite3
import os


def create_sample_database(db_path: str) -> None:
    """Create a sample employees database for testing."""
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            department TEXT,
            salary REAL NOT NULL,
            hire_date TEXT
        )
    """)

    sample_data = [
        (1, "Alice", "Johnson", "Engineering", 75000.00, "2020-03-15"),
        (2, "Bob", "Smith", "Marketing", 45000.00, "2019-07-22"),
        (3, "Charlie", "Brown", "Engineering", 82000.00, "2018-01-10"),
        (4, "Diana", "Williams", "Sales", 55000.00, "2021-05-03"),
        (5, "Edward", "Davis", "Marketing", 38000.00, "2022-09-18"),
        (6, "Fiona", "Miller", "Engineering", 91000.00, "2017-11-01"),
        (7, "George", "Wilson", "Sales", 62000.00, "2020-08-14"),
        (8, "Hannah", "Moore", "HR", 48000.00, "2021-02-28"),
        (9, "Ivan", "Taylor", "Engineering", 78000.00, "2019-04-09"),
        (10, "Julia", "Anderson", "Sales", 51000.00, "2022-01-20"),
    ]

    cursor.executemany(
        "INSERT INTO employees (id, first_name, last_name, department, salary, hire_date) VALUES (?, ?, ?, ?, ?, ?)",
        sample_data
    )

    conn.commit()
    conn.close()


def get_high_salary_employees(db_path: str) -> list:
    """
    Execute the SQL query to select all columns from employees
    where salary > 50000, ordered by last_name.

    SQL Query:
        SELECT *
        FROM employees
        WHERE salary > 50000
        ORDER BY last_name;

    Returns:
        List of tuples representing rows from the query result.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # The core SQL query for this problem
    query = """
        SELECT *
        FROM employees
        WHERE salary > 50000
        ORDER BY last_name;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results


def print_results(results: list) -> None:
    """Print query results in a formatted table."""
    if not results:
        print("No employees found with salary > 50000.")
        return

    # Column headers
    headers = ["id", "first_name", "last_name", "department", "salary", "hire_date"]
    header_widths = [max(len(str(h)), max(len(str(row[i])) for row in results)) for i, h in enumerate(headers)]

    # Print header
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, header_widths))
    separator = "-+-".join("-" * w for w in header_widths)

    print(f"\n{'=' * len(header_line)}")
    print("HIGH SALARY EMPLOYEES (salary > 50000, ordered by last_name)")
    print(f"{'=' * len(header_line)}")
    print(header_line)
    print(separator)

    # Print rows
    for row in results:
        row_line = " | ".join(str(val).ljust(w) for val, w in zip(row, header_widths))
        print(row_line)

    print(f"\nTotal employees found: {len(results)}")


def verify_results(results: list) -> bool:
    """Verify that results meet the expected criteria."""
    if not results:
        return False

    # Check 1: All salaries should be > 50000
    for row in results:
        salary = row[4]
        if salary <= 50000:
            print(f"FAIL: Found employee with salary {salary} <= 50000")
            return False

    # Check 2: Results should be ordered by last_name
    last_names = [row[2] for row in results]
    if last_names != sorted(last_names):
        print(f"FAIL: Results not ordered by last_name: {last_names}")
        return False

    # Check 3: Expected count (from sample data: 7 employees with salary > 50000)
    expected_count = 7
    if len(results) != expected_count:
        print(f"FAIL: Expected {expected_count} results, got {len(results)}")
        return False

    print("All verification checks PASSED.")
    return True


def get_query_string() -> str:
    """Return the SQL query string for reference/documentation."""
    return """SELECT *
FROM employees
WHERE salary > 50000
ORDER BY last_name;"""


if __name__ == "__main__":
    db_path = "sample_employees.db"

    print("=" * 60)
    print("Problem 0001: Select employees with salary > 50000")
    print("=" * 60)

    # Display the SQL query
    print(f"\nSQL Query:\n{get_query_string()}\n")

    # Create sample database
    print("Creating sample database...")
    create_sample_database(db_path)

    # Execute query
    print("Executing query...")
    results = get_high_salary_employees(db_path)

    # Display results
    print_results(results)

    # Verify correctness
    print()
    verify_results(results)

    # Cleanup
    os.remove(db_path)
    print("\nSample database cleaned up.")
