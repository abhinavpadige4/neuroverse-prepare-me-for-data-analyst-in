"""
SQL Q7: Window Function - Moving Average

Problem:
Given a table of daily sales, compute a 3-day moving average of sales
using SQL window functions. The moving average for each day should be
the average of that day's sales and the two preceding days.

Expected output columns: date, sales, moving_avg_3d

This solution uses SQLite (via Python's sqlite3) to demonstrate the
SQL window function approach, then validates results with assertions.
"""

import sqlite3
import os
import tempfile
from datetime import date, timedelta


def setup_database(db_path: str) -> None:
    """Create and populate the sales table with sample data."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS daily_sales")
    cur.execute("""
        CREATE TABLE daily_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date DATE NOT NULL,
            sales REAL NOT NULL
        )
    """)

    # Sample data: 10 days of sales
    base_date = date(2024, 1, 1)
    sales_data = [
        (base_date + timedelta(days=i), sales)
        for i, sales in enumerate([100, 150, 200, 120, 180, 250, 300, 220, 280, 350])
    ]

    cur.executemany(
        "INSERT INTO daily_sales (sale_date, sales) VALUES (?, ?)",
        sales_data,
    )
    conn.commit()
    conn.close()


def compute_moving_average(db_path: str) -> list:
    """
    Compute 3-day moving average using SQL window function.

    Uses ROWS BETWEEN 2 PRECEDING AND CURRENT ROW to define
    the window frame for the moving average calculation.

    Returns:
        List of tuples: (sale_date, sales, moving_avg_3d)
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = """
        SELECT
            sale_date,
            sales,
            ROUND(
                AVG(sales) OVER (
                    ORDER BY sale_date
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ), 2
            ) AS moving_avg_3d
        FROM daily_sales
        ORDER BY sale_date
    """

    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results


def compute_moving_average_with_partition(db_path: str) -> list:
    """
    Extended version: Moving average partitioned by region.

    Demonstrates PARTITION BY with window functions for
    per-group moving averages.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create a region table for extended example
    cur.execute("DROP TABLE IF EXISTS regional_sales")
    cur.execute("""
        CREATE TABLE regional_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date DATE NOT NULL,
            region TEXT NOT NULL,
            sales REAL NOT NULL
        )
    """)

    base_date = date(2024, 1, 1)
    regional_data = [
        (base_date + timedelta(days=i), "North", sales_n),
        (base_date + timedelta(days=i), "South", sales_s),
    ]
    sales_north = [100, 150, 200, 120, 180]
    sales_south = [80, 120, 160, 200, 240]
    rows = []
    for i in range(5):
        rows.append((base_date + timedelta(days=i), "North", sales_north[i]))
        rows.append((base_date + timedelta(days=i), "South", sales_south[i]))

    cur.executemany(
        "INSERT INTO regional_sales (sale_date, region, sales) VALUES (?, ?, ?)",
        rows,
    )
    conn.commit()

    query = """
        SELECT
            sale_date,
            region,
            sales,
            ROUND(
                AVG(sales) OVER (
                    PARTITION BY region
                    ORDER BY sale_date
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ), 2
            ) AS moving_avg_3d
        FROM regional_sales
        ORDER BY region, sale_date
    """

    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results


def compute_moving_average_with_rank(db_path: str) -> list:
    """
    Bonus: Combine moving average with RANK() to identify
    days where sales exceeded the moving average.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = """
        WITH avg_calc AS (
            SELECT
                sale_date,
                sales,
                AVG(sales) OVER (
                    ORDER BY sale_date
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ) AS moving_avg_3d
            FROM daily_sales
        )
        SELECT
            sale_date,
            sales,
            ROUND(moving_avg_3d, 2) AS moving_avg_3d,
            CASE
                WHEN sales > moving_avg_3d THEN 'Above Avg'
                WHEN sales < moving_avg_3d THEN 'Below Avg'
                ELSE 'At Avg'
            END AS performance,
            RANK() OVER (ORDER BY sales DESC) AS sales_rank
        FROM avg_calc
        ORDER BY sale_date
    """

    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results


