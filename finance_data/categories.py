from finance_data_base import FinanceDataBase
from constants import STANDARD_COLUMNS

class FinanceDataWithCategories(FinanceDataBase):
    CATEGORY_COLUMN = 'category'

    def __init__(self, finance_data, categories):
        self.finance_data = finance_data
        self.categories = categories

    def categorize(self):
        # TODO
        with open(os.path.join(config_dir, categories_filename), 'r') as f:
            c = json.load(f)
    
        def categorize_row(in_row):
            for category in c["categories"]:
                for substring in c["categories"][category]:
                    if substring.lower() in in_row[STANDARD_COLUMNS['NAME']].lower():
                        return category
            return ''
        self.df[self.CATEGORY_COLUMN] = self.df.apply(lambda row: categorize_row(row), axis=1)

        uncategorized_names = self.df[self.df[self.CATEGORY_COLUMN] == ''][STANDARD_COLUMNS['NAME']].unique()
        if len(uncategorized_names):
            print(f"\n{len(uncategorized_names)} Uncategorized Names...\n")
            for name in uncategorized_names:
                print(name)
