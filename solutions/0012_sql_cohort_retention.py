"""
Day 6 - SQL Window Functions & Advanced Analytics
Problem 12: Cohort Retention Analysis with CTEs
==================================================
Description:
    Write a SQL query to compute cohort retention: for each
    signup month, what fraction of users returned in month N?

Assumed schema:
    users (
        user_id       INT PRIMARY KEY,
        signup_date   DATE
    )
    activity (
        user_id       INT,
        activity_date DATE
    )

Solution:
    1. CTE to derive each user's signup cohort (year-month).
    2. CTE to compute the offset month between activity and signup.
    3. Aggregate to get retention rate per cohort per offset.

Complexity:
    Time:  O(n log n)  -- sort + groupby
    Space: O(n)

SQL:
    WITH user_cohort AS (
        SELECT user_id,
               DATE_TRUNC('month', signup_date) AS cohort_month
        FROM   users
    ),
    activity_with_offset AS (
        SELECT u.user_id,
               u.cohort_month,
               DATE_TRUNC('month', a.activity_date) AS activity_month,
               EXTRACT(MONTH FROM AGE(a.activity_date,
                                      u.cohort_month)) AS month_offset
        FROM   user_cohort u
        INNER  JOIN activity a
               ON u.user_id = a.user_id
    ),
    cohort_sizes AS (
        SELECT cohort_month,
               COUNT(DISTINCT user_id) AS cohort_size
        FROM   user_cohort
        GROUP  BY cohort_month
    )
    SELECT a.cohort_month,
           a.month_offset,
           COUNT(DISTINCT a.user_id) AS active_users,
           c.cohort_size,
           ROUND(
               COUNT(DISTINCT a.user_id) * 1.0 / c.cohort_size, 4
           ) AS retention_rate
    FROM   activity_with_offset a
    INNER  JOIN cohort_sizes c
           ON a.cohort_month = c.cohort_month
    GROUP  BY a.cohort_month, a.month_offset, c.cohort_size
    ORDER  BY a.cohort_month, a.month_offset;

Notes:
    - Cohort analysis is a staple of product analytics interviews.
    - month_offset = 0 is the signup month itself.
    - Retention rate = active_users / cohort_size.
"""

import pandas as pd


def cohort_retention(users_df: pd.DataFrame,
                     activity_df: pd.DataFrame) -> pd.DataFrame:
    """Compute cohort retention rates.

    Args:
        users_df: DataFrame with user_id, signup_date.
        activity_df: DataFrame with user_id, activity_date.

    Returns:
        DataFrame with columns
            [cohort_month, month_offset, active_users, cohort_size,
             retention_rate].
    """
    users = users_df.copy()
    users["signup_date"] = pd.to_datetime(users["signup_date"])
    users["cohort_month"] = users["signup_date"].dt.to_period("M")

    activity = activity_df.copy()
    activity["activity_date"] = pd.to_datetime(activity["activity_date"])
    activity["activity_month"] = activity["activity_date"].dt.to_period("M")

    merged = activity.merge(users[["user_id", "cohort_month"]],
                            on="user_id", how="inner")
    merged["month_offset"] = (
        (merged["activity_month"] - merged["cohort_month"]).apply(
            lambda x: x.n
        )
    )

    cohort_sizes = (
        users.groupby("cohort_month")["user_id"]
        .nunique()
        .reset_index(name="cohort_size")
    )

    retention = (
        merged.groupby(["cohort_month", "month_offset"], as_index=False)
        .agg(active_users=("user_id", "nunique"))
        .merge(cohort_sizes, on="cohort_month", how="left")
    )
    retention["retention_rate"] = (
        retention["active_users"] / retention["cohort_size"]
    ).round(4)
    return retention.sort_values(["cohort_month", "month_offset"])


if __name__ == "__main__":
    users = pd.DataFrame(
        {
            "user_id": [1, 2, 3, 4],
            "signup_date": pd.to_datetime(
                ["2026-01-05", "2026-01-15", "2026-02-01", "2026-02-20"]
            ),
        }
    )
    activity = pd.DataFrame(
        {
            "user_id": [1, 1, 1, 2, 3, 3, 4],
            "activity_date": pd.to_datetime(
                ["2026-01-10", "2026-02-10", "2026-03-10",
                 "2026-01-20", "2026-02-15", "2026-03-15",
                 "2026-02-25"]
            ),
        }
    )
    print(cohort_retention(users, activity))
