from pydantic import BaseModel
from finance_data import FinanceDataConfig, CategoriesConfig, CombineInOutColumnsConfig, NotesConfig
import datetime
from typing import Optional

class OutputConfig(BaseModel):
    path: str
    start_date: datetime.date
    end_date: Optional[datetime.date]

class SourceConfig(BaseModel):
    path: str

    finance_data_config: FinanceDataConfig
    negate_amount: Optional[bool]
    combine_in_out_amount_config: Optional[CombineInOutColumnsConfig]

    # source specific filters
    filter_names_with_substrings: Optional[list[str]]
    

class AppConfig(BaseModel):
    output: OutputConfig
    sources: list[SourceConfig]
    
    notes_config: Optional[NotesConfig]
    category_config: Optional[CategoriesConfig]

    # global filters
    filter_names_with_substrings: Optional[list[str]]
