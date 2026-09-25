"""
Pandas Q13: GroupBy, Aggregation, and Sort
=============================================

Problem:
Given a sales dataset, perform groupby operations with multiple aggregations,
then sort the results. This is a common Data Analyst interview question.

Tasks:
1. Group by 'region' and compute: total sales, average sale, count of transactions
2. Group by 'region' and 'product' for a multi-level aggregation
3. Sort results by total sales descending
4. Filter groups with total sales above a threshold
5. Use named aggregations for clean column naming
"""

import pandas as pd
import numpy as np
from datetime import datetime


# ============================================================
# SAMPLE DATA CREATION
# ============================================================

def create_sample_data():
    """Create a realistic sales dataset for practice."""
    np.random.seed(42)
    
    regions = ['North', 'South', 'East', 'West']
    products = ['Widget', 'Gadget', 'Doohickey', 'Thingamajig']
    
    data = {
        'transaction_id': range(1, 101),
        'date': pd.date_range('2024-01-01', periods=100, freq='D'),
        'region': np.random.choice(regions, 100),
        'product': np.random.choice(products, 100),
        'quantity': np.random.randint(1, 20, 100),
        'unit_price': np.random.uniform(10.0, 100.0, 100).round(2),
        'sales_rep': np.random.choice(['Alice', 'Bob', 'Charlie', 'Diana'], 100)
    }
    
    df = pd.DataFrame(data)
    df['total_sale'] = (df['quantity'] * df['unit_price']).round(2)
    return df


# ============================================================
# SOLUTION 1: Basic GroupBy with Multiple Aggregations
# ============================================================

def solution_basic_groupby(df):
    """
    Group by 'region' and compute:
    - total_sales: sum of total_sale
    - avg_sale: mean of total_sale
    - transaction_count: count of transactions
    - max_sale: maximum single sale
    - min_sale: minimum single sale
    
    Sort by total_sales descending.
    """
    result = (
        df.groupby('region')['total_sale']
        .agg(
            total_sales='sum',
            avg_sale='mean',
            transaction_count='count',
            max_sale='max',
            min_sale='min'
        )
        .sort_values('total_sales', ascending=False)
        .round(2)
    )
    
    return result


# ============================================================
# SOLUTION 2: Multi-Level GroupBy (Region + Product)
# ============================================================

def solution_multi_level_groupby(df):
    """
    Group by both 'region' and 'product', compute aggregations,
    then sort by total_sales descending.
    """
    result = (
        df.groupby(['region', 'product'])['total_sale']
        .agg(
            total_sales='sum',
            avg_sale='mean',
            count='count'
        )
        .sort_values('total_sales', ascending=False)
        .round(2)
    )
    
    return result


# ============================================================
# SOLUTION 3: Named Aggregations with Multiple Columns
# ============================================================

def solution_named_agg(df):
    """
    Use named aggregations to compute metrics from multiple columns
    in a single groupby operation.
    """
    result = (
        df.groupby('region')
        .agg(
            total_revenue=('total_sale', 'sum'),
            avg_revenue=('total_sale', 'mean'),
            total_units=('quantity', 'sum'),
            avg_unit_price=('unit_price', 'mean'),
            num_transactions=('transaction_id', 'count'),
            unique_products=('product', 'nunique')
        )
        .sort_values('total_revenue', ascending=False)
        .round(2)
    )
    
    return result


# ============================================================
# SOLUTION 4: Filter Groups with Threshold
# ============================================================

def solution_filter_groups(df, threshold=5000):
    """
    Group by region, compute total sales, then filter to only
    show regions where total sales exceed the threshold.
    """
    grouped = df.groupby('region')['total_sale'].agg(
        total_sales='sum',
        avg_sale='mean',
        count='count'
    )
    
    # Filter groups above threshold
    filtered = grouped[grouped['total_sales'] > threshold]
    
    # Sort descending
    result = filtered.sort_values('total_sales', ascending=False).round(2)
    
    return result


