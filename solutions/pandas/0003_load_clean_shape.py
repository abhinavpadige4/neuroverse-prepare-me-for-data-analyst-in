"""
Pandas Q11: Load, Clean, Shape

Exercise: Load a messy CSV dataset, clean it (handle missing values, duplicates,
type conversions, whitespace), then reshape it using pivot_table, melt, and
stack/unstack operations.

Prerequisites: pandas, numpy
"""

import pandas as pd
import numpy as np


def load_data() -> pd.DataFrame:
    """Load sample messy data simulating a real-world CSV import."""
    data = {
        "employee_id": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
                       101, 103, 111, 112, 113],
        "name": ["Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince",
                 "Eve Wilson", "Frank Castle", "Grace Hopper", "Henry Ford",
                 "Ivy Chen", "Jack Ma", "Alice Johnson", "Charlie Brown",
                 "Karen Page", "Leo Messi", "Mia Clark"],
        "department": ["Engineering", "Sales", "Engineering", "Marketing",
                       "Sales", "Engineering", "Engineering", "Sales",
                       "Marketing", "Engineering", "Engineering", "Engineering",
                       "Sales", "Marketing", "Engineering"],
        "salary": [95000, 72000, 88000, 65000, 71000, 92000, 105000, 68000,
                   63000, 98000, 95000, 88000, 70000, 61000, 89000],
        "hire_date": ["2020-03-15", "2019-07-01", "2021-01-10", "2018-11-20",
                      "2020-06-05", "2019-02-28", "2017-09-12", "2021-04-18",
                      "2022-01-05", "2020-08-22", "2020-03-15", "2021-01-10",
                      "2021-06-15", "2022-03-01", "2019-10-10"],
        "performance_score": [4.5, 3.8, 4.2, 3.5, 4.0, 4.8, 4.9, 3.2,
                              3.9, 4.6, 4.5, 4.2, 3.7, 3.4, 4.1],
        "region": ["West", "East", "West", "North", "East", "West",
                   "West", "East", "North", "West", "West", "West",
                   "East", "North", "West"],
    }
    df = pd.DataFrame(data)

    # Introduce messiness: missing values, extra whitespace, inconsistent types
    df.loc[2, "salary"] = np.nan
    df.loc[7, "performance_score"] = np.nan
    df.loc[10, "name"] = "  Alice Johnson  "  # extra whitespace
    df.loc[12, "department"] = "sales"  # inconsistent casing
    df.loc[13, "hire_date"] = "2022/03/01"  # inconsistent date format
    df.loc[14, "region"] = "west"  # inconsistent casing

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset: handle duplicates, missing values, types, whitespace."""
    print("=" * 60)
    print("STEP 1: LOAD & CLEAN")
    print("=" * 60)

    print(f"\nOriginal shape: {df.shape}")
    print(f"Original dtypes:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")

    # --- Remove exact duplicates ---
    df_clean = df.drop_duplicates()
    print(f"\nAfter dropping duplicates: {df_clean.shape[0]} rows")

    # --- Strip whitespace from string columns ---
    str_cols = df_clean.select_dtypes(include=["object"]).columns
    for col in str_cols:
        df_clean[col] = df_clean[col].str.strip()

    # --- Standardize casing for categorical columns ---
    df_clean["department"] = df_clean["department"].str.title()
    df_clean["region"] = df_clean["region"].str.title()

    # --- Convert hire_date to datetime (handle mixed formats) ---
    df_clean["hire_date"] = pd.to_datetime(df_clean["hire_date"], errors="coerce")

    # --- Handle missing salary: fill with department median ---
    dept_median = df_clean.groupby("department")["salary"].transform("median")
    df_clean["salary"] = df_clean["salary"].fillna(dept_median)

    # --- Handle missing performance_score: fill with overall mean ---
    overall_mean = df_clean["performance_score"].mean()
    df_clean["performance_score"] = df_clean["performance_score"].fillna(overall_mean)

    # --- Add derived columns ---
    df_clean["years_experience"] = (
        pd.Timestamp.now() - df_clean["hire_date"]
    ).dt.days / 365.25
    df_clean["years_experience"] = df_clean["years_experience"].round(1)

    # --- Reset index ---
    df_clean = df_clean.reset_index(drop=True)

    print(f"\nCleaned shape: {df_clean.shape}")
    print(f"Cleaned dtypes:\n{df_clean.dtypes}")
    print(f"\nRemaining missing values:\n{df_clean.isnull().sum()}")
    print(f"\nCleaned data preview:\n{df_clean.head(10).to_string()}")

    return df_clean


def reshape_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Reshape using pivot_table: salary by department and region."""
    print("\n" + "=" * 60)
    print("STEP 2: PIVOT TABLE")
    print("=" * 60)

    pivot = df.pivot_table(
        values="salary",
        index="department",
        columns="region",
        aggfunc=["mean", "count"],
        fill_value=0,
        margins=True,
        margins_name="Total",
    )

    print("\nAverage Salary by Department and Region:")
    print(pivot["mean"].to_string())
    print("\nEmployee Count by Department and Region:")
    print(pivot["count"].to_string())

    return pivot


def reshape_melt(df: pd.DataFrame) -> pd.DataFrame:
    """Reshape using melt: unpivot salary and performance_score."""
    print("\n" + "=" * 60)
    print("STEP 3: MELT (UNPIVOT)")
    print("=" * 60)

    melted = df.melt(
        id_vars=["employee_id", "name", "department", "region"],
        value_vars=["salary", "performance_score"],
        var_name="metric",
        value_name="value",
    )

    print(f"\nOriginal shape: {df.shape}")
    print(f"Melted shape: {melted.shape}")
    print("\nMelted data preview:")
    print(melted.head(12).to_string())

    # Filter melted data: high performers with salary above 80k
    high_performers = melted[
        (melted["metric"] == "performance_score") & (melted["value"] >= 4.0)
    ]
    print(f"\nHigh performers (score >= 4.0): {len(high_performers)} employees")
    print(high_performers[["name", "department", "value"]].to_string())

    return melted


