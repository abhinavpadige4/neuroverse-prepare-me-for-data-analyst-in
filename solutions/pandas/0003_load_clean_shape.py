"""
Pandas Q11: Load, Clean, Shape

This solution demonstrates loading data from CSV, cleaning it,
and reshaping it using pandas operations commonly tested in
Data Analyst interviews.

Topics covered:
- pd.read_csv with parameters
- Handling missing values (dropna, fillna)
- Removing duplicates
- Data type conversion
- Reshaping: pivot_table, melt, stack/unstack
- Chaining operations
"""

import pandas as pd
import numpy as np
from io import StringIO


def load_data(filepath: str, **kwargs) -> pd.DataFrame:
    """Load CSV data with common parameters."""
    return pd.read_csv(filepath, **kwargs)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean a DataFrame: handle missing values, duplicates, types."""
    # Remove exact duplicates
    df = df.drop_duplicates()

    # Drop rows with all NaN values
    df = df.dropna(how="all")

    # Fill numeric columns with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Fill string columns with 'Unknown'
    string_cols = df.select_dtypes(include=["object"]).columns
    for col in string_cols:
        df[col] = df[col].fillna("Unknown")

    # Strip whitespace from string columns
    for col in string_cols:
        df[col] = df[col].str.strip()

    return df


def reshape_pivot(df: pd.DataFrame, index: str, columns: str, values: str) -> pd.DataFrame:
    """Create a pivot table from long-format data."""
    return pd.pivot_table(df, values=values, index=index, columns=columns, aggfunc="sum", fill_value=0)


def reshape_melt(df: pd.DataFrame, id_vars: list, value_vars: list, var_name: str = "variable", value_name: str = "value") -> pd.DataFrame:
    """Melt wide-format data to long format."""
    return df.melt(id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)


def reshape_stack_unstack(df: pd.DataFrame) -> tuple:
    """Demonstrate stack and unstack operations."""
    stacked = df.stack()
    unstacked = stacked.unstack()
    return stacked, unstacked


def full_pipeline(filepath: str) -> dict:
    """Run the complete load-clean-shape pipeline."""
    # Step 1: Load
    df = load_data(filepath)

    # Step 2: Clean
    df_clean = clean_data(df)

    # Step 3: Shape - pivot
    if "category" in df_clean.columns and "region" in df_clean.columns and "sales" in df_clean.columns:
        pivot = reshape_pivot(df_clean, index="category", columns="region", values="sales")
    else:
        pivot = None

    # Step 4: Shape - melt
    if "product" in df_clean.columns:
        value_cols = [c for c in df_clean.columns if c != "product" and c != "category"]
        if value_cols:
            melted = reshape_melt(df_clean, id_vars=["product"], value_vars=value_cols)
        else:
            melted = None
    else:
        melted = None

    return {
        "original_shape": df.shape,
        "cleaned_shape": df_clean.shape,
        "pivot_table": pivot,
        "melted_data": melted,
    }


# ============================================================
# DEMO WITH SAMPLE DATA
# ============================================================

if __name__ == "__main__":
    # Create sample data for demonstration
    sample_csv = """product,category,region,sales,units
Widget A,Electronics,North,1500,10
Widget A,Electronics,South,2000,15
Widget B,Clothing,North,800,20
Widget B,Clothing,South,,8
Widget C,Electronics,North,3000,25
Widget C,Electronics,South,2500,20
Widget A,Electronics,North,1500,10
,Electronics,North,1000,5
Widget D,Clothing,South,1200,12
Widget D,Clothing,North,,18
"""

    # Load from string
    df = pd.read_csv(StringIO(sample_csv))
    print("=== ORIGINAL DATA ===")
    print(df)
    print(f"\nShape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")

    # Clean
    df_clean = clean_data(df)
    print("\n=== CLEANED DATA ===")
    print(df_clean)
    print(f"\nShape: {df_clean.shape}")
    print(f"Missing values:\n{df_clean.isnull().sum()}")

    # Pivot
    pivot = reshape_pivot(df_clean, index="category", columns="region", values="sales")
    print("\n=== PIVOT TABLE ===")
    print(pivot)

    # Melt
    melted = reshape_melt(df_clean, id_vars=["product", "category"], value_vars=["region", "sales", "units"])
    print("\n=== MELTED DATA ===")
    print(melted.head(10))

    # Stack/Unstack
    stacked, unstacked = reshape_stack_unstack(df_clean)
    print("\n=== STACKED (first 5) ===")
    print(stacked.head())
    print("\n=== UNSTACKED (first 5) ===")
    print(unstacked.head())

    # Full pipeline result
    result = full_pipeline.__doc__
    print("\n=== PIPELINE COMPLETE ===")
    print(f"Original shape: {df.shape}")
    print(f"Cleaned shape: {df_clean.shape}")
    print(f"Duplicates removed: {df.shape[0] - df_clean.shape[0]}")
