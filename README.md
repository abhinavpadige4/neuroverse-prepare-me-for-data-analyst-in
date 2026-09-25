# Data Analyst Interview Prep — 7-Day Sprint

A focused 7-day study plan to prepare for a Data Analyst interview. Includes:

- **Daily schedule** with topics, exercises, and curated resources
- **15 SQL & Python practice problems** with complete, runnable solutions
- **Notion page templates** (one per day) — see [`notion/`](./notion/)
- **Calendar events** (ICS file) — see [`calendar/data-analyst-prep.ics`](./calendar/data-analyst-prep.ics)

---

## 📅 7-Day Schedule

| Day | Date | Focus | Exercises |
|-----|------|-------|-----------|
| 1 | 2026-09-25 | SQL Fundamentals: SELECT, WHERE, ORDER BY, LIMIT | 0001, 0002 |
| 2 | 2026-09-26 | SQL Joins & Subqueries | 0003, 0004, 0005 |
| 3 | 2026-09-27 | SQL Window Functions, Dates, CASE WHEN | 0006, 0007, 0008, 0009 |
| 4 | 2026-09-28 | Python for Data Analysis: NumPy, Pandas basics | 0010 |
| 5 | 2026-09-29 | Pandas GroupBy, Merge, Reshaping | 0011, 0012 |
| 6 | 2026-09-30 | Data Visualization & Statistics | 0013, 0014 |
| 7 | 2026-10-01 | SQL ↔ Pandas Equivalents & Mock Interview | 0015 |

---

## 🧩 Practice Problems (15 total)

### SQL (9 problems)

| # | File | Topic |
|---|------|-------|
| 0001 | [`solutions/0001_sql_top10_salary.py`](./solutions/0001_sql_top10_salary.py) | Top-N with ORDER BY + LIMIT |
| 0002 | [`solutions/0002_sql_order_status_count.py`](./solutions/0002_sql_order_status_count.py) | GROUP BY + COUNT |
| 0003 | [`solutions/0003_sql_dept_emp_count.py`](./solutions/0003_sql_dept_emp_count.py) | INNER JOIN + aggregation |
| 0004 | [`solutions/0004_sql_employees_no_orders.py`](./solutions/0004_sql_employees_no_orders.py) | LEFT JOIN + IS NULL (anti-join) |
| 0005 | [`solutions/0005_sql_avg_salary_above.py`](./solutions/0005_sql_avg_salary_above.py) | Subqueries & correlated subqueries |
| 0006 | [`solutions/0006_row_number_dept.py`](./solutions/0006_row_number_dept.py) | ROW_NUMBER / RANK / DENSE_RANK |
| 0007 | [`solutions/0007_running_total_sales.py`](./solutions/0007_running_total_sales.py) | Running totals with window functions |
| 0008 | [`solutions/0008_sql_date_range.py`](./solutions/0008_sql_date_range.py) | Date filtering with BETWEEN |
| 0009 | [`solutions/0009_sql_case_when.py`](./solutions/0009_sql_case_when.py) | CASE WHEN bucketing |

### Python / Pandas (6 problems)

| # | File | Topic |
|---|------|-------|
| 0010 | [`solutions/0010_fill_missing_mean.py`](./solutions/0010_fill_missing_mean.py) | Missing data imputation |
| 0011 | [`solutions/0011_merge_left.py`](./solutions/0011_merge_left.py) | Pandas merge (LEFT JOIN) |
| 0012 | [`solutions/0012_python_groupby.py`](./solutions/0012_python_groupby.py) | GroupBy aggregation |
| 0013 | [`solutions/0013_line_plot_sales.py`](./solutions/0013_line_plot_sales.py) | Matplotlib line chart |
| 0014 | [`solutions/0014_python_ab_test.py`](./solutions/0014_python_ab_test.py) | Two-proportion z-test (A/B testing) |
| 0015 | [`solutions/0015_python_sql_join.py`](./solutions/0015_python_sql_join.py) | Pandas merge ↔ SQL JOIN |

---

## 📚 Resources by Day

