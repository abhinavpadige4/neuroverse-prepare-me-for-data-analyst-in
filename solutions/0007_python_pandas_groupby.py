"""
Day 4 - Python Pandas Fundamentals
Problem 7: GroupBy Revenue Analysis
=====================================
Description:
    Using pandas, compute total revenue per product category
    from an orders DataFrame.

Assumed DataFrame columns:
    order_id, customer_id, category, amount, order_date

Solution:
    Use groupby('category').agg(...) to compute sum, mean, count.

Complexity:
    Time:  O(n)   -- single pass groupby
    Space: O(k)   -- k = number of categories
"""

import pandas as pd


def revenue_by_category(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Compute total revenue per product category.

    Args:
        orders_df: DataFrame with columns
            [order_id, customer_id, category, amount, order_date].

    Returns:
        DataFrame with columns
            [category, total_revenue, avg_order_value, order_count],
        sorted descending by total_revenue.
    """
    result = (
        orders_df.groupby("category", as_index=False)
        .agg(
            total_revenue=("amount", "sum"),
            avg_order_value=("amount", "mean"),
            order_count=("order_id", "count"),
        )
        .sort_values("total_revenue", ascending=False)
    )
    return result


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "customer_id": [1, 2, 1, 3, 2, 4, 5, 6, 7, 8],
            "category": ["Electronics", "Books", "Electronics", "Books",
                         "Clothing", "Electronics", "Books", "Clothing",
                         "Electronics", "Books"],
            "amount": [500, 20, 300, 15, 80, 1200, 25, 60, 700, 30],
            "order_date": pd.date_range("2026-01-01", periods=10),
        }
    )
    print(revenue_by_category(sample))
