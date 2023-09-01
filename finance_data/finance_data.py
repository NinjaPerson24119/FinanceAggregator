# required for FinanceData methods to annotate type as itself
from __future__ import annotations

import pandas as pd
from finance_data.constants import STANDARD_COLUMNS
from datetime import datetime
from pydantic import BaseModel
from .preprocessors import Preprocessor
from .postprocessors import Postprocessor
from dataclasses import dataclass, field


class FinanceDataConfig(BaseModel):
    source: str
    column_mapping: dict[str, str]
    date_format: str


@dataclass
class FinanceDataConfigWithProcessors:
    source: str
    column_mapping: dict[str, str]
    date_format: str
    preprocessors: list[Preprocessor] = field(default_factory=list)
    postprocessors: list[Postprocessor] = field(default_factory=list)


class FinanceData:
    __std_columns = [
        STANDARD_COLUMNS["DATE"],
        STANDARD_COLUMNS["NAME"],
        STANDARD_COLUMNS["AMOUNT"],
        STANDARD_COLUMNS["SOURCE"],
    ]
    __std_loaded_columns = [
        x for x in __std_columns if x != STANDARD_COLUMNS["SOURCE"]
    ]

    def __init__(self):
        self.__df = pd.DataFrame(columns=self.__std_columns)

    @classmethod
    def from_csv(cls, path: str, config: FinanceDataConfigWithProcessors):
        return cls().__load(path, config)

    def __load(self, path: str, config: FinanceDataConfigWithProcessors):
        self.__config = config
        self.__df = pd.read_csv(path)

        # validate column mapping
        loaded_columns = list(self.__df.columns.values)
        for loaded_column, mapped_to_column in self.config.column_mapping.items():
            if not loaded_column in loaded_columns:
                raise ValueError(
                    f"column_mapping must contain {loaded_column} as a key"
                )
            if not mapped_to_column in self.__std_loaded_columns:
                raise ValueError(
                    f"column_mapping must map to {mapped_to_column} as a value"
                )

        self.__df[STANDARD_COLUMNS["SOURCE"]] = self.config.source

        # DEBUG
        print(self.config.source)
        print(self.__df.head())

        self.__process()

    def __standardize(self):
        # convert date strings to datetime
        self.__df[STANDARD_COLUMNS["DATE"]] = self.__df[
            STANDARD_COLUMNS["DATE"]
        ].astype(str)
        self.__df.apply(
            lambda row: datetime.strptime(
                row[STANDARD_COLUMNS["DATE"]], self.__config.date_format
            ),
            axis=1,
        )

        # rename columns
        self.__df = self.__df.rename(columns=self.__config.column_mapping)

        # remove trailing whitespace
        self.__df[STANDARD_COLUMNS["NAME"]] = self.__df.apply(
            lambda row: row[STANDARD_COLUMNS["NAME"]].strip(), axis=1
        )

    def __process(self):
        # preprocessors cannot expect the standard columns to be present
        for preprocessor in self.__config.preprocessors:
            self.__df = preprocessor.preprocess(self.__df)

        self.__standardize()
        for postprocessor in self.__config.postprocessors:
            self.__df = postprocessor.postprocess(self.__df)

    def combine(self, other: FinanceData):
        assert (
            self.__df != None and other.df != None
        ), "Both data sets must be initialized"

        self.__df = pd.concat([self.__df, other.df], ignore_index=True)
        self.__df = self.__df.sort_values(by=STANDARD_COLUMNS["DATE"])

    def to_csv(self, path: str):
        if self.__df.shape[0] == 0:
            print("No data to save. Skipping write to CSV.")
            return
        self.__df.to_csv(path, index=False)
