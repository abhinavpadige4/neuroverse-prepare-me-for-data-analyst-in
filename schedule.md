# 7-Day Data Analyst Interview Prep Schedule

Start date: **2026-09-25**. Each day: 2 hours focused study + 1 hour practice.

---

## Day 1 — 2026-09-25 — SQL Fundamentals

**Topics**
- SELECT, WHERE, ORDER BY, LIMIT
- Basic filtering, sorting, and projection
- Data types and NULL handling

**Practice**
1. `solutions/0001_sql_top10_salary.py` — Top 10 highest paid employees
2. `solutions/0002_sql_order_status_count.py` — Count orders per status

**Resources**
- SQLBolt SELECT: https://sqlbolt.com/lesson/select_queries_introduction
- W3Schools WHERE: https://www.w3schools.com/sql/sql_where.asp
- Mode Analytics SQL Tutorial: https://mode.com/sql-tutorial/

---

## Day 2 — 2026-09-26 — SQL Joins & Subqueries

**Topics**
- INNER, LEFT, RIGHT, FULL OUTER joins
- Subqueries and derived tables
- Correlated vs. non-correlated subqueries

**Practice**
3. `solutions/0003_sql_dept_emp_count.py` — Employees per department
4. `solutions/0004_sql_employees_no_orders.py` — Employees with no orders

**Resources**
- SQL Joins Visualizer: https://www.sqljoins.com/
- Mode Analytics Joins: https://mode.com/sql-tutorial/sql-joins/
- W3Schools Subqueries: https://www.w3schools.com/sql/sql_subqueries.asp

---

## Day 3 — 2026-09-27 — SQL Aggregation & Window Functions

**Topics**
- GROUP BY, HAVING, aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- Window functions: ROW_NUMBER, RANK, LAG, LEAD, running totals
- CTEs (WITH clause)

**Practice**
5. `solutions/0005_sql_monthly_revenue.py` — Monthly revenue with GROUP BY
6. `solutions/0006_sql_running_total.py` — Running total with window functions

**Resources**
- Mode Analytics Aggregation: https://mode.com/sql-tutorial/sql-group-by/
- SQL Window Functions (Mode): https://mode.com/sql-tutorial/sql-window-functions/
- LeetCode SQL 50: https://leetcode.com/sql-50/

---

## Day 4 — 2026-09-28 — Python Pandas Fundamentals

**Topics**
- Series and DataFrame basics
- Reading CSV/Excel, head/tail/dtypes/info
- Selecting columns, filtering rows, boolean indexing

**Practice**
7. `solutions/0007_python_pandas_load_filter.py` — Load CSV, filter, describe
8. `solutions/0008_python_pandas_groupby.py` — GroupBy + aggregation

**Resources**
- Pandas User Guide: https://pandas.pydata.org/docs/user_guide/index.html
- Pandas 10 Minutes: https://pandas.pydata.org/docs/10min.html
- Kaggle Pandas Course: https://www.kaggle.com/learn/pandas

---

## Day 5 — 2026-09-29 — Data Cleaning & Manipulation

**Topics**
- Handling missing values (dropna, fillna, interpolate)
- Duplicates, type conversion, string operations
- Merging and joining DataFrames

**Practice**
9. `solutions/0009_python_clean_missing.py` — Handle missing values
10. `solutions/0010_python_merge_join.py` — Merge two DataFrames

**Resources**
- Pandas Missing Data: https://pandas.pydata.org/docs/user_guide/missing_data.html
- Pandas Merge: https://pandas.pydata.org/docs/user_guide/merging.html
- Real Python Data Cleaning: https://realpython.com/python-data-cleaning/

---

## Day 6 — 2026-09-30 — Data Visualization

**Topics**
- Matplotlib: line, bar, scatter, histograms
- Seaborn: heatmaps, pair plots, distributions
- Plot best practices for business reporting

**Practice**
11. `solutions/0011_python_matplotlib_barchart.py` — Bar chart with matplotlib
12. `solutions/0012_python_seaborn_heatmap.py` — Correlation heatmap with seaborn

**Resources**
- Matplotlib Gallery: https://matplotlib.org/stable/gallery/index.html
- Seaborn Tutorial: https://seaborn.pydata.org/tutorial.html
- Plotly Python: https://plotly.com/python/

---

## Day 7 — 2026-10-01 — Statistics & A/B Testing

**Topics**
- Descriptive statistics: mean, median, mode, std, percentiles
- Distributions, hypothesis testing, p-values
- A/B testing: null/alternative hypothesis, t-test, chi-square
- SQL from Python with pandas

**Practice**
13. `solutions/0013_python_descriptive_stats.py` — Descriptive statistics
14. `solutions/0014_python_ab_test.py` — A/B test with t-test
15. `solutions/0015_python_sql_query.py` — Query a database with pandas + SQL

**Resources**
- A/B Testing (Wikipedia): https://en.wikipedia.org/wiki/A/B_testing
- SciPy Stats: https://docs.scipy.org/doc/scipy/reference/stats.html
- Statsmodels: https://www.statsmodels.org/stable/index.html

---

## Daily Routine (2 hours study + 1 hour practice)

- **09:00–09:30** — Review yesterday's notes
- **09:30–10:30** — Study today's topics from resources
- **10:30–11:00** — Take notes in Notion
- **11:00–12:00** — Solve today's 2 practice problems
- **12:00–12:15** — Review solutions, note mistakes
