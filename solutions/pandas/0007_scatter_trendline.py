"""
Data Analyst Interview Prep - Pandas Q15
Scatter Plot with Trendline

Objective:
  Given a dataset of advertising spend vs. sales revenue, create a scatter plot
  with a linear regression trendline, annotate R-squared, and extract key insights.

Skills Tested:
  - Pandas data manipulation
  - Matplotlib visualization
  - Linear regression (numpy/scipy)
  - Statistical interpretation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def generate_sample_data(n=50, seed=42):
    """Generate realistic ad spend vs sales data with noise."""
    rng = np.random.default_rng(seed)
    ad_spend = rng.uniform(1000, 50000, n)
    # Sales = 2.5 * ad_spend + noise (with slight diminishing returns)
    sales = 2.5 * ad_spend + rng.normal(0, 5000, n) - 0.00001 * ad_spend**2
    sales = np.clip(sales, 0, None)
    return pd.DataFrame({"ad_spend": ad_spend, "sales_revenue": sales})


def compute_trendline(df, x_col="ad_spend", y_col="sales_revenue"):
    """Compute linear regression trendline parameters."""
    x = df[x_col].values
    y = df[y_col].values
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value ** 2
    return {
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_squared,
        "p_value": p_value,
        "std_err": std_err,
    }


def plot_scatter_trendline(df, x_col="ad_spend", y_col="sales_revenue", title="Ad Spend vs Sales Revenue"):
    """Create scatter plot with linear regression trendline and annotations."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Scatter points
    ax.scatter(
        df[x_col],
        df[y_col],
        alpha=0.6,
        edgecolors="k",
        linewidths=0.5,
        s=60,
        color="steelblue",
        label="Data Points",
    )

    # Trendline
    params = compute_trendline(df, x_col, y_col)
    x_line = np.linspace(df[x_col].min(), df[x_col].max(), 100)
    y_line = params["slope"] * x_line + params["intercept"]
    ax.plot(
        x_line,
        y_line,
        color="red",
        linewidth=2,
        label=f"Trendline (R²={params['r_squared']:.3f})",
    )

    # Confidence band (approximate ±1 std_err)
    y_upper = y_line + params["std_err"]
    y_lower = y_line - params["std_err"]
    ax.fill_between(x_line, y_lower, y_upper, alpha=0.15, color="red", label="±1 Std Error")

    # Annotations
    ax.set_xlabel("Ad Spend ($)", fontsize=12)
    ax.set_ylabel("Sales Revenue ($)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(True, alpha=0.3)

    # Add equation text box
    eq_text = (
        f"y = {params['slope']:.3f}x + {params['intercept']:.1f}\n"
        f"R² = {params['r_squared']:.4f}  |  p = {params['p_value']:.2e}"
    )
    ax.text(
        0.7,
        0.9,
        eq_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="wheat", alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig("scatter_trendline.png", dpi=150, bbox_inches="tight")
    plt.show()
    return params


def extract_insights(df, params):
    """Generate textual insights from the analysis."""
    insights = []
    insights.append(f"Slope: For every $1 increase in ad spend, sales increase by ${params['slope']:.2f}.")
    insights.append(f"R-squared: {params['r_squared']:.1%} of variance in sales is explained by ad spend.")
    if params["p_value"] < 0.05:
        insights.append("The relationship is statistically significant (p < 0.05).")
    else:
        insights.append("The relationship is NOT statistically significant (p >= 0.05).")
    insights.append(f"Intercept: Baseline sales with zero ad spend = ${params['intercept']:.0f}.")
    insights.append(f"Standard error of slope: ${params['std_err']:.2f}.")
    return insights


def main():
    """Run the full exercise: generate data, plot, and report insights."""
    print("=" * 60)
    print("Pandas Q15: Scatter Plot with Trendline")
    print("=" * 60)

    # Generate data
    df = generate_sample_data()
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nDescriptive statistics:\n{df.describe()}")

    # Plot
    params = plot_scatter_trendline(df)

    # Insights
    print("\n" + "-" * 60)
    print("KEY INSIGHTS:")
    print("-" * 60)
    for i, insight in enumerate(extract_insights(df, params), 1):
        print(f"  {i}. {insight}")

    print("\n" + "=" * 60)
    print("Exercise complete. Plot saved as 'scatter_trendline.png'")
    print("=" * 60)

    return df, params


if __name__ == "__main__":
    main()
