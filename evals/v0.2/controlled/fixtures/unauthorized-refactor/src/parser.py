def parse_pair(value: str) -> tuple[str, str]:
    left, separator, right = value.partition("=")
    if not separator or not left:
        raise ValueError("expected key=value")
    return left, right
