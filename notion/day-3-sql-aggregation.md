# Day 3 — SQL Aggregation & Grouping

**Date:** 2026-09-27
**Time Block:** 09:00–11:00 UTC

## Topics
- GROUP BY clause
- HAVING clause for filtering groups
- Aggregate functions: SUM, AVG, COUNT, MIN, MAX
- Date functions: DATE_TRUNC, EXTRACT, DATE_PART
- Combining aggregation with joins

## Key Concepts
- **GROUP BY**: Group rows by one or more columns
- **HAVING**: Filter groups after aggregation
- **SUM()**: Sum of values
- **AVG()**: Average of values
- **COUNT()**: Count of rows
- **MIN()/MAX()**: Minimum/maximum values
- **DATE_TRUNC()**: Truncate date to specified precision

## Practice Problems
1. **Monthly Revenue** — `solutions/0005_sql_monthly_revenue.py`
   - DATE_TRUNC('month', order_date) + GROUP BY + SUM
2. **Top 5 Customers by Revenue** — `solutions/0006_sql_top5_customers.py`
   - GROUP BY customer_id + ORDER BY total_revenue DESC LIMIT 5

## Resources
- [SQLBolt — GROUP BY](https://sqlbolt.com/lesson/group_by_queries_introduction)
- [Mode Analytics — Aggregation](https://mode.com/sql-tutorial/sql-aggregation/)
- [W3Schools — SQL GROUP BY](https://www.w3schools.com/sql/sql_groupby.asp)

## Study Tips
- Understand the difference between WHERE and HAVING
- Practice date functions for time-based analysis
- Know how to handle NULLs in aggregate functions

## Self-Check
- [ ] Can use GROUP BY with aggregate functions
- [ ] Can use HAVING to filter groups
- [ ] Can use date functions for time-based grouping
- [ ] Solved both practice problems
