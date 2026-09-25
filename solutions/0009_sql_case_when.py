"""
Problem 0009 - SQL: Categorize Orders with CASE WHEN
=====================================================
Day 3 - CASE WHEN & Conditional Logic

Problem
-------
Given an `orders` table with columns (order_id, total), categorize each order
as 'small', 'medium', or 'large' based on total amount.

Solution
--------
    SELECT order_id,
           total,
           CASE
               WHEN total < 50  THEN 'small'
               WHEN total < 200 THEN 'medium'
               ELSE 'large'
           END AS order_size
    FROM orders
    ORDER BY total DESC;

Notes
-----
- CASE WHEN evaluates top-down; the first matching branch wins.
- CASE can be used in SELECT, WHERE, ORDER BY, and GROUP BY.
- Useful for bucketing, labeling, and pivoting.

Complexity
----------
- Time:  O(n)
- Space: O(1)
"""

import sqlite3

def setup_demo_db(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS orders;
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            total    REAL
        );
        INSERT INTO orders VALUES
            (1, 25.00), (2, 75.00), (3, 150.00),
            (4, 250.00), (5, 400.00), (6, 10.00);
    """)

def categorize_orders(conn):
    query = """
        SELECT order_id,
               total,
               CASE
                   WHEN total < 50  THEN 'small'
                   WHEN total < 200 THEN 'medium'
                   ELSE 'large'
               END AS order_size
        FROM orders
        ORDER BY total DESC;
    """
    return conn.execute(query).fetchall()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup_demo_db(conn)
    for row in categorize_orders(conn):
        print(row)
    conn.close()
