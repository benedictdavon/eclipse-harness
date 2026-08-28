from .api import Sender


class EmailSender(Sender):
    def send(self, recipient: str, body: str) -> None:
        if not recipient or not body:
            raise ValueError("recipient and body are required")
