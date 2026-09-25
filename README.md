# Data Analyst Interview Prep — 7-Day Sprint

## Overview

This repository is a structured 7-day preparation plan for Data Analyst interviews. It includes:
- A daily schedule with focused topics
- 15 practice questions (8 SQL + 7 Python/Pandas) with full solutions
- Curated resources with URLs
- Notion page templates and Calendar event descriptions

All solutions live under `solutions/sql/` and `solutions/pandas/`.

---

## 7-Day Schedule

### Day 1 — SQL Fundamentals
**Topics:** SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, basic aggregations (COUNT, SUM, AVG, MIN, MAX), GROUP BY, HAVING
**Practice:** Q1 (select_basic), Q2 (second_highest_salary), Q3 (group_by_aggregation)
**Goal:** Write clean SELECT queries with filtering, sorting, and aggregation.

### Day 2 — SQL Joins & Subqueries
**Topics:** INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN, subqueries, EXISTS, IN
**Practice:** Q4 (inner_join), Q6 (self_join)
**Goal:** Join multiple tables confidently; understand self-joins for hierarchical data.

### Day 3 — Advanced SQL & Window Functions
**Topics:** CTEs (WITH), window functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD), running totals, moving averages
**Practice:** Q5 (cte_running_total), Q7 (window_moving_avg)
**Goal:** Use CTEs for readability; apply window functions for analytics.

### Day 4 — SQL Views & Schema Design
**Topics:** CREATE VIEW, CREATE TABLE, data types, constraints, normalization basics
**Practice:** Q8 (create_view)
**Goal:** Create reusable views; understand basic schema design.

### Day 5 — Python/Pandas Fundamentals
**Topics:** Series, DataFrame, dtypes, missing data, basic operations, string methods
**Practice:** Q9 (sum_even), Q10 (char_frequency), Q11 (load_clean_shape)
**Goal:** Manipulate DataFrames fluently; handle missing data.

### Day 6 — Pandas Aggregation & Time Series
**Topics:** groupby, agg, pivot_table, datetime handling, resample, rolling
**Practice:** Q12 (filter_mean), Q13 (groupby_agg_sort), Q14 (datetime_resample)
**Goal:** Perform grouped aggregations and time-series analysis.

### Day 7 — Visualization & Mock Interview
**Topics:** matplotlib/seaborn basics, scatter plots, trendlines, storytelling with data
**Practice:** Q15 (scatter_trendline)
**Goal:** Create publication-quality charts; run a full mock interview.

---

## Practice Questions

### SQL Questions (Q1–Q8)

| # | File | Topic | Difficulty |
|---|------|-------|------------|
| Q1 | `solutions/sql/0001_select_basic.py` | SELECT, WHERE, ORDER BY | Easy |
| Q2 | `solutions/sql/0002_second_highest_salary.py` | Subquery, DISTINCT | Medium |
| Q3 | `solutions/sql/0003_group_by_aggregation.py` | GROUP BY, HAVING, aggregations | Medium |
| Q4 | `solutions/sql/0004_inner_join.py` | INNER JOIN | Easy |
| Q5 | `solutions/sql/0005_cte_running_total.py` | CTE, SUM() OVER() | Medium |
| Q6 | `solutions/sql/0006_self_join.py` | Self JOIN | Medium |
| Q7 | `solutions/sql/0007_window_moving_avg.py` | Window functions, AVG() OVER() | Hard |
| Q8 | `solutions/sql/0008_create_view.py` | CREATE VIEW | Easy |

### Python/Pandas Questions (Q9–Q15)

| # | File | Topic | Difficulty |
|---|------|-------|------------|
| Q9 | `solutions/pandas/0001_sum_even.py` | Series filtering, sum | Easy |
| Q10 | `solutions/pandas/0002_char_frequency.py` | String methods, value_counts | Easy |
| Q11 | `solutions/pandas/0003_load_clean_shape.py` | read_csv, dropna, shape | Easy |
| Q12 | `solutions/pandas/0004_filter_mean.py` | Boolean indexing, mean | Medium |
| Q13 | `solutions/pandas/0005_groupby_agg_sort.py` | groupby, agg, sort_values | Medium |
| Q14 | `solutions/pandas/0006_datetime_resample.py` | to_datetime, resample | Hard |
| Q15 | `solutions/pandas/0007_scatter_trendline.py` | matplotlib, scatter, polyfit | Medium |

---

## Resources

### SQL
- SQLZoo Interactive Exercises: https://sqlzoo.net/
- LeetCode SQL Problems: https://leetcode.com/problemset/database/
- Mode SQL Tutorial: https://mode.com/sql-tutorial/
- PostgreSQL Documentation: https://www.postgresql.org/docs/current/tutorial.html
- Window Functions Guide: https://www.postgresql.org/docs/current/functions-window.html

### Python / Pandas
- Pandas Official Documentation: https://pandas.pydata.org/docs/
- Pandas Cheat Sheet: https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
- Kaggle Pandas Course: https://www.kaggle.com/learn/pandas
- DataCamp Pandas Track: https://www.datacamp.com/learn/python/pandas
- Python for Data Analysis (Wes McKinney): https://www.oreilly.com/library/view/python-for-data/9781491912126/

