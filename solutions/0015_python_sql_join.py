"""
Problem 0015 - Python/Pandas: Merge (SQL JOIN equivalent)
==========================================================
Day 7 - Pandas Merge & SQL Equivalents

Problem
-------
Given two DataFrames:
    customers(customer_id, name, country)
    orders(order_id, customer_id, total)

Perform an INNER JOIN equivalent to list each order with the customer name.

Solution
--------
    merged = orders.merge(customers, on='customer_id', how='inner')

Notes
-----
- how='inner'  -> INNER JOIN
- how='left'   -> LEFT JOIN
- how='right'  -> RIGHT JOIN
- how='outer'  -> FULL OUTER JOIN
- how='cross'  -> CROSS JOIN
- on=...       -> equi-join key
- suffixes=('_left','_right') -> disambiguate overlapping columns

Complexity
----------
- Time:  O(n + m) with hash join
- Space: O(n + m)
"""

import pandas as pd

def build_data():
    customers = pd.DataFrame({
        'customer_id': [1, 2, 3, 4],
        'name':        ['Alice', 'Bob', 'Carol', 'Dave'],
        'country':     ['US', 'UK', 'CA', 'US'],
    })
    orders = pd.DataFrame({
        'order_id':    [101, 102, 103, 104, 105],
        'customer_id': [1, 2, 1, 3, 99],  # 99 has no matching customer
        'total':       [120.0, 80.0, 45.0, 200.0, 30.0],
    })
    return customers, orders

def inner_join(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    return orders.merge(customers, on='customer_id', how='inner')

def left_join(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    return orders.merge(customers, on='customer_id', how='left')

if __name__ == "__main__":
    customers, orders = build_data()
    print("INNER JOIN:")
    print(inner_join(customers, orders))
    print("\nLEFT JOIN:")
    print(left_join(customers, orders))
