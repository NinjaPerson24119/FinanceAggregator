
from finance_data.constants import STANDARD_COLUMNS
from .preprocessor import Preprocessor
import pandas as pd

class AddMissingHeader(Preprocessor):
    def __init__(self, header: list[str]):
        self.header = header

    def add_header(self, df: pd.DataFrame) -> pd.DataFrame:
        copy = df.copy()
        if len(copy.columns) != len(self.header):
            raise ValueError(
                f"Header length ({len(self.header)}) does not match number of columns ({len(copy.columns)})"
            )
        copy.columns = self.header
        return copy

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.add_header(df)