def reshape_stack_unstack(df: pd.DataFrame) -> pd.DataFrame:
    """Reshape using stack/unstack: create multi-index and flatten."""
    print("\n" + "=" * 60)
    print("STEP 4: STACK / UNSTACK")
    print("=" * 60)

    # Create a multi-index DataFrame
    multi_idx = df.set_index(["department", "region"])[["salary", "performance_score"]]
    print("\nMulti-index DataFrame:")
    print(multi_idx.to_string())

    # Stack: convert columns to rows (long format)
    stacked = multi_idx.stack()
    stacked.name = "value"
    print("\nStacked (long format):")
    print(stacked.head(10).to_string())

    # Unstack: convert back to wide format
    unstacked = stacked.unstack()
    print("\nUnstacked (wide format):")
    print(unstacked.head(10).to_string())

    # Practical example: pivot with multi-level columns
    pivot_multi = df.pivot_table(
        values=["salary", "performance_score"],
        index="department",
        columns="region",
        aggfunc="mean",
        fill_value=0,
    )
    print("\nMulti-level pivot (mean salary & score by dept/region):")
    print(pivot_multi.round(2).to_string())

    return pivot_multi


def reshape_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """Convert wide format to long format using pivot_longer equivalent."""
    print("\n" + "=" * 60)
    print("STEP 5: WIDE TO LONG CONVERSION")
    print("=" * 60)

    # Create a wide-format summary
    wide_summary = df.groupby("department").agg(
        avg_salary=("salary", "mean"),
        avg_score=("performance_score", "mean"),
        headcount=("employee_id", "count"),
    ).reset_index()

    print("\nWide format summary:")
    print(wide_summary.to_string())

    # Convert to long format
    long_summary = wide_summary.melt(
        id_vars=["department"],
        value_vars=["avg_salary", "avg_score", "headcount"],
        var_name="metric",
        value_name="value",
    )

    print("\nLong format summary:")
    print(long_summary.to_string())

    return long_summary


def validate_cleaning(df_original: pd.DataFrame, df_clean: pd.DataFrame) -> None:
    """Validate that cleaning was done correctly."""
    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    # Check no missing values remain
    assert df_clean.isnull().sum().sum() == 0, "Missing values remain after cleaning!"
    print("✓ No missing values remain")

    # Check no duplicates
    assert df_clean.duplicated().sum() == 0, "Duplicates remain after cleaning!"
    print("✓ No duplicate rows")

    # Check date column is datetime
    assert pd.api.types.is_datetime64_any_dtype(df_clean["hire_date"]), \
        "hire_date is not datetime type!"
    print("✓ hire_date is datetime type")

    # Check salary is numeric
    assert pd.api.types.is_numeric_dtype(df_clean["salary"]), \
        "salary is not numeric type!"
    print("✓ salary is numeric type")

    # Check department casing is consistent
    depts = df_clean["department"].unique()
    assert all(d == d.title() for d in depts), "Department casing inconsistent!"
    print(f"✓ Department casing consistent: {sorted(depts)}")

    # Check region casing is consistent
    regions = df_clean["region"].unique()
    assert all(r == r.title() for r in regions), "Region casing inconsistent!"
    print(f"✓ Region casing consistent: {sorted(regions)}")

    # Check row count decreased (duplicates removed)
    assert df_clean.shape[0] < df_original.shape[0], \
        "Row count should decrease after deduplication!"
    print(f"✓ Rows reduced from {df_original.shape[0]} to {df_clean.shape[0]}")

    print("\n✓ All validations passed!")


def main():
    """Run the complete load, clean, and reshape pipeline."""
    print("Pandas Q11: Load, Clean, Shape")
    print("=" * 60)

    # Step 1: Load and clean
    df_raw = load_data()
    df_clean = clean_data(df_raw)

    # Step 2: Validate cleaning
    validate_cleaning(df_raw, df_clean)

    # Step 3: Reshape operations
    pivot_result = reshape_pivot(df_clean)
    melted_result = reshape_melt(df_clean)
    stack_result = reshape_stack_unstack(df_clean)
    long_result = reshape_wide_to_long(df_clean)

    # Final summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Original data: {df_raw.shape[0]} rows x {df_raw.shape[1]} columns")
    print(f"Cleaned data:  {df_clean.shape[0]} rows x {df_clean.shape[1]} columns")
    print(f"Pivot table:   {pivot_result.shape[0]} rows x {pivot_result.shape[1]} columns")
    print(f"Melted data:   {melted_result.shape[0]} rows x {melted_result.shape[1]} columns")
    print(f"Stacked data:  {stack_result.shape[0]} rows x {stack_result.shape[1]} columns")
    print(f"Long summary:  {long_result.shape[0]} rows x {long_result.shape[1]} columns")
    print("\nKey takeaways:")
    print("  1. Always inspect data before cleaning (dtypes, nulls, duplicates)")
    print("  2. Clean in order: duplicates → whitespace → types → missing values")
    print("  3. pivot_table is for aggregation; melt is for unpivoting")
    print("  4. stack/unstack work with multi-index DataFrames")
    print("  5. Wide-to-long conversion is essential for time-series analysis")


if __name__ == "__main__":
    main()
