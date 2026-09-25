"""
Pandas Q14: Datetime Resampling
================================
Interview Topic: Time-series resampling with pandas

Problem:
Given a DataFrame of daily sales transactions, perform the following:
1. Parse the date column into datetime.
2. Resample daily sales to weekly totals (Monday-start).
3. Resample daily sales to monthly averages.
4. Compute a 7-day rolling average on daily sales.
5. Identify the week with the highest total sales.
6. Compute year-over-year growth for monthly totals.

This solution demonstrates:
- pd.to_datetime parsing
- .resample() with 'W', 'M', 'D' frequencies
- .agg() on resampled groups
- .rolling() for moving averages
- .pct_change() for growth rates
- .idxmax() for peak detection
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sample_data():
    """Generate 180 days of sample daily sales data."""
    np.random.seed(42)
    start_date = datetime(2023, 1, 1)
    dates = pd.date_range(start=start_date, periods=180, freq='D')
    base_sales = 1000
    trend = np.linspace(0, 200, 180)
    weekly_seasonality = 150 * np.sin(np.arange(180) * 2 * np.pi / 7)
    noise = np.random.normal(0, 100, 180)
    daily_sales = base_sales + trend + weekly_seasonality + noise
    daily_sales = np.clip(daily_sales, 100, None)

    df = pd.DataFrame({
        'date': dates,
        'sales': np.round(daily_sales, 2),
        'transactions': np.random.randint(10, 100, 180),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 180)
    })
    return df


def parse_datetime(df):
    """Step 1: Ensure date column is datetime64 dtype."""
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df


def resample_weekly(df):
    """Step 2: Resample daily sales to weekly totals (Monday-start)."""
    weekly = df['sales'].resample('W-MON').agg(['sum', 'mean', 'count'])
    weekly.columns = ['weekly_total', 'weekly_avg', 'days_count']
    return weekly


def resample_monthly(df):
    """Step 3: Resample daily sales to monthly averages."""
    monthly = df['sales'].resample('M').agg(['mean', 'sum', 'std'])
    monthly.columns = ['monthly_avg', 'monthly_total', 'monthly_std']
    return monthly


def rolling_average(df, window=7):
    """Step 4: Compute a 7-day rolling average on daily sales."""
    rolling = df['sales'].rolling(window=window, min_periods=1).mean()
    result = df.copy()
    result['rolling_7d_avg'] = rolling
    return result


def find_peak_week(weekly):
    """Step 5: Identify the week with the highest total sales."""
    peak_idx = weekly['weekly_total'].idxmax()
    peak_value = weekly['weekly_total'].max()
    return {'peak_week_end': peak_idx, 'peak_total_sales': peak_value}


def yoy_growth(monthly):
    """Step 6: Compute year-over-year growth for monthly totals."""
    growth = monthly['monthly_total'].pct_change(periods=12) * 100
    result = monthly.copy()
    result['yoy_growth_pct'] = growth
    return result


def resample_with_custom_agg(df):
    """Bonus: Resample with custom aggregation function."""
    def custom_agg(series):
        return {
            'total': series.sum(),
            'avg': series.mean(),
            'median': series.median(),
            'max': series.max(),
            'min': series.min(),
            'std': series.std(),
            'count': series.count()
        }

    weekly_custom = df['sales'].resample('W-MON').agg(custom_agg)
    return weekly_custom


def resample_by_region(df):
    """Bonus: Resample sales by region to weekly totals."""
    pivot = df.pivot_table(
        index='date',
        columns='region',
        values='sales',
        aggfunc='sum'
    )
    weekly_by_region = pivot.resample('W-MON').sum()
    return weekly_by_region


def run_all():
    """Execute all steps and print results."""
    print("=" * 60)
    print("Pandas Q14: Datetime Resampling - Full Solution")
    print("=" * 60)

    # Generate and parse data
    df = generate_sample_data()
    df = parse_datetime(df)
    print(f"\nOriginal data shape: {df.shape}")
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    print(f"\nFirst 5 rows:\n{df.head()}")

    # Weekly resampling
    weekly = resample_weekly(df)
    print(f"\n{'=' * 60}")
    print("Weekly Resampled Data (first 5 weeks):")
    print(weekly.head())

    # Monthly resampling
    monthly = resample_monthly(df)
    print(f"\n{'=' * 60}")
    print("Monthly Resampled Data:")
    print(monthly)

    # Rolling average
    rolling_df = rolling_average(df, window=7)
    print(f"\n{'=' * 60}")
    print("Daily Sales with 7-Day Rolling Average (last 10 rows):")
    print(rolling_df[['sales', 'rolling_7d_avg']].tail(10))

    # Peak week
    peak = find_peak_week(weekly)
    print(f"\n{'=' * 60}")
    print(f"Peak Week: {peak['peak_week_end'].strftime('%Y-%m-%d')}")
    print(f"Peak Total Sales: ${peak['peak_total_sales']:,.2f}")

    # YoY growth
    yoy = yoy_growth(monthly)
    print(f"\n{'=' * 60}")
    print("Monthly Totals with YoY Growth:")
    print(yoy[['monthly_total', 'yoy_growth_pct']])

    # Custom aggregation
    custom = resample_with_custom_agg(df)
    print(f"\n{'=' * 60}")
    print("Custom Weekly Aggregation (first 3 weeks):")
    print(custom.head(3))

    # By region
    by_region = resample_by_region(df)
    print(f"\n{'=' * 60}")
    print("Weekly Sales by Region (first 3 weeks):")
    print(by_region.head(3))

    return {
        'daily': df,
        'weekly': weekly,
        'monthly': monthly,
        'rolling': rolling_df,
        'peak': peak,
        'yoy': yoy,
        'custom': custom,
        'by_region': by_region
    }


def run_tests():
    """Run comprehensive tests on all functions."""
    print("\n" + "=" * 60)
    print("Running Tests...")
    print("=" * 60)

    passed = 0
    failed = 0

    # Test 1: Data generation
    df = generate_sample_data()
    assert df.shape[0] == 180, f"Expected 180 rows, got {df.shape[0]}"
    assert 'date' in df.columns
    assert 'sales' in df.columns
    assert 'transactions' in df.columns
    assert 'region' in df.columns
    passed += 1
    print("PASS: Test 1 - Data generation")

    # Test 2: Datetime parsing
    df_parsed = parse_datetime(df)
    assert df_parsed.index.dtype == 'datetime64[ns]'
    assert df_parsed.index.name == 'date'
    passed += 1
    print("PASS: Test 2 - Datetime parsing")

    # Test 3: Weekly resampling
    weekly = resample_weekly(df_parsed)
    assert 'weekly_total' in weekly.columns
    assert 'weekly_avg' in weekly.columns
    assert 'days_count' in weekly.columns
    assert len(weekly) > 0
    # Each week should have 7 days (except possibly first/last)
    for idx, row in weekly.iterrows():
        assert row['days_count'] <= 7
    passed += 1
    print("PASS: Test 3 - Weekly resampling")

    # Test 4: Monthly resampling
    monthly = resample_monthly(df_parsed)
    assert 'monthly_avg' in monthly.columns
    assert 'monthly_total' in monthly.columns
    assert 'monthly_std' in monthly.columns
    assert len(monthly) == 6  # 180 days = 6 months
    passed += 1
    print("PASS: Test 4 - Monthly resampling")

    # Test 5: Rolling average
    rolling_df = rolling_average(df_parsed, window=7)
    assert 'rolling_7d_avg' in rolling_df.columns
    assert len(rolling_df) == 180
    # First value should equal first sales value (min_periods=1)
    assert abs(rolling_df['rolling_7d_avg'].iloc[0] - rolling_df['sales'].iloc[0]) < 0.01
    passed += 1
    print("PASS: Test 5 - Rolling average")

    # Test 6: Peak week detection
    peak = find_peak_week(weekly)
    assert 'peak_week_end' in peak
    assert 'peak_total_sales' in peak
    assert peak['peak_total_sales'] == weekly['weekly_total'].max()
    passed += 1
    print("PASS: Test 6 - Peak week detection")

    # Test 7: YoY growth
    yoy = yoy_growth(monthly)
    assert 'yoy_growth_pct' in yoy.columns
    # First 12 months should have NaN for YoY (no prior year)
    assert yoy['yoy_growth_pct'].iloc[0] != yoy['yoy_growth_pct'].iloc[0]  # NaN check
    passed += 1
    print("PASS: Test 7 - YoY growth")

    # Test 8: Custom aggregation
    custom = resample_with_custom_agg(df_parsed)
    assert 'total' in custom.columns
    assert 'avg' in custom.columns
    assert 'median' in custom.columns
    assert 'max' in custom.columns
    assert 'min' in custom.columns
    assert 'std' in custom.columns
    assert 'count' in custom.columns
    passed += 1
    print("PASS: Test 8 - Custom aggregation")

    # Test 9: Resample by region
    by_region = resample_by_region(df_parsed)
    assert 'North' in by_region.columns
    assert 'South' in by_region.columns
    assert 'East' in by_region.columns
    assert 'West' in by_region.columns
    passed += 1
    print("PASS: Test 9 - Resample by region")

    # Test 10: Weekly totals sum matches daily totals
    total_daily = df_parsed['sales'].sum()
    total_weekly = weekly['weekly_total'].sum()
    assert abs(total_daily - total_weekly) < 0.01
    passed += 1
    print("PASS: Test 10 - Weekly totals match daily totals")

    # Test 11: Monthly totals sum matches daily totals
    total_monthly = monthly['monthly_total'].sum()
    assert abs(total_daily - total_monthly) < 0.01
    passed += 1
    print("PASS: Test 11 - Monthly totals match daily totals")

    # Test 12: Rolling average is between min and max of window
    for i in range(6, len(rolling_df)):
        window_min = rolling_df['sales'].iloc[i-6:i+1].min()
        window_max = rolling_df['sales'].iloc[i-6:i+1].max()
        assert window_min <= rolling_df['rolling_7d_avg'].iloc[i] <= window_max
    passed += 1
    print("PASS: Test 12 - Rolling average bounds")

    # Test 13: All sales values are positive
    assert (df_parsed['sales'] > 0).all()
    passed += 1
    print("PASS: Test 13 - All sales positive")

    # Test 14: Date range is correct
    assert df_parsed.index.min() == pd.Timestamp('2023-01-01')
    assert df_parsed.index.max() == pd.Timestamp('2023-06-29')
    passed += 1
    print("PASS: Test 14 - Date range correct")

    # Test 15: Regions are valid
    valid_regions = {'North', 'South', 'East', 'West'}
    assert set(df['region'].unique()).issubset(valid_regions)
    passed += 1
    print("PASS: Test 15 - Valid regions")

    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    print(f"{'=' * 60}")

    return passed, failed


if __name__ == '__main__':
    results = run_all()
    run_tests()
