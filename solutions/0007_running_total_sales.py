"""
0007_running_total_sales.py
=============================
Calculate running total of sales per day using SUM() OVER (ORDER BY date).

This solution demonstrates:
- SQL window function: SUM() OVER (ORDER BY date)
- Python/pandas equivalent using cumsum()
- Unit tests with sample data

Interview Context:
- Window functions are a core SQL topic for data analyst interviews
- Running totals are common in financial/sales reporting
- Understanding both SQL and pandas approaches shows versatility
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ============================================================
# SQL SOLUTION (for reference / interview explanation)
# ============================================================

SQL_QUERY = """
-- Running total of sales per day
-- Uses SUM() window function with ORDER BY date

SELECT
    sale_date,
    daily_sales,
    SUM(daily_sales) OVER (
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_sales
FROM
    daily_sales
ORDER BY
    sale_date;

-- Alternative: if you want running total per region
SELECT
    sale_date,
    region,
    daily_sales,
    SUM(daily_sales) OVER (
        PARTITION BY region
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_sales
FROM
    daily_sales
ORDER BY
    region,
    sale_date;
"""


# ============================================================
# PYTHON/PANDAS SOLUTION
# ============================================================

def calculate_running_total(df: pd.DataFrame, date_col: str = 'sale_date',
                             sales_col: str = 'daily_sales') -> pd.DataFrame:
    """
    Calculate running total of sales per day.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with date and sales columns.
    date_col : str
        Name of the date column (default: 'sale_date').
    sales_col : str
        Name of the sales column (default: 'daily_sales').

    Returns
    -------
    pd.DataFrame
        DataFrame with an added 'running_total_sales' column.

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'sale_date': ['2023-01-01', '2023-01-02', '2023-01-03'],
    ...     'daily_sales': [100, 200, 150]
    ... })
    >>> result = calculate_running_total(df)
    >>> print(result['running_total_sales'].tolist())
    [100, 300, 450]
    """
    result = df.copy()
    result[date_col] = pd.to_datetime(result[date_col])
    result = result.sort_values(date_col).reset_index(drop=True)
    result['running_total_sales'] = result[sales_col].cumsum()
    return result


def calculate_running_total_by_region(df: pd.DataFrame, date_col: str = 'sale_date',
                                       sales_col: str = 'daily_sales',
                                       region_col: str = 'region') -> pd.DataFrame:
    """
    Calculate running total of sales per day, partitioned by region.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with date, sales, and region columns.
    date_col : str
        Name of the date column (default: 'sale_date').
    sales_col : str
        Name of the sales column (default: 'daily_sales').
    region_col : str
        Name of the region column (default: 'region').

    Returns
    -------
    pd.DataFrame
        DataFrame with an added 'running_total_sales' column.
    """
    result = df.copy()
    result[date_col] = pd.to_datetime(result[date_col])
    result = result.sort_values([region_col, date_col]).reset_index(drop=True)
    result['running_total_sales'] = result.groupby(region_col)[sales_col].cumsum()
    return result


def calculate_running_total_with_window(df: pd.DataFrame, date_col: str = 'sale_date',
                                         sales_col: str = 'daily_sales',
                                         window_days: int = 7) -> pd.DataFrame:
    """
    Calculate rolling window total of sales (e.g., 7-day rolling sum).

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with date and sales columns.
    date_col : str
        Name of the date column (default: 'sale_date').
    sales_col : str
        Name of the sales column (default: 'daily_sales').
    window_days : int
        Number of days in the rolling window (default: 7).

    Returns
    -------
    pd.DataFrame
        DataFrame with an added 'rolling_total_sales' column.
    """
    result = df.copy()
    result[date_col] = pd.to_datetime(result[date_col])
    result = result.sort_values(date_col).reset_index(drop=True)
    result['rolling_total_sales'] = result[sales_col].rolling(
        window=window_days, min_periods=1
    ).sum()
    return result


# ============================================================
# SAMPLE DATA GENERATION
# ============================================================

def generate_sample_data(num_days: int = 30, start_date: str = '2023-01-01') -> pd.DataFrame:
    """
    Generate sample daily sales data for testing.

    Parameters
    ----------
    num_days : int
        Number of days to generate (default: 30).
    start_date : str
        Start date in YYYY-MM-DD format (default: '2023-01-01').

    Returns
    -------
    pd.DataFrame
        DataFrame with sale_date and daily_sales columns.
    """
    np.random.seed(42)
    dates = pd.date_range(start=start_date, periods=num_days, freq='D')
    daily_sales = np.random.randint(50, 500, size=num_days)
    return pd.DataFrame({
        'sale_date': dates,
        'daily_sales': daily_sales
    })


def generate_sample_data_with_regions(num_days: int = 15, num_regions: int = 3,
                                        start_date: str = '2023-01-01') -> pd.DataFrame:
    """
    Generate sample daily sales data with regions for testing.

    Parameters
    ----------
    num_days : int
        Number of days per region (default: 15).
    num_regions : int
        Number of regions (default: 3).
    start_date : str
        Start date in YYYY-MM-DD format (default: '2023-01-01').

    Returns
    -------
    pd.DataFrame
        DataFrame with sale_date, region, and daily_sales columns.
    """
    np.random.seed(42)
    regions = [f'Region_{i}' for i in range(1, num_regions + 1)]
    dates = pd.date_range(start=start_date, periods=num_days, freq='D')

    data = []
    for region in regions:
        for date in dates:
            data.append({
                'sale_date': date,
                'region': region,
                'daily_sales': np.random.randint(50, 500)
            })

    return pd.DataFrame(data)


# ============================================================
# UNIT TESTS
# ============================================================

def test_running_total_basic():
    """Test basic running total calculation."""
    df = pd.DataFrame({
        'sale_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'daily_sales': [100, 200, 150, 300]
    })

    result = calculate_running_total(df)

    expected = [100, 300, 450, 750]
    assert result['running_total_sales'].tolist() == expected, \
        f"Expected {expected}, got {result['running_total_sales'].tolist()}"
    print("✓ test_running_total_basic PASSED")


def test_running_total_single_row():
    """Test running total with a single row."""
    df = pd.DataFrame({
        'sale_date': ['2023-01-01'],
        'daily_sales': [500]
    })

    result = calculate_running_total(df)

    assert result['running_total_sales'].tolist() == [500]
    print("✓ test_running_total_single_row PASSED")


def test_running_total_unsorted_input():
    """Test that unsorted input is handled correctly."""
    df = pd.DataFrame({
        'sale_date': ['2023-01-03', '2023-01-01', '2023-01-02'],
        'daily_sales': [150, 100, 200]
    })

    result = calculate_running_total(df)

    expected = [100, 300, 450]
    assert result['running_total_sales'].tolist() == expected, \
        f"Expected {expected}, got {result['running_total_sales'].tolist()}"
    print("✓ test_running_total_unsorted_input PASSED")


def test_running_total_by_region():
    """Test running total partitioned by region."""
    df = pd.DataFrame({
        'sale_date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02'],
        'region': ['A', 'B', 'A', 'B'],
        'daily_sales': [100, 200, 150, 250]
    })

    result = calculate_running_total_by_region(df)

    region_a = result[result['region'] == 'A']['running_total_sales'].tolist()
    region_b = result[result['region'] == 'B']['running_total_sales'].tolist()

    assert region_a == [100, 250], f"Region A expected [100, 250], got {region_a}"
    assert region_b == [200, 450], f"Region B expected [200, 450], got {region_b}"
    print("✓ test_running_total_by_region PASSED")


def test_running_total_with_window():
    """Test rolling window total calculation."""
    df = pd.DataFrame({
        'sale_date': ['2023-01-01', '2023-01-02', '2023-01-03',
                      '2023-01-04', '2023-01-05'],
        'daily_sales': [100, 200, 150, 300, 250]
    })

    result = calculate_running_total_with_window(df, window_days=3)

    expected = [100, 300, 450, 650, 700]
    assert result['rolling_total_sales'].tolist() == expected, \
        f"Expected {expected}, got {result['rolling_total_sales'].tolist()}"
    print("✓ test_running_total_with_window PASSED")


def test_running_total_preserves_original():
    """Test that original DataFrame is not modified."""
    df = pd.DataFrame({
        'sale_date': ['2023-01-01', '2023-01-02'],
        'daily_sales': [100, 200]
    })

    original_copy = df.copy()
    _ = calculate_running_total(df)

    assert df.equals(original_copy), "Original DataFrame was modified!"
    print("✓ test_running_total_preserves_original PASSED")


def test_running_total_with_large_dataset():
    """Test running total with a larger dataset."""
    df = generate_sample_data(num_days=100)
    result = calculate_running_total(df)

    # Verify the last running total equals the sum of all daily sales
    expected_total = df['daily_sales'].sum()
    actual_total = result['running_total_sales'].iloc[-1]

    assert actual_total == expected_total, \
        f"Expected total {expected_total}, got {actual_total}"

    # Verify running total is monotonically non-decreasing
    running_totals = result['running_total_sales'].values
    for i in range(1, len(running_totals)):
        assert running_totals[i] >= running_totals[i-1], \
            f"Running total decreased at index {i}"

    print("✓ test_running_total_with_large_dataset PASSED")


def test_running_total_zero_sales():
    """Test running total with zero sales values."""
    df = pd.DataFrame({
        'sale_date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'daily_sales': [0, 0, 100]
    })

    result = calculate_running_total(df)

    expected = [0, 0, 100]
    assert result['running_total_sales'].tolist() == expected
    print("✓ test_running_total_zero_sales PASSED")


# ============================================================
# MAIN EXECUTION
# ============================================================

def run_all_tests():
    """Run all unit tests."""
    print("=" * 60)
    print("Running Tests for 0007_running_total_sales.py")
    print("=" * 60)
    print()

    test_running_total_basic()
    test_running_total_single_row()
    test_running_total_unsorted_input()
    test_running_total_by_region()
    test_running_total_with_window()
    test_running_total_preserves_original()
    test_running_total_with_large_dataset()
    test_running_total_zero_sales()

    print()
    print("=" * 60)
    print("All 8 tests PASSED!")
    print("=" * 60)


def demonstrate():
    """Demonstrate the running total calculation with sample data."""
    print("=" * 60)
    print("DEMONSTRATION: Running Total of Sales Per Day")
    print("=" * 60)
    print()

    # Generate sample data
    df = generate_sample_data(num_days=10)
    print("Input Data (first 10 days):")
    print(df.to_string(index=False))
    print()

    # Calculate running total
    result = calculate_running_total(df)
    print("Result with Running Total:")
    print(result.to_string(index=False))
    print()

    # Demonstrate by region
    print("-" * 60)
    print("Running Total by Region:")
    print("-" * 60)
    df_regions = generate_sample_data_with_regions(num_days=5, num_regions=2)
    result_regions = calculate_running_total_by_region(df_regions)
    print(result_regions.to_string(index=False))
    print()

    # Demonstrate rolling window
    print("-" * 60)
    print("7-Day Rolling Window Total:")
    print("-" * 60)
    df_window = generate_sample_data(num_days=10)
    result_window = calculate_running_total_with_window(df_window, window_days=7)
    print(result_window.to_string(index=False))
    print()

    # Print SQL query for reference
    print("-" * 60)
    print("SQL Query (for interview reference):")
    print("-" * 60)
    print(SQL_QUERY)


if __name__ == '__main__':
    demonstrate()
    print()
    run_all_tests()