### Interview Prep
- Data Analyst Interview Questions (StrataScratch): https://www.stratascratch.com/interview-questions
- DataLemur SQL Interview Questions: https://datalemur.com/
- LeetCode Data Analysis: https://leetcode.com/explore/learn/card/sql-introduction/
- Kaggle Competitions (practice): https://www.kaggle.com/competitions

### Visualization
- Matplotlib Gallery: https://matplotlib.org/stable/gallery/index.html
- Seaborn Tutorial: https://seaborn.pydata.org/tutorial.html
- Plotly Interactive Charts: https://plotly.com/python/

---

## Notion Pages

Create the following pages in your Notion workspace:

### Page 1: Interview Prep Dashboard
- Title: Data Analyst Interview Prep — 7-Day Sprint
- Sections: Daily Schedule (checkboxes), Progress Tracker, Notes
- Template:
  - Day 1: SQL Fundamentals [ ]
  - Day 2: SQL Joins & Subqueries [ ]
  - Day 3: Advanced SQL & Window Functions [ ]
  - Day 4: SQL Views & Schema Design [ ]
  - Day 5: Python/Pandas Fundamentals [ ]
  - Day 6: Pandas Aggregation & Time Series [ ]
  - Day 7: Visualization & Mock Interview [ ]

### Page 2: SQL Practice Log
- Columns: Question #, Topic, Difficulty, Attempted (date), Correct (Y/N), Notes
- Pre-fill rows for Q1–Q8

### Page 3: Python Practice Log
- Columns: Question #, Topic, Difficulty, Attempted (date), Correct (Y/N), Notes
- Pre-fill rows for Q9–Q15

### Page 4: Resources & Links
- Database with columns: Resource Name, URL, Category (SQL/Python/Interview/Viz), Notes
- Pre-populate with all URLs listed above

### Page 5: Mock Interview Notes
- Sections: Questions Asked, My Answers, Feedback, Areas to Improve
- Use for Day 7 mock interview

---

## Calendar Events

Create these events in your calendar (Google Calendar / Outlook):

| Day | Time | Event | Details |
|-----|------|-------|--------|
| Day 1 | 9:00–11:00 | SQL Fundamentals Study | Read SQLZoo lessons 1–4; complete Q1–Q3 |
| Day 1 | 14:00–15:00 | SQL Practice Session | LeetCode easy SQL problems (10 questions) |
| Day 2 | 9:00–11:00 | SQL Joins Study | Read Mode SQL Tutorial joins section; complete Q4, Q6 |
| Day 2 | 14:00–15:00 | SQL Practice Session | LeetCode medium SQL problems (10 questions) |
| Day 3 | 9:00–11:00 | Advanced SQL Study | PostgreSQL window functions docs; complete Q5, Q7 |
| Day 3 | 14:00–15:00 | SQL Practice Session | StrataScratch medium/hard problems |
| Day 4 | 9:00–10:00 | SQL Views & Schema | Complete Q8; review normalization |
| Day 4 | 10:00–12:00 | SQL Review & Weak Areas | Revisit any incorrect questions from Days 1–3 |
| Day 5 | 9:00–11:00 | Pandas Fundamentals | Kaggle Pandas course; complete Q9–Q11 |
| Day 5 | 14:00–15:00 | Pandas Practice | Kaggle exercises (missing data, strings) |
| Day 6 | 9:00–11:00 | Pandas Aggregation & Time Series | Complete Q12–Q14 |
| Day 6 | 14:00–15:00 | Pandas Practice | Kaggle time series exercises |
| Day 7 | 9:00–10:00 | Visualization | Complete Q15; review matplotlib/seaborn |
| Day 7 | 10:00–12:00 | Mock Interview | Full mock interview; document in Notion |
| Day 7 | 14:00–15:00 | Review & Final Prep | Review all notes; prepare questions for interviewers |

---

## How to Use This Repository

1. **Clone the repo:** `git clone <repo-url> && cd data-analyst-interview-prep`
2. **Set up environment:** `pip install pandas matplotlib seaborn numpy`
3. **Follow the daily schedule** above, completing practice questions each day.
4. **Run solutions:** `python solutions/sql/0001_select_basic.py` (SQL solutions use SQLite in-memory DB)
5. **Track progress** in Notion pages and calendar events.
6. **On Day 7**, run a full mock interview and document everything.

## Directory Structure

```
data-analyst-interview-prep/
├── README.md
├── solutions/
│   ├── sql/
│   │   ├── 0001_select_basic.py
│   │   ├── 0002_second_highest_salary.py
│   │   ├── 0003_group_by_aggregation.py
│   │   ├── 0004_inner_join.py
│   │   ├── 0005_cte_running_total.py
│   │   ├── 0006_self_join.py
│   │   ├── 0007_window_moving_avg.py
│   │   └── 0008_create_view.py
│   └── pandas/
│       ├── 0001_sum_even.py
│       ├── 0002_char_frequency.py
│       ├── 0003_load_clean_shape.py
│       ├── 0004_filter_mean.py
│       ├── 0005_groupby_agg_sort.py
│       ├── 0006_datetime_resample.py
│       └── 0007_scatter_trendline.py
```

## Tips for Success

- **Consistency over intensity:** 2–3 focused hours daily beats 8-hour cram sessions.
- **Explain your thinking:** In interviews, narrate your approach before writing code.
- **Edge cases matter:** Always consider NULLs, duplicates, and empty results.
- **Practice under time pressure:** Set a 15-minute timer per question.
- **Review mistakes:** Revisit incorrect questions the next day.
