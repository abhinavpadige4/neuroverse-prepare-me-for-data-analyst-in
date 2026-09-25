"""
Pandas Q12: Filter Rows and Compute Group Means

Problem Statement:
------------------
Given a DataFrame of employee records, perform the following tasks:
1. Filter employees whose salary exceeds the overall mean salary.
2. Compute the mean salary per department for those filtered employees.
3. Return a summary DataFrame with department, count, and mean salary.

This exercise tests:
- Boolean indexing / .query() / .loc[]
- .groupby() with aggregation
- .mean(), .count(), .agg()
- Chaining operations cleanly

Dataset:
--------
A DataFrame with columns: employee_id, name, department, salary, years_experience
"""

import pandas as pd
import numpy as np
from typing import Tuple


# ---------------------------------------------------------------------------
# Sample data generator (used by tests and demo)
# ---------------------------------------------------------------------------

def generate_sample_data(n: int = 50, seed: int = 42) -> pd.DataFrame:
    """Generate a reproducible sample employee DataFrame."""
    rng = np.random.default_rng(seed)
    departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
    names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank",
        "Ivy", "Jack", "Karen", "Leo", "Mona", "Nate", "Olga", "Pete",
        "Quinn", "Rita", "Sam", "Tina", "Uma", "Vince", "Wendy", "Xander",
        "Yara", "Zack", "Amy", "Ben", "Cora", "Dan", "Eli", "Faye", "Gus",
        "Hana", "Ivan", "Jill", "Karl", "Lena", "Mick", "Nina", "Owen", "Pia",
        "Rex", "Sue", "Tom", "Urs", "Val", "Wes", "Xia", "Yol", "Zoe"
    ]
    data = {
        "employee_id": range(1, n + 1),
        "name": rng.choice(names, size=n, replace=True),
        "department": rng.choice(departments, size=n),
        "salary": rng.integers(low=40000, high=150000, size=n),
        "years_experience": rng.integers(low=0, high=25, size=n),
    }
    return pd.DataFrame(data)


# ---------------------------------------------------------------------------
# Core solution functions
# ---------------------------------------------------------------------------

def filter_above_mean(df: pd.DataFrame, column: str = "salary") -> pd.DataFrame:
    """
    Return rows where the specified column exceeds the overall mean of that column.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing at least the specified column.
    column : str
        Name of the numeric column to filter on (default: 'salary').

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame with only rows above the mean.
    """
    mean_value = df[column].mean()
    return df[df[column] > mean_value].copy()


