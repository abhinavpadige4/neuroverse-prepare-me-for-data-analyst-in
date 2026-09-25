"""
Problem: Use ROW_NUMBER to rank employees by salary within each department.

SQL Equivalent:
    SELECT
        employee_id,
        last_name,
        department,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department
            ORDER BY salary DESC
        ) AS rank_within_dept
    FROM employees
    ORDER BY department, rank_within_dept;

This solution demonstrates the ROW_NUMBER window function concept using pandas.
"""

import pandas as pd


def create_sample_employees() -> pd.DataFrame:
    """Create a sample employees DataFrame for demonstration."""
    data = {
        "employee_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        "last_name": [
            "Smith", "Johnson", "Williams", "Brown", "Jones",
            "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
            "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"
        ],
        "department": [
            "Engineering", "Engineering", "Engineering", "Engineering",
            "Sales", "Sales", "Sales", "Sales",
            "Marketing", "Marketing", "Marketing",
            "Finance", "Finance", "Finance",
            "Engineering"
        ],
        "salary": [
            95000, 120000, 85000, 110000,
            65000, 72000, 58000, 80000,
            70000, 62000, 75000,
            90000, 88000, 92000,
            105000
        ]
    }
    return pd.DataFrame(data)


def rank_employees_by_salary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank employees by salary within each department using ROW_NUMBER logic.

    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)
    assigns a unique sequential integer to rows within each partition
    (department), ordered by salary descending.

    Args:
        df: DataFrame with columns [employee_id, last_name, department, salary]

    Returns:
        DataFrame with an added 'rank_within_dept' column
    """
    # Sort by department and salary descending to establish correct order
    df_sorted = df.sort_values(
        by=["department", "salary"],
        ascending=[True, False]
    ).reset_index(drop=True)

    # Apply ROW_NUMBER: rank within each department partition
    # groupby().cumcount() + 1 gives 1-based sequential numbering per group
    df_sorted["rank_within_dept"] = (
        df_sorted.groupby("department").cumcount() + 1
    )

    return df_sorted


def rank_employees_sql_style(df: pd.DataFrame) -> pd.DataFrame:
    """
    Alternative implementation using transform for clarity.
    Demonstrates the same ROW_NUMBER concept with a different pandas approach.
    """
    df_result = df.copy()

    # Use transform with a lambda to assign row numbers within each group
    df_result["rank_within_dept"] = (
        df_result
        .sort_values(["department", "salary"], ascending=[True, False])
        .groupby("department")
        .transform(lambda x: range(1, len(x) + 1))
    )

    return df_result


def get_top_n_per_department(df: pd.DataFrame, n: int = 2) -> pd.DataFrame:
    """
    Get the top N highest-paid employees per department using ROW_NUMBER.

    This is a common interview pattern:
        SELECT * FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn
            FROM employees
        ) WHERE rn <= N;

    Args:
        df: DataFrame with employee data
        n: Number of top employees to keep per department

    Returns:
        Filtered DataFrame with only top N employees per department
    """
    ranked = rank_employees_by_salary(df)
    return ranked[ranked["rank_within_dept"] <= n].reset_index(drop=True)


def get_department_leaders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the highest-paid employee (rank 1) in each department.

    Equivalent SQL:
        SELECT * FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) rn
            FROM employees
        ) WHERE rn = 1;

    Args:
        df: DataFrame with employee data

    Returns:
        DataFrame with only the top earner per department
    """
    ranked = rank_employees_by_salary(df)
    return ranked[ranked["rank_within_dept"] == 1].reset_index(drop=True)


def print_sql_equivalent():
    """Print the equivalent SQL query for reference."""
    sql = """SELECT
    employee_id,
    last_name,
    department,
    salary,
    ROW_NUMBER() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS rank_within_dept
FROM employees
ORDER BY department, rank_within_dept;"""
    print("=" * 60)
    print("EQUIVALENT SQL QUERY:")
    print("=" * 60)
    print(sql)
    print()


def main():
    """Main function demonstrating ROW_NUMBER ranking by department."""
    print("=" * 60)
    print("ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)")
    print("=" * 60)
    print()

    # Create sample data
    employees = create_sample_employees()
    print("Original Employees Data:")
    print("-" * 60)
    print(employees.to_string(index=False))
    print()

    # Apply ROW_NUMBER ranking
    ranked = rank_employees_by_salary(employees)
    print("Employees Ranked by Salary Within Each Department:")
    print("-" * 60)
    print(ranked.to_string(index=False))
    print()

    # Show top 2 per department
    top_2 = get_top_n_per_department(employees, n=2)
    print("Top 2 Highest-Paid Employees Per Department:")
    print("-" * 60)
    print(top_2.to_string(index=False))
    print()

    # Show department leaders
    leaders = get_department_leaders(employees)
    print("Department Leaders (Highest Paid Per Department):")
    print("-" * 60)
    print(leaders.to_string(index=False))
    print()

    # Print SQL equivalent
    print_sql_equivalent()

    # Verify correctness
    print("=" * 60)
    print("VERIFICATION:")
    print("=" * 60)

    # Check that ranks are sequential within each department
    for dept in ranked["department"].unique():
        dept_ranks = ranked[ranked["department"] == dept]["rank_within_dept"]
        expected = list(range(1, len(dept_ranks) + 1))
        assert list(dept_ranks) == expected, (
            f"Rank verification failed for {dept}: "
            f"got {list(dept_ranks)}, expected {expected}"
        )
        print(f"  {dept}: ranks {list(dept_ranks)} - CORRECT")

    # Check that salaries are in descending order within each department
    for dept in ranked["department"].unique():
        dept_salaries = ranked[ranked["department"] == dept]["salary"].tolist()
        assert dept_salaries == sorted(dept_salaries, reverse=True), (
            f"Salary order verification failed for {dept}"
        )
        print(f"  {dept}: salaries descending - CORRECT")

    print()
    print("All verifications passed!")


if __name__ == "__main__":
    main()
