import pandas as pd
from constants import STANDARD_COLUMNS

class FinanceDataBase:
    std_columns_list = [STANDARD_COLUMNS['DATE'], STANDARD_COLUMNS['NAME'], STANDARD_COLUMNS['AMOUNT'], STANDARD_COLUMNS['SOURCE']]

    def __init__(self):
        self.df = pd.DataFrame(columns=self.std_columns_list)

    @classmethod
    def from_csv(cls, path, source):
        return cls().load(path, source) 

    def load(self, path, source):
        self.df = pd.read_csv(path)
        self.df[STANDARD_COLUMNS['SOURCE']] = source

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    def standardize(self, column_mapping):
        self.preprocess()

        for std_column in self.std_columns_list:
            assert std_column in column_mapping, f"column_mapping must contain {std_column}"
        self.df = self.df.rename(columns=column_mapping)

        self.postprocess()

    def combine(self, other):
        # TODO
        other.standardize()
        other.filter_by_names()

        self.df = pd.concat([self.df, other.df], ignore_index=True)

        # sort and filter by date
        self.filter_by_date()

        # remove trailing whitespace
        self.df[STANDARD_COLUMNS['NAME']] = self.df.apply(lambda row: row[STANDARD_COLUMNS['NAME']].strip(), axis=1)

    def to_csv(self, path):
        self.df.to_csv(path, index=False)

    