# ============================================================
# SOLUTION 5: Top N Products per Region
# ============================================================

def solution_top_n_per_group(df, n=2):
    """
    For each region, find the top N products by total sales.
    This uses groupby + rank + filter pattern.
    """
    # Compute total sales per region-product combination
    region_product = (
        df.groupby(['region', 'product'])['total_sale']
        .sum()
        .reset_index()
        .rename(columns={'total_sale': 'total_sales'})
    )
    
    # Rank products within each region
    region_product['rank'] = (
        region_product
        .groupby('region')['total_sales']
        .rank(ascending=False, method='first')
    )
    
    # Keep only top N per region
    result = (
        region_product[region_product['rank'] <= n]
        .sort_values(['region', 'rank'])
        .drop(columns='rank')
        .reset_index(drop=True)
    )
    
    return result


# ============================================================
# SOLUTION 6: Time-Based GroupBy with Resample
# ============================================================

def solution_time_groupby(df):
    """
    Group sales by month and region, compute monthly totals,
    then sort chronologically.
    """
    df_copy = df.copy()
    df_copy['month'] = df_copy['date'].dt.to_period('M')
    
    result = (
        df_copy.groupby(['month', 'region'])['total_sale']
        .agg(
            monthly_sales='sum',
            avg_daily_sale='mean',
            transaction_count='count'
        )
        .sort_values(['month', 'monthly_sales'], ascending=[True, False])
        .round(2)
    )
    
    return result


# ============================================================
# SOLUTION 7: Pivot Table with Aggregation
# ============================================================

def solution_pivot_table(df):
    """
    Create a pivot table showing total sales by region (rows)
    and product (columns), with sum as aggregation.
    """
    pivot = pd.pivot_table(
        df,
        values='total_sale',
        index='region',
        columns='product',
        aggfunc='sum',
        fill_value=0,
        margins=True,
        margins_name='Total'
    )
    
    # Sort by Total column descending
    result = pivot.sort_values('Total', ascending=False).round(2)
    
    return result


# ============================================================
# TESTS
# ============================================================

