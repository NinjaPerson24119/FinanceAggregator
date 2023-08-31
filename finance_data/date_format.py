from finance_data_base import FinanceDataBase
from constants import STANDARD_COLUMNS

class FinanceDataWithDateFormat(FinanceDataBase):
    def __init__(self, finance_data):
        self.finance_data = finance_data

    def format_dates(self):
        # fix dates like 20220922 to 2022-09-22
        self.df[STANDARD_COLUMNS['DATE']] = self.df[STANDARD_COLUMNS['DATE']].astype(str)
        self.df[STANDARD_COLUMNS['DATE']] = self.df.apply(lambda row: f"{row[STANDARD_COLUMNS['DATE']][:4]}-{row[STANDARD_COLUMNS['DATE']][4:6]}-{row[STANDARD_COLUMNS['DATE']][6:8]}", axis=1)
