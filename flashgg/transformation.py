import awkward as ak
import numpy as np
import pickle
from time import time

import logging
logger = logging.getLogger(__name__)



class Cut:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return "Cut({}, '{}')".format(self.name, self.expression)

    def __repr__(self):
        return self.__str__()



class Tagger:
    def __init__(self, name, regressor_name, variables, systematics, predicted_variable):
        self.name = name
        self.regressor_name = regressor_name
        self.variables = [var for var in variables]
        self.systematics = [sys for sys in systematics]
        self.predicted_variable = predicted_variable


    def __str__(self):
        string = '\n'.join(["Tagger - {}:".format(self.name),
            "\t regressor: {}".format(self.regressor_name),
            "\t variables: {}".format(self.variables),
            "\t systematics: {}".format(self.systematics),
            "\t predicted variable: {}".format(self.predicted_variable)])

        return string


    def __repr__(self):
        return "Tagger - {}".format(self.name)


    def predict(self, df):
        start = time()
        self.set_regressor()
        logger.info("Applying {}".format(self))
        df[self.predicted_variable] = ak.Array(self._get_predictions_dict(df))
        stop = time()
        logger.info("Predicted dataframe: \n{} \nin {:.2f} seconds".format(df.type, stop - start))

        return df


    def set_regressor(self):
        self.regressor = pickle.load(open(self.regressor_name, 'rb'))


    def _get_predicted_array(self, df, sys):
        np_arr_input = np.array([df[var][sys] for var in self.variables])
        np_arr_output = self.regressor.predict(np_arr_input.T)
        return ak.from_numpy(np_arr_output)


    def _get_predictions_dict(self, df):
        predictions = {}
        for sys in self.systematics:
            predictions[sys] = self._get_predicted_array(df, sys)
        return predictions
