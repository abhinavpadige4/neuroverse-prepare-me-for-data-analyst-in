"""
Day 6 - SQL Window Functions & Advanced Analytics
Problem 11: Running Total & Rank with Window Functions
========================================================
Description:
    Write a SQL query that computes:
    - Running total revenue per customer over time
    - Rank of each customer by total revenue
    - Month-over-month revenue growth

Assumed schema:
    orders (
        order_id    INT PRIMARY KEY,
        customer_id INT,
        status      VARCHAR,
        order_date  DATE,
        amount      DECIMAL(10,2)
    )

Solution:
    Use SUM() OVER (PARTITION BY ... ORDER BY ...) for running totals,
    RANK() for customer ranking, and LAG() for month-over-month growth.

Complexity:
    Time:  O(n log n)  -- sort by partition + order
    Space: O(n)

SQL:
    WITH monthly AS (
        SELECT customer_id,
               DATE_TRUNC('month', order_date) AS month,
               SUM(amount) AS monthly_revenue
        FROM   orders
        WHERE  status <> 'cancelled'
        GROUP  BY customer_id, DATE_TRUNC('month', order_date)
    ),
    ranked AS (
        SELECT customer_id,
               month,
               monthly_revenue,
               SUM(monthly_revenue) OVER (
                   PARTITION BY customer_id
                   ORDER BY month
               ) AS running_total,
               LAG(monthly_revenue) OVER (
                   PARTITION BY customer_id
                   ORDER BY month
               ) AS prev_month_revenue
        FROM   monthly
    )
    SELECT customer_id,
           month,
           monthly_revenue,
           running_total,
           prev_month_revenue,
           CASE
               WHEN prev_month_revenue IS NULL OR prev_month_revenue = 0 THEN NULL
               ELSE (monthly_revenue - prev_month_revenue) / prev_month_revenue
           END AS mom_growth
    FROM   ranked
    ORDER  BY customer_id, month;

Notes:
    - PARTITION BY restarts the window per customer.
    - LAG() returns the previous row's value within the partition.
    - Handle divide-by-zero for growth calculation.
"""

import pandas as pd


def running_total_and_growth(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Compute running total revenue and month-over-month growth per customer.

    Args:
        orders_df: DataFrame with order_id, customer_id, amount,
            order_date, status.

    Returns:
        DataFrame with columns
            [customer_id, month, monthly_revenue, running_total,
             prev_month_revenue, mom_growth].
    """
    df = orders_df[orders_df["status"] != "cancelled"].copy()
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()

    monthly = (
        df.groupby(["customer_id", "month"], as_index=False)
        .agg(monthly_revenue=("amount", "sum"))
        .sort_values(["customer_id", "month"])
    )

    monthly["running_total"] = monthly.groupby("customer_id")[
        "monthly_revenue"
    ].cumsum()
    monthly["prev_month_revenue"] = monthly.groupby("customer_id")[
        "monthly_revenue"
    ].shift(1)
    monthly["mom_growth"] = (
        (monthly["monthly_revenue"] - monthly["prev_month_revenue"])
        / monthly["prev_month_revenue"]
    )
    return monthly


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5, 6],
            "customer_id": [1, 1, 1, 2, 2, 2],
            "status": ["delivered"] * 6,
            "order_date": pd.to_datetime(
                ["2026-01-05", "2026-02-10", "2026-03-15",
                 "2026-01-20", "2026-02-25", "2026-03-30"]
            ),
            "amount": [100, 200, 300, 50, 100, 150],
        }
    )
    print(running_total_and_growth(sample))
