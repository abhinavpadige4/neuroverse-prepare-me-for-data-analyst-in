"""
SQL Q6: Self Join
=================
Topic: Self Join (joining a table to itself)
Difficulty: Medium

Problem:
Given an 'employees' table with columns (id, name, salary, manager_id),
find each employee's name alongside their manager's name.

Self-join is used when you need to compare rows within the same table.
Common interview scenarios:
hierarchical data (employees/managers), finding duplicates,
comparing records across time periods.

Expected Output:
+----------------+----------------+
| employee_name  | manager_name   |
+----------------+----------------+
| Alice          | Bob            |
| Charlie        | Bob            |
| Diana          | Alice          |
+----------------+----------------+
"""

import sqlite3
import os


def setup_database(db_path: str = ":memory:") -> sqlite3.Connection:
    """Create and populate the employees table for self-join practice."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL,
            manager_id INTEGER,
            FOREIGN KEY (manager_id) REFERENCES employees(id)
        )
    """)

    # Sample data: Bob is the top manager (no manager)
    employees_data = [
        (1, "Bob", 150000.00, None),
        (2, "Alice", 120000.00, 1),
        (3, "Charlie", 95000.00, 1),
        (4, "Diana", 110000.00, 2),
        (5, "Eve", 85000.00, 2),
        (6, "Frank", 90000.00, 3),
        (7, "Grace", 105000.00, 4),
    ]

    cursor.executemany(
        "INSERT INTO employees (id, name, salary, manager_id) VALUES (?, ?, ?, ?)",
        employees_data,
    )
    conn.commit()
    return conn


def solution_basic_self_join(conn: sqlite3.Connection) -> list:
    """
    Solution 1: Basic Self Join
    ---------------------------
    Find each employee's name alongside their manager's name.
    
    Key concept: Alias the same table twice with different names.
    Join condition: employees.manager_id = managers.id
    
    Returns: List of tuples (employee_name, manager_name)
    """
    cursor = conn.cursor()

    query = """
        SELECT 
            e.name AS employee_name,
            m.name AS manager_name
        FROM employees e
        INNER JOIN employees m ON e.manager_id = m.id
        ORDER BY e.name;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    return results


def solution_with_salary_comparison(conn: sqlite3.Connection) -> list:
    """
    Solution 2: Self Join with Salary Comparison
    ---------------------------------------------
    Find employees who earn more than their manager.
    
    This is a classic interview question that tests understanding of
    self-join with additional filtering conditions.
    
    Returns: List of tuples (employee_name, employee_salary, manager_name, manager_salary)
    """
    cursor = conn.cursor()

    query = """
        SELECT 
            e.name AS employee_name,
            e.salary AS employee_salary,
            m.name AS manager_name,
            m.salary AS manager_salary
        FROM employees e
        INNER JOIN employees m ON e.manager_id = m.id
        WHERE e.salary > m.salary
        ORDER BY (e.salary - m.salary) DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    return results


def solution_find_peers(conn: sqlite3.Connection) -> list:
    """
    Solution 3: Find Peers (Same Manager)
    -------------------------------------
    Find employees who share the same manager (peers).
    
    This demonstrates a self-join where two rows from the same table
    are joined on a common attribute (manager_id) but must be different rows.
    
    Returns: List of tuples (employee1_name, employee2_name, manager_name)
    """
    cursor = conn.cursor()

    query = """
        SELECT 
            e1.name AS employee1_name,
            e2.name AS employee2_name,
            m.name AS manager_name
        FROM employees e1
        INNER JOIN employees e2 ON e1.manager_id = e2.manager_id
        INNER JOIN employees m ON e1.manager_id = m.id
        WHERE e1.id < e2.id
        ORDER BY m.name, e1.name, e2.name;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    return results


def solution_hierarchy_depth(conn: sqlite3.Connection) -> list:
    """
    Solution 4: Multi-Level Hierarchy (2 levels deep)
    -------------------------------------------------
    Find employees, their managers, and their managers' managers (grand-managers).
    
    This requires two self-joins to traverse the hierarchy.
    
    Returns: List of tuples (employee_name, manager_name, grand_manager_name)
    """
    cursor = conn.cursor()

    query = """
        SELECT 
            e.name AS employee_name,
            m1.name AS manager_name,
            m2.name AS grand_manager_name
        FROM employees e
        INNER JOIN employees m1 ON e.manager_id = m1.id
        LEFT JOIN employees m2 ON m1.manager_id = m2.id
        WHERE e.manager_id IS NOT NULL
        ORDER BY e.name;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    return results


