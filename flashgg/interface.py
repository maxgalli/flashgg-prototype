import logging
logger = logging.getLogger(__name__)


class Dataset:
    def __init__(self, name, tree_name, file_names):
        self.name = name
        self.tree_name = tree_name
        self.file_names = [fn for fn in file_names]

    def __str__(self):
        return "Dataset-{}".format(self.name)

    def __repr__(self):
        return self.__str__()


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


class Task:
    def __init__(self, dataset, transformations, action="dump"):
        self.dataset = dataset
        self.transformations = transformations
        self.action = action
