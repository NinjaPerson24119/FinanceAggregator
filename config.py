from pydantic import BaseModel
from finance_data import FinanceDataConfig, CategoriesConfig, CombineInOutColumnsConfig, NotesConfig
import datetime
from typing import Optional

class OutputConfig(BaseModel):
    path: str
    start_date: datetime.date
    end_date: Optional[datetime.date] = None

class SourceConfig(BaseModel):
    path: str

    finance_data_config: FinanceDataConfig
    negate_amount: Optional[bool] = None
    combine_in_out_amount_config: Optional[CombineInOutColumnsConfig] = None

    # source specific filters
    filter_names_with_substrings: Optional[list[str]] = None
    

class AppConfig(BaseModel):
    output: OutputConfig
    sources: list[SourceConfig]
    
    notes_config: Optional[NotesConfig] = None
    category_config: Optional[CategoriesConfig] = None

    # global filters
    filter_names_with_substrings: Optional[list[str]] = None
