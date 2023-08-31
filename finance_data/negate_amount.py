from finance_data_base import FinanceDataBase
from constants import STANDARD_COLUMNS

class FinanceDataNegateAmount(FinanceDataBase):
    def __init__(self, finance_data: FinanceDataBase):
        self.finance_data = finance_data

    def negate_amount(self):
        # some credit cards indicate expenses with positive values, so negate the amount
        self.df[STANDARD_COLUMNS['AMOUNT']] = self.df.apply(lambda row: -row[STANDARD_COLUMNS['AMOUNT']], axis=1)

    def postprocess(self):
        super().postprocess()
        self.negate_amount()
