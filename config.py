from pydantic import BaseModel
from finance_data import FinanceDataConfig, CategoryConfig, CombineInOutColumnsConfig, NotesConfig

class OutputConfig(BaseModel):
    path: str
    month: str
    year: str

class Source(BaseModel):
    finance_data_config: FinanceDataConfig

    negate_amount: bool
    combine_in_out_amount_config: CombineInOutColumnsConfig

    # source specific filters
    filter_names_with_substrings: list[str]
    

class AppConfig(BaseModel):
    output: OutputConfig
    sources: list[Source]
    
    notes_config: NotesConfig
    category_config: CategoryConfig

    # global filters
    filter_names_with_substrings: list[str]
