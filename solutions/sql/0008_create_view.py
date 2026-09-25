"""
SQL Q8: Create a View
======================

Problem:
--------
Given a table `employees` with columns (id, name, department, salary, hire_date),
create a view called `high_earners` that shows employees earning above the
average salary, displaying only name, department, and salary.

Also create a second view `dept_summary` that shows department-level
aggregations (employee count, avg salary, max salary) for departments
with more than 2 employees.

Learning Objectives:
- CREATE VIEW syntax and usage
- Views vs tables (virtual vs physical)
- Querying views like tables
- DROP VIEW
- Views with JOINs and aggregations
- Performance considerations

Difficulty: Medium
Estimated Time: 20 minutes
"""

import sqlite3
import os
import sys


def setup_database(db_path: str) -> sqlite3.Connection:
    """Create and populate the sample database."""
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the employees table
    cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL,
            hire_date TEXT NOT NULL
        )
    """)

    # Insert sample data
    employees_data = [
        (1, "Alice Johnson", "Engineering", 95000, "2019-03-15"),
        (2, "Bob Smith", "Engineering", 88000, "2020-01-10"),
        (3, "Carol White", "Marketing", 72000, "2018-06-20"),
        (4, "David Brown", "Marketing", 68000, "2021-02-28"),
        (5, "Eve Davis", "Engineering", 105000, "2017-11-05"),
        (6, "Frank Miller", "Sales", 62000, "2022-04-12"),
        (7, "Grace Lee", "Sales", 78000, "2019-08-30"),
        (8, "Henry Wilson", "Engineering", 92000, "2020-07-22"),
        (9, "Ivy Chen", "Marketing", 81000, "2018-09-14"),
        (10, "Jack Taylor", "Sales", 55000, "2023-01-05"),
        (11, "Karen Adams", "Engineering", 110000, "2016-05-18"),
        (12, "Leo Martinez", "Sales", 71000, "2021-10-09"),
    ]

    cursor.executemany(
        "INSERT INTO employees (id, name, department, salary, hire_date) VALUES (?, ?, ?, ?, ?)",
        employees_data
    )

    conn.commit()
    return conn


def create_high_earners_view(conn: sqlite3.Connection) -> None:
    """
    Solution Part 1: Create a view for high earners.

    A view is a virtual table defined by a SELECT query.
    It doesn't store data physically — it's computed on each access.
    """
    cursor = conn.cursor()

    # Drop the view if it already exists (for idempotency)
    cursor.execute("DROP VIEW IF EXISTS high_earners")

    # Create the view
    cursor.execute("""
        CREATE VIEW high_earners AS
        SELECT
            name,
            department,
            salary
        FROM employees
        WHERE salary > (
            SELECT AVG(salary)
            FROM employees
        )
    """)

    conn.commit()
    print("[OK] View 'high_earners' created successfully.")


def create_dept_summary_view(conn: sqlite3.Connection) -> None:
    """
    Solution Part 2: Create a department summary view with aggregations.

    Demonstrates that views can contain GROUP BY, HAVING, and expressions.
    """
    cursor = conn.cursor()

    cursor.execute("DROP VIEW IF EXISTS dept_summary")

    cursor.execute("""
        CREATE VIEW dept_summary AS
        SELECT
            department,
            COUNT(*) AS employee_count,
            ROUND(AVG(salary), 2) AS avg_salary,
            MAX(salary) AS max_salary,
            MIN(salary) AS min_salary
        FROM employees
        GROUP BY department
        HAVING COUNT(*) > 2
    """)

    conn.commit()
    print("[OK] View 'dept_summary' created successfully.")


def create_view_with_join(conn: sqlite3.Connection) -> None:
    """
    Solution Part 3: Create a view that joins with another table.

    Demonstrates views can encapsulate complex JOIN logic.
    """
    cursor = conn.cursor()

    # Create a departments reference table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            dept_name TEXT PRIMARY KEY,
            location TEXT NOT NULL,
            budget REAL NOT NULL
        )
    """)

    cursor.executemany(
        "INSERT OR REPLACE INTO departments (dept_name, location, budget) VALUES (?, ?, ?)",
        [
            ("Engineering", "Building A", 500000),
            ("Marketing", "Building B", 200000),
            ("Sales", "Building C", 300000),
        ]
    )

    cursor.execute("DROP VIEW IF EXISTS employee_dept_details")

    cursor.execute("""
        CREATE VIEW employee_dept_details AS
        SELECT
            e.name,
            e.department,
            e.salary,
            d.location,
            d.budget,
            ROUND(e.salary * 100.0 / d.budget, 2) AS salary_pct_of_budget
        FROM employees e
        INNER JOIN departments d ON e.department = d.dept_name
    """)

    conn.commit()
    print("[OK] View 'employee_dept_details' created successfully.")


