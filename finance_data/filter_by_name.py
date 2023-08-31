from finance_data_base import FinanceDataBase
from constants import STANDARD_COLUMNS

class FinanceDataFilterByName(FinanceDataBase):
    def __init__(self, finance_data: FinanceDataBase, name_substrings_to_filter: list[str]):
        self.finance_data = finance_data
        self.name_substrings_to_filter = name_substrings_to_filter

    def filter_by_name(self):
        for substring in self.name_substrings_to_filter:
            self.df = self.df[
                ~self.df[STANDARD_COLUMNS["NAME"]].str.contains(substring)
            ]

    def postprocess(self):
        super().postprocess()
        self.filter_by_name()
