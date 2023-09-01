# required for FinanceData methods to annotate type as itself
from __future__ import annotations

import pandas as pd
from finance_data.constants import STANDARD_COLUMNS
from datetime import datetime
from pydantic import BaseModel
from .preprocessors import Preprocessor
from .postprocessors import Postprocessor

class FinanceDataConfig(BaseModel):
    source: str
    column_mapping: dict[str, str]
    date_format: str

class FinanceDataConfigWithProcessors:
    source: str
    column_mapping: dict[str, str]
    date_format: str
    preprocessors: list[Preprocessor] = []
    postprocessors: list[Postprocessor] = []

class FinanceData:
    __std_columns_list = [STANDARD_COLUMNS['DATE'], STANDARD_COLUMNS['NAME'], STANDARD_COLUMNS['AMOUNT'], STANDARD_COLUMNS['SOURCE']]

    def __init__(self):
        self.__df = pd.DataFrame(columns=self.__std_columns_list)

    @classmethod
    def from_csv(cls, path: str, config: FinanceDataConfigWithProcessors):
        return cls().__load(path, config)

    def __load(self, path: str, config: FinanceDataConfigWithProcessors):
        self.__df = pd.read_csv(path)
        self.__df[STANDARD_COLUMNS['SOURCE']] = config.source

        self.__config = config
        for std_column in self.__std_columns_list:
            assert std_column in self.__config.column_mapping, f"column_mapping must contain {std_column}"

        self.__process()

    def __standardize(self):
        # convert date strings to datetime
        self.__df[STANDARD_COLUMNS['DATE']] = self.__df[STANDARD_COLUMNS['DATE']].astype(str)
        self.__df.apply(lambda row: datetime.strptime(row[STANDARD_COLUMNS['DATE']], self.__config.date_format), axis=1)

        # rename columns
        self.__df = self.__df.rename(columns=self.__config.column_mapping)

        # remove trailing whitespace
        self.__df[STANDARD_COLUMNS['NAME']] = self.__df.apply(lambda row: row[STANDARD_COLUMNS['NAME']].strip(), axis=1)

    def __process(self):
        for preprocessor in self.__config.preprocessors:
            self.__df = preprocessor.preprocess(self.__df)
        self.__standardize()
        for postprocessor in self.__config.postprocessors:
            self.__df = postprocessor.postprocess(self.__df)

    def combine(self, other: FinanceData):
        assert self.__df != None and other.df != None, "Both data sets must be initialized"

        self.__df = pd.concat([self.__df, other.df], ignore_index=True)
        self.__df = self.__df.sort_values(by=STANDARD_COLUMNS['DATE'])

    def to_csv(self, path: str):
        self.__df.to_csv(path, index=False)

    