"""
Problem 0002 - SQL: Count Orders Per Status
===========================================
Day 1 - SQL Fundamentals (GROUP BY, COUNT)

Problem
-------
Given an `orders` table with columns (order_id, customer_id, status, order_date, total),
write a SQL query to count the number of orders per status.

Solution
--------
    SELECT status, COUNT(*) AS order_count
    FROM orders
    GROUP BY status
    ORDER BY order_count DESC;

Notes
-----
- GROUP BY collapses rows that share the same status into a single row.
- COUNT(*) counts all rows in each group (including NULLs).
- COUNT(order_id) would skip NULL order_ids.

Complexity
----------
- Time:  O(n)  -- single pass with hash aggregation
- Space: O(k)  -- k = number of distinct statuses

Variant: include statuses with zero orders (using a reference table):
    SELECT s.status, COUNT(o.order_id) AS order_count
    FROM statuses s
    LEFT JOIN orders o ON o.status = s.status
    GROUP BY s.status;
"""

import sqlite3

def setup_demo_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS orders;
        CREATE TABLE orders (
            order_id    INTEGER PRIMARY KEY,
            customer_id INTEGER,
            status      TEXT,
            order_date  TEXT,
            total       REAL
        );
        INSERT INTO orders (customer_id, status, order_date, total) VALUES
            (1, 'completed', '2026-09-01', 120.00),
            (2, 'pending',   '2026-09-02',  45.50),
            (1, 'completed', '2026-09-03',  88.00),
            (3, 'cancelled', '2026-09-04',  30.00),
            (2, 'completed', '2026-09-05', 210.00),
            (4, 'pending',   '2026-09-06',  65.00),
            (5, 'completed', '2026-09-07',  99.99),
            (3, 'cancelled', '2026-09-08',  12.00);
        """
    )

def orders_per_status(conn: sqlite3.Connection):
    query = """
        SELECT status, COUNT(*) AS order_count
        FROM orders
        GROUP BY status
        ORDER BY order_count DESC;
    """
    return conn.execute(query).fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup_demo_db(conn)
    for row in orders_per_status(conn):
        print(row)
    conn.close()
