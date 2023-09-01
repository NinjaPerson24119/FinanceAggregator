import calendar
import pandas as pd
from finance_data.constants import STANDARD_COLUMNS
import datetime
from .postprocessor import Postprocessor


class FilterByDate(Postprocessor):
    def __init__(self, start: datetime.datetime, end: datetime.datetime = None):
        self.start = start
        self.end = end
        if end is None:
            # default to end of month defined by start
            self.end = datetime.datetime(
                start.year, start.month, calendar.monthrange(start.year, start.month)[1]
            )

    def filter_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[
            (df[STANDARD_COLUMNS["DATE"]] >= self.start)
            & (df[STANDARD_COLUMNS["DATE"]] <= self.end)
        ]

    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.filter_by_date(df)
