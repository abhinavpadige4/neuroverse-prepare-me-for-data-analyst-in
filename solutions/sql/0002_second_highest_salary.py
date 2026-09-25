"""
SQL Q2: Second Highest Salary
==============================
Problem:
    Write a SQL query to find the second highest salary from the Employee table.

Table Schema:
    CREATE TABLE Employee (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        salary DECIMAL(10,2)
    );

Sample Data:
    +----+--------+--------+
    | id | name   | salary |
    +----+--------+--------+
    |  1 | Alice  | 90000  |
    |  2 | Bob    | 85000  |
    |  3 | Charlie| 95000  |
    |  4 | Diana  | 85000  |
    |  5 | Eve    | 70000  |
    +----+--------+--------+

Expected Output:
    SecondHighestSalary
    -------------------
    85000

Approaches Covered:
    1. Subquery with MAX (classic)
    2. LIMIT/OFFSET
    3. DENSE_RANK window function
    4. Correlated subquery
"""

import sqlite3
import os


def setup_database(db_path: str = ":memory:") -> sqlite3.Connection:
    """Create and populate the Employee table with sample data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employee (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)

    sample_data = [
        (1, "Alice", 90000.00),
        (2, "Bob", 85000.00),
        (3, "Charlie", 95000.00),
        (4, "Diana", 85000.00),
        (5, "Eve", 70000.00),
        (6, "Frank", 95000.00),
        (7, "Grace", 60000.00),
    ]

    cursor.executemany(
        "INSERT INTO Employee (id, name, salary) VALUES (?, ?, ?)",
        sample_data,
    )
    conn.commit()
    return conn


def approach_1_subquery_max(conn: sqlite3.Connection) -> float | None:
    """
    Approach 1: Subquery with MAX
    
    Logic: The second highest salary is the maximum salary that is
    less than the overall maximum salary.
    
    SQL:
        SELECT MAX(salary) AS SecondHighestSalary
        FROM Employee
        WHERE salary < (SELECT MAX(salary) FROM Employee);
    
    Pros: Simple, intuitive, works on all SQL dialects.
    Cons: Two table scans; returns NULL if fewer than 2 distinct salaries.
    """
    query = """
        SELECT MAX(salary) AS SecondHighestSalary
        FROM Employee
        WHERE salary < (SELECT MAX(salary) FROM Employee)
    """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else None


def approach_2_limit_offset(conn: sqlite3.Connection) -> float | None:
    """
    Approach 2: LIMIT / OFFSET
    
    Logic: Order salaries descending, skip the first (highest),
    and take the next one.
    
    SQL:
        SELECT DISTINCT salary AS SecondHighestSalary
        FROM Employee
        ORDER BY salary DESC
        LIMIT 1 OFFSET 1;
    
    Pros: Very readable; efficient with indexes.
    Cons: DISTINCT needed to handle ties; dialect-specific syntax.
    """
    query = """
        SELECT DISTINCT salary AS SecondHighestSalary
        FROM Employee
        ORDER BY salary DESC
        LIMIT 1 OFFSET 1
    """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else None


def approach_3_dense_rank(conn: sqlite3.Connection) -> float | None:
    """
    Approach 3: DENSE_RANK Window Function
    
    Logic: Assign dense ranks to distinct salaries in descending order.
    The second highest salary has rank = 2.
    
    SQL:
        SELECT salary AS SecondHighestSalary
        FROM (
            SELECT DISTINCT salary,
                   DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
            FROM Employee
        ) ranked
        WHERE rnk = 2;
    
    Pros: Handles ties correctly; extensible to Nth highest.
    Cons: Requires window function support (SQL Server 2005+, MySQL 8+, PostgreSQL 9.0+).
    """
    query = """
        SELECT salary AS SecondHighestSalary
        FROM (
            SELECT DISTINCT salary,
                   DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
            FROM Employee
        ) ranked
        WHERE rnk = 2
    """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else None


def approach_4_correlated_subquery(conn: sqlite3.Connection) -> float | None:
    """
    Approach 4: Correlated Subquery
    
    Logic: Find the maximum salary where exactly one distinct salary
    is greater than it.
    
    SQL:
        SELECT salary AS SecondHighestSalary
        FROM Employee e1
        WHERE (SELECT COUNT(DISTINCT salary) FROM Employee e2 WHERE e2.salary > e1.salary) = 1
        GROUP BY salary
        LIMIT 1;
    
    Pros: Works without window functions; generalizable.
    Cons: Correlated subquery can be slow on large tables.
    """
    query = """
        SELECT salary AS SecondHighestSalary
        FROM Employee e1
        WHERE (SELECT COUNT(DISTINCT salary) FROM Employee e2 WHERE e2.salary > e1.salary) = 1
        GROUP BY salary
        LIMIT 1
    """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else None


def run_all_approaches():
    """Execute all approaches and verify they produce consistent results."""
    print("=" * 60)
    print("SQL Q2: Second Highest Salary - All Approaches")
    print("=" * 60)

    conn = setup_database()

    # Display sample data
    print("\nSample Data:")
    print("-" * 40)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, salary FROM Employee ORDER BY id")
    rows = cursor.fetchall()
    print(f"{'ID':<5} {'Name':<12} {'Salary':>10}")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<12} {row[2]:>10,.2f}")

    # Run each approach
    approaches = [
        ("Approach 1: Subquery with MAX", approach_1_subquery_max),
        ("Approach 2: LIMIT / OFFSET", approach_2_limit_offset),
        ("Approach 3: DENSE_RANK Window", approach_3_dense_rank),
        ("Approach 4: Correlated Subquery", approach_4_correlated_subquery),
    ]

    print("\nResults:")
    print("-" * 40)
    results = []
    for name, func in approaches:
        result = func(conn)
        results.append(result)
        print(f"  {name}: {result:,.2f}" if result else f"  {name}: NULL")

    # Verify consistency
    print("\nVerification:")
    print("-" * 40)
    unique_results = set(r for r in results if r is not None)
    if len(unique_results) == 1:
        print(f"  ✓ All approaches agree: {unique_results.pop():,.2f}")
    else:
        print(f"  ✗ Mismatch detected! Results: {results}")

    # Edge case: only one distinct salary
    print("\nEdge Case - Single distinct salary:")
    print("-" * 40)
    conn2 = sqlite3.connect(":memory:")
    cursor2 = conn2.cursor()
    cursor2.execute("""
        CREATE TABLE Employee (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)
    cursor2.executemany(
        "INSERT INTO Employee VALUES (?, ?, ?)",
        [(1, "Solo", 50000.00), (2, "Clone", 50000.00)],
    )
    conn2.commit()
    edge_result = approach_1_subquery_max(conn2)
    print(f"  Result: {edge_result} (expected: NULL)")
    print(f"  {'✓' if edge_result is None else '✗'} Correctly returns NULL")

    conn.close()
    conn2.close()

    return results


