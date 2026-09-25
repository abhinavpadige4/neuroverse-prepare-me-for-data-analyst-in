"""
0011_merge_left.py
Merge two DataFrames on 'id' column using how='left'.

Data Analyst Interview Prep - Day 4 (Python/Pandas)
"""

import pandas as pd
import numpy as np


def create_sample_data():
    """Create sample DataFrames for demonstration."""
    customers = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'email': [
            'alice@example.com',
            'bob@example.com',
            'charlie@example.com',
            'diana@example.com',
            'eve@example.com'
        ]
    })

    orders = pd.DataFrame({
        'id': [1, 2, 3, 3, 4],
        'order_date': ['2023-01-15', '2023-02-20', '2023-01-10', '2023-03-05', '2023-02-28'],
        'amount': [250.00, 150.00, 300.00, 200.00, 400.00]
    })

    return customers, orders


def merge_left(customers_df, orders_df):
    """
    Merge two DataFrames on 'id' column using how='left'.

    A left merge keeps all rows from the left DataFrame (customers)
    and matches rows from the right DataFrame (orders). If no match
    is found, NaN values are filled for the right DataFrame columns.

    Parameters:
        customers_df (pd.DataFrame): Left DataFrame with customer info.
        orders_df (pd.DataFrame): Right DataFrame with order info.

    Returns:
        pd.DataFrame: Merged DataFrame with all customer rows and matched orders.
    """
    merged = pd.merge(
        customers_df,
        orders_df,
        on='id',
        how='left'
    )
    return merged


def merge_left_with_suffix(customers_df, orders_df):
    """
    Merge with suffixes to handle overlapping column names.

    Parameters:
        customers_df (pd.DataFrame): Left DataFrame.
        orders_df (pd.DataFrame): Right DataFrame.

    Returns:
        pd.DataFrame: Merged DataFrame with suffixed duplicate columns.
    """
    merged = pd.merge(
        customers_df,
        orders_df,
        on='id',
        how='left',
        suffixes=('_customer', '_order')
    )
    return merged


def merge_left_indicator(customers_df, orders_df):
    """
    Merge with _merge indicator to show match status.

    Parameters:
        customers_df (pd.DataFrame): Left DataFrame.
        orders_df (pd.DataFrame): Right DataFrame.

    Returns:
        pd.DataFrame: Merged DataFrame with _merge column indicating match type.
    """
    merged = pd.merge(
        customers_df,
        orders_df,
        on='id',
        how='left',
        indicator=True
    )
    return merged


def analyze_merge_result(merged_df):
    """
    Analyze the merge result: count matches, unmatched rows, etc.

    Parameters:
        merged_df (pd.DataFrame): Merged DataFrame.

    Returns:
        dict: Summary statistics about the merge.
    """
    total_rows = len(merged_df)
    matched_rows = merged_df['amount'].notna().sum()
    unmatched_rows = merged_df['amount'].isna().sum()
    match_rate = (matched_rows / total_rows) * 100 if total_rows > 0 else 0

    return {
        'total_rows': total_rows,
        'matched_rows': int(matched_rows),
        'unmatched_rows': int(unmatched_rows),
        'match_rate_percent': round(match_rate, 2)
    }


