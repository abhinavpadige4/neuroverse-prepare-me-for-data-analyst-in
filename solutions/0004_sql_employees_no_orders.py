"""
Day 2 - SQL Joins & Subqueries
Problem 4: Employees With No Orders (LEFT JOIN + IS NULL)
===========================================================
Description:
    Write a SQL query to find employees who have not placed any
    orders using a LEFT JOIN and IS NULL.

Assumed schema:
    employees (
        employee_id   INT PRIMARY KEY,
        first_name    VARCHAR,
        last_name     VARCHAR,
        department_id INT
    )
    orders (
        order_id    INT PRIMARY KEY,
        employee_id INT,
        order_date  DATE,
        amount      DECIMAL(10,2)
    )

Solution:
    LEFT JOIN employees to orders, then filter where
    orders.order_id IS NULL (no matching order row).

Complexity:
    Time:  O(n + m)  -- hash join
    Space: O(m)      -- hash table on orders

SQL:
    SELECT e.employee_id,
           e.first_name,
           e.last_name
    FROM   employees e
    LEFT   JOIN orders o
           ON e.employee_id = o.employee_id
    WHERE  o.order_id IS NULL;

Alternative (NOT IN subquery):
    SELECT employee_id, first_name, last_name
    FROM   employees
    WHERE  employee_id NOT IN (SELECT DISTINCT employee_id FROM orders);

Notes:
    - LEFT JOIN + IS NULL is generally faster than NOT IN on large tables.
    - NOT IN can misbehave if the subquery returns NULLs.
"""

import pandas as pd


def employees_without_orders(employees_df: pd.DataFrame,
                             orders_df: pd.DataFrame) -> pd.DataFrame:
    """Return employees who have not placed any orders.

    Args:
        employees_df: DataFrame with employee_id, first_name, last_name.
        orders_df: DataFrame with order_id, employee_id.

    Returns:
        DataFrame of employees with no matching order.
    """
    merged = employees_df.merge(
        orders_df[["order_id"]].drop_duplicates(),
        on="employee_id",
        how="left",
    )
    return merged[merged["order_id"].isna()][
        ["employee_id", "first_name", "last_name"]
    ]


if __name__ == "__main__":
    employees = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5],
            "first_name": ["Alice", "Bob", "Carol", "Dave", "Eve"],
            "last_name": ["A", "B", "C", "D", "E"],
        }
    )
    orders = pd.DataFrame(
        {
            "order_id": [101, 102, 103],
            "employee_id": [1, 2, 2],
        }
    )
    print(employees_without_orders(employees, orders))