def solution_duplicate_detection(conn: sqlite3.Connection) -> list:
    """
    Solution 5: Duplicate Detection via Self Join
    ----------------------------------------------
    Find employees with the same salary (potential duplicates).
    
    Self-join pattern for finding duplicates is a common interview topic.
    
    Returns: List of tuples (employee1_name, employee2_name, salary)
    """
    cursor = conn.cursor()

    query = """
        SELECT 
            e1.name AS employee1_name,
            e2.name AS employee2_name,
            e1.salary AS salary
        FROM employees e1
        INNER JOIN employees e2 ON e1.salary = e2.salary
        WHERE e1.id < e2.id
        ORDER BY e1.salary DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    return results


def run_tests():
    """Run comprehensive tests on all self-join solutions."""
    conn = setup_database()
    all_passed = True

    # Test 1: Basic Self Join
    print("=" * 60)
    print("TEST 1: Basic Self Join - Employee with Manager")
    print("=" * 60)
    results = solution_basic_self_join(conn)
    print(f"Results ({len(results)} rows):")
    for row in results:
        print(f"  Employee: {row[0]:12s} | Manager: {row[1]}")

    # Verify: Should have 6 rows (all except Bob who has no manager)
    assert len(results) == 6, f"Expected 6 rows, got {len(results)}"
    # Verify: Alice's manager should be Bob
    alice_row = [r for r in results if r[0] == "Alice"][0]
    assert alice_row[1] == "Bob", f"Alice's manager should be Bob, got {alice_row[1]}"
    print("  ✓ PASSED\n")

    # Test 2: Salary Comparison
    print("=" * 60)
    print("TEST 2: Employees Earning More Than Manager")
    print("=" * 60)
    results = solution_with_salary_comparison(conn)
    print(f"Results ({len(results)} rows):")
    for row in results:
        print(f"  {row[0]:12s} (${row[1]:,.0f}) > {row[2]:12s} (${row[3]:,.0f})")

    # Verify: Alice ($120k) earns more than Bob ($150k)? No.
    # Diana ($110k) > Alice ($120k)? No.
    # Eve ($85k) > Alice ($120k)? No.
    # Frank ($90k) > Charlie ($95k)? No.
    # Grace ($105k) > Diana ($110k)? No.
    # Actually none earn more than their manager in this dataset.
    # Let's verify the logic is correct by checking count.
    assert len(results) == 0, f"Expected 0 rows (no one earns more than manager), got {len(results)}"
    print("  ✓ PASSED (no employees earn more than their manager)\n")

    # Test 3: Find Peers
    print("=" * 60)
    print("TEST 3: Find Peers (Same Manager)")
    print("=" * 60)
    results = solution_find_peers(conn)
    print(f"Results ({len(results)} rows):")
    for row in results:
        print(f"  {row[0]:12s} & {row[1]:12s} | Manager: {row[2]}")

    # Verify: Alice and Charlie share manager Bob
    # Eve and Diana share manager Alice
    # Frank has no peer under Charlie
    # Grace has no peer under Diana
    assert len(results) == 2, f"Expected 2 peer pairs, got {len(results)}"
    # Check Alice-Charlie pair exists
    alice_charlie = [r for r in results if r[0] == "Alice" and r[1] == "Charlie"]
    assert len(alice_charlie) == 1, "Alice and Charlie should be peers under Bob"
    print("  ✓ PASSED\n")

    # Test 4: Hierarchy Depth
    print("=" * 60)
    print("TEST 4: Multi-Level Hierarchy (2 levels)")
    print("=" * 60)
    results = solution_hierarchy_depth(conn)
    print(f"Results ({len(results)} rows):")
    for row in results:
        gm = row[2] if row[2] else "(none)"
        print(f"  {row[0]:12s} -> {row[1]:12s} -> {gm}")

    # Verify: Diana -> Alice -> Bob
    diana_row = [r for r in results if r[0] == "Diana"][0]
    assert diana_row[1] == "Alice", f"Diana's manager should be Alice, got {diana_row[1]}"
    assert diana_row[2] == "Bob", f"Diana's grand-manager should be Bob, got {diana_row[2]}"
    print("  ✓ PASSED\n")

    # Test 5: Duplicate Detection
    print("=" * 60)
    print("TEST 5: Duplicate Salary Detection")
    print("=" * 60)
    results = solution_duplicate_detection(conn)
    print(f"Results ({len(results)} rows):")
    for row in results:
        print(f"  {row[0]:12s} & {row[1]:12s} | Salary: ${row[2]:,.0f}")

    # In our dataset, all salaries are unique, so no duplicates.
    assert len(results) == 0, f"Expected 0 duplicate pairs, got {len(results)}"
    print("  ✓ PASSED (all salaries are unique)\n")

    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)

    conn.close()
    return all_passed


def print_explanations():
    """Print detailed explanations for interview preparation."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           SELF JOIN - INTERVIEW PREPARATION NOTES            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  WHAT IS A SELF JOIN?                                        ║
║  ─────────────────────                                       ║
║  A self-join joins a table to itself. You alias the table    ║
║  with different names to distinguish between the two         ║
║  instances in the FROM clause.                               ║
║                                                              ║
║  SYNTAX:                                                     ║
║  ───────                                                     ║
║  SELECT t1.col, t2.col                                       ║
║  FROM table_name t1                                          ║
║  JOIN table_name t2 ON t1.key = t2.key;                     ║
║                                                              ║
║  COMMON INTERVIEW USE CASES:                                 ║
║  ────────────────────────────                                ║
║  1. Hierarchical data (employees/managers)                   ║
║  2. Finding duplicates (same value in different rows)        ║
║  3. Comparing records across time periods                    ║
║  4. Finding gaps or sequences                                ║
║  5. Peer/group comparisons                                   ║
║                                                              ║
║  KEY TIPS:                                                   ║
║  ───────                                                     ║
║  • Always use table aliases (e1, e2 or t1, t2)              ║
║  • Use WHERE t1.id < t2.id to avoid duplicate pairs         ║
║  • Use LEFT JOIN when some rows may not have a match         ║
║  • For deep hierarchies, consider recursive CTEs instead     ║
║                                                              ║
║  PERFORMANCE NOTE:                                           ║
║  ─────────────────                                            ║
║  Self-joins can be expensive on large tables. Ensure         ║
║  indexes exist on the join columns. For very deep            ║
║  hierarchies (>3 levels), use recursive CTEs.                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    print_explanations()
    success = run_tests()
    if success:
        print("\n🎉 All self-join exercises completed successfully!")
        print("   Ready for your Data Analyst interview!")