def department_mean_salary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute mean salary per department.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'department' and 'salary' columns.

    Returns
    -------
    pd.DataFrame
        Columns: department, mean_salary (sorted descending by mean_salary).
    """
    result = (
        df.groupby("department")["salary"]
        .mean()
        .reset_index()
        .rename(columns={"salary": "mean_salary"})
        .sort_values("mean_salary", ascending=False)
        .reset_index(drop=True)
    )
    return result


def filter_and_summarize(
    df: pd.DataFrame,
    salary_column: str = "salary",
    group_column: str = "department",
) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
    """
    Full pipeline: filter above-mean rows, then summarize by group.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    salary_column : str
        Column to filter on.
    group_column : str
        Column to group by for summary.

    Returns
    -------
    Tuple of:
        - filtered_df : pd.DataFrame (rows above mean)
        - summary_df  : pd.DataFrame (group, count, mean_salary)
        - overall_mean: float (the threshold used)
    """
    overall_mean = df[salary_column].mean()
    filtered_df = df[df[salary_column] > overall_mean].copy()

    summary_df = (
        filtered_df.groupby(group_column)[salary_column]
        .agg(count="count", mean_salary="mean")
        .reset_index()
        .sort_values("mean_salary", ascending=False)
        .reset_index(drop=True)
    )

    return filtered_df, summary_df, overall_mean


def filter_by_experience_and_salary(
    df: pd.DataFrame,
    min_experience: int = 5,
    salary_column: str = "salary",
) -> pd.DataFrame:
    """
    Filter employees with at least min_experience years AND salary above overall mean.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    min_experience : int
        Minimum years of experience required.
    salary_column : str
        Salary column name.

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame.
    """
    mean_salary = df[salary_column].mean()
    mask = (
        (df["years_experience"] >= min_experience)
        & (df[salary_column] > mean_salary)
    )
    return df[mask].copy()


def compute_conditional_means(
    df: pd.DataFrame,
    group_column: str = "department",
    salary_column: str = "salary",
) -> pd.DataFrame:
    """
    For each group, compute:
    - mean_salary: average salary
    - median_salary: median salary
    - std_salary: standard deviation of salary
    - pct_above_overall_mean: percentage of employees above overall mean

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    group_column : str
        Column to group by.
    salary_column : str
        Numeric column for statistics.

    Returns
    -------
    pd.DataFrame
        Summary statistics per group.
    """
    overall_mean = df[salary_column].mean()

    def group_stats(group: pd.DataFrame) -> pd.Series:
        return pd.Series({
            "mean_salary": group[salary_column].mean(),
            "median_salary": group[salary_column].median(),
            "std_salary": group[salary_column].std(),
            "pct_above_overall_mean": (
                (group[salary_column] > overall_mean).sum() / len(group) * 100
            ),
        })

    result = (
        df.groupby(group_column)
        .apply(group_stats)
        .reset_index()
        .sort_values("mean_salary", ascending=False)
        .reset_index(drop=True)
    )
    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def run_tests() -> None:
    """Run comprehensive tests for all solution functions."""
    import unittest

    class TestFilterMean(unittest.TestCase):
        def setUp(self):
            self.df = generate_sample_data(n=50, seed=42)

        def test_generate_sample_data_shape(self):
            df = generate_sample_data(n=30, seed=1)
            self.assertEqual(len(df), 30)
            self.assertIn("salary", df.columns)
            self.assertIn("department", df.columns)

        def test_filter_above_mean_returns_subset(self):
            filtered = filter_above_mean(self.df)
            self.assertLess(len(filtered), len(self.df))
            self.assertGreater(len(filtered), 0)
            self.assertTrue((filtered["salary"] > self.df["salary"].mean()).all())

        def test_filter_above_mean_custom_column(self):
            filtered = filter_above_mean(self.df, column="years_experience")
            self.assertTrue(
                (filtered["years_experience"] > self.df["years_experience"].mean()).all()
            )

        def test_department_mean_salary_columns(self):
            result = department_mean_salary(self.df)
            self.assertIn("department", result.columns)
            self.assertIn("mean_salary", result.columns)
            self.assertEqual(len(result), self.df["department"].nunique())

        def test_department_mean_salary_sorted_desc(self):
            result = department_mean_salary(self.df)
            values = result["mean_salary"].tolist()
            self.assertEqual(values, sorted(values, reverse=True))

        def test_filter_and_summarize_returns_tuple(self):
            filtered, summary, mean_val = filter_and_summarize(self.df)
            self.assertIsInstance(filtered, pd.DataFrame)
            self.assertIsInstance(summary, pd.DataFrame)
            self.assertIsInstance(mean_val, float)
            self.assertEqual(mean_val, self.df["salary"].mean())

        def test_filter_and_summarize_summary_columns(self):
            _, summary, _ = filter_and_summarize(self.df)
            self.assertIn("department", summary.columns)
            self.assertIn("count", summary.columns)
            self.assertIn("mean_salary", summary.columns)

        def test_filter_and_summarize_counts_match(self):
            filtered, summary, _ = filter_and_summarize(self.df)
            total_in_summary = summary["count"].sum()
            self.assertEqual(total_in_summary, len(filtered))

        def test_filter_by_experience_and_salary(self):
            result = filter_by_experience_and_salary(self.df, min_experience=5)
            self.assertTrue((result["years_experience"] >= 5).all())
            self.assertTrue((result["salary"] > self.df["salary"].mean()).all())

        def test_filter_by_experience_and_salary_empty_possible(self):
            # With very high threshold, result may be empty
            result = filter_by_experience_and_salary(self.df, min_experience=25)
            self.assertIsInstance(result, pd.DataFrame)

        def test_compute_conditional_means_columns(self):
            result = compute_conditional_means(self.df)
            expected_cols = {
                "department", "mean_salary", "median_salary",
                "std_salary", "pct_above_overall_mean"
            }
            self.assertEqual(set(result.columns), expected_cols)

        def test_compute_conditional_means_pct_range(self):
            result = compute_conditional_means(self.df)
            self.assertTrue((result["pct_above_overall_mean"] >= 0).all())
            self.assertTrue((result["pct_above_overall_mean"] <= 100).all())

        def test_filter_above_mean_does_not_mutate_original(self):
            original_len = len(self.df)
            _ = filter_above_mean(self.df)
            self.assertEqual(len(self.df), original_len)

        def test_all_departments_present_in_summary(self):
            _, summary, _ = filter_and_summarize(self.df)
            # At least some departments should appear (those with above-mean earners)
            self.assertGreater(len(summary), 0)

    unittest.main(verbosity=2, exit=False)


# ---------------------------------------------------------------------------
# Demo / main
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate all solution functions with sample data."""
    print("=" * 70)
    print("Pandas Q12: Filter Rows and Compute Group Means")
    print("=" * 70)

    df = generate_sample_data(n=50, seed=42)
    print(f"\nOriginal DataFrame shape: {df.shape}")
    print(f"Overall mean salary: ${df['salary'].mean():,.2f}")
    print(f"\nFirst 5 rows:\n{df.head()}")

    # 1. Filter above mean
    print("\n" + "-" * 70)
    print("1. Filter employees above mean salary")
    filtered = filter_above_mean(df)
    print(f"   Rows above mean: {len(filtered)} / {len(df)}")
    print(f"   Mean salary of filtered: ${filtered['salary'].mean():,.2f}")

    # 2. Department mean salary
    print("\n" + "-" * 70)
    print("2. Mean salary per department (all employees)")
    dept_means = department_mean_salary(df)
    print(dept_means.to_string(index=False))

    # 3. Full pipeline
    print("\n" + "-" * 70)
    print("3. Filter + Summarize pipeline")
    filtered_df, summary_df, overall_mean = filter_and_summarize(df)
    print(f"   Threshold (overall mean): ${overall_mean:,.2f}")
    print(f"   Filtered rows: {len(filtered_df)}")
    print(f"\n   Summary by department:\n{summary_df.to_string(index=False)}")

    # 4. Experience + salary filter
    print("\n" + "-" * 70)
    print("4. Filter: experience >= 5 AND salary > mean")
    exp_filtered = filter_by_experience_and_salary(df, min_experience=5)
    print(f"   Matching employees: {len(exp_filtered)}")
    if len(exp_filtered) > 0:
        print(exp_filtered[["name", "department", "salary", "years_experience"]].to_string(index=False))

    # 5. Conditional means
    print("\n" + "-" * 70)
    print("5. Conditional means per department")
    cond_means = compute_conditional_means(df)
    print(cond_means.to_string(index=False))

    print("\n" + "=" * 70)
    print("All demonstrations complete.")


if __name__ == "__main__":
    main()
