import json
import os
from pathlib import Path

from db.db import AbstractDb
from db.not_found import NotFound
from tasks.task import Task
from tasks.tasks_obj import TasksObj

class JsonDb(AbstractDb):
    """Class that handles reading and writing to a json task database."""

    def __init__(self) -> None:
        self.db_path = Path.home() / '.db.json'
        pass

    def read_all(self) -> TasksObj:
        """Reads all tasks."""
        self.__create_if_doesnt_exist()

        with open(self.db_path, "r") as file:
            data = json.load(file)

            if "tasks" in data:
                return data
            else:
                return { "tasks": [] }
        
    def read(self, idx: int) -> Task:
        """
        Read a single task

        Args:
            idx(int): Index of a task we want to read.
        """
        self.__create_if_doesnt_exist()

        contents = self.read_all()
        try:
            task = contents["tasks"][idx]
            return task
        except KeyError:
            raise NotFound()


    def write(self, task: Task) -> int:
        """
        Write a single task

        Args:
            task(Task): Task we want to write to the db.
        """
        contents = self.read_all()

        contents["tasks"].append(task)
        
        self.__write_all(contents)

        return len(contents["tasks"]) - 1

    def __create_if_doesnt_exist(self):
        """If our DB file doesn't exist - create it."""
        if not os.path.exists(self.db_path):
            self.__write_all({'tasks': []})

    def __write_all(self, tasks: TasksObj):
        """
        Writes new contents to db file

        Args:
            tasks(TasksObj): A new object to overwrite the contents.
        """
        with open(self.db_path, "w") as file:
            file.write(json.dumps(tasks))



