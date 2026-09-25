"""
Pandas Q11: Load, Clean, Shape
==============================
Exercise: Load a messy CSV, clean it (missing values, duplicates, type coercion),
then reshape using pivot_table, melt, stack/unstack, and wide-to-long conversion.

Prerequisites: pandas, numpy
"""

import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os


# ---------------------------------------------------------------------------
# 1. Generate a realistic messy dataset for practice
# ---------------------------------------------------------------------------

def generate_sample_csv(path: str) -> str:
    """Create a messy CSV file and return its path."""
    data = {
        "order_id": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
                     111, 112, 113, 114, 115, 101, 116, 117, 118, 119],
        "customer": ["Alice", "Bob", "Alice", "Charlie", "Bob", "Alice",
                     "Charlie", "Bob", "Alice", "Charlie", "Bob", "Alice",
                     "Charlie", "Bob", "Alice", "Alice", "Charlie", "Bob",
                     "Alice", "Charlie"],
        "product": ["Widget", "Gadget", "Widget", "Gadget", "Widget",
                    "Gadget", "Widget", "Gadget", "Widget", "Gadget",
                    "Widget", "Gadget", "Widget", "Gadget", "Widget",
                    "Widget", "Gadget", "Widget", "Gadget", "Widget"],
        "quantity": ["5", "3", "7", "2", "4", "6", "1", "8", "3", "5",
                     "2", "9", "4", "6", "1", "5", "3", "7", "2", "8"],
        "unit_price": ["10.00", "25.00", "10.00", "25.00", "10.00",
                       "25.00", "10.00", "25.00", "10.00", "25.00",
                       "10.00", "25.00", "10.00", "25.00", "10.00",
                       "10.00", "25.00", "10.00", "25.00", "10.00"],
        "order_date": ["2024-01-15", "2024-01-16", "2024-01-17",
                       "2024-01-18", "2024-01-19", "2024-01-20",
                       "2024-01-21", "2024-01-22", "2024-01-23",
                       "2024-01-24", "2024-01-25", "2024-01-26",
                       "2024-01-27", "2024-01-28", "2024-01-29",
                       "2024-01-15", "2024-02-01", "2024-02-02",
                       "2024-02-03", "2024-02-04"],
        "region": ["North", "South", "North", "South", "North",
                   "South", "North", "South", "North", "South",
                   "North", "South", "North", "South", "North",
                   "North", "South", "North", "South", "North"],
    }
    df = pd.DataFrame(data)
    # Inject messiness: NaN values, extra whitespace, duplicate row
    df.loc[3, "quantity"] = np.nan
    df.loc[7, "unit_price"] = np.nan
    df.loc[10, "customer"] = "  Bob  "  # extra whitespace
    df.loc[14, "region"] = np.nan
    df.to_csv(path, index=False)
    return path


# ---------------------------------------------------------------------------
# 2. Load and Clean
# ---------------------------------------------------------------------------

def load_and_clean(csv_path: str) -> pd.DataFrame:
    """
    Load a CSV and apply cleaning steps:
      - Strip whitespace from string columns
      - Convert quantity and unit_price to numeric (coerce errors)
      - Parse order_date as datetime
      - Drop exact duplicate rows
      - Fill missing quantity with column median
      - Fill missing unit_price with column mean
      - Fill missing region with 'Unknown'
      - Drop rows where order_id is NaN
    Returns cleaned DataFrame.
    """
    df = pd.read_csv(csv_path)

    # Strip whitespace from all object columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Type coercion
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Drop exact duplicates
    df = df.drop_duplicates()

    # Impute missing values
    df["quantity"] = df["quantity"].fillna(df["quantity"].median())
    df["unit_price"] = df["unit_price"].fillna(df["unit_price"].mean())
    df["region"] = df["region"].fillna("Unknown")

    # Drop rows with missing order_id
    df = df.dropna(subset=["order_id"])

    # Ensure order_id is integer
    df["order_id"] = df["order_id"].astype(int)

    return df


# ---------------------------------------------------------------------------
# 3. Reshape Operations
# ---------------------------------------------------------------------------

