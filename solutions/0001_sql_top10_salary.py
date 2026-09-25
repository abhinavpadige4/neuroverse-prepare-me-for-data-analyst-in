"""
Day 1 - SQL Basics
Problem 1: Top 10 Highest Paid Employees
=========================================
Description:
    Write a SQL query to select the top 10 highest paid employees
    from the `employees` table.

Assumed schema:
    employees (
        employee_id   INT PRIMARY KEY,
        first_name    VARCHAR,
        last_name     VARCHAR,
        department    VARCHAR,
        salary        DECIMAL(10,2)
    )

Solution:
    ORDER BY salary DESC, then LIMIT 10.

Complexity:
    Time:  O(n log n)  -- sorting n rows
    Space: O(1)        -- streaming sort, no extra tables

SQL:
    SELECT employee_id,
           first_name,
           last_name,
           department,
           salary
    FROM   employees
    ORDER  BY salary DESC
    LIMIT  10;

Notes:
    - Use DESC for descending order (highest first).
    - LIMIT is MySQL/Postgres syntax; SQL Server uses TOP 10,
      Oracle uses FETCH FIRST 10 ROWS ONLY.
    - If ties exist at rank 10, use DENSE_RANK() window function
      to include all tied employees.
"""

import pandas as pd


def top10_highest_paid(employees_df: pd.DataFrame) -> pd.DataFrame:
    """Return the top 10 highest paid employees.

    Args:
        employees_df: DataFrame with columns
            [employee_id, first_name, last_name, department, salary].

    Returns:
        DataFrame with the 10 rows having the highest salary,
        sorted descending by salary.
    """
    cols = ["employee_id", "first_name", "last_name", "department", "salary"]
    return employees_df[cols].sort_values("salary", ascending=False).head(10)


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "employee_id": list(range(1, 16)),
            "first_name": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                           "K", "L", "M", "N", "O"],
            "last_name":  ["Smith"] * 15,
            "department": ["Eng"] * 15,
            "salary": [50000, 60000, 70000, 80000, 90000, 100000, 110000,
                       120000, 130000, 140000, 150000, 160000, 170000,
                       180000, 190000],
        }
    )
    print(top10_highest_paid(sample))
