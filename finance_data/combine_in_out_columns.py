from finance_data_base import FinanceDataBase
from constants import STANDARD_COLUMNS
from pydantic import BaseModel

class CombineInOutColumnsConfig(BaseModel):
    in_column: str
    out_column: str
    combined_column: str

class FinanceDataCombineInOutColumns(FinanceDataBase):
    def __init__(self, finance_data: FinanceDataBase, in_out_amount_config: CombineInOutColumnsConfig):
        self.finance_data = finance_data
        self.in_out_amount_config = in_out_amount_config

    def combine_in_out_columns(self):
        # handle separate in/out amount columns by combining them into one column
        self.df[self.in_out_amount_config.out_column] = self.df[self.in_out_amount_config.out_column].fillna(0)
        self.df[self.in_out_amount_config.in_column] = self.df[self.in_out_amount_config.in_column].fillna(0)
        self.df[STANDARD_COLUMNS['AMOUNT']] = self.df.apply(lambda row: row[self.in_out_amount_config.out_column] - row[self.in_out_amount_config.in_column], axis=1)

    def preprocess(self):
        super().preprocess()
        self.combine_in_out_columns()
