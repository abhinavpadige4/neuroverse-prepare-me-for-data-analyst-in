# Day 5 — Python Pandas Time Series & Cleaning

**Date:** 2026-09-29
**Time Block:** 09:00–11:00 UTC

## Topics
- Datetime handling and conversion
- Resampling time series data
- Rolling windows and moving averages
- Data cleaning: missing values, duplicates, outliers
- String manipulation and validation

## Key Concepts
- **pd.to_datetime()**: Convert to datetime
- **dt accessor**: Datetime properties and methods
- **resample()**: Aggregate time series to specified frequency
- **rolling()**: Calculate rolling window statistics
- **fillna()**: Fill missing values
- **drop_duplicates()**: Remove duplicate rows
- **str accessor**: String methods for Series

## Practice Problems
1. **Daily Revenue Time Series** — `solutions/0009_python_pandas_timeseries.py`
   - Group by date, reindex to full range, rolling average
2. **Data Cleaning Pipeline** — `solutions/0010_python_pandas_cleaning.py`
   - Strip whitespace, title case, fill missing, validate emails

## Resources
- [Pandas Time Series Guide](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- [Pandas Missing Data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [Kaggle — Data Cleaning](https://www.kaggle.com/learn/data-cleaning)

## Study Tips
- Practice creating date ranges and reindexing
- Understand the difference between resample and groupby
- Know common data cleaning patterns

## Self-Check
- [ ] Can convert and manipulate datetime columns
- [ ] Can create rolling window statistics
- [ ] Can clean messy data with pandas
- [ ] Solved both practice problems
