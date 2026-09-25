# Data Analyst Interview Prep — 7-Day Plan

A complete 7-day study plan to prepare for a Data Analyst interview, with:
- Daily topics and schedule
- 15 SQL & Python practice problems with full solutions
- Curated learning resources with URLs
- Notion pages (one per day) in `notion/`
- Calendar events (one per day) in `calendar/`

## Repository Structure

```
.
├── README.md                          # This file
├── solutions/                         # 15 practice problems with solutions
│   ├── 0001_sql_top10_salary.py
│   ├── 0002_sql_order_status_count.py
│   ├── 0003_sql_dept_emp_count.py
│   ├── 0004_sql_employees_no_orders.py
│   ├── 0005_sql_monthly_revenue.py
│   ├── 0006_sql_top5_customers.py
│   ├── 0007_python_pandas_groupby.py
│   ├── 0008_python_pandas_merge.py
│   ├── 0009_python_pandas_timeseries.py
│   ├── 0010_python_pandas_cleaning.py
│   ├── 0011_sql_window_functions.py
│   ├── 0012_sql_cohort_retention.py
│   ├── 0013_python_statistics_hypothesis.py
│   ├── 0014_python_descriptive_stats.py
│   └── 0015_sql_funnel_analysis.py
├── notion/                            # Notion page content (one per day)
│   ├── day-1-sql-basics.md
│   ├── day-2-sql-joins-subqueries.md
│   ├── day-3-sql-aggregation.md
│   ├── day-4-python-pandas-fundamentals.md
│   ├── day-5-python-pandas-timeseries.md
│   ├── day-6-sql-window-functions.md
│   └── day-7-statistics-ab-testing.md
└── calendar/                          # Calendar events (ICS format)
    ├── day-1-sql-basics.ics
    ├── day-2-sql-joins-subqueries.ics
    ├── day-3-sql-aggregation.ics
    ├── day-4-python-pandas-fundamentals.ics
    ├── day-5-python-pandas-timeseries.ics
    ├── day-6-sql-window-functions.ics
    └── day-7-statistics-ab-testing.ics
```

---

## 7-Day Study Schedule

### Day 1 — SQL Basics (2026-09-25)
**Topics:** SELECT, WHERE, ORDER BY, LIMIT, basic filtering and sorting

**Practice Problems:**
1. [Top 10 Highest Paid Employees](solutions/0001_sql_top10_salary.py)
2. [Count Orders Per Status](solutions/0002_sql_order_status_count.py)

