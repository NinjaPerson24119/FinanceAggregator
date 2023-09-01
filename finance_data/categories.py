from finance_data.finance_data import FinanceData
from finance_data import STANDARD_COLUMNS
from pydantic import BaseModel
import pandas as pd

CATEGORY_COLUMN = 'category'

class CategoryConfig(BaseModel):
    category: str
    # substrings to match in name
    substrings: list[str]

class FinanceDataWithCategories(FinanceData):
    def __init__(self, finance_data: FinanceData, categories: list[CategoryConfig]):
        self.finance_data = finance_data
        self.categories = categories

    def category_from_row(self, row: pd.Series) -> str:
        for category in self.categories:
            for substring in self.category.substrings:
                if substring.lower() in row[STANDARD_COLUMNS['NAME']].lower():
                    return category
        return ''

    def categorize(self):
        self.df[CATEGORY_COLUMN] = self.df.apply(lambda row: self.category_from_row(row), axis=1)

    def print_uncategorized_names(self):
        uncategorized_names = self.df[self.df[CATEGORY_COLUMN] == ''][STANDARD_COLUMNS['NAME']].unique()
        if len(uncategorized_names):
            print(f"\n{len(uncategorized_names)} Uncategorized Names...\n")
            for name in uncategorized_names:
                print(name)

    def postprocess(self):
        super().postprocess()
        self.categorize()
        self.print_uncategorized_names()
