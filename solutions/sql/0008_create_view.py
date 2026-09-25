"""
SQL Q8: Create a View
=====================
Objective: Learn how to create, query, and manage SQL views.

A VIEW is a virtual table defined by a SELECT query. It does not store data
physically; instead, it runs the underlying query each time it is referenced.

Use cases:
  - Simplify complex queries
  - Restrict access to sensitive columns
  - Provide a stable interface over changing schemas

Prerequisites: SQLite3 (built-in Python module)
"""

import sqlite3
import os
import tempfile


def setup_database(db_path: str) -> sqlite3.Connection:
    """Create a sample database with employees and departments tables."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE departments (
            dept_id   INTEGER PRIMARY KEY,
            dept_name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE employees (
            emp_id    INTEGER PRIMARY KEY,
            name      TEXT NOT NULL,
            dept_id   INTEGER NOT NULL,
            salary    REAL NOT NULL,
            hire_date TEXT NOT NULL,
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        )
    """)

    departments = [
        (1, 'Engineering'),
        (2, 'Marketing'),
        (3, 'Sales'),
        (4, 'Finance'),
    ]
    cur.executemany("INSERT INTO departments VALUES (?, ?)", departments)

    employees = [
        (1, 'Alice',   1, 95000, '2020-03-15'),
        (2, 'Bob',     1, 88000, '2019-07-01'),
        (3, 'Charlie', 2, 72000, '2021-01-10'),
        (4, 'Diana',   2, 68000, '2022-05-20'),
        (5, 'Eve',     3, 78000, '2018-11-05'),
        (6, 'Frank',   3, 82000, '2020-09-12'),
        (7, 'Grace',   4, 91000, '2017-04-22'),
        (8, 'Hank',    4, 85000, '2021-08-30'),
        (9, 'Ivy',     1, 102000, '2016-06-18'),
        (10, 'Jack',   2, 65000, '2023-02-14'),
    ]
    cur.executemany(
        "INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees
    )

    conn.commit()
    return conn


def create_views(conn: sqlite3.Connection) -> None:
    """Create multiple views demonstrating different patterns."""
    cur = conn.cursor()

    # View 1: Basic view — join employees with departments
    cur.execute("""
        CREATE VIEW IF NOT EXISTS v_employee_details AS
        SELECT
            e.emp_id,
            e.name       AS employee_name,
            d.dept_name  AS department,
            e.salary,
            e.hire_date
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
    """)

    # View 2: Aggregated view — department-level summary
    cur.execute("""
        CREATE VIEW IF NOT EXISTS v_dept_summary AS
        SELECT
            d.dept_name,
            COUNT(e.emp_id)   AS headcount,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            MIN(e.salary)     AS min_salary,
            MAX(e.salary)     AS max_salary
        FROM departments d
        LEFT JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_id, d.dept_name
    """)

    # View 3: Filtered view — high earners only
    cur.execute("""
        CREATE VIEW IF NOT EXISTS v_high_earners AS
        SELECT
            e.emp_id,
            e.name       AS employee_name,
            d.dept_name  AS department,
            e.salary,
            e.hire_date
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE e.salary >= 85000
    """)

    # View 4: Computed column view — tenure in years
    cur.execute("""
        CREATE VIEW IF NOT EXISTS v_tenure AS
        SELECT
            e.emp_id,
            e.name       AS employee_name,
            d.dept_name  AS department,
            e.hire_date,
            ROUND(
                (julianday('now') - julianday(e.hire_date)) / 365.25,
                1
            ) AS years_of_service
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
    """)

    conn.commit()


