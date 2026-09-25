# Day 6 — SQL Window Functions & Advanced Analytics

**Date:** 2026-09-30
**Time Block:** 09:00–11:00 UTC

## Topics
- Window functions: ROW_NUMBER, RANK, DENSE_RANK
- LAG and LEAD for previous/next row values
- Running totals with SUM() OVER()
- Common Table Expressions (CTEs)
- Cohort analysis

## Key Concepts
- **ROW_NUMBER()**: Unique row number within partition
- **RANK()**: Rank with ties (gaps in numbering)
- **DENSE_RANK()**: Rank with ties (no gaps)
- **LAG()**: Value from previous row
- **LEAD()**: Value from next row
- **PARTITION BY**: Restart window per group
- **CTE (WITH clause)**: Named subqueries for readability

## Practice Problems
1. **Running Total & Rank with Window Functions** — `solutions/0011_sql_window_functions.py`
   - SUM() OVER(PARTITION BY customer ORDER BY month)
   - LAG() for month-over-month growth
2. **Cohort Retention Analysis with CTEs** — `solutions/0012_sql_cohort_retention.py`
   - Multiple CTEs for cohort analysis

## Resources
- [Mode Analytics — Window Functions](https://mode.com/sql-tutorial/sql-window-functions/)
- [SQLBolt — Window Functions](https://sqlbolt.com/lesson/window_functions_introduction)
- [Use The Index — Window Functions](https://use-the-index-luke.com/blog/2020-06/window-functions)

## Study Tips
- Understand the difference between RANK and DENSE_RANK
- Practice PARTITION BY for per-group calculations
- Use CTEs to break down complex queries

## Self-Check
- [ ] Can use ROW_NUMBER, RANK, DENSE_RANK
- [ ] Can use LAG and LEAD for row comparisons
- [ ] Can write CTEs for complex queries
- [ ] Solved both practice problems
