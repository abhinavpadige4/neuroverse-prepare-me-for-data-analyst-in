"""
Day 7 - Statistics & A/B Testing
Problem 15: Funnel Analysis (SQL + Python)
============================================
Description:
    Write a SQL query to compute a conversion funnel:
    visit -> signup -> purchase, with conversion rates
    between each step.

Assumed schema:
    events (
        event_id    INT PRIMARY KEY,
        user_id     INT,
        event_type  VARCHAR,   -- 'visit', 'signup', 'purchase'
        event_date  TIMESTAMP
    )

Solution:
    1. CTE to get distinct users per event type.
    2. Compute counts per step.
    3. Compute conversion rates between consecutive steps.

Complexity:
    Time:  O(n log n)  -- sort + groupby
    Space: O(u)        -- u = number of unique users

SQL:
    WITH funnel AS (
        SELECT 'visit'    AS step, 1 AS step_order,
               COUNT(DISTINCT user_id) AS users
        FROM   events WHERE event_type = 'visit'
        UNION ALL
        SELECT 'signup'   AS step, 2 AS step_order,
               COUNT(DISTINCT user_id) AS users
        FROM   events WHERE event_type = 'signup'
        UNION ALL
        SELECT 'purchase' AS step, 3 AS step_order,
               COUNT(DISTINCT user_id) AS users
        FROM   events WHERE event_type = 'purchase'
    )
    SELECT step,
           users,
           LAG(users) OVER (ORDER BY step_order) AS prev_step_users,
           ROUND(
               users * 1.0 / NULLIF(LAG(users) OVER (ORDER BY step_order), 0),
               4
           ) AS step_conversion_rate,
           ROUND(
               users * 1.0 / (
                   SELECT users FROM funnel WHERE step = 'visit'
               ),
               4
           ) AS overall_conversion_rate
    FROM   funnel
    ORDER  BY step_order;

Notes:
    - LAG() gets the previous step's user count.
    - NULLIF prevents divide-by-zero.
    - Overall conversion rate is relative to the top of the funnel.
"""

import pandas as pd


def funnel_analysis(events_df: pd.DataFrame,
                    steps: list[str] | None = None) -> pd.DataFrame:
    """Compute a conversion funnel with step and overall conversion rates.

    Args:
        events_df: DataFrame with user_id, event_type, event_date.
        steps: Ordered list of funnel steps (default: visit, signup, purchase).

    Returns:
        DataFrame with columns
            [step, users, prev_step_users, step_conversion_rate,
             overall_conversion_rate].
    """
    if steps is None:
        steps = ["visit", "signup", "purchase"]

    rows = []
    for step in steps:
        users = events_df.loc[
            events_df["event_type"] == step, "user_id"
        ].nunique()
        rows.append({"step": step, "users": users})

    funnel = pd.DataFrame(rows)
    funnel["prev_step_users"] = funnel["users"].shift(1)
    funnel["step_conversion_rate"] = (
        funnel["users"] / funnel["prev_step_users"]
    ).round(4)
    top = funnel["users"].iloc[0]
    funnel["overall_conversion_rate"] = (funnel["users"] / top).round(4)
    return funnel


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "event_id": list(range(1, 21)),
            "user_id": [1, 1, 1, 2, 2, 3, 3, 4, 4, 4,
                        5, 5, 6, 6, 7, 7, 8, 8, 9, 10],
            "event_type": ["visit", "signup", "purchase",
                           "visit", "signup",
                           "visit", "signup",
                           "visit", "signup", "purchase",
                           "visit", "signup",
                           "visit", "signup",
                           "visit", "signup",
                           "visit", "signup",
                           "visit", "visit"],
            "event_date": pd.date_range("2026-01-01", periods=20, freq="h"),
        }
    )
    print(funnel_analysis(sample))