def query_views(conn: sqlite3.Connection) -> None:
    """Demonstrate querying each view and printing results."""
    cur = conn.cursor()

    print("=" * 70)
    print("VIEW 1: v_employee_details — Full employee-department join")
    print("=" * 70)
    cur.execute("SELECT * FROM v_employee_details ORDER BY emp_id")
    rows = cur.fetchall()
    header = f"{'ID':<4} {'Name':<10} {'Department':<14} {'Salary':>10} {'Hire Date':<12}"
    print(header)
    print("-" * 70)
    for r in rows:
        print(f"{r['emp_id']:<4} {r['employee_name']:<10} {r['department']:<14} {r['salary']:>10,.0f} {r['hire_date']:<12}")
    print(f"\nTotal rows: {len(rows)}\n")

    print("=" * 70)
    print("VIEW 2: v_dept_summary — Department-level aggregation")
    print("=" * 70)
    cur.execute("SELECT * FROM v_dept_summary ORDER BY avg_salary DESC")
    rows = cur.fetchall()
    header = f"{'Department':<14} {'Headcount':>9} {'Avg Salary':>12} {'Min Salary':>12} {'Max Salary':>12}"
    print(header)
    print("-" * 70)
    for r in rows:
        print(f"{r['dept_name']:<14} {r['headcount']:>9} {r['avg_salary']:>12,.2f} {r['min_salary']:>12,.0f} {r['max_salary']:>12,.0f}")
    print()

    print("=" * 70)
    print("VIEW 3: v_high_earners — Employees earning >= $85,000")
    print("=" * 70)
    cur.execute("SELECT * FROM v_high_earners ORDER BY salary DESC")
    rows = cur.fetchall()
    header = f"{'ID':<4} {'Name':<10} {'Department':<14} {'Salary':>10} {'Hire Date':<12}"
    print(header)
    print("-" * 70)
    for r in rows:
        print(f"{r['emp_id']:<4} {r['employee_name']:<10} {r['department']:<14} {r['salary']:>10,.0f} {r['hire_date']:<12}")
    print(f"\nTotal high earners: {len(rows)}\n")

    print("=" * 70)
    print("VIEW 4: v_tenure — Employees with computed tenure")
    print("=" * 70)
    cur.execute("SELECT * FROM v_tenure ORDER BY years_of_service DESC")
    rows = cur.fetchall()
    header = f"{'ID':<4} {'Name':<10} {'Department':<14} {'Hire Date':<12} {'Years':>6}"
    print(header)
    print("-" * 70)
    for r in rows:
        print(f"{r['emp_id']:<4} {r['employee_name']:<10} {r['department']:<14} {r['hire_date']:<12} {r['years_of_service']:>6}")
    print()


def demonstrate_view_management(conn: sqlite3.Connection) -> None:
    """Show how to list, drop, and recreate views."""
    cur = conn.cursor()

    print("=" * 70)
    print("VIEW MANAGEMENT: Listing all views in the database")
    print("=" * 70)
    cur.execute("""
        SELECT name, sql
        FROM sqlite_master
        WHERE type = 'view'
        ORDER BY name
    """)
    views = cur.fetchall()
    for v in views:
        print(f"\n  View: {v['name']}")
        print(f"  SQL:  {v['sql'][:100]}..." if len(v['sql']) > 100 else f"  SQL:  {v['sql']}")
    print(f"\nTotal views: {len(views)}")

    # Drop and recreate a view
    print("\n" + "=" * 70)
    print("Dropping and recreating v_high_earners with a new threshold")
    print("=" * 70)
    cur.execute("DROP VIEW IF EXISTS v_high_earners")
    cur.execute("""
        CREATE VIEW v_high_earners AS
        SELECT
            e.emp_id,
            e.name       AS employee_name,
            d.dept_name  AS department,
            e.salary,
            e.hire_date
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE e.salary >= 90000
    """)
    conn.commit()

    cur.execute("SELECT * FROM v_high_earners ORDER BY salary DESC")
    rows = cur.fetchall()
    print(f"\nHigh earners (>= $90,000): {len(rows)} employees")
    for r in rows:
        print(f"  {r['employee_name']:<10} {r['department']:<14} ${r['salary']:>10,.0f}")


