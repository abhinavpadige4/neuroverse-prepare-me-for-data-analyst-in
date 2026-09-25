"""
Problem 0014 - Python: A/B Test with Two-Proportion Z-Test
============================================================
Day 6 - Statistics & A/B Testing

Problem
-------
An A/B test compares conversion rates between a control group and a treatment
group. Given counts of successes and trials for each group, compute the
two-proportion z-test statistic and p-value, and decide whether to reject
the null hypothesis at alpha = 0.05.

Solution
--------
    p_pool = (x1 + x2) / (n1 + n2)
    se     = sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z      = (p1 - p2) / se
    p_value = 2 * (1 - Phi(|z|))   # two-sided

Notes
-----
- H0: p1 = p2 (no difference)
- H1: p1 != p2 (two-sided)
- Reject H0 if p_value < alpha.
- For large samples, the normal approximation is valid.
- scipy.stats.proportions_ztest does this in one call.

Complexity
----------
- Time:  O(1)
- Space: O(1)
"""

import math
from typing import Tuple

def two_proportion_z_test(x1: int, n1: int, x2: int, n2: int) -> Tuple[float, float, bool]:
    """Return (z_stat, p_value, reject_h0_at_0.05)."""
    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se
    # Two-sided p-value using the standard normal CDF (erf-based).
    p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return z, p_value, p_value < 0.05

if __name__ == "__main__":
    # Example: control 100/1000, treatment 130/1000
    z, p, reject = two_proportion_z_test(x1=100, n1=1000, x2=130, n2=1000)
    print(f"z = {z:.4f}")
    print(f"p-value = {p:.4f}")
    print(f"Reject H0 at alpha=0.05? {reject}")
