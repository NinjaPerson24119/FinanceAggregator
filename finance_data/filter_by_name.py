from finance_data.finance_data import FinanceData
from finance_data import STANDARD_COLUMNS

class FinanceDataFilterByName(FinanceData):
    def __init__(self, finance_data: FinanceData, name_substrings_to_filter: list[str]):
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
