from pydantic import BaseModel
from finance_aggregator.finance_data import (
    FinanceDataConfig,
    CategoriesConfig,
    CombineInOutColumnsConfig,
    NotesConfig,
)
from typing import Optional


class OutputConfig(BaseModel):
    start_date: str
    end_date: Optional[str] = None


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

    notes: Optional[NotesConfig] = None
    categories: Optional[CategoriesConfig] = None

    # global filters
    filter_names_with_substrings: Optional[list[str]] = None
