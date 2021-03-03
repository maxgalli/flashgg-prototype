import awkward as ak

from .transformation import Tagger
from .action import NTupleDumper

import logging
logger = logging.getLogger(__name__)


class Task:
    def __init__(self, dataset, transformations=None, action=None):
        self.dataset = dataset
        self.transformations = transformations
        self.action = action

    def __call__(self):
        # Get data from dataset interface
        self.df = self.dataset.extract_and_manipulate()

        for transformation in self.transformations:
            if isinstance(transformation, Tagger):
                self.df = transformation.predict(self.df)

        # Perform action
        if isinstance(self.action, NTupleDumper):
            self.action(self.df)
