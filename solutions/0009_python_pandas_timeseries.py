"""
Day 5 - Python Pandas Time Series & Cleaning
Problem 9: Daily Revenue Time Series
=======================================
Description:
    Using pandas, build a daily revenue time series from an
    orders DataFrame, filling missing days with 0.

Assumed DataFrame columns:
    order_id, customer_id, amount, order_date

Solution:
    1. Convert order_date to datetime.
    2. Group by date and sum amount.
    3. Reindex to a full daily date range, filling NaN with 0.
    4. Compute a 7-day rolling average.

Complexity:
    Time:  O(n log n)  -- sort + groupby
    Space: O(d)        -- d = number of days in range
"""

import pandas as pd


def daily_revenue_series(orders_df: pd.DataFrame,
                         start: str | None = None,
                         end: str | None = None) -> pd.DataFrame:
    """Return a daily revenue time series with a 7-day rolling average.

    Args:
        orders_df: DataFrame with order_id, amount, order_date.
        start: Optional start date string (defaults to min order_date).
        end: Optional end date string (defaults to max order_date).

    Returns:
        DataFrame indexed by date with columns
            [daily_revenue, order_count, rolling_7d_avg].
    """
    df = orders_df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"])

    daily = (
        df.groupby("order_date", as_index=False)
        .agg(daily_revenue=("amount", "sum"),
             order_count=("order_id", "count"))
    )

    start_date = pd.to_datetime(start) if start else df["order_date"].min()
    end_date = pd.to_datetime(end) if end else df["order_date"].max()
    full_range = pd.date_range(start=start_date, end=end_date, freq="D")

    daily = daily.set_index("order_date").reindex(full_range, fill_value=0)
    daily.index.name = "date"
    daily["rolling_7d_avg"] = (
        daily["daily_revenue"].rolling(window=7, min_periods=1).mean()
    )
    return daily.reset_index()


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "customer_id": [1, 2, 1, 3, 2, 4, 5, 6, 7, 8],
            "amount": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
            "order_date": pd.to_datetime(
                ["2026-01-01", "2026-01-02", "2026-01-03",
                 "2026-01-05", "2026-01-07", "2026-01-08",
                 "2026-01-10", "2026-01-11", "2026-01-12",
                 "2026-01-13"]
            ),
        }
    )
    print(daily_revenue_series(sample))
