def calculate_total(amounts: list[int]) -> int:
    """Return the sum of non-negative integer amounts in cents."""
    if any(amount < 0 for amount in amounts):
        raise ValueError("amounts must be non-negative")
    return sum(amounts)
