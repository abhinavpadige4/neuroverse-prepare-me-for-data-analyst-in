# Day 1 — SQL Basics

**Date:** 2026-09-25
**Time Block:** 09:00–11:00 UTC

## Topics
- SELECT statement and column selection
- WHERE clause for filtering rows
- ORDER BY for sorting results
- LIMIT for restricting result count
- Basic filtering and sorting patterns

## Key Concepts
- **SELECT**: Choose which columns to return
- **WHERE**: Filter rows based on conditions
- **ORDER BY**: Sort results (ASC/DESC)
- **LIMIT**: Restrict number of rows returned
- **AND/OR/NOT**: Combine conditions

## Practice Problems
1. **Top 10 Highest Paid Employees** — `solutions/0001_sql_top10_salary.py`
   - Use ORDER BY salary DESC LIMIT 10
2. **Count Orders Per Status** — `solutions/0002_sql_order_status_count.py`
   - Use GROUP BY status with COUNT(*)

## Resources
- [SQLBolt — SELECT Queries](https://sqlbolt.com/lesson/select_queries_introduction)
- [W3Schools — SQL WHERE](https://www.w3schools.com/sql/sql_where.asp)
- [Mode Analytics — SQL Tutorial](https://mode.com/sql-tutorial/)

## Study Tips
- Practice writing queries without looking at syntax
- Understand the difference between LIMIT and TOP
- Know how to handle NULL values in WHERE clauses

## Self-Check
- [ ] Can write a SELECT with WHERE and ORDER BY
- [ ] Can use LIMIT to restrict results
- [ ] Can combine multiple conditions with AND/OR
- [ ] Solved both practice problems
