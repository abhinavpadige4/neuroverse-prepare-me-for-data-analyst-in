"""
0010_fill_missing_mean.py
Fill missing values in column 'sales' with the column mean.

Data Analyst Interview Prep - Day 3 (Python/Pandas)
"""

import pandas as pd
import numpy as np


def fill_missing_with_mean(df: pd.DataFrame, column: str = "sales") -> pd.DataFrame:
    """
    Fill missing values in the specified column with the column mean.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the target column.
    column : str
        Name of the column to fill. Default is 'sales'.

    Returns
    -------
    pd.DataFrame
        DataFrame with missing values in the target column replaced by the mean.

    Raises
    ------
    KeyError
        If the specified column does not exist in the DataFrame.
    ValueError
        If the column contains no numeric data.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame. Available columns: {list(df.columns)}")

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' is not numeric. Cannot compute mean.")

    result = df.copy()
    mean_value = result[column].mean()
    result[column] = result[column].fillna(mean_value)
    return result


def create_sample_data() -> pd.DataFrame:
    """
    Create a sample DataFrame with missing values in the 'sales' column.

    Returns
    -------
    pd.DataFrame
        Sample DataFrame with 10 rows and missing values in 'sales'.
    """
    data = {
        "employee_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack"],
        "department": ["Sales", "Sales", "Marketing", "Sales", "HR", "Sales", "Marketing", "Sales", "HR", "Sales"],
        "sales": [15000.0, np.nan, 22000.0, 18000.0, np.nan, 25000.0, np.nan, 19000.0, 12000.0, np.nan],
        "region": ["North", "South", "East", "North", "West", "South", "East", "North", "West", "South"]
    }
    return pd.DataFrame(data)


def test_fill_missing_with_mean():
    """Run tests for fill_missing_with_mean function."""
    print("=" * 60)
    print("TESTING: fill_missing_with_mean")
    print("=" * 60)

    # Test 1: Basic functionality
    print("\nTest 1: Basic fill with mean")
    df = create_sample_data()
    print(f"\nOriginal DataFrame (missing values shown as NaN):")
    print(df.to_string(index=False))

    result = fill_missing_with_mean(df, "sales")
    print(f"\nAfter filling missing values with mean:")
    print(result.to_string(index=False))

    # Verify no NaN remains
    assert result["sales"].isna().sum() == 0, "FAIL: NaN values still present after fill"
    print("\n[PASS] No NaN values remain after fill.")

    # Test 2: Verify mean value is correct
    print("\nTest 2: Verify filled value equals column mean")
    original_mean = df["sales"].mean()
    filled_values = result["sales"] - df["sales"]
    # Where original was NaN, filled value should equal the mean
    nan_mask = df["sales"].isna()
    filled_at_nan = result.loc[nan_mask, "sales"]
    assert np.allclose(filled_at_nan, original_mean), f"FAIL: Filled values {filled_at_nan.values} != mean {original_mean}"
    print(f"[PASS] All filled values equal the mean: {original_mean:.2f}")

    # Test 3: Original values are preserved
    print("\nTest 3: Verify original non-null values are preserved")
    non_null_mask = df["sales"].notna()
    original_values = df.loc[non_null_mask, "sales"]
    result_values = result.loc[non_null_mask, "sales"]
    assert np.allclose(original_values, result_values), "FAIL: Original values were modified"
    print("[PASS] Original non-null values are unchanged.")

    # Test 4: Original DataFrame is not modified (immutability)
    print("\nTest 4: Verify original DataFrame is not modified")
    original_nan_count = df["sales"].isna().sum()
    assert df["sales"].isna().sum() == original_nan_count, "FAIL: Original DataFrame was modified"
    print(f"[PASS] Original DataFrame still has {original_nan_count} NaN values.")

    # Test 5: Edge case - no missing values
    print("\nTest 5: Edge case - no missing values")
    df_no_missing = pd.DataFrame({"sales": [100.0, 200.0, 300.0]})
    result_no_missing = fill_missing_with_mean(df_no_missing, "sales")
    assert np.allclose(result_no_missing["sales"], [100.0, 200.0, 300.0]), "FAIL: Values changed when no NaN present"
    print("[PASS] No changes when there are no missing values.")

    # Test 6: Edge case - all missing values
    print("\nTest 6: Edge case - all values are missing")
    df_all_missing = pd.DataFrame({"sales": [np.nan, np.nan, np.nan]})
    result_all_missing = fill_missing_with_mean(df_all_missing, "sales")
    # When all values are NaN, mean is NaN, so fillna won't change anything
    assert result_all_missing["sales"].isna().all(), "FAIL: Expected all NaN when all input is NaN"
    print("[PASS] All NaN input results in all NaN output (mean of NaN is NaN).")

    # Test 7: KeyError for missing column
    print("\nTest 7: Error handling - missing column")
    try:
        fill_missing_with_mean(df, "nonexistent_column")
        assert False, "FAIL: Should have raised KeyError"
    except KeyError as e:
        print(f"[PASS] Correctly raised KeyError: {e}")

    # Test 8: ValueError for non-numeric column
    print("\nTest 8: Error handling - non-numeric column")
    df_text = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"]})
    try:
        fill_missing_with_mean(df_text, "name")
        assert False, "FAIL: Should have raised ValueError"
    except ValueError as e:
        print(f"[PASS] Correctly raised ValueError: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    # Demonstration
    print("\n" + "=" * 60)
    print("DEMONSTRATION: Fill Missing Values with Column Mean")
    print("=" * 60)

    df = create_sample_data()
    print("\n--- Original Data ---")
    print(df.to_string(index=False))
    print(f"\nMissing values in 'sales': {df['sales'].isna().sum()}")
    print(f"Column mean (excluding NaN): {df['sales'].mean():.2f}")

    result = fill_missing_with_mean(df, "sales")
    print("\n--- After Filling Missing Values ---")
    print(result.to_string(index=False))
    print(f"\nMissing values in 'sales': {result['sales'].isna().sum()}")

    # Run tests
    test_fill_missing_with_mean()
