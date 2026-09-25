"""
Day 3 - SQL Aggregation & Window Functions
Problem 6: Top 5 Customers by Revenue
=======================================
Description:
    Write a SQL query to find the top 5 customers by total revenue.

Assumed schema:
    orders (
        order_id    INT PRIMARY KEY,
        customer_id INT,
        status      VARCHAR,
        order_date  DATE,
        amount      DECIMAL(10,2)
    )
    customers (
        customer_id INT PRIMARY KEY,
        name        VARCHAR,
        email       VARCHAR
    )

Solution:
    Aggregate revenue per customer, join to customers for names,
    ORDER BY total_revenue DESC, LIMIT 5.

Complexity:
    Time:  O(n log n)  -- aggregation + sort
    Space: O(k)        -- k = number of customers

SQL:
    SELECT c.customer_id,
           c.name,
           SUM(o.amount) AS total_revenue
    FROM   customers c
    INNER  JOIN orders o
           ON c.customer_id = o.customer_id
    WHERE  o.status <> 'cancelled'
    GROUP  BY c.customer_id, c.name
    ORDER  BY total_revenue DESC
    LIMIT  5;

Notes:
    - Use INNER JOIN to only include customers who have orders.
    - Filter cancelled orders before aggregating.
"""

import pandas as pd


def top5_customers_by_revenue(customers_df: pd.DataFrame,
                              orders_df: pd.DataFrame) -> pd.DataFrame:
    """Return the top 5 customers by total revenue.

    Args:
        customers_df: DataFrame with customer_id, name.
        orders_df: DataFrame with order_id, customer_id, amount, status.

    Returns:
        DataFrame with columns [customer_id, name, total_revenue],
        sorted descending by total_revenue, top 5 rows.
    """
    valid = orders_df[orders_df["status"] != "cancelled"]
    agg = (
        valid.groupby("customer_id", as_index=False)
        .agg(total_revenue=("amount", "sum"))
    )
    merged = customers_df.merge(agg, on="customer_id", how="inner")
    return merged.sort_values("total_revenue", ascending=False).head(5)


if __name__ == "__main__":
    customers = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4, 5, 6],
            "name": ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank"],
        }
    )
    orders = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5, 6, 7, 8],
            "customer_id": [1, 1, 2, 3, 3, 4, 5, 6],
            "status": ["delivered", "delivered", "delivered",
                       "cancelled", "delivered", "delivered",
                       "delivered", "delivered"],
            "amount": [100, 200, 300, 400, 500, 600, 700, 800],
        }
    )
    print(top5_customers_by_revenue(customers, orders))