def query_views(conn: sqlite3.Connection) -> None:
    """Demonstrate querying views like regular tables."""
    cursor = conn.cursor()

    print("\n" + "=" * 60)
    print("QUERYING VIEWS")
    print("=" * 60)

    # Query high_earners view
    print("\n--- High Earners (above average salary) ---")
    cursor.execute("SELECT * FROM high_earners ORDER BY salary DESC")
    rows = cursor.fetchall()
    print(f"{'Name':<20} {'Department':<15} {'Salary':>10}")
    print("-" * 47)
    for row in rows:
        print(f"{row[0]:<20} {row[1]:<15} ${row[2]:>9,.0f}")
    print(f"\nTotal high earners: {len(rows)}")

    # Query dept_summary view
    print("\n--- Department Summary (departments with >2 employees) ---")
    cursor.execute("SELECT * FROM dept_summary ORDER BY avg_salary DESC")
    rows = cursor.fetchall()
    print(f"{'Department':<15} {'Count':>6} {'Avg Salary':>12} {'Max Salary':>12} {'Min Salary':>12}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<15} {row[1]:>6} ${row[2]:>10,.2f} ${row[3]:>10,.0f} ${row[4]:>10,.0f}")

    # Query the join view
    print("\n--- Employee Department Details (top 5 by salary) ---")
    cursor.execute("""
        SELECT name, department, salary, location, salary_pct_of_budget
        FROM employee_dept_details
        ORDER BY salary DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()
    print(f"{'Name':<18} {'Dept':<14} {'Salary':>10} {'Location':<12} {'% Budget':>9}")
    print("-" * 66)
    for row in rows:
        print(f"{row[0]:<18} {row[1]:<14} ${row[2]:>9,.0f} {row[3]:<12} {row[4]:>8.2f}%")

    # Demonstrate filtering a view
    print("\n--- High Earners in Engineering Only ---")
    cursor.execute("""
        SELECT name, salary
        FROM high_earners
        WHERE department = 'Engineering'
        ORDER BY salary DESC
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"  {row[0]}: ${row[1]:,.0f}")


def verify_views_exist(conn: sqlite3.Connection) -> bool:
    """Verify that all views were created successfully."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type = 'view'
        ORDER BY name
    """)
    views = [row[0] for row in cursor.fetchall()]
    expected = ["dept_summary", "employee_dept_details", "high_earners"]

    all_present = all(v in views for v in expected)
    print(f"\nViews in database: {views}")
    print(f"All expected views present: {all_present}")
    return all_present


def test_view_behavior(conn: sqlite3.Connection) -> bool:
    """
    Test that views reflect underlying data changes.
    Views are virtual — they always show current data.
    """
    cursor = conn.cursor()

    # Get initial count from high_earners
    cursor.execute("SELECT COUNT(*) FROM high_earners")
    initial_count = cursor.fetchone()[0]

    # Insert a new high earner
    cursor.execute("""
        INSERT INTO employees (id, name, department, salary, hire_date)
        VALUES (13, 'Mia Thompson', 'Engineering', 120000, '2023-06-01')
    """)
    conn.commit()

    # View should now include the new employee
    cursor.execute("SELECT COUNT(*) FROM high_earners")
    new_count = cursor.fetchone()[0]

    view_updated = new_count > initial_count
    print(f"\n[TEST] View reflects data changes: {view_updated}")
    print(f"  Before insert: {initial_count} high earners")
    print(f"  After insert:  {new_count} high earners")

    # Verify the new employee appears
    cursor.execute("""
        SELECT name FROM high_earners WHERE name = 'Mia Thompson'
    """)
    found = cursor.fetchone() is not None
    print(f"  New employee visible in view: {found}")

    # Clean up
    cursor.execute("DELETE FROM employees WHERE id = 13")
    conn.commit()

    return view_updated and found


def test_view_drop(conn: sqlite3.Connection) -> bool:
    """Test dropping a view."""
    cursor = conn.cursor()

    # Create a temporary view
    cursor.execute("""
        CREATE VIEW temp_test_view AS
        SELECT id, name FROM employees WHERE id = 1
    """)
    conn.commit()

    # Verify it exists
    cursor.execute("SELECT COUNT(*) FROM temp_test_view")
    exists_before = cursor.fetchone()[0] == 1

    # Drop it
    cursor.execute("DROP VIEW temp_test_view")
    conn.commit()

    # Verify it's gone
    try:
        cursor.execute("SELECT * FROM temp_test_view")
        exists_after = True
    except sqlite3.OperationalError:
        exists_after = False

    test_passed = exists_before and not exists_after
    print(f"\n[TEST] DROP VIEW works correctly: {test_passed}")
    return test_passed


def run_all_tests(conn: sqlite3.Connection) -> bool:
    """Run all tests and return overall pass/fail."""
    print("\n" + "=" * 60)
    print("RUNNING TESTS")
    print("=" * 60)

    results = []
    results.append(verify_views_exist(conn))
    results.append(test_view_behavior(conn))
    results.append(test_view_drop(conn))

    all_passed = all(results)
    print(f"\n{'=' * 60}")
    print(f"OVERALL: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print(f"{'=' * 60}")
    return all_passed


def cleanup(db_path: str) -> None:
    """Remove the temporary database file."""
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"\n[Cleanup] Removed temporary database: {db_path}")


def main():
    """Main entry point."""
    db_path = "test_views.db"

    print("=" * 60)
    print("SQL Q8: CREATE VIEW - Complete Solution")
    print("=" * 60)

    # Setup
    conn = setup_database(db_path)
    print("[OK] Database created with sample data.")

    # Create views
    create_high_earners_view(conn)
    create_dept_summary_view(conn)
    create_view_with_join(conn)

    # Query views
    query_views(conn)

    # Run tests
    all_passed = run_all_tests(conn)

    # Cleanup
    conn.close()
    cleanup(db_path)

    # Print key takeaways
    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
1. CREATE VIEW defines a virtual table from a SELECT query.
2. Views don't store data — they compute results on access.
3. Views always reflect current underlying data.
4. Views can contain JOINs, aggregations, subqueries.
5. Use DROP VIEW IF EXISTS for idempotent scripts.
6. Views simplify complex queries for consumers.
7. Views can be used in WHERE clauses of other queries.
8. Performance: views add a layer of indirection;
   materialized views (not in SQLite) cache results.
""")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
