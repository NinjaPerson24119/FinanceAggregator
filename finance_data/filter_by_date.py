import calendar
import pandas as pd
from finance_data_base import FinanceDataBase
from constants import STANDARD_COLUMNS

class FinanceDataCreditCard(FinanceDataBase):
    def __init__(self, finance_data):
        self.finance_data = finance_data

class FinanceDataFilteredByDate:
    # maps the first 3 characters of a month to its full name.
    # e.g. "jan" -> "January"
    MONTH_MAPPING = {month.lower(): index for index, month in enumerate(calendar.month_abbr) if month}
    
    def __init__(self, finance_data):
        self.finance_data = finance_data

    def filter_by_date(self, month, year):
        month = self.MONTH_MAPPING[month[:3]]
        day = calendar.monthrange(int(year), month)[1]
        assert self.df[STANDARD_COLUMNS['DATE']].shape[0] == pd.to_datetime(self.df[STANDARD_COLUMNS['DATE']]).shape[0]
        self.df[STANDARD_COLUMNS['DATE']] = pd.to_datetime(self.df[STANDARD_COLUMNS['DATE']])
        self.df = self.df[(self.df[STANDARD_COLUMNS['DATE']] >= f'{year}-{month}-1') & (self.df[STANDARD_COLUMNS['DATE']] <= f'{year}-{month}-{day}')]
        self.df = self.df.sort_values(by=STANDARD_COLUMNS['DATE'])
