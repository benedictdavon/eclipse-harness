from .protocol import Handler

HANDLERS: dict[str, Handler] = {}


def register(name: str, handler: Handler) -> None:
    HANDLERS[name] = handler
