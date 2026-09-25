"""
Problem 0012 - Python/Pandas: GroupBy Aggregation
==================================================
Day 5 - Pandas GroupBy

Problem
-------
Given a DataFrame of sales with columns (date, region, product, revenue),
compute total revenue per region and per product, and identify the top
region-product combination.

Solution
--------
    df.groupby('region')['revenue'].sum()
    df.groupby(['region', 'product'])['revenue'].sum().reset_index()
    df.groupby(['region', 'product'])['revenue'].sum().idxmax()

Notes
-----
- groupby returns a GroupBy object; aggregations are lazy until called.
- .agg() accepts multiple functions:
        df.groupby('region')['revenue'].agg(['sum','mean','count'])
- .transform() returns a Series aligned with the original index.

Complexity
----------
- Time:  O(n log n) for sorting groups
- Space: O(k) where k = number of groups
"""

import pandas as pd

def build_sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        'date':    ['2026-09-01']*4 + ['2026-09-02']*4,
        'region':  ['North','South','East','West','North','South','East','West'],
        'product': ['A','B','C','D','A','B','C','D'],
        'revenue': [100, 200, 150, 50, 120, 220, 180, 60],
    })

def revenue_by_region(df: pd.DataFrame) -> pd.Series:
    return df.groupby('region')['revenue'].sum()

def revenue_by_region_product(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(['region', 'product'])['revenue'].sum().reset_index()

def top_region_product(df: pd.DataFrame):
    grouped = df.groupby(['region', 'product'])['revenue'].sum()
    idx = grouped.idxmax()
    return idx, grouped.loc[idx]

if __name__ == "__main__":
    df = build_sample_df()
    print("Revenue by region:")
    print(revenue_by_region(df))
    print("\nRevenue by region+product:")
    print(revenue_by_region_product(df))
    print("\nTop region-product:")
    print(top_region_product(df))
