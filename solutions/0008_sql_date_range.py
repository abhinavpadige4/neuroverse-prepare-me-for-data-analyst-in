"""
Problem 0008 - SQL: Orders Within a Date Range
===============================================
Day 3 - Date/Time Functions

Problem
-------
Given an `orders` table with columns (order_id, customer_id, order_date, total),
write a SQL query to find all orders placed between two dates (inclusive).

Solution
--------
    SELECT order_id, customer_id, order_date, total
    FROM orders
    WHERE order_date BETWEEN '2026-09-01' AND '2026-09-30'
    ORDER BY order_date;

Notes
-----
- BETWEEN is inclusive on both ends.
- For timestamps, prefer >= and < to avoid missing rows at the boundary:
        WHERE order_date >= '2026-09-01' AND order_date < '2026-10-01'
- Use DATE(order_date) to compare only the date portion of a timestamp.

Common date functions:
    DATE(), DATETIME(), EXTRACT(YEAR FROM ...), DATE_TRUNC('month', ...)
    DATE_ADD(date, INTERVAL n DAY), DATEDIFF(end, start)

Complexity
----------
- Time:  O(log n) with an index on order_date, else O(n)
- Space: O(1)
"""

import sqlite3

def setup_demo_db(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS orders;
        CREATE TABLE orders (
            order_id    INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date  TEXT,
            total       REAL
        );
        INSERT INTO orders VALUES
            (1, 10, '2026-08-25', 50.00),
            (2, 11, '2026-09-01', 75.00),
            (3, 12, '2026-09-15', 120.00),
            (4, 13, '2026-09-30', 90.00),
            (5, 14, '2026-10-05', 60.00);
    """)

def orders_in_range(conn):
    query = """
        SELECT order_id, customer_id, order_date, total
        FROM orders
        WHERE order_date BETWEEN '2026-09-01' AND '2026-09-30'
        ORDER BY order_date;
    """
    return conn.execute(query).fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup_demo_db(conn)
    for row in orders_in_range(conn):
        print(row)
    conn.close()
