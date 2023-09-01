from finance_data.constants import STANDARD_COLUMNS
from pydantic import BaseModel
import pandas as pd
from .postprocessor import Postprocessor

CATEGORY_COLUMN = "category"


class CategoriesConfig(BaseModel):
    categories: dict[str, list[str]]


class WithCategories(Postprocessor):
    def __init__(self, categories_config: list[CategoriesConfig]):
        self.categories_config = categories_config

    def category_from_row(self, row: pd.Series) -> str:
        for category_name, substrings in self.categories_config.items():
            for substring in substrings:
                if substring.lower() in row[STANDARD_COLUMNS["NAME"]].lower():
                    return category_name
        return ""

    def categorize(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.apply(lambda row: self.category_from_row(row), axis=1)

    def print_uncategorized_names(self, df: pd.DataFrame):
        uncategorized_names = df[df[CATEGORY_COLUMN] == ""][
            STANDARD_COLUMNS["NAME"]
        ].unique()
        if len(uncategorized_names):
            print(f"\n{len(uncategorized_names)} Uncategorized Names...\n")
            for name in uncategorized_names:
                print(name)

    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        result = self.categorize(df)
        self.print_uncategorized_names(df)
        return result
