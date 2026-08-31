from typing import Protocol


class Sender(Protocol):
    def send(self, recipient: str, body: str) -> None: ...