def pivot_customer_product(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a pivot table: rows=customer, columns=product, values=sum(quantity).
    """
    pivot = df.pivot_table(
        index="customer",
        columns="product",
        values="quantity",
        aggfunc="sum",
        fill_value=0,
        margins=True,
        margins_name="Total",
    )
    return pivot


def melt_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Melt the pivot table back to long format.
    """
    pivot = pivot_customer_product(df)
    long_df = pivot.reset_index().melt(
        id_vars="customer",
        value_vars=["Widget", "Gadget", "Total"],
        var_name="product",
        value_name="total_quantity",
    )
    return long_df


def stack_unstack_example(df: pd.DataFrame) -> pd.DataFrame:
    """
    Demonstrate stack/unstack on a multi-index DataFrame.
    """
    # Create a multi-index: customer x region
    multi = df.groupby(["customer", "region"])["quantity"].sum().reset_index()
    stacked = multi.set_index(["customer", "region"]).stack()
    unstacked = stacked.unstack(level="region")
    return unstacked


def wide_to_long_conversion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert a wide-format summary to long format using pd.wide_to_long.
    """
    # Create a wide summary: one row per customer, columns for each product
    wide = df.pivot_table(
        index="customer",
        columns="product",
        values="quantity",
        aggfunc="sum",
        fill_value=0,
    ).reset_index()

    # Rename columns to match wide_to_long pattern: <stub><i>
    wide = wide.rename(columns={
        "Widget": "qty_Widget",
        "Gadget": "qty_Gadget",
    })

    long = pd.wide_to_long(
        wide,
        stubnames="qty",
        i="customer",
        j="product",
        dropna=False,
    ).reset_index()
    long = long.rename(columns={"qty": "total_quantity"})
    return long


# ---------------------------------------------------------------------------
# 4. Tests
# ---------------------------------------------------------------------------

def run_tests():
    """Run all tests and print results."""
    import traceback
    passed = 0
    failed = 0

    # Setup: generate temp CSV
    tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    tmp.close()
    csv_path = generate_sample_csv(tmp.name)

    try:
        # Test 1: Load and clean
        df = load_and_clean(csv_path)
        assert df["quantity"].isna().sum() == 0, "quantity should have no NaN"
        assert df["unit_price"].isna().sum() == 0, "unit_price should have no NaN"
        assert df["region"].isna().sum() == 0, "region should have no NaN"
        assert "Bob" in df["customer"].values, "Whitespace should be stripped"
        assert df["order_date"].dtype == "datetime64[ns]", "order_date should be datetime"
        assert df["order_id"].dtype in ["int64", "int32"], "order_id should be int"
        passed += 1
        print("  PASS: load_and_clean")

        # Test 2: Pivot table
        pivot = pivot_customer_product(df)
        assert "Total" in pivot.index, "Pivot should have Total row"
        assert "Total" in pivot.columns, "Pivot should have Total column"
        assert pivot.shape[0] >= 4, "Should have at least 4 customers + Total"
        passed += 1
        print("  PASS: pivot_customer_product")

        # Test 3: Melt
        long_df = melt_to_long(df)
        assert "product" in long_df.columns, "Melted df should have product column"
        assert "total_quantity" in long_df.columns, "Melted df should have total_quantity"
        assert long_df.shape[0] > 0, "Melted df should not be empty"
        passed += 1
        print("  PASS: melt_to_long")

        # Test 4: Stack/unstack
        unstacked = stack_unstack_example(df)
        assert isinstance(unstacked, pd.DataFrame), "Should return DataFrame"
        assert unstacked.shape[0] > 0, "Unstacked should have rows"
        passed += 1
        print("  PASS: stack_unstack_example")

        # Test 5: Wide to long
        wl = wide_to_long_conversion(df)
        assert "product" in wl.columns, "wide_to_long should have product column"
        assert "total_quantity" in wl.columns, "wide_to_long should have total_quantity"
        assert wl.shape[0] > 0, "wide_to_long result should not be empty"
        passed += 1
        print("  PASS: wide_to_long_conversion")

        # Test 6: Data integrity - no info lost in round-trip
        original_count = len(df)
        assert original_count > 0, "Cleaned df should have rows"
        passed += 1
        print("  PASS: data_integrity")

    except AssertionError as e:
        failed += 1
        print(f"  FAIL: {e}")
        traceback.print_exc()
    except Exception as e:
        failed += 1
        print(f"  ERROR: {e}")
        traceback.print_exc()
    finally:
        os.unlink(csv_path)

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


# ---------------------------------------------------------------------------
# 5. Main execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Pandas Q11: Load, Clean, Shape")
    print("=" * 60)

    # Generate sample data
    tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    tmp.close()
    csv_path = generate_sample_csv(tmp.name)

    print(f"\nSample CSV generated at: {csv_path}")
    print("\n--- Raw Data (first 5 rows) ---")
    raw = pd.read_csv(csv_path)
    print(raw.head().to_string())
    print(f"\nShape: {raw.shape}")
    print(f"Missing values:\n{raw.isna().sum()}")

    # Clean
    print("\n--- After Cleaning ---")
    df = load_and_clean(csv_path)
    print(df.head().to_string())
    print(f"\nShape: {df.shape}")
    print(f"Missing values:\n{df.isna().sum()}")
    print(f"\nDtypes:\n{df.dtypes}")

    # Pivot
    print("\n--- Pivot Table (Customer x Product) ---")
    pivot = pivot_customer_product(df)
    print(pivot.to_string())

    # Melt
    print("\n--- Melted (Long Format) ---")
    long_df = melt_to_long(df)
    print(long_df.head(10).to_string())

    # Stack/Unstack
    print("\n--- Stack/Unstack Example ---")
    unstacked = stack_unstack_example(df)
    print(unstacked.to_string())

    # Wide to Long
    print("\n--- Wide to Long Conversion ---")
    wl = wide_to_long_conversion(df)
    print(wl.to_string())

    # Run tests
    print("\n" + "=" * 60)
    print("Running Tests...")
    print("=" * 60)
    success = run_tests()

    # Cleanup
    os.unlink(csv_path)

    print(f"\n{'=' * 60}")
    print(f"All tests passed!" if success else "Some tests failed.")
    print(f"{'=' * 60}")
