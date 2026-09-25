"""
Day 7 - Statistics & A/B Testing
Problem 13: A/B Test with Hypothesis Testing
==============================================
Description:
    Given two groups (control and treatment) of conversion rates,
    perform a two-proportion z-test to determine if the treatment
    has a statistically significant effect.

Assumed inputs:
    control_conversions: number of conversions in control group
    control_total: total users in control group
    treatment_conversions: number of conversions in treatment group
    treatment_total: total users in treatment group

Solution:
    1. Compute conversion rates for each group.
    2. Compute pooled proportion.
    3. Compute z-statistic and p-value.
    4. Compare p-value to significance level (alpha = 0.05).

Complexity:
    Time:  O(1)   -- constant time computation
    Space: O(1)

SQL equivalent (for reference):
    SELECT 'control' AS group_name,
           SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) AS conversions,
           COUNT(*) AS total_users,
           AVG(converted) AS conversion_rate
    FROM   experiment_results
    WHERE  group_name = 'control'
    UNION ALL
    SELECT 'treatment' AS group_name,
           SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) AS conversions,
           COUNT(*) AS total_users,
           AVG(converted) AS conversion_rate
    FROM   experiment_results
    WHERE  group_name = 'treatment';
"""

import math
from dataclasses import dataclass


@dataclass
class ABTestResult:
    """Result of an A/B test."""
    control_rate: float
    treatment_rate: float
    lift: float
    z_statistic: float
    p_value: float
    significant: bool
    confidence_level: float


def two_proportion_z_test(
    control_conversions: int,
    control_total: int,
    treatment_conversions: int,
    treatment_total: int,
    alpha: float = 0.05
) -> ABTestResult:
    """Perform a two-proportion z-test for A/B testing.

    Args:
        control_conversions: Number of conversions in control group.
        control_total: Total users in control group.
        treatment_conversions: Number of conversions in treatment group.
        treatment_total: Total users in treatment group.
        alpha: Significance level (default 0.05).

    Returns:
        ABTestResult with all test statistics.
    """
    # Conversion rates
    p1 = control_conversions / control_total
    p2 = treatment_conversions / treatment_total

    # Pooled proportion
    p_pool = (control_conversions + treatment_conversions) / (
        control_total + treatment_total
    )

    # Standard error
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / control_total + 1 / treatment_total))

    # Z-statistic
    z = (p2 - p1) / se if se > 0 else 0

    # P-value (two-tailed)
    # Using normal approximation
    p_value = 2 * (1 - _normal_cdf(abs(z)))

    # Lift
    lift = (p2 - p1) / p1 if p1 > 0 else 0

    # Significance
    significant = p_value < alpha

    return ABTestResult(
        control_rate=p1,
        treatment_rate=p2,
        lift=lift,
        z_statistic=z,
        p_value=p_value,
        significant=significant,
        confidence_level=1 - alpha
    )


def _normal_cdf(x: float) -> float:
    """Approximate the standard normal CDF using the error function."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


if __name__ == "__main__":
    # Example: Control has 100 conversions out of 1000 users
    # Treatment has 120 conversions out of 1000 users
    result = two_proportion_z_test(
        control_conversions=100,
        control_total=1000,
        treatment_conversions=120,
        treatment_total=1000,
        alpha=0.05
    )

    print(f"Control rate: {result.control_rate:.4f}")
    print(f"Treatment rate: {result.treatment_rate:.4f}")
    print(f"Lift: {result.lift:.2%}")
    print(f"Z-statistic: {result.z_statistic:.4f}")
    print(f"P-value: {result.p_value:.4f}")
    print(f"Significant at {result.confidence_level:.0%} confidence: {result.significant}")
