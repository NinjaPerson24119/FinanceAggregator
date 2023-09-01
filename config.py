from pydantic import BaseModel
from finance_data.finance_data import FinanceDataBaseConfig
from finance_data.categories import CategoryConfig
from finance_data.combine_in_out_columns import CombineInOutAmountConfig
from finance_data.notes import NotesConfig

class OutputConfig(BaseModel):
    path: str
    month: str
    year: str

class Source(BaseModel):
    finance_data_config: FinanceDataBaseConfig

    negate_amount: bool
    combine_in_out_amount_config: CombineInOutAmountConfig

    # source specific filters
    filter_names_with_substrings: list[str]
    

class AppConfig(BaseModel):
    output: OutputConfig
    sources: list[Source]
    
    notes_config: NotesConfig
    category_config: CategoryConfig

    # global filters
    filter_names_with_substrings: list[str]
