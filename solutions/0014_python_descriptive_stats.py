"""
Day 7 - Statistics & A/B Testing
Problem 14: Descriptive Statistics & Data Profiling
======================================================
Description:
    Using pandas, compute descriptive statistics for a dataset:
    - Count, mean, median, std, min, max, quartiles
    - Detect outliers using IQR method
    - Compute correlation matrix

Assumed DataFrame columns:
    user_id, age, income, orders_count, avg_order_value

Solution:
    Use pandas describe(), quantile(), and corr() methods.

Complexity:
    Time:  O(n)   -- single pass for stats
    Space: O(k^2) -- k = number of numeric columns (correlation matrix)
"""

import pandas as pd
import numpy as np


def descriptive_stats(df: pd.DataFrame) -> dict:
    """Compute descriptive statistics for a DataFrame.

    Args:
        df: DataFrame with numeric columns.

    Returns:
        Dictionary with keys:
            - 'summary': DataFrame of describe() output
            - 'outliers': DataFrame of rows flagged as outliers
            - 'correlation': DataFrame of correlation matrix
            - 'missing': Series of missing value counts per column
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Summary statistics
    summary = df[numeric_cols].describe(percentiles=[0.25, 0.5, 0.75])

    # Missing values
    missing = df.isnull().sum()

    # Outliers using IQR method
    outlier_mask = pd.Series(False, index=df.index)
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_mask |= (df[col] < lower) | (df[col] > upper)

    outliers = df[outlier_mask]

    # Correlation matrix
    correlation = df[numeric_cols].corr()

    return {
        "summary": summary,
        "outliers": outliers,
        "correlation": correlation,
        "missing": missing,
    }


def profile_dataset(df: pd.DataFrame) -> str:
    """Return a text summary of the dataset profile.

    Args:
        df: DataFrame to profile.

    Returns:
        Multi-line string with dataset profile.
    """
    stats = descriptive_stats(df)
    lines = [
        f"Dataset shape: {df.shape[0]} rows x {df.shape[1]} columns",
        f"Columns: {list(df.columns)}",
        f"Missing values:\n{stats['missing'].to_string()}",
        f"\nSummary statistics:\n{stats['summary'].to_string()}",
        f"\nOutliers detected: {len(stats['outliers'])} rows",
        f"\nCorrelation matrix:\n{stats['correlation'].round(3).to_string()}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    np.random.seed(42)
    sample = pd.DataFrame(
        {
            "user_id": list(range(1, 21)),
            "age": np.random.randint(18, 65, size=20),
            "income": np.random.normal(50000, 15000, size=20),
            "orders_count": np.random.poisson(5, size=20),
            "avg_order_value": np.random.normal(50, 20, size=20),
        }
    )
    # Inject an outlier
    sample.loc[0, "income"] = 500000
    print(profile_dataset(sample))