def run_tests():
    """Run comprehensive tests on all solutions."""
    df = create_sample_data()
    
    print("=" * 60)
    print("PANDAS Q13: GROUPBY, AGGREGATION, AND SORT - TESTS")
    print("=" * 60)
    
    # Test 1: Basic GroupBy
    print("\n--- Test 1: Basic GroupBy ---")
    result1 = solution_basic_groupby(df)
    assert len(result1) == 4, f"Expected 4 regions, got {len(result1)}"
    assert 'total_sales' in result1.columns
    assert 'avg_sale' in result1.columns
    assert 'transaction_count' in result1.columns
    assert result1['total_sales'].is_monotonic_decreasing, "Not sorted descending"
    print(f"PASS: {len(result1)} regions, sorted by total_sales")
    print(result1)
    
    # Test 2: Multi-Level GroupBy
    print("\n--- Test 2: Multi-Level GroupBy ---")
    result2 = solution_multi_level_groupby(df)
    assert isinstance(result2.index, pd.MultiIndex), "Should have MultiIndex"
    assert len(result2) <= 16, "Max 4 regions x 4 products = 16"
    print(f"PASS: {len(result2)} region-product combinations")
    print(result2.head(10))
    
    # Test 3: Named Aggregations
    print("\n--- Test 3: Named Aggregations ---")
    result3 = solution_named_agg(df)
    expected_cols = ['total_revenue', 'avg_revenue', 'total_units',
                     'avg_unit_price', 'num_transactions', 'unique_products']
    for col in expected_cols:
        assert col in result3.columns, f"Missing column: {col}"
    print(f"PASS: All {len(expected_cols)} columns present")
    print(result3)
    
    # Test 4: Filter Groups
    print("\n--- Test 4: Filter Groups (threshold=5000) ---")
    result4 = solution_filter_groups(df, threshold=5000)
    if len(result4) > 0:
        assert (result4['total_sales'] > 5000).all(), "All should exceed threshold"
    print(f"PASS: {len(result4)} regions above threshold")
    print(result4)
    
    # Test 5: Top N per Group
    print("\n--- Test 5: Top 2 Products per Region ---")
    result5 = solution_top_n_per_group(df, n=2)
    assert len(result5) <= 8, "Max 4 regions x 2 products = 8"
    for region in df['region'].unique():
        region_rows = result5[result5['region'] == region]
        assert len(region_rows) <= 2, f"Region {region} has more than 2 products"
    print(f"PASS: {len(result5)} rows (top 2 per region)")
    print(result5)
    
    # Test 6: Time-Based GroupBy
    print("\n--- Test 6: Time-Based GroupBy ---")
    result6 = solution_time_groupby(df)
    assert isinstance(result6.index, pd.MultiIndex)
    print(f"PASS: {len(result6)} month-region combinations")
    print(result6.head(10))
    
    # Test 7: Pivot Table
    print("\n--- Test 7: Pivot Table ---")
    result7 = solution_pivot_table(df)
    assert 'Total' in result7.columns, "Should have Total column"
    assert 'Total' in result7.index, "Should have Total row"
    print(f"PASS: Pivot table with margins")
    print(result7)
    
    # Test 8: Verify aggregation correctness
    print("\n--- Test 8: Aggregation Correctness ---")
    manual_total = df[df['region'] == 'North']['total_sale'].sum()
    result_total = result1.loc['North', 'total_sales']
    assert abs(manual_total - result_total) < 0.01, \
        f"Mismatch: manual={manual_total}, result={result_total}"
    print(f"PASS: North region total verified: {result_total:.2f}")
    
    # Test 9: Verify sort order
    print("\n--- Test 9: Sort Order Verification ---")
    sales_values = result1['total_sales'].values
    for i in range(len(sales_values) - 1):
        assert sales_values[i] >= sales_values[i + 1], "Not sorted descending"
    print("PASS: Results correctly sorted descending")
    
    # Test 10: Edge case - empty groupby
    print("\n--- Test 10: Edge Cases ---")
    empty_df = pd.DataFrame(columns=df.columns)
    result_empty = solution_basic_groupby(empty_df)
    assert len(result_empty) == 0, "Empty df should produce empty result"
    print("PASS: Empty DataFrame handled correctly")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == '__main__':
    # Create sample data
    df = create_sample_data()
    
    print("=" * 60)
    print("PANDAS Q13: GROUPBY, AGGREGATION, AND SORT")
    print("=" * 60)
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nBasic stats:")
    print(df[['quantity', 'unit_price', 'total_sale']].describe())
    
    # Run all solutions
    print("\n" + "=" * 60)
    print("SOLUTION 1: Basic GroupBy with Multiple Aggregations")
    print("=" * 60)
    print(solution_basic_groupby(df))
    
    print("\n" + "=" * 60)
    print("SOLUTION 2: Multi-Level GroupBy (Region + Product)")
    print("=" * 60)
    print(solution_multi_level_groupby(df))
    
    print("\n" + "=" * 60)
    print("SOLUTION 3: Named Aggregations")
    print("=" * 60)
    print(solution_named_agg(df))
    
    print("\n" + "=" * 60)
    print("SOLUTION 4: Filter Groups Above Threshold")
    print("=" * 60)
    print(solution_filter_groups(df, threshold=5000))
    
    print("\n" + "=" * 60)
    print("SOLUTION 5: Top 2 Products per Region")
    print("=" * 60)
    print(solution_top_n_per_group(df, n=2))
    
    print("\n" + "=" * 60)
    print("SOLUTION 6: Time-Based GroupBy (Monthly)")
    print("=" * 60)
    print(solution_time_groupby(df))
    
    print("\n" + "=" * 60)
    print("SOLUTION 7: Pivot Table")
    print("=" * 60)
    print(solution_pivot_table(df))
    
    # Run tests
    print("\n" + "=" * 60)
    print("RUNNING TESTS")
    print("=" * 60)
    run_tests()
