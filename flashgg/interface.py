from .helpers.convert import get_dataset

import awkward as ak

import logging
logger = logging.getLogger(__name__)


def setup_logging(logfile, level=logging.INFO):
    from rich.logging import RichHandler
    logger = logging.getLogger("flashgg-logger")

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(rich_tracebacks=True),
            logging.FileHandler(logfile, "w")
            ]
        )

    return logger


class Dataset:
    """
    Interface to local or remote datasets.
    A dataset consists of a TTree object stored into one or more ROOT files.
    The latter is meant to support the TChain approach.

    Attributes:
        name (string): name given to the dataset
        tree_name (string): name with which the TTree is stored in the ROOT files
        file_names (list): names of the input ROOT files
        variables (list): branches we want to read from the TTree; if None, all branches
            will be read
    """
    def __init__(self, name, tree_name, file_names, variables=None):
        self.name = name
        self.tree_name = tree_name
        self.file_names = [*file_names]
        if variables:
            self.variables = [*variables]
        else:
            self.variables = variables

    def __str__(self):
        string = '\n'.join(["Dataset - {}:".format(self.name),
            "\t tree: {}".format(self.tree_name),
            "\t files: {}".format(self.file_names),
            "\t variables: {}".format(self.variables)])

        return string

    def __repr__(self):
        return "Dataset-{}".format(self.name)


class Cut:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return "Cut({}, '{}')".format(self.name, self.expression)

    def __repr__(self):
        return self.__str__()


class Tagger:
    def __init__(self, name, regressor, variables, systematics, predicted_variable):
        self.name = name
        self.regressor = regressor
        self.variables = [var for var in variables]
        self.systematics = [sys for sys in systematics]
        self.predicted_variable = predicted_variable

    def __str__(self):
        string = '\n'.join(["Tagger - {}:".format(self.name),
            "\t regressor: {}".format(self.regressor),
            "\t variables: {}".format(self.variables),
            "\t systematics: {}".format(self.systematics),
            "\t predicted variable: {}".format(self.predicted_variable)])

        return string

    def __repr__(self):
        return "Tagger - {}".format(self.name)


class NTupleDumper():
    def __init__(self, output_file):
        self.output_file = output_file


class Task:
    def __init__(self, dataset, transformations=None, action=None):
        self.dataset_api = dataset
        self.transformations = transformations
        self.action = action

    def __call__(self):
        # Get data from dataset interface
        logger.info("Extracting dataset:\n {}".format(self.dataset_api))
        self.dataset = get_dataset(self.dataset_api)

        # Perform action
        if isinstance(self.action, NTupleDumper):
            ak.to_parquet(self.dataset, self.action.output_file)