### Day 1 — SQL Fundamentals
- [SQLBolt — SELECT queries](https://sqlbolt.com/lesson/select_queries_introduction)
- [W3Schools — SQL WHERE](https://www.w3schools.com/sql/sql_where.asp)
- [Mode Analytics — SQL Tutorial](https://mode.com/sql-tutorial/)

### Day 2 — SQL Joins & Subqueries
- [SQL Joins Visualizer](https://www.sqljoins.com/)
- [Mode Analytics — SQL Joins](https://mode.com/sql-tutorial/sql-joins/)
- [W3Schools — SQL Subqueries](https://www.w3schools.com/sql/sql_subqueries.asp)

### Day 3 — Window Functions, Dates, CASE
- [Mode Analytics — Window Functions](https://mode.com/sql-tutorial/sql-window-functions/)
- [SQLBolt — Window Functions](https://sqlbolt.com/lesson/window_functions_introduction)
- [W3Schools — SQL CASE](https://www.w3schools.com/sql/sql_case.asp)

### Day 4 — Python for Data Analysis
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [Pandas User Guide — Getting Started](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)
- [Real Python — Pandas Tutorial](https://realpython.com/pandas-basics/)

### Day 5 — Pandas GroupBy & Merge
- [Pandas — GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Pandas — Merging DataFrames](https://pandas.pydata.org/docs/user_guide/merging.html)
- [Real Python — Pandas Merge](https://realpython.com/pandas-merge-join-concat/)

### Day 6 — Visualization & Statistics
- [Matplotlib Quickstart](https://matplotlib.org/stable/getting_started/index.html)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)
- [Khan Academy — A/B Testing](https://www.khanacademy.org/math/statistics-probability/comparing-groups-of-populations/ab-testing)

### Day 7 — SQL ↔ Pandas & Mock Interview
- [Pandas — SQL Queries with Pandas](https://pandas.pydata.org/docs/user_guide/sql.html)
- [DataLemur — SQL Interview Questions](https://www.datalemur.com/)
- [StrataScratch — Data Analyst Interview Prep](https://www.stratascratch.com/interview-prep)

---

## 🗂️ Repo Structure

```
.
├── README.md
├── solutions/
│   ├── 0001_sql_top10_salary.py
│   ├── 0002_sql_order_status_count.py
│   ├── 0003_sql_dept_emp_count.py
│   ├── 0004_sql_employees_no_orders.py
│   ├── 0005_sql_avg_salary_above.py
│   ├── 0006_row_number_dept.py
│   ├── 0007_running_total_sales.py
│   ├── 0008_sql_date_range.py
│   ├── 0009_sql_case_when.py
│   ├── 0010_fill_missing_mean.py
│   ├── 0011_merge_left.py
│   ├── 0012_python_groupby.py
│   ├── 0013_line_plot_sales.py
│   ├── 0014_python_ab_test.py
│   └── 0015_python_sql_join.py
├── notion/
│   ├── day-01-sql-basics.md
│   ├── day-02-sql-joins.md
│   ├── day-03-sql-window-functions.md
│   ├── day-04-python-pandas-basics.md
│   ├── day-05-pandas-groupby-merge.md
│   ├── day-06-visualization-statistics.md
│   └── day-07-sql-pandas-mock-interview.md
└── calendar/
    └── data-analyst-prep.ics
```

---

## 🚀 How to Run the Solutions

Each solution file is self-contained and runnable:

```bash
# SQL solutions use in-memory SQLite — no setup needed
python solutions/0001_sql_top10_salary.py

# Python/Pandas solutions require pandas (and matplotlib for 0013)
pip install pandas matplotlib numpy
python solutions/0012_python_groupby.py
```

---

## 🎯 Interview Tips

1. **SQL**: Practice writing queries without looking at syntax. Focus on joins, window functions, and date handling — these appear in ~80% of DA interviews.
2. **Python**: Master `groupby`, `merge`, `pivot_table`, and basic data cleaning.
3. **Statistics**: Know when to use z-test vs t-test, and how to interpret p-values.
4. **Communication**: Always state your assumptions, walk through your approach, and validate your results.

Good luck! 🍀
