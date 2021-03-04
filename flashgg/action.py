from .exceptions import FormatNotSupported

import awkward as ak
import uproot3

import logging
logger = logging.getLogger(__name__)



class NTupleDumper():
    def __init__(self, output_file, variables=None):
        # Check if the output file has a supported format
        supported_formats = [
                'root', 'parquet'
                ]
        self.of_format = output_file.rsplit('.', maxsplit=1)[-1]
        if self.of_format not in supported_formats:
            raise FormatNotSupported(supported_formats)

        self.output_file = output_file

        if variables:
            self.variables = [*variables]
        else:
            self.variables = []


    def __call__(self, df):
        if self.of_format == "root":
            self._write_to_root(df)
            logger.info("Dumped file {}".format(self.output_file))
        elif self.of_format == "parquet":
            ak.to_parquet(df, self.output_file)
            logger.info("Dumped file {}".format(self.output_file))


    def _write_to_root(self, df):
        variables, systematics = self._infer_metadata(df)
        with uproot3.recreate(self.output_file) as f:
            branchdict = {}
            arraydict = {}
            for var in variables:
                for sys in systematics:
                    if sys in df[var].fields:
                        branchdict["{}_{}".format(var, sys)] = str(df[var][sys].type.type)
                        arraydict["{}_{}".format(var, sys)] = df[var][sys]
            f["OutputTree"] = uproot3.newtree(branchdict)
            f["OutputTree"].extend(arraydict)


    def _infer_metadata(self, df):
        if self.variables:
            variables = [var for var in df.fields if var in self.variables]
        else:
            variables = [*df.fields]
        systematics = []
        for var in df.fields:
            for sys in df[var].fields:
                if sys not in systematics:
                    systematics.append(sys)
        return variables, systematics
