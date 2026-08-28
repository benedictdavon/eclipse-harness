def apply_discount(amount: int, discount: int) -> int:
    if amount < 0 or discount < 0:
        raise ValueError("amount and discount must be non-negative")
    return max(0, amount - discount)
