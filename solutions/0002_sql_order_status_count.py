"""
Day 1 - SQL Basics
Problem 2: Count Orders Per Status
===================================
Description:
    Write a SQL query to count the number of orders per status
    in the `orders` table.

Assumed schema:
    orders (
        order_id    INT PRIMARY KEY,
        customer_id INT,
        status      VARCHAR,   -- e.g. 'pending', 'shipped', 'delivered', 'cancelled'
        order_date  DATE,
        amount      DECIMAL(10,2)
    )

Solution:
    GROUP BY status and use COUNT(*) to count rows per group.

Complexity:
    Time:  O(n)   -- single pass with hash aggregation
    Space: O(k)   -- k = number of distinct statuses

SQL:
    SELECT status,
           COUNT(*) AS order_count
    FROM   orders
    GROUP  BY status
    ORDER  BY order_count DESC;

Notes:
    - COUNT(*) counts all rows including NULLs; COUNT(status)
      would skip NULL statuses.
    - ORDER BY order_count DESC puts the most common status first.
"""

import pandas as pd


def count_orders_per_status(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Return the number of orders per status.

    Args:
        orders_df: DataFrame with an 'orders' column.

    Returns:
        DataFrame with columns [status, order_count], sorted
        descending by order_count.
    """
    result = (
        orders_df.groupby("status", dropna=False)
        .size()
        .reset_index(name="order_count")
        .sort_values("order_count", ascending=False)
    )
    return result


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "order_id": list(range(1, 11)),
            "customer_id": [1, 1, 2, 2, 3, 3, 4, 5, 5, 6],
            "status": ["pending", "shipped", "delivered", "pending",
                       "cancelled", "delivered", "shipped", "pending",
                       "delivered", "cancelled"],
            "order_date": pd.date_range("2026-01-01", periods=10),
            "amount": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        }
    )
    print(count_orders_per_status(sample))
