from .interface import Dataset
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
            for n, file_name in enumerate(task.dataset_api.file_names):
                dataset_api = Dataset(
                        "{}-{}".format(task.dataset_api.name, n),
                        task.dataset_api.tree_name,
                        [file_name],
                        task.dataset_api.variables
                        )
                small_task = Task(dataset_api, task.transformations, task.action)
                small_tasks.append(small_task)
        return small_tasks
