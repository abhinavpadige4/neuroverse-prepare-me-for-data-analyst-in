"""
Pandas Q15: Scatter Plot with Trendline
=========================================
Objective: Create a scatter plot with a linear regression trendline using Pandas and Matplotlib.

This exercise demonstrates:
- Generating synthetic data with a known relationship
- Computing linear regression coefficients
- Creating a scatter plot with a trendline
- Adding statistical annotations

Prerequisites:
- pandas
- numpy
- matplotlib
- scipy (for linear regression)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def generate_sample_data(n=100, seed=42):
    """
    Generate synthetic data with a known linear relationship.
    
    Parameters:
    -----------
    n : int
        Number of data points to generate
    seed : int
        Random seed for reproducibility
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with 'x' and 'y' columns
    """
    np.random.seed(seed)
    
    # Generate x values uniformly distributed between 0 and 100
    x = np.random.uniform(0, 100, n)
    
    # Generate y values with a linear relationship: y = 2.5*x + 10 + noise
    # This creates a clear trend with some random variation
    noise = np.random.normal(0, 15, n)
    y = 2.5 * x + 10 + noise
    
    df = pd.DataFrame({'x': x, 'y': y})
    return df


def compute_regression(df):
    """
    Compute linear regression statistics for the data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with 'x' and 'y' columns
    
    Returns:
    --------
    dict
        Dictionary containing regression statistics
    """
    slope, intercept, r_value, p_value, std_err = stats.linregress(df['x'], df['y'])
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_value ** 2,
        'p_value': p_value,
        'std_error': std_err
    }


def create_scatter_with_trendline(df, regression_stats, save_path=None):
    """
    Create a scatter plot with a linear regression trendline.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with 'x' and 'y' columns
    regression_stats : dict
        Dictionary containing regression statistics
    save_path : str, optional
        File path to save the plot. If None, plot is displayed interactively.
    
    Returns:
    --------
    tuple
        (fig, ax) matplotlib figure and axes objects
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Plot scatter points
    ax.scatter(
        df['x'], df['y'],
        alpha=0.6,
        color='steelblue',
        edgecolors='navy',
        linewidth=0.5,
        s=50,
        label='Data Points'
    )
    
    # Generate trendline
    x_line = np.linspace(df['x'].min(), df['x'].max(), 100)
    y_line = regression_stats['slope'] * x_line + regression_stats['intercept']
    
    # Plot trendline
    ax.plot(
        x_line, y_line,
        color='red',
        linewidth=2.5,
        label=f'Trendline: y = {regression_stats["slope"]:.2f}x + {regression_stats["intercept"]:.2f}'
    )
    
    # Add confidence interval band
    x_mean = df['x'].mean()
    n = len(df)
    residual_std = np.std(df['y'] - (regression_stats['slope'] * df['x'] + regression_stats['intercept']))
    
    # Calculate confidence interval
    se_pred = residual_std * np.sqrt(1 + 1/n + (x_line - x_mean)**2 / ((df['x'] - x_mean)**2).sum())
    
    ax.fill_between(
        x_line,
        y_line - 1.96 * se_pred,
        y_line + 1.96 * se_pred,
        color='red',
        alpha=0.15,
        label='95% Confidence Interval'
    )
    
    # Add statistics annotation
    stats_text = (
        f"R² = {regression_stats['r_squared']:.4f}\n"
        f"Slope = {regression_stats['slope']:.4f}\n"
        f"Intercept = {regression_stats['intercept']:.4f}\n"
        f"p-value = {regression_stats['p_value']:.2e}\n"
        f"Std Error = {regression_stats['std_error']:.4f}"
    )
    
    ax.text(
        0.02, 0.98, stats_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    )
    
    # Add labels and title
    ax.set_xlabel('X Variable', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y Variable', fontsize=12, fontweight='bold')
    ax.set_title('Scatter Plot with Linear Regression Trendline', fontsize=14, fontweight='bold')
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend
    ax.legend(loc='upper right', fontsize=10)
    
    # Tight layout
    plt.tight_layout()
    
    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    return fig, ax


def analyze_data_quality(df):
    """
    Perform basic data quality analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with 'x' and 'y' columns
    
    Returns:
    --------
    dict
        Dictionary containing data quality metrics
    """
    analysis = {
        'total_records': len(df),
        'missing_values': df.isnull().sum().to_dict(),
        'x_stats': {
            'mean': df['x'].mean(),
            'std': df['x'].std(),
            'min': df['x'].min(),
            'max': df['x'].max(),
            'median': df['x'].median()
        },
        'y_stats': {
            'mean': df['y'].mean(),
            'std': df['y'].std(),
            'min': df['y'].min(),
            'max': df['y'].max(),
            'median': df['y'].median()
        },
        'correlation': df['x'].corr(df['y'])
    }
    
    return analysis


def detect_outliers(df, threshold=2.0):
    """
    Detect outliers using z-score method.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with 'x' and 'y' columns
    threshold : float
        Z-score threshold for outlier detection
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing only outlier records
    """
    # Calculate z-scores for y values
    y_mean = df['y'].mean()
    y_std = df['y'].std()
    df['z_score'] = (df['y'] - y_mean) / y_std
    
    # Identify outliers
    outliers = df[df['z_score'].abs() > threshold].copy()
    
    return outliers


def main():
    """
    Main function to demonstrate the complete workflow.
    """
    print("=" * 60)
    print("Pandas Q15: Scatter Plot with Trendline")
    print("=" * 60)
    
    # Step 1: Generate sample data
    print("\n[Step 1] Generating sample data...")
    df = generate_sample_data(n=100, seed=42)
    print(f"Generated {len(df)} data points")
    print(f"\nFirst 5 rows:\n{df.head()}")
    
    # Step 2: Analyze data quality
    print("\n[Step 2] Analyzing data quality...")
    quality_metrics = analyze_data_quality(df)
    print(f"Total records: {quality_metrics['total_records']}")
    print(f"Missing values: {quality_metrics['missing_values']}")
    print(f"Correlation (x, y): {quality_metrics['correlation']:.4f}")
    print(f"\nX statistics: {quality_metrics['x_stats']}")
    print(f"Y statistics: {quality_metrics['y_stats']}")
    
    # Step 3: Detect outliers
    print("\n[Step 3] Detecting outliers...")
    outliers = detect_outliers(df, threshold=2.0)
    print(f"Found {len(outliers)} outliers (z-score > 2.0)")
    if len(outliers) > 0:
        print(f"\nOutlier records:\n{outliers[['x', 'y', 'z_score']]}")
    
    # Step 4: Compute regression
    print("\n[Step 4] Computing linear regression...")
    regression_stats = compute_regression(df)
    print(f"Slope: {regression_stats['slope']:.4f}")
    print(f"Intercept: {regression_stats['intercept']:.4f}")
    print(f"R²: {regression_stats['r_squared']:.4f}")
    print(f"p-value: {regression_stats['p_value']:.2e}")
    print(f"Standard Error: {regression_stats['std_error']:.4f}")
    
    # Step 5: Create visualization
    print("\n[Step 5] Creating scatter plot with trendline...")
    fig, ax = create_scatter_with_trendline(
        df, regression_stats,
        save_path='scatter_trendline.png'
    )
    
    # Step 6: Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Data points: {len(df)}")
    print(f"Outliers detected: {len(outliers)}")
    print(f"Linear relationship strength (R²): {regression_stats['r_squared']:.4f}")
    print(f"Statistical significance (p < 0.05): {regression_stats['p_value'] < 0.05}")
    print(f"\nInterpretation:")
    if regression_stats['r_squared'] > 0.7:
        print("  Strong linear relationship detected.")
    elif regression_stats['r_squared'] > 0.4:
        print("  Moderate linear relationship detected.")
    else:
        print("  Weak linear relationship detected.")
    
    if regression_stats['p_value'] < 0.05:
        print("  Relationship is statistically significant.")
    else:
        print("  Relationship is NOT statistically significant.")
    
    print("\n" + "=" * 60)
    print("Exercise Complete!")
    print("=" * 60)
    
    return df, regression_stats, outliers


if __name__ == '__main__':
    df, regression_stats, outliers = main()