**Resources:**
- [SQLBolt — SELECT Queries](https://sqlbolt.com/lesson/select_queries_introduction)
- [W3Schools — SQL WHERE](https://www.w3schools.com/sql/sql_where.asp)
- [Mode Analytics — SQL Tutorial](https://mode.com/sql-tutorial/)

**Notion Page:** [notion/day-1-sql-basics.md](notion/day-1-sql-basics.md)
**Calendar Event:** [calendar/day-1-sql-basics.ics](calendar/day-1-sql-basics.ics)

---

### Day 2 — SQL Joins & Subqueries (2026-09-26)
**Topics:** INNER, LEFT, RIGHT, FULL joins; subqueries and derived tables

**Practice Problems:**
3. [Department Employee Count (INNER JOIN)](solutions/0003_sql_dept_emp_count.py)
4. [Employees With No Orders (LEFT JOIN + IS NULL)](solutions/0004_sql_employees_no_orders.py)

**Resources:**
- [SQL Joins Visualizer](https://www.sqljoins.com/)
- [Mode Analytics — SQL Joins](https://mode.com/sql-tutorial/sql-joins/)
- [W3Schools — SQL Subqueries](https://www.w3schools.com/sql/sql_subqueries.asp)

**Notion Page:** [notion/day-2-sql-joins-subqueries.md](notion/day-2-sql-joins-subqueries.md)
**Calendar Event:** [calendar/day-2-sql-joins-subqueries.ics](calendar/day-2-sql-joins-subqueries.ics)

---

### Day 3 — SQL Aggregation & Grouping (2026-09-27)
**Topics:** GROUP BY, HAVING, aggregate functions (SUM, AVG, COUNT, MIN, MAX), date functions

**Practice Problems:**
5. [Monthly Revenue](solutions/0005_sql_monthly_revenue.py)
6. [Top 5 Customers by Revenue](solutions/0006_sql_top5_customers.py)

**Resources:**
- [SQLBolt — GROUP BY](https://sqlbolt.com/lesson/group_by_queries_introduction)
- [Mode Analytics — Aggregation](https://mode.com/sql-tutorial/sql-aggregation/)
- [W3Schools — SQL GROUP BY](https://www.w3schools.com/sql/sql_groupby.asp)

**Notion Page:** [notion/day-3-sql-aggregation.md](notion/day-3-sql-aggregation.md)
**Calendar Event:** [calendar/day-3-sql-aggregation.ics](calendar/day-3-sql-aggregation.ics)

---

### Day 4 — Python Pandas Fundamentals (2026-09-28)
**Topics:** DataFrames, Series, groupby, merge/join, filtering, indexing

**Practice Problems:**
7. [GroupBy Revenue Analysis](solutions/0007_python_pandas_groupby.py)
8. [Merge Customers with Orders](solutions/0008_python_pandas_merge.py)

**Resources:**
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [Pandas Cookbook](https://pandas.pydata.org/docs/cookbook.html)
- [Kaggle — Pandas Micro-Course](https://www.kaggle.com/learn/pandas)

**Notion Page:** [notion/day-4-python-pandas-fundamentals.md](notion/day-4-python-pandas-fundamentals.md)
**Calendar Event:** [calendar/day-4-python-pandas-fundamentals.ics](calendar/day-4-python-pandas-fundamentals.ics)

---

### Day 5 — Python Pandas Time Series & Cleaning (2026-09-29)
**Topics:** Datetime handling, resampling, rolling windows, data cleaning, missing values

**Practice Problems:**
9. [Daily Revenue Time Series](solutions/0009_python_pandas_timeseries.py)
10. [Data Cleaning Pipeline](solutions/0010_python_pandas_cleaning.py)

**Resources:**
- [Pandas Time Series Guide](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- [Pandas Missing Data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [Kaggle — Data Cleaning](https://www.kaggle.com/learn/data-cleaning)

**Notion Page:** [notion/day-5-python-pandas-timeseries.md](notion/day-5-python-pandas-timeseries.md)
**Calendar Event:** [calendar/day-5-python-pandas-timeseries.ics](calendar/day-5-python-pandas-timeseries.ics)

---

### Day 6 — SQL Window Functions & Advanced Analytics (2026-09-30)
**Topics:** Window functions (ROW_NUMBER, RANK, LAG, LEAD), CTEs, cohort analysis

**Practice Problems:**
11. [Running Total & Rank with Window Functions](solutions/0011_sql_window_functions.py)
12. [Cohort Retention Analysis with CTEs](solutions/0012_sql_cohort_retention.py)

**Resources:**
- [Mode Analytics — Window Functions](https://mode.com/sql-tutorial/sql-window-functions/)
- [SQLBolt — Window Functions](https://sqlbolt.com/lesson/window_functions_introduction)
- [Use The Index — Window Functions](https://use-the-index-luke.com/blog/2020-06/window-functions)

**Notion Page:** [notion/day-6-sql-window-functions.md](notion/day-6-sql-window-functions.md)
**Calendar Event:** [calendar/day-6-sql-window-functions.ics](calendar/day-6-sql-window-functions.ics)

---

### Day 7 — Statistics & A/B Testing (2026-10-01)
**Topics:** Descriptive statistics, hypothesis testing, A/B testing, funnel analysis

**Practice Problems:**
13. [A/B Test with Hypothesis Testing](solutions/0013_python_statistics_hypothesis.py)
14. [Descriptive Statistics & Data Profiling](solutions/0014_python_descriptive_stats.py)
15. [Funnel Analysis (SQL + Python)](solutions/0015_sql_funnel_analysis.py)

**Resources:**
- [Khan Academy — Statistics](https://www.khanacademy.org/math/statistics-probability)
- [StatQuest — A/B Testing](https://www.youtube.com/playlist?list=PLblx53-FGE08sU0VtS0Lp0y0000000000)
- [Evan Miller — Sample Size for A/B Tests](https://www.evanmiller.org/how-not-to-run-an-ab-test.html)

**Notion Page:** [notion/day-7-statistics-ab-testing.md](notion/day-7-statistics-ab-testing.md)
**Calendar Event:** [calendar/day-7-statistics-ab-testing.ics](calendar/day-7-statistics-ab-testing.ics)

---

## Practice Problems Summary

| # | Day | Problem | File |
|---|-----|---------|------|
| 1 | 1 | Top 10 Highest Paid Employees | `solutions/0001_sql_top10_salary.py` |
| 2 | 1 | Count Orders Per Status | `solutions/0002_sql_order_status_count.py` |
| 3 | 2 | Department Employee Count | `solutions/0003_sql_dept_emp_count.py` |
| 4 | 2 | Employees With No Orders | `solutions/0004_sql_employees_no_orders.py` |
| 5 | 3 | Monthly Revenue | `solutions/0005_sql_monthly_revenue.py` |
| 6 | 3 | Top 5 Customers by Revenue | `solutions/0006_sql_top5_customers.py` |
| 7 | 4 | GroupBy Revenue Analysis | `solutions/0007_python_pandas_groupby.py` |
| 8 | 4 | Merge Customers with Orders | `solutions/0008_python_pandas_merge.py` |
| 9 | 5 | Daily Revenue Time Series | `solutions/0009_python_pandas_timeseries.py` |
| 10 | 5 | Data Cleaning Pipeline | `solutions/0010_python_pandas_cleaning.py` |
| 11 | 6 | Running Total & Rank | `solutions/0011_sql_window_functions.py` |
| 12 | 6 | Cohort Retention Analysis | `solutions/0012_sql_cohort_retention.py` |
| 13 | 7 | A/B Test Hypothesis Testing | `solutions/0013_python_statistics_hypothesis.py` |
| 14 | 7 | Descriptive Statistics | `solutions/0014_python_descriptive_stats.py` |
| 15 | 7 | Funnel Analysis | `solutions/0015_sql_funnel_analysis.py` |

---

## How to Use This Repository

1. **Follow the daily schedule** — each day has specific topics, problems, and resources.
2. **Solve the practice problems** — each solution file contains:
   - Problem description
   - Assumed schema
   - SQL solution (for SQL problems)
   - Python/pandas implementation
   - Complexity analysis
   - Sample test data
3. **Review the resources** — each day has curated links to tutorials and documentation.
4. **Use the Notion pages** — copy the markdown content into Notion for your personal study notes.
5. **Import the Calendar events** — import the `.ics` files into your calendar to block study time.

## Prerequisites

- Basic Python knowledge
- Basic SQL knowledge
- Pandas library installed (`pip install pandas numpy`)
- A SQL environment (PostgreSQL, MySQL, SQLite, or online like SQLFiddle)

## Additional Resources

- [LeetCode SQL Problems](https://leetcode.com/problemset/database/)
- [StrataScratch](https://www.stratascratch.com/)
- [DataCamp — Data Analyst Track](https://www.datacamp.com/track/data-analyst)
- [Kaggle Datasets](https://www.kaggle.com/datasets)

---

**Good luck with your Data Analyst interview!** 🎯
