from __future__ import annotations
import pandas as pd
from finance_data import STANDARD_COLUMNS
from datetime import datetime
from pydantic import BaseModel

STANDARD_COLUMNS = {"DATE": "date", "NAME": "name", "AMOUNT": "amount"}

class FinanceDataConfig(BaseModel):
    source: str
    column_mapping: dict[str, str]
    date_format: str

class FinanceData:
    std_columns_list = [STANDARD_COLUMNS['DATE'], STANDARD_COLUMNS['NAME'], STANDARD_COLUMNS['AMOUNT'], STANDARD_COLUMNS['SOURCE']]

    def __init__(self):
        self.df = pd.DataFrame(columns=self.std_columns_list)

    @classmethod
    def from_csv(cls, path: str, config: FinanceDataConfig):
        return cls().load(path, config)

    def load(self, path: str, config: FinanceDataConfig):
        self.df = pd.read_csv(path)
        self.df[STANDARD_COLUMNS['SOURCE']] = config.source

        self.config = config
        for std_column in self.std_columns_list:
            assert std_column in self.config.column_mapping, f"column_mapping must contain {std_column}"

        self.process()

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    def standardize(self):
        # convert date strings to datetime
        self.df[STANDARD_COLUMNS['DATE']] = self.df[STANDARD_COLUMNS['DATE']].astype(str)
        self.df.apply(lambda row: datetime.strptime(row[STANDARD_COLUMNS['DATE']], self.config.date_format), axis=1)

        # rename columns
        self.df = self.df.rename(columns=self.config.column_mapping)

        # remove trailing whitespace
        self.df[STANDARD_COLUMNS['NAME']] = self.df.apply(lambda row: row[STANDARD_COLUMNS['NAME']].strip(), axis=1)

    def process(self):
        self.preprocess()
        self.standardize()
        self.postprocess()

    def combine(self, other: FinanceData):
        assert self.df != None and other.df != None, "Both data sets must be initialized"

        self.df = pd.concat([self.df, other.df], ignore_index=True)
        self.df = self.df.sort_values(by=STANDARD_COLUMNS['DATE'])

    def to_csv(self, path: str):
        self.df.to_csv(path, index=False)

    