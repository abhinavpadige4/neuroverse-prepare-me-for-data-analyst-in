# 7-Day Data Analyst Interview Prep Schedule

Start date: **2026-09-25**. Each day: 2 hours focused study + 1 hour practice.

Daily routine:
- **09:00–09:30** — Review yesterday's notes
- **09:30–10:30** — Study today's topics from resources
- **10:30–11:00** — Take notes in Notion
- **11:00–12:00** — Solve today's practice problems
- **12:00–12:15** — Review solutions, note mistakes

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

**Notion:** `notion/day-1-sql-basics.md`
**Calendar:** `calendar/day-1-sql-basics.ics`

---

## Day 2 — 2026-09-26 — SQL Joins & Subqueries

**Topics**
- INNER, LEFT, RIGHT, FULL OUTER joins
- Subqueries and derived tables
- Correlated vs. non-correlated subqueries

**Practice**
3. `solutions/0003_sql_dept_emp_count.py` — Employees per department (INNER JOIN)
4. `solutions/0004_sql_employees_no_orders.py` — Employees with no orders (LEFT JOIN + IS NULL)

**Resources**
- SQL Joins Visualizer: https://www.sqljoins.com/
- Mode Analytics Joins: https://mode.com/sql-tutorial/sql-joins/
- W3Schools Subqueries: https://www.w3schools.com/sql/sql_subqueries.asp

**Notion:** `notion/day-2-sql-joins-subqueries.md`
**Calendar:** `calendar/day-2-sql-joins-subqueries.ics`

---

## Day 3 — 2026-09-27 — SQL Aggregation & Grouping

**Topics**
- GROUP BY, HAVING, aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- Date functions (DATE_TRUNC, DATEPART)
- Filtering with WHERE vs. HAVING

**Practice**
5. `solutions/0005_sql_monthly_revenue.py` — Monthly revenue with GROUP BY
6. `solutions/0006_sql_top5_customers.py` — Top 5 customers by revenue

**Resources**
- SQLBolt GROUP BY: https://sqlbolt.com/lesson/group_by_queries_introduction
- Mode Analytics Aggregation: https://mode.com/sql-tutorial/sql-aggregation/
- W3Schools GROUP BY: https://www.w3schools.com/sql/sql_groupby.asp

**Notion:** `notion/day-3-sql-aggregation.md`
**Calendar:** `calendar/day-3-sql-aggregation.ics`

---

## Day 4 — 2026-09-28 — Python Pandas Fundamentals

**Topics**
- Series and DataFrame basics
- Reading CSV/Excel, head/tail/dtypes/info
- Selecting columns, filtering rows, boolean indexing
- groupby + agg, merge/join

**Practice**
7. `solutions/0007_python_pandas_groupby.py` — GroupBy revenue analysis
8. `solutions/0008_python_pandas_merge.py` — Merge customers with orders

**Resources**
- Pandas User Guide: https://pandas.pydata.org/docs/user_guide/index.html
- Pandas 10 Minutes: https://pandas.pydata.org/docs/10min.html
- Kaggle Pandas Course: https://www.kaggle.com/learn/pandas

**Notion:** `notion/day-4-python-pandas-fundamentals.md`
**Calendar:** `calendar/day-4-python-pandas-fundamentals.ics`

---

## Day 5 — 2026-09-29 — Pandas Time Series & Data Cleaning

**Topics**
- Datetime handling, resampling, rolling windows
- Handling missing values (dropna, fillna, interpolate)
- Duplicates, type conversion, string operations
- Data validation and cleaning pipelines

**Practice**
9. `solutions/0009_python_pandas_timeseries.py` — Daily revenue time series with rolling avg
10. `solutions/0010_python_pandas_cleaning.py` — Data cleaning pipeline

**Resources**
- Pandas Time Series Guide: https://pandas.pydata.org/docs/user_guide/timeseries.html
- Pandas Missing Data: https://pandas.pydata.org/docs/user_guide/missing_data.html
- Kaggle Data Cleaning: https://www.kaggle.com/learn/data-cleaning

**Notion:** `notion/day-5-python-pandas-timeseries.md`
**Calendar:** `calendar/day-5-python-pandas-timeseries.ics`

---

## Day 6 — 2026-09-30 — SQL Window Functions & Advanced Analytics

**Topics**
- Window functions: ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD
- Running totals, month-over-month growth
- CTEs (WITH clause)
- Cohort retention analysis

**Practice**
11. `solutions/0011_sql_window_functions.py` — Running total & MoM growth
12. `solutions/0012_sql_cohort_retention.py` — Cohort retention with CTEs

**Resources**
- Mode Analytics Window Functions: https://mode.com/sql-tutorial/sql-window-functions/
- LeetCode SQL 50: https://leetcode.com/sql-50/
- SQL Window Functions (DataCamp): https://www.datacamp.com/tutorial/sql-window-functions

**Notion:** `notion/day-6-sql-window-functions.md`
**Calendar:** `calendar/day-6-sql-window-functions.ics`

---

## Day 7 — 2026-10-01 — Statistics, A/B Testing & Funnel Analysis

**Topics**
- Descriptive statistics: mean, median, mode, std, percentiles
- Outlier detection (IQR method), correlation
- Hypothesis testing: null/alternative, p-values, z-test
- A/B testing: two-proportion z-test, lift, significance
- Funnel analysis: step conversion rates

**Practice**
13. `solutions/0013_python_statistics_hypothesis.py` — Two-proportion z-test for A/B testing
14. `solutions/0014_python_descriptive_stats.py` — Descriptive stats & outlier detection
15. `solutions/0015_sql_funnel_analysis.py` — Funnel analysis (SQL + Python)

**Resources**
- A/B Testing (Wikipedia): https://en.wikipedia.org/wiki/A/B_testing
- SciPy Stats: https://docs.scipy.org/doc/scipy/reference/stats.html
- Statsmodels: https://www.statsmodels.org/stable/index.html
- Evan Miller — A/B Testing: https://www.evanmiller.org/how-not-to-run-an-ab-test.html

**Notion:** `notion/day-7-statistics-ab-testing.md`
**Calendar:** `calendar/day-7-statistics-ab-testing.ics`

---

## Mock Interview Checklist (Day 7 evening)

- [ ] Explain a past project end-to-end (STAR format)
- [ ] Walk through a SQL query out loud (verbalize your thought process)
- [ ] Explain the difference between INNER JOIN and LEFT JOIN
- [ ] Explain what a p-value means in plain English
- [ ] Explain cohort retention and how you'd compute it
- [ ] Explain how you'd design an A/B test for a landing page change
- [ ] Explain how you'd handle missing data in a dataset
- [ ] Explain the difference between mean and median, and when to use each