def run_tests() -> None:
    """Run comprehensive tests on the moving average calculations."""
    print("=" * 60)
    print("Running Tests for SQL Q7: Window Moving Average")
    print("=" * 60)

    # Use a temporary database file
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = tmp.name
    tmp.close()

    try:
        # Setup
        setup_database(db_path)

        # Test 1: Basic moving average
        print("\n[Test 1] Basic 3-day moving average...")
        results = compute_moving_average(db_path)

        assert len(results) == 10, f"Expected 10 rows, got {len(results)}"

        # Day 1: only 1 day of data, avg = 100
        assert results[0][2] == 100.0, f"Day 1 avg: expected 100.0, got {results[0][2]}"

        # Day 2: avg of (100, 150) = 125
        assert results[1][2] == 125.0, f"Day 2 avg: expected 125.0, got {results[1][2]}"

        # Day 3: avg of (100, 150, 200) = 150
        assert results[2][2] == 150.0, f"Day 3 avg: expected 150.0, got {results[2][2]}"

        # Day 4: avg of (150, 200, 120) = 156.67
        assert results[3][2] == 156.67, f"Day 4 avg: expected 156.67, got {results[3][2]}"

        # Day 5: avg of (200, 120, 180) = 166.67
        assert results[4][2] == 166.67, f"Day 5 avg: expected 166.67, got {results[4][2]}"

        # Day 10: avg of (280, 350) wait no - (220, 280, 350) = 283.33
        assert results[9][2] == 283.33, f"Day 10 avg: expected 283.33, got {results[9][2]}"

        print("  PASSED: All basic moving average assertions passed.")

        # Test 2: Partitioned moving average
        print("\n[Test 2] Partitioned moving average by region...")
        partitioned = compute_moving_average_with_partition(db_path)

        assert len(partitioned) == 10, f"Expected 10 rows, got {len(partitioned)}"

        # North region day 1: avg = 100
        north_day1 = [r for r in partitioned if r[1] == "North" and r[0] == str(date(2024, 1, 1))]
        assert len(north_day1) == 1
        assert north_day1[0][3] == 100.0, f"North Day 1: expected 100.0, got {north_day1[0][3]}"

        # South region day 1: avg = 80
        south_day1 = [r for r in partitioned if r[1] == "South" and r[0] == str(date(2024, 1, 1))]
        assert len(south_day1) == 1
        assert south_day1[0][3] == 80.0, f"South Day 1: expected 80.0, got {south_day1[0][3]}"

        # North day 3: avg of (100, 150, 200) = 150
        north_day3 = [r for r in partitioned if r[1] == "North" and r[0] == str(date(2024, 1, 3))]
        assert north_day3[0][3] == 150.0, f"North Day 3: expected 150.0, got {north_day3[0][3]}"

        print("  PASSED: All partitioned moving average assertions passed.")

        # Test 3: Moving average with rank and performance
        print("\n[Test 3] Moving average with RANK and performance label...")
        ranked = compute_moving_average_with_rank(db_path)

        assert len(ranked) == 10, f"Expected 10 rows, got {len(ranked)}"

        # Day 1: sales=100, avg=100, should be 'At Avg'
        assert ranked[0][3] == "At Avg", f"Day 1 perf: expected 'At Avg', got '{ranked[0][3]}'"

        # Day 2: sales=150, avg=125, should be 'Above Avg'
        assert ranked[1][3] == "Above Avg", f"Day 2 perf: expected 'Above Avg', got '{ranked[1][3]}'"

        # Day 4: sales=120, avg=156.67, should be 'Below Avg'
        assert ranked[3][3] == "Below Avg", f"Day 4 perf: expected 'Below Avg', got '{ranked[3][3]}'"

        # Rank 1 should be the highest sales day (350)
        rank1 = [r for r in ranked if r[4] == 1]
        assert len(rank1) == 1
        assert rank1[0][1] == 350, f"Rank 1 sales: expected 350, got {rank1[0][1]}"

        print("  PASSED: All rank/performance assertions passed.")

        # Test 4: Verify data integrity
        print("\n[Test 4] Data integrity checks...")
        results = compute_moving_average(db_path)

        # All moving averages should be positive
        for row in results:
            assert row[2] > 0, f"Moving avg should be positive, got {row[2]}"

        # Moving average should be between min and max of the window
        for i, row in enumerate(results):
            window = [results[j][1] for j in range(max(0, i - 2), i + 1)]
            expected_avg = round(sum(window) / len(window), 2)
            assert row[2] == expected_avg, (
                f"Row {i}: expected {expected_avg}, got {row[2]}"
            )

        print("  PASSED: All data integrity checks passed.")

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED")
        print("=" * 60)

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def print_results() -> None:
    """Print formatted results for demonstration."""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = tmp.name
    tmp.close()

    try:
        setup_database(db_path)

        print("\n" + "=" * 60)
        print("SQL Q7: 3-Day Moving Average Results")
        print("=" * 60)
        print(f"{'Date':<12} {'Sales':<10} {'Moving Avg (3d)':<18}")
        print("-" * 40)

        results = compute_moving_average(db_path)
        for row in results:
            print(f"{str(row[0]):<12} {row[1]:<10.0f} {row[2]:<18.2f}")

        print("\n" + "=" * 60)
        print("SQL Q7: Partitioned Moving Average (by Region)")
        print("=" * 60)
        print(f"{'Date':<12} {'Region':<8} {'Sales':<10} {'Moving Avg (3d)':<18}")
        print("-" * 48)

        partitioned = compute_moving_average_with_partition(db_path)
        for row in partitioned:
            print(f"{str(row[0]):<12} {row[1]:<8} {row[2]:<10.0f} {row[3]:<18.2f}")

        print("\n" + "=" * 60)
        print("SQL Q7: Moving Average with Performance & Rank")
        print("=" * 60)
        print(f"{'Date':<12} {'Sales':<8} {'Avg':<10} {'Performance':<14} {'Rank':<6}")
        print("-" * 50)

        ranked = compute_moving_average_with_rank(db_path)
        for row in ranked:
            print(f"{str(row[0]):<12} {row[1]:<8.0f} {row[2]:<10.2f} {row[3]:<14} {row[4]:<6}")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


if __name__ == "__main__":
    print("SQL Q7: Window Function - Moving Average")
    print("Solution using ROWS BETWEEN for window frame definition")
    print()

    # Print demonstration results
    print_results()

    # Run tests
    print()
    run_tests()
