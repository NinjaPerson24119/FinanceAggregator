from finance_data.finance_data import FinanceData
from finance_data import STANDARD_COLUMNS
from pydantic import BaseModel
import pandas as pd
from postprocessor import Postprocessor

CATEGORY_COLUMN = 'category'

class CategoryConfig(BaseModel):
    category: str
    # substrings to match in name
    substrings: list[str]

class FinanceDataWithCategories(Postprocessor):
    def __init__(self, categories: list[CategoryConfig]):
        self.categories = categories

    def category_from_row(self, row: pd.Series) -> str:
        for category in self.categories:
            for substring in self.category.substrings:
                if substring.lower() in row[STANDARD_COLUMNS['NAME']].lower():
                    return category
        return ''

    def categorize(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.apply(lambda row: self.category_from_row(row), axis=1)

    def print_uncategorized_names(self, df: pd.DataFrame):
        uncategorized_names = df[df[CATEGORY_COLUMN] == ''][STANDARD_COLUMNS['NAME']].unique()
        if len(uncategorized_names):
            print(f"\n{len(uncategorized_names)} Uncategorized Names...\n")
            for name in uncategorized_names:
                print(name)

    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        result = self.categorize(df)
        self.print_uncategorized_names(df)
        return result