def test_merge_left():
    """Run tests to verify merge_left functionality."""
    print("=" * 60)
    print("TESTING: merge_left")
    print("=" * 60)

    # Test 1: Basic left merge
    print("\n--- Test 1: Basic Left Merge ---")
    customers, orders = create_sample_data()
    merged = merge_left(customers, orders)

    assert len(merged) == 6, f"Expected 6 rows (5 customers, Charlie has 2 orders), got {len(merged)}"
    assert 'name' in merged.columns, "Missing 'name' column"
    assert 'amount' in merged.columns, "Missing 'amount' column"
    assert 'order_date' in merged.columns, "Missing 'order_date' column"

    # Eve (id=5) should have NaN for order columns
    eve_row = merged[merged['id'] == 5]
    assert eve_row['amount'].isna().all(), "Eve should have NaN amount (no orders)"
    assert eve_row['order_date'].isna().all(), "Eve should have NaN order_date"

    # Alice (id=1) should have matched order
    alice_row = merged[merged['id'] == 1]
    assert alice_row['amount'].notna().all(), "Alice should have a matched amount"

    print(f"Merged shape: {merged.shape}")
    print(merged.to_string(index=False))
    print("PASSED: Basic left merge works correctly.")

    # Test 2: All left rows preserved
    print("\n--- Test 2: All Left Rows Preserved ---")
    left_ids = set(customers['id'].tolist())
    merged_ids = set(merged['id'].tolist())
    assert left_ids.issubset(merged_ids), "All left IDs must be present in merged result"
    print(f"Left IDs: {sorted(left_ids)}")
    print(f"Merged IDs: {sorted(merged_ids)}")
    print("PASSED: All left DataFrame rows are preserved.")

    # Test 3: Unmatched rows have NaN
    print("\n--- Test 3: Unmatched Rows Have NaN ---")
    unmatched = merged[merged['amount'].isna()]
    assert len(unmatched) == 1, f"Expected 1 unmatched row, got {len(unmatched)}"
    assert unmatched['name'].values[0] == 'Eve', "Unmatched customer should be Eve"
    print(f"Unmatched rows: {len(unmatched)}")
    print("PASSED: Unmatched rows correctly have NaN values.")

    # Test 4: Merge with indicator
    print("\n--- Test 4: Merge with Indicator ---")
    merged_ind = merge_left_indicator(customers, orders)
    assert '_merge' in merged_ind.columns, "Missing _merge indicator column"
    both_count = (merged_ind['_merge'] == 'both').sum()
    left_only_count = (merged_ind['_merge'] == 'left_only').sum()
    assert both_count == 5, f"Expected 5 'both' matches, got {both_count}"
    assert left_only_count == 1, f"Expected 1 'left_only', got {left_only_count}"
    print(f"Both matches: {both_count}, Left only: {left_only_count}")
    print("PASSED: Merge indicator works correctly.")

    # Test 5: Analysis function
    print("\n--- Test 5: Merge Analysis ---")
    analysis = analyze_merge_result(merged)
    assert analysis['total_rows'] == 6
    assert analysis['matched_rows'] == 5
    assert analysis['unmatched_rows'] == 1
    assert analysis['match_rate_percent'] == 83.33
    print(f"Analysis: {analysis}")
    print("PASSED: Analysis function returns correct statistics.")

    # Test 6: Empty right DataFrame
    print("\n--- Test 6: Empty Right DataFrame ---")
    empty_orders = pd.DataFrame(columns=['id', 'order_date', 'amount'])
    merged_empty = merge_left(customers, empty_orders)
    assert len(merged_empty) == 5, "Should preserve all 5 customer rows"
    assert merged_empty['amount'].isna().all(), "All amounts should be NaN"
    print(f"Merged with empty orders shape: {merged_empty.shape}")
    print("PASSED: Empty right DataFrame handled correctly.")

    # Test 7: Duplicate IDs in right DataFrame
    print("\n--- Test 7: Duplicate IDs in Right DataFrame ---")
    charlie_rows = merged[merged['id'] == 3]
    assert len(charlie_rows) == 2, f"Charlie should have 2 rows (2 orders), got {len(charlie_rows)}"
    print(f"Charlie's rows: {len(charlie_rows)}")
    print("PASSED: Duplicate IDs in right DataFrame produce multiple rows.")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


def main():
    """Main function demonstrating left merge with sample data."""
    print("=" * 60)
    print("0011: Merge Two DataFrames on 'id' Using how='left'")
    print("=" * 60)

    # Create sample data
    customers, orders = create_sample_data()

    print("\n--- Customers DataFrame ---")
    print(customers.to_string(index=False))

    print("\n--- Orders DataFrame ---")
    print(orders.to_string(index=False))

    # Perform left merge
    merged = merge_left(customers, orders)

    print("\n--- Merged Result (Left Join) ---")
    print(merged.to_string(index=False))

    # Show analysis
    analysis = analyze_merge_result(merged)
    print(f"\n--- Merge Analysis ---")
    print(f"Total rows: {analysis['total_rows']}")
    print(f"Matched rows: {analysis['matched_rows']}")
    print(f"Unmatched rows: {analysis['unmatched_rows']}")
    print(f"Match rate: {analysis['match_rate_percent']}%")

    # Show merge with indicator
    print("\n--- Merge with Indicator ---")
    merged_ind = merge_left_indicator(customers, orders)
    print(merged_ind.to_string(index=False))

    # Run tests
    print("\n")
    test_merge_left()


if __name__ == '__main__':
    main()
