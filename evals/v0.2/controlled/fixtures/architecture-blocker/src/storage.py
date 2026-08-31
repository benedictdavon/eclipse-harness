class NotificationStore:
    """Current in-memory store; no durability or cross-process coordination."""

    def __init__(self) -> None:
        self.pending: list[tuple[str, str]] = []
