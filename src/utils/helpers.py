"""
General helper utilities.
"""

from typing import Iterable


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers.

    Args:
        numerator: Numerator value.
        denominator: Denominator value.
        default: Default when denominator is zero.

    Returns:
        Division result or default.
    """
    if denominator == 0:
        return default
    return numerator / denominator


def format_currency(amount: float) -> str:
    """
    Format a number as currency.

    Args:
        amount: Numeric amount.

    Returns:
        Currency string.
    """
    return f"${amount:,.0f}"


def unique_list(values: Iterable[str]) -> list[str]:
    """
    Return sorted unique values.

    Args:
        values: Iterable of strings.

    Returns:
        Sorted list of unique values.
    """
    return sorted(set(values))
