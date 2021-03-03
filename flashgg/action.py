import awkward as ak

import logging
logger = logging.getLogger(__name__)


class NTupleDumper():
    def __init__(self, output_file):
        self.output_file = output_file

    def __call__(self, df):
        ak.to_parquet(df, self.output_file)