def get_sql_queries() -> dict[str, str]:
    """Return all SQL query strings for reference/copy-paste."""
    return {
        "approach_1_subquery_max": """
            SELECT MAX(salary) AS SecondHighestSalary
            FROM Employee
            WHERE salary < (SELECT MAX(salary) FROM Employee);
        """.strip(),
        "approach_2_limit_offset": """
            SELECT DISTINCT salary AS SecondHighestSalary
            FROM Employee
            ORDER BY salary DESC
            LIMIT 1 OFFSET 1;
        """.strip(),
        "approach_3_dense_rank": """
            SELECT salary AS SecondHighestSalary
            FROM (
                SELECT DISTINCT salary,
                       DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
                FROM Employee
            ) ranked
            WHERE rnk = 2;
        """.strip(),
        "approach_4_correlated_subquery": """
            SELECT salary AS SecondHighestSalary
            FROM Employee e1
            WHERE (SELECT COUNT(DISTINCT salary) FROM Employee e2 WHERE e2.salary > e1.salary) = 1
            GROUP BY salary
            LIMIT 1;
        """.strip(),
    }


if __name__ == "__main__":
    run_all_approaches()

    print("\n" + "=" * 60)
    print("SQL Queries for Reference")
    print("=" * 60)
    queries = get_sql_queries()
    for name, sql in queries.items():
        print(f"\n-- {name}")
        print(sql)
