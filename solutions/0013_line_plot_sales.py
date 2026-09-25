import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def create_monthly_sales_data():
    """Generate sample monthly sales data for demonstration."""
    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    sales = [12000, 15000, 18000, 16500, 21000, 24000,
             22000, 26000, 28000, 25000, 30000, 35000]
    df = pd.DataFrame({'month': months, 'sales': sales})
    return df


def plot_monthly_sales(df, output_path='monthly_sales_plot.png'):
    """Create a line plot of monthly sales using matplotlib.

    Args:
        df: DataFrame with 'month' and 'sales' columns.
        output_path: File path to save the plot.

    Returns:
        The saved file path.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        df['month'],
        df['sales'],
        marker='o',
        linewidth=2,
        markersize=8,
        color='#1f77b4',
        label='Monthly Sales'
    )

    ax.set_title('Monthly Sales Trend', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Sales ($)', fontsize=12)

    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'${x:,.0f}')
    )

    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper left', fontsize=11)

    for x, y in zip(df['month'], df['sales']):
        ax.annotate(
            f'${y:,.0f}',
            (x, y),
            textcoords='offset points',
            xytext=(0, 12),
            ha='center',
            fontsize=9,
            color='#333333'
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return output_path


if __name__ == '__main__':
    data = create_monthly_sales_data()
    print(data)
    saved = plot_monthly_sales(data)
    print(f'Plot saved to {saved}')
