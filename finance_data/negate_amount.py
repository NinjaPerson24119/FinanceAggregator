from finance_data.finance_data import FinanceData
from finance_data import STANDARD_COLUMNS

class FinanceDataNegateAmount(FinanceData):
    def __init__(self, finance_data: FinanceData):
        self.finance_data = finance_data

    def negate_amount(self):
        # some credit cards indicate expenses with positive values, so negate the amount
        self.df[STANDARD_COLUMNS['AMOUNT']] = self.df.apply(lambda row: -row[STANDARD_COLUMNS['AMOUNT']], axis=1)

    def postprocess(self):
        super().postprocess()
        self.negate_amount()
