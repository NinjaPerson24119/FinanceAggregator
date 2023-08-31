from pydantic import BaseModel
from finance_data import CategoryConfig, CombineInOutAmountConfig, NotesConfig

class OutputConfig(BaseModel):
    path: str
    month: str
    year: str

class Source(BaseModel):
    name: str
    column_mapping: dict[str, str]
    date_format: str

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
