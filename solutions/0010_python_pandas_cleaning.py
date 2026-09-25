"""
Day 5 - Python Pandas Time Series & Cleaning
Problem 10: Data Cleaning Pipeline
=======================================
Description:
    Using pandas, clean a messy customers DataFrame:
    - Strip whitespace from string columns
    - Standardize case (title case for names)
    - Fill missing values
    - Remove duplicates
    - Validate email format

Assumed DataFrame columns:
    customer_id, name, email, signup_date, country

Solution:
    Chain pandas operations to clean each column.

Complexity:
    Time:  O(n)   -- single pass per operation
    Space: O(n)
"""

import re
import pandas as pd

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Clean a messy customers DataFrame.

    Args:
        df: DataFrame with columns
            [customer_id, name, email, signup_date, country].

    Returns:
        Cleaned DataFrame with:
            - stripped whitespace on string columns
            - title-cased names
            - missing country filled with 'Unknown'
            - missing signup_date filled with NaT
            - duplicates on customer_id removed (keep first)
            - invalid emails set to None
    """
    out = df.copy()

    # Strip whitespace on all object columns
    for col in out.select_dtypes(include=["object"]).columns:
        out[col] = out[col].astype(str).str.strip().replace("nan", pd.NA)

    # Title-case names
    if "name" in out.columns:
        out["name"] = out["name"].str.title()

    # Fill missing country
    if "country" in out.columns:
        out["country"] = out["country"].fillna("Unknown")

    # Ensure signup_date is datetime
    if "signup_date" in out.columns:
        out["signup_date"] = pd.to_datetime(out["signup_date"], errors="coerce")

    # Validate emails
    if "email" in out.columns:
        out["email"] = out["email"].apply(
            lambda e: e if (isinstance(e, str) and EMAIL_RE.match(e)) else None
        )

    # Drop duplicates on customer_id
    if "customer_id" in out.columns:
        out = out.drop_duplicates(subset=["customer_id"], keep="first")

    return out.reset_index(drop=True)


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "customer_id": [1, 2, 2, 3, 4],
            "name": ["  alice smith ", "BOB JONES", "Bob Jones",
                     "carol", None],
            "email": ["alice@example.com", "bob@example.com",
                      "bad-email", "carol@example.com", None],
            "signup_date": ["2025-01-01", "2025-02-15", "2025-02-15",
                            "2025-03-10", "not-a-date"],
            "country": ["US", "US", "US", None, "UK"],
        }
    )
    print(clean_customers(sample))
