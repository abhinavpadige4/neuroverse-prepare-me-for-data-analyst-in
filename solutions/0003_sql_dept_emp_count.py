"""
Day 2 - SQL Joins & Subqueries
Problem 3: Department Employee Count (INNER JOIN)
==================================================
Description:
    Write a SQL query to list each department and the number of
    employees in it using an INNER JOIN.

Assumed schema:
    employees (
        employee_id   INT PRIMARY KEY,
        first_name    VARCHAR,
        last_name     VARCHAR,
        department_id INT,
        salary        DECIMAL(10,2)
    )
    departments (
        department_id INT PRIMARY KEY,
        department_name VARCHAR
    )

Solution:
    INNER JOIN employees to departments on department_id,
    then GROUP BY department and COUNT employees.

Complexity:
    Time:  O(n + m)  -- hash join + aggregation
    Space: O(k)      -- k = number of departments

SQL:
    SELECT d.department_name,
           COUNT(e.employee_id) AS employee_count
    FROM   departments d
    INNER  JOIN employees e
           ON d.department_id = e.department_id
    GROUP  BY d.department_name
    ORDER  BY employee_count DESC;

Notes:
    - INNER JOIN drops departments with zero employees.
    - Use LEFT JOIN from departments to include empty departments.
"""

import pandas as pd


def dept_employee_count(employees_df: pd.DataFrame,
                        departments_df: pd.DataFrame) -> pd.DataFrame:
    """Return each department and the number of employees in it.

    Args:
        employees_df: DataFrame with employee_id, department_id.
        departments_df: DataFrame with department_id, department_name.

    Returns:
        DataFrame with columns [department_name, employee_count],
        sorted descending by employee_count.
    """
    merged = employees_df.merge(departments_df, on="department_id", how="inner")
    result = (
        merged.groupby("department_name", as_index=False)
        .agg(employee_count=("employee_id", "count"))
        .sort_values("employee_count", ascending=False)
    )
    return result


if __name__ == "__main__":
    employees = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5, 6],
            "department_id": [10, 10, 20, 20, 30, 10],
        }
    )
    departments = pd.DataFrame(
        {
            "department_id": [10, 20, 30, 40],
            "department_name": ["Engineering", "Sales", "HR", "Marketing"],
        }
    )
    print(dept_employee_count(employees, departments))
