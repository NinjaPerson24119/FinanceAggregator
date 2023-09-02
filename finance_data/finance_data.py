# required for FinanceData methods to annotate type as itself
from __future__ import annotations

import pandas as pd
from finance_data.constants import STANDARD_COLUMNS
from datetime import datetime
from pydantic import BaseModel
from .preprocessors import Preprocessor
from .postprocessors import Postprocessor
from dataclasses import dataclass, field
from finance_data.errors import ConfigurationError
from typing import Optional


class FinanceDataConfig(BaseModel):
    source: str
    column_mapping: dict[str, str]
    date_format: str
    add_missing_header: Optional[list[str]]


@dataclass
class FinanceDataConfigWithProcessors:
    source: str
    column_mapping: dict[str, str]
    date_format: str
    add_missing_header: Optional[list[str]] = None
    preprocessors: list[Preprocessor] = field(default_factory=list)
    postprocessors: list[Postprocessor] = field(default_factory=list)


class FinanceData:
    __std_columns = [
        STANDARD_COLUMNS["DATE"],
        STANDARD_COLUMNS["NAME"],
        STANDARD_COLUMNS["AMOUNT"],
        STANDARD_COLUMNS["SOURCE"],
    ]
    __std_loaded_columns = [x for x in __std_columns if x != STANDARD_COLUMNS["SOURCE"]]

    def __init__(self):
        self.__df = pd.DataFrame(columns=self.__std_columns)

    @classmethod
    def from_csv(cls, path: str, config: FinanceDataConfigWithProcessors):
        instance = cls()
        instance.__load(path, config)
        return instance

    def __load(self, path: str, config: FinanceDataConfigWithProcessors):
        print(f"Loading {config.source}...")
        self.__config = config
        if self.__config.add_missing_header is not None:
            self.__df = pd.read_csv(
                path, header=None, names=self.__config.add_missing_header
            )
        else:
            self.__df = pd.read_csv(path)

        self.__process()

    def __validate_column_mapping(self):
        loaded_columns = list(self.__df.columns.values)
        for loaded_column, mapped_to_column in self.__config.column_mapping.items():
            if not loaded_column in loaded_columns:
                raise ConfigurationError(
                    f"Cannot map '{loaded_column}' as a key because it is not a column in the source data. Source data has columns: {loaded_columns}"
                )
            if not mapped_to_column in self.__std_loaded_columns:
                raise ConfigurationError(
                    f"Cannot map'{mapped_to_column}' as a value because it is not a required standard column. Standard columns to load are: {self.__std_loaded_columns}"
                )

    def __validate_has_standardized_columns(self):
        for column in self.__std_columns:
            if not column in self.__df.columns.values:
                raise ConfigurationError(
                    f"Data is missing required column '{column}'. Data has columns: {self.__df.columns.values}"
                )

    def __standardize(self):
        # rename columns
        self.__validate_column_mapping()
        self.__df = self.__df.rename(columns=self.__config.column_mapping)

        # add source column
        self.__df[STANDARD_COLUMNS["SOURCE"]] = self.__config.source

        # validate that all standard columns are present
        self.__validate_has_standardized_columns()

        # slice off non-standard columns
        self.__df = self.__df[self.__std_columns]

        # convert date cells to datetime
        self.__df[STANDARD_COLUMNS["DATE"]] = self.__df[STANDARD_COLUMNS["DATE"]].apply(
            lambda date: pd.to_datetime(
                datetime.strptime(str(date), self.__config.date_format)
            )
        )

        # remove trailing whitespace
        self.__df[STANDARD_COLUMNS["NAME"]] = self.__df.apply(
            lambda row: row[STANDARD_COLUMNS["NAME"]].strip(), axis=1
        )

    def __process(self):
        # preprocessors cannot expect the standard columns to be present
        for preprocessor in self.__config.preprocessors:
            print(f"\tPreprocessing with {preprocessor.__class__.__name__}...")
            self.__df = preprocessor.preprocess(self.__df)

        self.__standardize()

        for postprocessor in self.__config.postprocessors:
            print(f"\tPostprocessing with {postprocessor.__class__.__name__}...")
            self.__df = postprocessor.postprocess(self.__df)

        print("\n")

    def combine(self, other: FinanceData):
        if other.__df.empty:
            return

        self.__df = pd.concat([self.__df, other.__df], ignore_index=True)
        self.__df = self.__df.sort_values(by=STANDARD_COLUMNS["DATE"])

    def to_csv(self, path: str):
        if self.__df.shape[0] == 0:
            print("\tNo data to save. Skipping write to CSV.")
            return
        self.__df.to_csv(path, index=False)
