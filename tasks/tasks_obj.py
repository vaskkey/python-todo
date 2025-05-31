from typing import List, TypedDict

from tasks.task import Task


class TasksObj(TypedDict):
    """Contains a list of all tasks user has added"""

    tasks: List[Task]
