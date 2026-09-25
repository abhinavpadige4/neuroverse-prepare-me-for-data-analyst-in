"""
Day 4 - Python Pandas Fundamentals
Problem 8: Merge Customers with Orders
=======================================
Description:
    Using pandas, merge a customers DataFrame with an orders
    DataFrame to produce a customer-level summary.

Assumed DataFrames:
    customers: customer_id, name, signup_date
    orders:    order_id, customer_id, amount, order_date

Solution:
    Use pd.merge with how='left' to keep all customers,
    then aggregate order metrics per customer.

Complexity:
    Time:  O(n + m)  -- hash join
    Space: O(n + m)
"""

import pandas as pd


def customer_order_summary(customers_df: pd.DataFrame,
                           orders_df: pd.DataFrame) -> pd.DataFrame:
    """Return a per-customer summary of their orders.

    Args:
        customers_df: DataFrame with customer_id, name, signup_date.
        orders_df: DataFrame with order_id, customer_id, amount, order_date.

    Returns:
        DataFrame with columns
            [customer_id, name, signup_date, order_count, total_spent,
             avg_order_value, first_order_date, last_order_date],
        sorted descending by total_spent.
    """
    agg = (
        orders_df.groupby("customer_id", as_index=False)
        .agg(
            order_count=("order_id", "count"),
            total_spent=("amount", "sum"),
            avg_order_value=("amount", "mean"),
            first_order_date=("order_date", "min"),
            last_order_date=("order_date", "max"),
        )
    )
    merged = customers_df.merge(agg, on="customer_id", how="left")
    # Fill NaN for customers with no orders
    merged["order_count"] = merged["order_count"].fillna(0).astype(int)
    merged["total_spent"] = merged["total_spent"].fillna(0.0)
    merged["avg_order_value"] = merged["avg_order_value"].fillna(0.0)
    return merged.sort_values("total_spent", ascending=False)


if __name__ == "__main__":
    customers = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4],
            "name": ["Alice", "Bob", "Carol", "Dave"],
            "signup_date": pd.to_datetime(
                ["2025-01-01", "2025-02-15", "2025-03-10", "2025-04-05"]
            ),
        }
    )
    orders = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5],
            "customer_id": [1, 1, 2, 3, 3],
            "amount": [100, 200, 300, 400, 500],
            "order_date": pd.to_datetime(
                ["2026-01-05", "2026-02-10", "2026-01-20",
                 "2026-03-01", "2026-03-15"]
            ),
        }
    )
    print(customer_order_summary(customers, orders))
