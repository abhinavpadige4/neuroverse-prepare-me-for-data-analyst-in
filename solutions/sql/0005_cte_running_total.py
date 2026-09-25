"""
SQL Q5: CTE Running Total
=========================
Problem: Given a table of daily sales, compute a running total of sales
using a Common Table Expression (CTE). The running total should accumulate
sales from the earliest date to the current date.

Difficulty: Medium
Topic: CTEs, Window Functions, Running Totals

Interview Context:
- Running totals are extremely common in finance, sales, and analytics
- CTEs improve readability and allow recursive or multi-step computations
- Understanding window functions (SUM() OVER) is essential for data analysts
"""

import sqlite3
import os


def setup_database(db_path: str = ":memory:") -> sqlite3.Connection:
    """Create and populate a sample sales database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT NOT NULL,
            product TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    # Insert sample data
    sample_data = [
        ("2024-01-01", "Widget A", 150.00),
        ("2024-01-01", "Widget B", 200.00),
        ("2024-01-02", "Widget A", 175.00),
        ("2024-01-02", "Widget C", 300.00),
        ("2024-01-03", "Widget B", 250.00),
        ("2024-01-03", "Widget A", 125.00),
        ("2024-01-04", "Widget C", 400.00),
        ("2024-01-04", "Widget B", 180.00),
        ("2024-01-05", "Widget A", 220.00),
        ("2024-01-05", "Widget C", 350.00),
    ]

    cursor.executemany(
        "INSERT INTO daily_sales (sale_date, product, amount) VALUES (?, ?, ?)",
        sample_data
    )
    conn.commit()
    return conn


def solution_approach_1_cte_with_window_function(conn: sqlite3.Connection):
    """
    APPROACH 1: CTE with Window Function (Recommended)
    
    Uses SUM() OVER (ORDER BY ...) to compute running total directly.
    This is the most efficient and readable approach.
    """
    query = """
    WITH daily_totals AS (
        SELECT 
            sale_date,
            SUM(amount) AS daily_total
        FROM daily_sales
        GROUP BY sale_date
    )
    SELECT 
        sale_date,
        daily_total,
        SUM(daily_total) OVER (
            ORDER BY sale_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_total
    FROM daily_totals
    ORDER BY sale_date;
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def solution_approach_2_cte_with_self_join(conn: sqlite3.Connection):
    """
    APPROACH 2: CTE with Self-Join (Alternative without window functions)
    
    Uses a correlated subquery / self-join pattern to compute running total.
    Useful when window functions are not available (older SQL versions).
    """
    query = """
    WITH daily_totals AS (
        SELECT 
            sale_date,
            SUM(amount) AS daily_total
        FROM daily_sales
        GROUP BY sale_date
    )
    SELECT 
        dt1.sale_date,
        dt1.daily_total,
        (SELECT SUM(dt2.daily_total) 
         FROM daily_totals dt2 
         WHERE dt2.sale_date <= dt1.sale_date
        ) AS running_total
    FROM daily_totals dt1
    ORDER BY dt1.sale_date;
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def solution_approach_3_recursive_cte(conn: sqlite3.Connection):
    """
    APPROACH 3: Recursive CTE (Educational)
    
    Demonstrates recursive CTE pattern for running totals.
    Less efficient but shows understanding of recursive logic.
    """
    query = """
    WITH RECURSIVE daily_totals AS (
        SELECT 
            sale_date,
            SUM(amount) AS daily_total
        FROM daily_sales
        GROUP BY sale_date
    ),
    running_calc AS (
        -- Anchor: first date
        SELECT 
            sale_date,
            daily_total,
            daily_total AS running_total,
            ROW_NUMBER() OVER (ORDER BY sale_date) AS rn
        FROM daily_totals
    ),
    recursive_totals AS (
        -- Base case: first row
        SELECT sale_date, daily_total, running_total, rn
        FROM running_calc
        WHERE rn = 1
        
        UNION ALL
        
        -- Recursive case: add next day's total
        SELECT 
            rc.sale_date,
            rc.daily_total,
            rt.running_total + rc.daily_total AS running_total,
            rc.rn
        FROM running_calc rc
        INNER JOIN recursive_totals rt ON rc.rn = rt.rn + 1
    )
    SELECT sale_date, daily_total, running_total
    FROM recursive_totals
    ORDER BY sale_date;
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def solution_approach_4_per_product_running_total(conn: sqlite3.Connection):
    """
    APPROACH 4: Running Total Per Product (Advanced)
    
    Computes running total partitioned by product.
    Common interview follow-up question.
    """
    query = """
    WITH product_daily AS (
        SELECT 
            sale_date,
            product,
            SUM(amount) AS daily_amount
        FROM daily_sales
        GROUP BY sale_date, product
    )
    SELECT 
        sale_date,
        product,
        daily_amount,
        SUM(daily_amount) OVER (
            PARTITION BY product 
            ORDER BY sale_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS product_running_total
    FROM product_daily
    ORDER BY product, sale_date;
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def run_tests():
    """Run comprehensive tests to verify all approaches produce correct results."""
    print("=" * 60)
    print("SQL Q5: CTE Running Total - Test Suite")
    print("=" * 60)
    
    conn = setup_database()
    
    # Test 1: Window Function Approach
    print("\n--- Test 1: CTE with Window Function ---")
    results_1 = solution_approach_1_cte_with_window_function(conn)
    for row in results_1:
        print(f"  Date: {row[0]}, Daily: ${row[1]:.2f}, Running: ${row[2]:.2f}")
    
    # Verify expected values
    expected_totals = [650.00, 1125.00, 1500.00, 2080.00, 2650.00]
    actual_totals = [row[2] for row in results_1]
    assert actual_totals == expected_totals, f"Test 1 FAILED: {actual_totals} != {expected_totals}"
    print("  ✓ PASSED")
    
    # Test 2: Self-Join Approach
    print("\n--- Test 2: CTE with Self-Join ---")
    results_2 = solution_approach_2_cte_with_self_join(conn)
    for row in results_2:
        print(f"  Date: {row[0]}, Daily: ${row[1]:.2f}, Running: ${row[2]:.2f}")
    
    actual_totals_2 = [row[2] for row in results_2]
    assert actual_totals_2 == expected_totals, f"Test 2 FAILED: {actual_totals_2} != {expected_totals}"
    print("  ✓ PASSED")
    
    # Test 3: Recursive CTE
    print("\n--- Test 3: Recursive CTE ---")
    results_3 = solution_approach_3_recursive_cte(conn)
    for row in results_3:
        print(f"  Date: {row[0]}, Daily: ${row[1]:.2f}, Running: ${row[2]:.2f}")
    
    actual_totals_3 = [row[2] for row in results_3]
    assert actual_totals_3 == expected_totals, f"Test 3 FAILED: {actual_totals_3} != {expected_totals}"
    print("  ✓ PASSED")
    
    # Test 4: Per-Product Running Total
    print("\n--- Test 4: Per-Product Running Total ---")
    results_4 = solution_approach_4_per_product_running_total(conn)
    for row in results_4:
        print(f"  Date: {row[0]}, Product: {row[1]}, Daily: ${row[2]:.2f}, Running: ${row[3]:.2f}")
    
    # Verify Widget A running totals: 150, 325, 450, 670
    widget_a = [(row[0], row[3]) for row in results_4 if row[1] == "Widget A"]
    expected_a = [("2024-01-01", 150.0), ("2024-01-02", 325.0),
                  ("2024-01-03", 450.0), ("2024-01-05", 670.0)]
    assert widget_a == expected_a, f"Test 4 FAILED for Widget A: {widget_a} != {expected_a}"
    print("  ✓ PASSED")
    
    # Test 5: Edge case - single row
    print("\n--- Test 5: Edge Case - Single Row ---")
    conn2 = sqlite3.connect(":memory:")
    cursor2 = conn2.cursor()
    cursor2.execute("""
        CREATE TABLE daily_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT NOT NULL,
            product TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)
    cursor2.execute("INSERT INTO daily_sales VALUES (1, '2024-01-01', 'X', 100.0)")
    conn2.commit()
    
    results_5 = solution_approach_1_cte_with_window_function(conn2)
    assert results_5[0][2] == 100.0, f"Test 5 FAILED: {results_5}"
    print(f"  Single row running total: ${results_5[0][2]:.2f}")
    print("  ✓ PASSED")
    
    # Test 6: Edge case - zero amounts
    print("\n--- Test 6: Edge Case - Zero Amounts ---")
    conn3 = sqlite3.connect(":memory:")
    cursor3 = conn3.cursor()
    cursor3.execute("""
        CREATE TABLE daily_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT NOT NULL,
            product TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)
    cursor3.executemany(
        "INSERT INTO daily_sales (sale_date, product, amount) VALUES (?, ?, ?)",
        [("2024-01-01", "A", 0.0), ("2024-01-02", "A", 0.0), ("2024-01-03", "A", 50.0)]
    )
    conn3.commit()
    
    results_6 = solution_approach_1_cte_with_window_function(conn3)
    expected_zero = [0.0, 0.0, 50.0]
    actual_zero = [row[2] for row in results_6]
    assert actual_zero == expected_zero, f"Test 6 FAILED: {actual_zero} != {expected_zero}"
    print(f"  Running totals with zeros: {actual_zero}")
    print("  ✓ PASSED")
    
    # Cleanup
    conn.close()
    conn2.close()
    conn3.close()
    
    print("\n" + "=" * 60)
    print("ALL 6 TESTS PASSED ✓")
    print("=" * 60)


def print_interview_tips():
    """Print key interview tips for this problem."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║              INTERVIEW TIPS - CTE Running Total              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ 1. ALWAYS start with the window function approach:           ║
║    SUM() OVER (ORDER BY date)                                ║
║                                                              ║
║ 2. Know the ROWS BETWEEN syntax:                             ║
║    - UNBOUNDED PRECEDING AND CURRENT ROW = running total     ║
║    - N PRECEDING AND CURRENT ROW = N-day moving total        ║
║                                                              ║
║ 3. Common follow-ups:                                        ║
║    - Running total per group (PARTITION BY)                  ║
║    - Moving average (AVG() OVER with N rows)                 ║
║    - Rank/Percentile with running totals                     ║
║                                                              ║
║ 4. Performance: Window functions are O(n) vs self-join O(n²)║
║                                                              ║
║ 5. Always ORDER BY the date column for correct accumulation  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    print_interview_tips()
    run_tests()
