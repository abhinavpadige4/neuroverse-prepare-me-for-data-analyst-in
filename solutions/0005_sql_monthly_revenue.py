"""
Day 3 - SQL Aggregation & Window Functions
Problem 5: Monthly Revenue
===========================
Description:
    Write a SQL query to compute total revenue per month from
    the `orders` table.

Assumed schema:
    orders (
        order_id    INT PRIMARY KEY,
        customer_id INT,
        status      VARCHAR,
        order_date  DATE,
        amount      DECIMAL(10,2)
    )

Solution:
    Extract year-month from order_date, GROUP BY it, SUM(amount).

Complexity:
    Time:  O(n)   -- single pass aggregation
    Space: O(m)   -- m = number of distinct months

SQL (Postgres / MySQL):
    SELECT DATE_TRUNC('month', order_date) AS month,
           SUM(amount)                     AS total_revenue,
           COUNT(*)                        AS order_count
    FROM   orders
    WHERE  status <> 'cancelled'
    GROUP  BY DATE_TRUNC('month', order_date)
    ORDER  BY month;

SQL (SQL Server):
    SELECT DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1) AS month,
           SUM(amount) AS total_revenue
    FROM   orders
    GROUP  BY YEAR(order_date), MONTH(order_date)
    ORDER  BY month;

Notes:
    - DATE_TRUNC('month', ...) truncates to the first day of the month.
    - Filter out cancelled orders before summing.
"""

import pandas as pd


def monthly_revenue(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Return total revenue per month.

    Args:
        orders_df: DataFrame with order_date (datetime) and amount.

    Returns:
        DataFrame with columns [month, total_revenue, order_count],
        sorted ascending by month.
    """
    df = orders_df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    result = (
        df.groupby("month", as_index=False)
        .agg(total_revenue=("amount", "sum"),
             order_count=("order_id", "count"))
        .sort_values("month")
    )
    return result


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5, 6],
            "customer_id": [1, 2, 1, 3, 2, 4],
            "status": ["delivered", "delivered", "cancelled",
                       "delivered", "delivered", "delivered"],
            "order_date": pd.to_datetime(
                ["2026-01-05", "2026-01-20", "2026-02-01",
                 "2026-02-15", "2026-03-10", "2026-03-25"]
            ),
            "amount": [100, 200, 300, 400, 500, 600],
        }
    )
    print(monthly_revenue(sample))
