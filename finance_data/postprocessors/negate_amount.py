from finance_data.constants import STANDARD_COLUMNS
from .postprocessor import Postprocessor
import pandas as pd


class NegateAmount(Postprocessor):
    def negate_amount(self, df: pd.DataFrame) -> pd.DataFrame:
        # some credit cards indicate expenses with positive values, so negate the amount
        copy = df.copy()
        copy[STANDARD_COLUMNS["AMOUNT"]] = copy.apply(
            lambda row: -row[STANDARD_COLUMNS["AMOUNT"]], axis=1
        )
        return copy

    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.negate_amount(df)
