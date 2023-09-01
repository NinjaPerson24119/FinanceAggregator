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
    __std_loaded_columns = [x for x in __std_columns if x != STANDARD_COLUMNS["SOURCE"]]

    def __init__(self):
        self.__df = pd.DataFrame(columns=self.__std_columns)

    @classmethod
    def from_csv(cls, path: str, config: FinanceDataConfigWithProcessors):
        return cls().__load(path, config)

    def __load(self, path: str, config: FinanceDataConfigWithProcessors):
        self.__config = config
        self.__df = pd.read_csv(path)

        self.__process()

    def __validate_columns(self):
        has_all_columns = True
        for column in self.__std_columns:
            if not column in self.__df.columns.values:
                has_all_columns = False
                break
        if has_all_columns:
            return

        # validate column mapping
        loaded_columns = list(self.__df.columns.values)
        for loaded_column, mapped_to_column in self.__config.column_mapping.items():
            if not loaded_column in loaded_columns:
                print(self.__df.head())
                raise ValueError(
                    f"Column validation failed. This may be because column_mapping did not contain '{loaded_column}' as a key."
                )
            if not mapped_to_column in self.__std_loaded_columns:
                print(self.__df.head())
                raise ValueError(
                    f"Column validation failed. This may be because column_mapping did not map to '{mapped_to_column}' as a value."
                )

    def __standardize(self):
        # rename columns, if they pass or fail, we still want to validate to surface information to the user
        try:
            self.__df = self.__df.rename(columns=self.__config.column_mapping)
        finally:
            self.__validate_columns()

        # add source column
        self.__df[STANDARD_COLUMNS["SOURCE"]] = self.__config.source

        # convert date strings to datetime
        self.__df[STANDARD_COLUMNS["DATE"]] = self.__df[STANDARD_COLUMNS["DATE"]].apply(
            lambda date_str: pd.to_datetime(datetime.strptime(
                date_str, self.__config.date_format
            ))
        )
        print(self.__df.head())

        # remove trailing whitespace
        self.__df[STANDARD_COLUMNS["NAME"]] = self.__df.apply(
            lambda row: row[STANDARD_COLUMNS["NAME"]].strip(), axis=1
        )

    def __process(self):
        # preprocessors cannot expect the standard columns to be present
        for preprocessor in self.__config.preprocessors:
            print(f"Preprocessing with {preprocessor.__class__.__name__}...")
            self.__df = preprocessor.preprocess(self.__df)

        self.__standardize()

        for postprocessor in self.__config.postprocessors:
            print(f"Postprocessing with {postprocessor.__class__.__name__}...")
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
