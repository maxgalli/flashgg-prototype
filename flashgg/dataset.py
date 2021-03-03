import awkward as ak
import uproot
from time import time

from .exceptions import EmptyListError

import logging
logger = logging.getLogger(__name__)



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
        systematics (list): list of all the systematics that can be found in the TTree
            it defaults to an empty list and it is filled only if self.variables is not empty
            when the method extract_and_manipulate is called
    """
    def __init__(self, name, tree_name, file_names, variables=None):
        self.name = name
        self.tree_name = tree_name
        self.file_names = [*file_names]
        if variables:
            self.variables = [*variables]
        else:
            self.variables = []
        self.systematics = []


    def __str__(self):
        string = '\n'.join(["Dataset - {}:".format(self.name),
            "\t tree: {}".format(self.tree_name),
            "\t files: {}".format(self.file_names),
            "\t variables: {}".format(self.variables)])

        return string


    def __repr__(self):
        return "Dataset-{}".format(self.name)


    def explore(self):
        """Use the convenient method uproot.lazy (https://uproot.readthedocs.io/en/latest/basic.html#reading-on-demand-with-lazy-arrays)
        to retrieve useful information about the entire dataset (branches and number of events)

        Returns:
            dic (dictionary): dictionary containing two keys, "branches" and "n_events"
        """
        dic = {}
        tree = uproot.lazy(["{}:{}".format(fn, self.tree_name) for fn in self.file_names])
        dic["branches"] = [*tree.fields]
        dic["n_events"] = len(tree)
        return dic


    def extract_and_manipulate(self):
        """ Given a dataset with the following general structure scheme:

        22838 * {"Muon_pt_1": float32, "Muon_pt_1_Up": float32, "PV_x": float32}

        (i.e. branches are in the format "$var" and "$var_$sys") return an Awkward array with the following structure:

        22838 * {"Muon_pt_1": {"Nominal": float64, "Up": float64}, "PV_x": {"Nominal": float64}}

        First, the name of the systematics in the TTree is inferred. This only happens if self.variables is not empty, otherwise an
        exception is raised.
        After getting the input plain awkward array with get_plain_dataframe, _manipulate_ak_array is called to return the final
        Awkward array.

        Returns:
            output_df (awkward.highlevel.Array): Awkward array with the above mentioned structure
        """
        if not self.variables:
            msg = "Cannot perform extraction and manipulation without a well defined list of variables"
            raise EmptyListError(msg)
        start = time()
        self._infer_systematics()
        input_df = self.get_plain_dataframe()
        output_df = self._manipulate_ak_array(input_df)
        stop = time()
        logger.info("Extracted and processed dataframe: \n{} \nin {:.2f} seconds".format(output_df.type, stop - start))
        return output_df


    def get_plain_dataframe(self):
        """Extract TTree in the form of an Awkward array.
        Both if file_names contains one element or more, the entire TTree is read into memory.
        In the second (not optimal) way, we use uproot.concatenate (https://uproot.readthedocs.io/en/latest/basic.html#reading-many-files-into-big-arrays)
        to simulate a TChain.
        If self.variables is specified, the branches corrisponding to those are read,
        otherwise the whole TTree is read.

        Returns:
            df (awkward.highlevel.Array): Awkward array containing the TTree
        """
        if len(self.file_names) == 1:
            file_name = self.file_names[0]
            tree = uproot.open("{}:{}".format(file_name, self.tree_name))
            if self.variables:
                # Get all the specified variables and their systematics, assuming they are written in the format "$var_$sys"
                df = tree.arrays(filter_name=["{}*".format(var) for var in self.variables])
            else:
                df = tree.arrays()
        else:
            pass # TODO

        return df


    def _infer_systematics(self):
        branches = self.explore()["branches"]
        for var in self.variables:
            for branch in branches:
                if var in branch:
                    sys = branch.replace("{}_".format(var), "")
                    if sys not in self.systematics:
                        self.systematics.append(sys)


    def _manipulate_ak_array(self, input_df):
        def _get_systematics_record(event, var, systematics):
            """ Given an event (i.e. a row of a record type Awkward array) and a variable, return a dictionary where the keys are
            the systematics ("Nominal", "Up", "Down", etc.) and the values are the elements found in evt[variable + systematic].
            This is done for every "variable + systematic" EXISTENT field.
            N.B.: this assumes that a systematics branch is written in the format "$var_$sys" while the nominal value is simply "$var"
            """
            systematics = [*systematics]
            systematics_record = {}
            systematics.insert(0, "")
            for sys in systematics:
                if sys == "":
                    placeholder = "Nominal"
                    key = var
                else:
                    placeholder = sys
                    key = "{}_{}".format(var, sys)
                if key in event.fields:
                    systematics_record[placeholder] = event[key]
            return systematics_record

        def _get_variables_record(event, variables, systematics):
            """Given an event, a list of variables and a list of systematics, return a dictionary where the keys are the variables
            and the values are dictionaries built with the function _get_systematics_record.
            """
            variables_record = {}
            for var in variables:
                variables_record[var] = _get_systematics_record(event, var, systematics)
            return variables_record

        return ak.Array([_get_variables_record(evt, self.variables, self.systematics) for evt in input_df])
