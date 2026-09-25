# Day 2 — SQL Joins & Subqueries

**Date:** 2026-09-26
**Time Block:** 09:00–11:00 UTC

## Topics
- INNER JOIN: matching rows from both tables
- LEFT JOIN: all rows from left, matches from right
- RIGHT JOIN: all rows from right, matches from left
- FULL OUTER JOIN: all rows from both tables
- Subqueries and derived tables

## Key Concepts
- **INNER JOIN**: Only rows with matches in both tables
- **LEFT JOIN**: All rows from left table, NULLs for non-matches
- **RIGHT JOIN**: All rows from right table, NULLs for non-matches
- **FULL OUTER JOIN**: All rows from both tables
- **Subqueries**: Queries nested within other queries
- **Derived Tables**: Subqueries in FROM clause

## Practice Problems
1. **Department Employee Count** — `solutions/0003_sql_dept_emp_count.py`
   - INNER JOIN departments to employees, GROUP BY department
2. **Employees With No Orders** — `solutions/0004_sql_employees_no_orders.py`
   - LEFT JOIN + IS NULL pattern

## Resources
- [SQL Joins Visualizer](https://www.sqljoins.com/)
- [Mode Analytics — SQL Joins](https://mode.com/sql-tutorial/sql-joins/)
- [W3Schools — SQL Subqueries](https://www.w3schools.com/sql/sql_subqueries.asp)

## Study Tips
- Draw Venn diagrams to visualize joins
- Practice the LEFT JOIN + IS NULL pattern for "not in" queries
- Understand when to use INNER vs LEFT JOIN

## Self-Check
- [ ] Can explain the difference between INNER and LEFT JOIN
- [ ] Can use LEFT JOIN + IS NULL to find non-matches
- [ ] Can write a subquery in the WHERE clause
- [ ] Solved both practice problems
