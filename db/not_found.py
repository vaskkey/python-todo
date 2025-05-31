class NotFound(Exception):
    def __init__(self) -> None:
        super().__init__("Task not found")

