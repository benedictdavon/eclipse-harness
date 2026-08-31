from typing import Protocol


class Handler(Protocol):
    def parse(self, value: str) -> dict[str, str]: ...
