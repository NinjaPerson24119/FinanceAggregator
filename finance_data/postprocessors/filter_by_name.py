from finance_data.constants import STANDARD_COLUMNS
from .postprocessor import Postprocessor
import pandas as pd

class FilterByName(Postprocessor):
    def __init__(self, name_substrings_to_filter: list[str]):
        self.name_substrings_to_filter = name_substrings_to_filter

    def filter_by_name(self, df: pd.DataFrame) -> pd.DataFrame:
        copy = df.copy()
        for substring in self.name_substrings_to_filter:
            copy = copy[
                ~copy[STANDARD_COLUMNS["NAME"]].str.contains(substring)
            ]
        return copy

    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.filter_by_name(df)
