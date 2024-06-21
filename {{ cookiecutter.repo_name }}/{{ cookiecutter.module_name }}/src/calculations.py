# src/calculations.py

"""Basic module

This module is a template example and is only included to show how to document code.

This module allows user to make mathematical calculations.

Examples:
    >>> from test_env_3.src.module import square, add
    >>> square(2.0)
    4.0
    >>> square(4.0)
    16.0
    >>> add(2.0, 2.0)
    4.0
    >>> add(2.0, -2.0)
    0.0

The following methods are part of this module:

- `square(a)` - Returns the squared result of a number.
- `add(a, b)` - Returns the sum of two numbers.
"""

def square(a: float) -> float:
    """Multiple `a` by itself

    Examples:
        >>> square(2.0)
        4.0
        >>> square(4.0)
        16.0

    Args:
        a (float): Any number

    Returns:
        float: Returns `a`**2
    """
    return a**2


def add(a: float, b: float) -> float:
    """Add `a` and `b` together

    Examples:
        >>> add(2.0, 2.0)
        4.0
        >>> add(2.0, -2.0)
        0.0

    Args:
        a (float): Any number
        b (float): Any number

    Returns:
        float: Returns the sum of `a` and `b`
    """

    return a + b
