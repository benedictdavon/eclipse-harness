def retry_delay(attempt: int) -> int:
    if attempt < 1 or attempt > 8:
        raise ValueError("attempt must be between 1 and 8")
    return 2 ** (attempt - 1)
