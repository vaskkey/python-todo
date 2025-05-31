from abc import abstractmethod

from tasks.task import Task
from tasks.tasks_obj import TasksObj


class AbstractDb:
    """Class that handles reading and writing to a task database."""
    def __init__(self) -> None:
        pass

    @abstractmethod
    def read_all(self) -> TasksObj:
        """Reads all tasks."""
        pass

    @abstractmethod
    def read(self, idx: int) -> Task:
        """
        Read a single task

        Args:
            idx(int): Index of a task we want to read.
        """
        pass

    @abstractmethod
    def write(self, task: Task) -> int:
        """
        Write a single task

        Args:
            task(Task): Task we want to write to the db.
        """
        pass
