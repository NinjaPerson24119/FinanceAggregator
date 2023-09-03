from finance_aggregator.finance_data.constants import StandardColumns
from finance_aggregator.finance_data.postprocessors.postprocessor import Postprocessor
import pandas as pd


class NegateAmount(Postprocessor):
    def negate_amount(self, df: pd.DataFrame) -> pd.DataFrame:
        # some credit cards indicate expenses with positive values, so negate the amount
        copy = df.copy()
        copy[StandardColumns.amount] = copy.apply(
            lambda row: -row[StandardColumns.amount], axis=1
        )
        return copy

    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.negate_amount(df)
