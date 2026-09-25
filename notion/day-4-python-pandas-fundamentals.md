# Day 4 — Python Pandas Fundamentals

**Date:** 2026-09-28
**Time Block:** 09:00–11:00 UTC

## Topics
- DataFrame and Series creation
- Indexing and slicing
- groupby() for aggregation
- merge() and join() for combining DataFrames
- Filtering and boolean indexing

## Key Concepts
- **DataFrame**: 2D labeled data structure
- **Series**: 1D labeled data structure
- **groupby()**: Split-apply-combine pattern
- **merge()**: SQL-like join operations
- **loc[]/iloc[]**: Label-based and position-based indexing
- **agg()**: Apply multiple aggregations

## Practice Problems
1. **GroupBy Revenue Analysis** — `solutions/0007_python_pandas_groupby.py`
   - groupby('category').agg(sum, mean, count)
2. **Merge Customers with Orders** — `solutions/0008_python_pandas_merge.py`
   - pd.merge(customers, orders, on='customer_id', how='left')

## Resources
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [Pandas Cookbook](https://pandas.pydata.org/docs/cookbook.html)
- [Kaggle — Pandas Micro-Course](https://www.kaggle.com/learn/pandas)

## Study Tips
- Practice groupby with multiple aggregation functions
- Understand the difference between merge and join
- Know how to handle missing values after a left merge

## Self-Check
- [ ] Can create and manipulate DataFrames
- [ ] Can use groupby with agg()
- [ ] Can merge two DataFrames
- [ ] Solved both practice problems
