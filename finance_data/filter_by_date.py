import calendar
import pandas as pd
from finance_data_base import FinanceDataBase
from constants import STANDARD_COLUMNS

class FinanceDataFilteredByDate(FinanceDataBase):
    # maps the first 3 characters of a month to its index.
    # e.g. "jan" -> 1
    MONTH_MAPPING = {month.lower(): index for index, month in enumerate(calendar.month_abbr) if month}
    
    def __init__(self, finance_data, month, year):
        self.finance_data = finance_data
        self.month = month
        self.year = year

    def filter_by_date(self):
        month = self.MONTH_MAPPING[self.month[:3]]
        day = calendar.monthrange(int(year), month)[1]
        self.df = self.df[(self.df[STANDARD_COLUMNS['DATE']] >= f'{year}-{month}-1') & (self.df[STANDARD_COLUMNS['DATE']] <= f'{year}-{month}-{day}')]
        self.df = self.df.sort_values(by=STANDARD_COLUMNS['DATE'])

    def postprocess(self):
        super.postprocess()
        self.filter_by_date()
