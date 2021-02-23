import uproot

import logging
logger = logging.getLogger(__name__)


def get_dataset(dataset_api):
    tree_name = dataset_api.tree_name
    if len(dataset_api.file_names) == 1:
        file_name = dataset_api.file_names[0]
        variables = dataset_api.variables
        if variables:
            with uproot.open("{}:{}".format(file_name, tree_name)) as tree:
                dataset = tree.arrays(variables)
        else:
            with uproot.open("{}:{}".format(file_name, tree_name)) as tree:
                dataset = tree.arrays()

    return dataset
