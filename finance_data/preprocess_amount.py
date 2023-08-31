from finance_data_base import FinanceDataBase
from constants import STANDARD_COLUMNS
from pydantic import BaseModel

class CombineInOutAmountConfig(BaseModel):
    in_column: str
    out_column: str
    combined_column: str

class FinanceDataPreprocessAmount(FinanceDataBase):
    def __init__(self, finance_data: FinanceDataBase, negate_amount: bool, in_out_amount_config: CombineInOutAmountConfig | None = None):
        self.finance_data = finance_data
        self.in_out_amount_config = in_out_amount_config
        self.negate_amount = negate_amount

    def combine_in_out_columns(self):
        # handle separate in/out amount columns
        self.df[self.in_out_amount_config.out_column] = self.df[self.in_out_amount_config.out_column].fillna(0)
        self.df[self.in_out_amount_config.in_column] = self.df[self.in_out_amount_config.in_column].fillna(0)
        self.df[STANDARD_COLUMNS['AMOUNT']] = self.df.apply(lambda row: row[self.in_out_amount_config.out_column] - row[self.in_out_amount_config.in_column], axis=1)

    def negate_amount(self):
        # some credit cards indicate expenses with positive values, so negate the amount
        self.df[STANDARD_COLUMNS['AMOUNT']] = self.df.apply(lambda row: -row[STANDARD_COLUMNS['AMOUNT']], axis=1)

    def preprocess(self):
        super().preprocess()
        self.combine_in_out_columns()
        if self.negate_amount:
            self.negate_amount()
