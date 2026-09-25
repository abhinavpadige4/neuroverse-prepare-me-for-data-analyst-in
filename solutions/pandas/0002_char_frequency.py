"""
Python Q10: Character Frequency Analysis
=========================================

Problem:
Given a string, compute the frequency of each character.
Return a pandas DataFrame with columns ['character', 'count'] sorted by count descending.

Example:
    Input:  "hello world"
    Output:
        character  count
        0         l        3
        1         o        2
        2         h        1
        3         e        1
        4         w        1
        5         r        1
        6         d        1
        7         (space)  1

Difficulty: Easy
Topics: pandas, string manipulation, value_counts, DataFrame construction
"""

import pandas as pd
from collections import Counter


def char_frequency(text: str, include_spaces: bool = True) -> pd.DataFrame:
    """
    Compute character frequency for a given string.

    Parameters
    ----------
    text : str
        The input string to analyze.
    include_spaces : bool, default=True
        If True, include whitespace characters in the count.
        If False, exclude all whitespace.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['character', 'count'] sorted by count descending,
        then alphabetically by character for ties.

    Examples
    --------
    >>> df = char_frequency("hello world")
    >>> print(df)
       character  count
    0           l      3
    1           o      2
    2           d      1
    3           e      1
    4           h      1
    5           r      1
    6           w      1
    7              1
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    if include_spaces:
        filtered_text = text
    else:
        filtered_text = text.replace(" ", "").replace("\t", "").replace("\n", "")

    if len(filtered_text) == 0:
        return pd.DataFrame(columns=["character", "count"])

    # Method 1: Using collections.Counter
    counter = Counter(filtered_text)

    # Build DataFrame
    df = pd.DataFrame(
        list(counter.items()),
        columns=["character", "count"]
    )

    # Sort by count descending, then character ascending for ties
    df = df.sort_values(
        by=["count", "character"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return df


def char_frequency_pandas(text: str, include_spaces: bool = True) -> pd.DataFrame:
    """
    Alternative implementation using pandas Series.value_counts().

    Parameters
    ----------
    text : str
        The input string to analyze.
    include_spaces : bool, default=True
        If True, include whitespace characters in the count.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['character', 'count'] sorted by count descending.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    if include_spaces:
        filtered_text = text
    else:
        filtered_text = text.replace(" ", "").replace("\t", "").replace("\n", "")

    if len(filtered_text) == 0:
        return pd.DataFrame(columns=["character", "count"])

    # Method 2: Using pandas value_counts
    series = pd.Series(list(filtered_text))
    counts = series.value_counts().reset_index()
    counts.columns = ["character", "count"]

    # Sort by count descending, then character ascending for ties
    counts = counts.sort_values(
        by=["count", "character"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return counts


def top_n_characters(text: str, n: int = 5, include_spaces: bool = True) -> pd.DataFrame:
    """
    Get the top N most frequent characters.

    Parameters
    ----------
    text : str
        The input string to analyze.
    n : int, default=5
        Number of top characters to return.
    include_spaces : bool, default=True
        If True, include whitespace characters.

    Returns
    -------
    pd.DataFrame
        Top N characters by frequency.
    """
    df = char_frequency(text, include_spaces=include_spaces)
    return df.head(n)


def character_percentage(text: str, include_spaces: bool = True) -> pd.DataFrame:
    """
    Compute character frequency as percentage of total characters.

    Parameters
    ----------
    text : str
        The input string to analyze.
    include_spaces : bool, default=True
        If True, include whitespace characters.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['character', 'count', 'percentage'] sorted by count descending.
    """
    df = char_frequency(text, include_spaces=include_spaces)

    if len(df) == 0:
        return df

    total = df["count"].sum()
    df["percentage"] = round((df["count"] / total) * 100, 2)

    return df


# =============================================================================
# TESTS
# =============================================================================

def run_tests():
    """Run comprehensive tests for character frequency functions."""
    print("=" * 60)
    print("Running Tests for Character Frequency Analysis")
    print("=" * 60)

    passed = 0
    failed = 0

    # Test 1: Basic frequency
    print("\nTest 1: Basic character frequency")
    result = char_frequency("hello")
    expected = pd.DataFrame({
        "character": ["l", "h", "e", "o"],
        "count": [2, 1, 1, 1]
    })
    assert result["character"].tolist() == expected["character"].tolist(), \
        f"Expected {expected['character'].tolist()}, got {result['character'].tolist()}"
    assert result["count"].tolist() == expected["count"].tolist(), \
        f"Expected {expected['count'].tolist()}, got {result['count'].tolist()}"
    print("  PASSED")
    passed += 1

    # Test 2: With spaces
    print("\nTest 2: Character frequency with spaces")
    result = char_frequency("hello world")
    assert result["count"].iloc[0] == 3, "Expected 'l' to have count 3"
    assert result["character"].iloc[0] == "l", "Expected 'l' to be most frequent"
    print("  PASSED")
    passed += 1

    # Test 3: Exclude spaces
    print("\nTest 3: Exclude spaces")
    result = char_frequency("hello world", include_spaces=False)
    assert " " not in result["character"].values, "Space should not be in results"
    print("  PASSED")
    passed += 1

    # Test 4: Empty string
    print("\nTest 4: Empty string")
    result = char_frequency("")
    assert len(result) == 0, "Empty string should return empty DataFrame"
    assert list(result.columns) == ["character", "count"], "Columns should be correct"
    print("  PASSED")
    passed += 1

    # Test 5: Single character
    print("\nTest 5: Single character")
    result = char_frequency("a")
    assert len(result) == 1
    assert result["character"].iloc[0] == "a"
    assert result["count"].iloc[0] == 1
    print("  PASSED")
    passed += 1

    # Test 6: All same characters
    print("\nTest 6: All same characters")
    result = char_frequency("aaaa")
    assert len(result) == 1
    assert result["character"].iloc[0] == "a"
    assert result["count"].iloc[0] == 4
    print("  PASSED")
    passed += 1

    # Test 7: Pandas method matches Counter method
    print("\nTest 7: Pandas method matches Counter method")
    text = "data analyst interview preparation"
    result1 = char_frequency(text)
    result2 = char_frequency_pandas(text)
    assert result1["character"].tolist() == result2["character"].tolist()
    assert result1["count"].tolist() == result2["count"].tolist()
    print("  PASSED")
    passed += 1

    # Test 8: Top N characters
    print("\nTest 8: Top N characters")
    result = top_n_characters("hello world", n=3)
    assert len(result) == 3
    assert result["count"].iloc[0] >= result["count"].iloc[1]
    assert result["count"].iloc[1] >= result["count"].iloc[2]
    print("  PASSED")
    passed += 1

    # Test 9: Character percentage
    print("\nTest 9: Character percentage")
    result = character_percentage("aabb")
    assert len(result) == 2
    assert result["percentage"].sum() == 100.0
    assert result["percentage"].iloc[0] == 50.0
    print("  PASSED")
    passed += 1

    # Test 10: Case sensitivity
    print("\nTest 10: Case sensitivity")
    result = char_frequency("Aa")
    assert len(result) == 2
    assert "A" in result["character"].values
    assert "a" in result["character"].values
    print("  PASSED")
    passed += 1

    # Test 11: Special characters
    print("\nTest 11: Special characters")
    result = char_frequency("hello!@#")
    assert "!" in result["character"].values
    assert "@" in result["character"].values
    assert "#" in result["character"].values
    print("  PASSED")
    passed += 1

    # Test 12: Type error handling
    print("\nTest 12: Type error handling")
    try:
        char_frequency(123)
        assert False, "Should have raised TypeError"
    except TypeError:
        print("  PASSED")
        passed += 1

    # Test 13: Sorting with ties
    print("\nTest 13: Sorting with ties (alphabetical for same count)")
    result = char_frequency("abc")
    # All have count 1, should be sorted alphabetically
    assert result["character"].tolist() == ["a", "b", "c"]
    print("  PASSED")
    passed += 1

    # Test 14: Large string performance
    print("\nTest 14: Large string")
    large_text = "a" * 1000 + "b" * 500 + "c" * 250
    result = char_frequency(large_text)
    assert result["count"].iloc[0] == 1000
    assert result["character"].iloc[0] == "a"
    print("  PASSED")
    passed += 1

    # Test 15: Unicode characters
    print("\nTest 15: Unicode characters")
    result = char_frequency("café")
    assert "é" in result["character"].values
    print("  PASSED")
    passed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("=" * 60)

    return passed == (passed + failed)


# =============================================================================
# DEMO / USAGE EXAMPLES
# =============================================================================

def demo():
    """Demonstrate usage of character frequency functions."""
    print("=" * 60)
    print("Character Frequency Analysis - Demo")
    print("=" * 60)

    # Example 1: Basic usage
    print("\n--- Example 1: Basic Character Frequency ---")
    text = "data analyst interview preparation"
    print(f"Input: '{text}'")
    df = char_frequency(text)
    print(df.to_string(index=False))

    # Example 2: Without spaces
    print("\n--- Example 2: Without Spaces ---")
    df = char_frequency(text, include_spaces=False)
    print(df.to_string(index=False))

    # Example 3: Top 5 characters
    print("\n--- Example 3: Top 5 Characters ---")
    df = top_n_characters(text, n=5)
    print(df.to_string(index=False))

    # Example 4: Percentage breakdown
    print("\n--- Example 4: Character Percentage ---")
    df = character_percentage(text)
    print(df.to_string(index=False))

    # Example 5: Real-world text analysis
    print("\n--- Example 5: Real-World Text Analysis ---")
    paragraph = """Python is a powerful programming language used for data analysis.
    It has excellent libraries like pandas, numpy, and matplotlib for data science."""
    print(f"Text length: {len(paragraph)} characters")
    print(f"Unique characters: {len(char_frequency(paragraph))}")
    print(f"\nMost frequent characters:")
    df = top_n_characters(paragraph, n=10)
    print(df.to_string(index=False))

    # Example 6: Compare two texts
    print("\n--- Example 6: Compare Character Distributions ---")
    text1 = "hello world"
    text2 = "goodbye world"
    print(f"Text 1: '{text1}'")
    print(f"Text 2: '{text2}'")

    df1 = char_frequency(text1, include_spaces=False)
    df2 = char_frequency(text2, include_spaces=False)

    print("\nText 1 frequencies:")
    print(df1.to_string(index=False))
    print("\nText 2 frequencies:")
    print(df2.to_string(index=False))


if __name__ == "__main__":
    # Run tests first
    success = run_tests()

    # Run demo if tests pass
    if success:
        print("\nAll tests passed! Running demo...\n")
        demo()
    else:
        print("\nSome tests failed. Please fix before running demo.")
