from .dataset import Dataset
from .interface import Task

import logging
logger = logging.getLogger(__name__)


class RunManager:
    def __init__(self, tasks):
        self.tasks = self._make_small_tasks(tasks)

    def run_locally(self, parallelization="sequential"):
        for task in self.tasks:
            task()

    def _make_small_tasks(self, tasks):
        small_tasks = []
        for task in tasks:
            for n, file_name in enumerate(task.dataset.file_names):
                dataset = Dataset(
                        "{}-{}".format(task.dataset.name, n),
                        task.dataset.tree_name,
                        [file_name],
                        task.dataset.variables
                        )
                small_task = Task(dataset, task.transformations, task.action)
                small_tasks.append(small_task)
        return small_tasks
