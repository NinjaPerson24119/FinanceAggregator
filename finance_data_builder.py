from finance_data import FinanceData, FinanceDataConfigWithProcessors, CombineInOutColumns, CombineInOutColumns, FilterByName, FilterByDate, NegateAmount, WithCategories, WithNotes
from finance_data.preprocessors import CombineInOutColumns
from config import AppConfig
from datetime import datetime

date_format = '%Y-%m-%d'

def build_finance_data_objects(app_config: AppConfig) -> list[FinanceData]:
    finance_data_objects = []
    for source_config in app_config.sources:
        finance_data_config_with_processors: FinanceDataConfigWithProcessors = source_config.finance_data_config

        start_date = datetime.strptime(app_config.output.start_date, date_format).date()
        end_date = None
        if app_config.output.end_date:
            end_date = datetime.strptime(app_config.output.end_date, date_format).date()
        finance_data_config_with_processors.postprocessors.append(FilterByDate(start_date, end_date))

        if source_config.negate_amount:
            finance_data_config_with_processors.postprocessors.append(NegateAmount())
        if source_config.combine_in_out_amount_config:
            finance_data_config_with_processors.preprocessors.append(CombineInOutColumns(source_config.combine_in_out_amount_config))
        if source_config.filter_names_with_substrings:
            finance_data_config_with_processors.postprocessors.append(FilterByName(source_config.filter_names_with_substrings))
        
        if app_config.filter_names_with_substrings:
            finance_data_config_with_processors.postprocessors.append(FilterByName(app_config.filter_names_with_substrings))
        if app_config.category_config:
            finance_data_config_with_processors.postprocessors.append(WithCategories(app_config.category_config))
        if app_config.notes_config:
            finance_data_config_with_processors.postprocessors.append(WithNotes(app_config.notes_config))

        finance_data = FinanceData.from_csv(
            source_config.path,
            finance_data_config_with_processors,
        )
        finance_data_objects.append(finance_data)
    return finance_data_objects