def run_tests(conn: sqlite3.Connection) -> bool:
    """Run assertions to verify view correctness."""
    cur = conn.cursor()
    all_passed = True

    # Test 1: v_employee_details returns all 10 employees
    cur.execute("SELECT COUNT(*) AS cnt FROM v_employee_details")
    count = cur.fetchone()['cnt']
    assert count == 10, f"Expected 10 rows in v_employee_details, got {count}"
    print("  [PASS] v_employee_details returns 10 rows")

    # Test 2: v_dept_summary has 4 departments
    cur.execute("SELECT COUNT(*) AS cnt FROM v_dept_summary")
    count = cur.fetchone()['cnt']
    assert count == 4, f"Expected 4 rows in v_dept_summary, got {count}"
    print("  [PASS] v_dept_summary returns 4 departments")

    # Test 3: Engineering headcount is 3
    cur.execute("SELECT headcount FROM v_dept_summary WHERE dept_name = 'Engineering'")
    hc = cur.fetchone()['headcount']
    assert hc == 3, f"Expected Engineering headcount 3, got {hc}"
    print("  [PASS] Engineering headcount = 3")

    # Test 4: v_high_earners (>= 85000) has 5 employees
    cur.execute("SELECT COUNT(*) AS cnt FROM v_high_earners")
    count = cur.fetchone()['cnt']
    assert count == 5, f"Expected 5 high earners, got {count}"
    print("  [PASS] v_high_earners returns 5 employees")

    # Test 5: v_tenure has computed years_of_service for all
    cur.execute("SELECT COUNT(*) AS cnt FROM v_tenure WHERE years_of_service IS NOT NULL")
    count = cur.fetchone()['cnt']
    assert count == 10, f"Expected 10 rows with tenure, got {count}"
    print("  [PASS] v_tenure has computed tenure for all 10 employees")

    # Test 6: Ivy has the highest salary in v_high_earners
    cur.execute("SELECT employee_name FROM v_high_earners ORDER BY salary DESC LIMIT 1")
    top = cur.fetchone()['employee_name']
    assert top == 'Ivy', f"Expected Ivy as top earner, got {top}"
    print("  [PASS] Ivy is the top earner")

    # Test 7: Views appear in sqlite_master
    cur.execute("SELECT COUNT(*) AS cnt FROM sqlite_master WHERE type = 'view'")
    count = cur.fetchone()['cnt']
    assert count == 4, f"Expected 4 views in sqlite_master, got {count}"
    print("  [PASS] 4 views registered in sqlite_master")

    # Test 8: View reflects underlying data changes
    cur.execute("UPDATE employees SET salary = 110000 WHERE emp_id = 1")
    conn.commit()
    cur.execute("SELECT salary FROM v_employee_details WHERE emp_id = 1")
    new_sal = cur.fetchone()['salary']
    assert new_sal == 110000, f"Expected 110000 after update, got {new_sal}"
    print("  [PASS] View reflects underlying data changes")

    # Restore
    cur.execute("UPDATE employees SET salary = 95000 WHERE emp_id = 1")
    conn.commit()

    print(f"\n  All {8} tests passed!")
    return all_passed


def main():
    """Main entry point — runs the full exercise."""
    print("SQL Q8: Create a View")
    print("=" * 70)

    # Use a temp file so the database persists during the session
    tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    db_path = tmp.name
    tmp.close()

    try:
        conn = setup_database(db_path)
        print("\n[1/4] Database created with 4 departments and 10 employees.\n")

        create_views(conn)
        print("[2/4] Four views created successfully.\n")

        query_views(conn)

        demonstrate_view_management(conn)

        print("\n" + "=" * 70)
        print("RUNNING TESTS")
        print("=" * 70)
        run_tests(conn)

        conn.close()
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)

    print("\n" + "=" * 70)
    print("EXERCISE COMPLETE")
    print("=" * 70)
    print("""
Key takeaways:
  1. CREATE VIEW defines a virtual table from a SELECT query.
  2. Views do NOT store data — they execute the query on each access.
  3. Views simplify complex joins and aggregations.
  4. Views can restrict column access (security benefit).
  5. DROP VIEW removes the definition; data in base tables is unaffected.
  6. Views reflect real-time changes in underlying tables.
  7. Use IF NOT EXISTS to avoid errors on repeated creation.
  8. sqlite_master catalogs all views with their SQL definitions.
""")


if __name__ == '__main__':
    main()
