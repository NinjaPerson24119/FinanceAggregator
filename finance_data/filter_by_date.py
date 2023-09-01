import calendar
import pandas as pd
from finance_data.finance_data import FinanceData
from finance_data import STANDARD_COLUMNS
import datetime

class FinanceDataFilterByDate(FinanceData): 
    def __init__(self, finance_data, start: datetime.datetime, end: datetime.datetime = None):
        self.finance_data = finance_data
        self.start = start
        self.end = end
        if end is None:
            # default to end of month defined by start
            self.end = datetime.datetime(start.year, start.month, calendar.monthrange(start.year, start.month)[1])

    def filter_by_date(self):
        self.df = self.df[(self.df[STANDARD_COLUMNS['DATE']] >= self.start) & (self.df[STANDARD_COLUMNS['DATE']] <= self.end)]

    def postprocess(self):
        super.postprocess()
        self.filter_by_date()
