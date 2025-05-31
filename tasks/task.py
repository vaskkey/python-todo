from typing import TypedDict


class Task(TypedDict):
    """Represents a single task user has added."""

    done: bool
    value: str
