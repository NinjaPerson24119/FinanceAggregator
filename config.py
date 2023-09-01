from pydantic import BaseModel
from finance_data import FinanceDataConfig, CategoryConfig, CombineInOutColumnsConfig, NotesConfig
import datetime

class OutputConfig(BaseModel):
    path: str
    start_date: datetime.date
    end_date: datetime.date | None

class SourceConfig(BaseModel):
    path: str

    finance_data_config: FinanceDataConfig
    negate_amount: bool
    combine_in_out_amount_config: CombineInOutColumnsConfig

    # source specific filters
    filter_names_with_substrings: list[str]
    

class AppConfig(BaseModel):
    output: OutputConfig
    sources: list[SourceConfig]
    
    notes_config: NotesConfig
    category_config: CategoryConfig

    # global filters
    filter_names_with_substrings: list[str]
