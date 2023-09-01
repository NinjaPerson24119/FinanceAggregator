from finance_data.constants import STANDARD_COLUMNS
from pydantic import BaseModel
from preprocessor import Preprocessor
import pandas as pd

class CombineInOutColumnsConfig(BaseModel):
    in_column: str
    out_column: str

class CombineInOutColumns(Preprocessor):
    def __init__(self, in_out_amount_config: CombineInOutColumnsConfig):
        self.in_out_amount_config = in_out_amount_config

    def combine_in_out_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        # handle separate in/out amount columns by combining them into one column
        copy = df.copy()
        copy[self.in_out_amount_config.out_column] = copy[self.in_out_amount_config.out_column].fillna(0)
        copy[self.in_out_amount_config.in_column] = copy[self.in_out_amount_config.in_column].fillna(0)
        copy[STANDARD_COLUMNS['AMOUNT']] = copy.apply(lambda row: row[self.in_out_amount_config.in_column] - row[self.in_out_amount_config.out_column], axis=1)
        return copy

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.combine_in_out_columns(df)
