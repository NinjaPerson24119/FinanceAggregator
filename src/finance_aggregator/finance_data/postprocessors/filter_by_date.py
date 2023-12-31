import calendar
import pandas as pd
from finance_aggregator.finance_data.constants import StandardColumns
import datetime
from finance_aggregator.finance_data.postprocessors.postprocessor import Postprocessor


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
            (df[StandardColumns.date] >= pd.to_datetime(self.start))
            & (df[StandardColumns.date] <= pd.to_datetime(self.end))
        ]

    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.filter_by_date(df)
