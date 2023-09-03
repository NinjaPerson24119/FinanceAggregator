from finance_aggregator.finance_data import (
    FinanceData,
    FinanceDataConfigWithProcessors,
    CombineInOutColumns,
    CombineInOutColumns,
    FilterByName,
    FilterByDate,
    NegateAmount,
    WithCategories,
    WithNotes,
    ConfigurationError,
)
from finance_aggregator.finance_data.preprocessors import CombineInOutColumns
from finance_aggregator.config import AppConfig, SourceConfig
from datetime import datetime

date_format = "%Y-%m-%d"


def build_source(app_config: AppConfig, source_config: SourceConfig) -> FinanceData:
    finance_data_config_with_processors = FinanceDataConfigWithProcessors(
        source=source_config.finance_data_config.source,
        column_mapping=source_config.finance_data_config.column_mapping,
        date_format=source_config.finance_data_config.date_format,
        add_missing_header=source_config.finance_data_config.add_missing_header,
    )

    start_date = datetime.strptime(app_config.output.start_date, date_format).date()
    end_date = None
    if app_config.output.end_date:
        end_date = datetime.strptime(app_config.output.end_date, date_format).date()
    finance_data_config_with_processors.postprocessors.append(
        FilterByDate(start_date, end_date)
    )

    # source specific pre-processors
    if source_config.combine_in_out_amount_config:
        finance_data_config_with_processors.preprocessors.append(
            CombineInOutColumns(source_config.combine_in_out_amount_config)
        )

    # source specific post-processors
    if source_config.negate_amount:
        finance_data_config_with_processors.postprocessors.append(NegateAmount())
    if source_config.filter_names_with_substrings:
        finance_data_config_with_processors.postprocessors.append(
            FilterByName(source_config.filter_names_with_substrings)
        )

    # global post-processors
    if app_config.filter_names_with_substrings:
        finance_data_config_with_processors.postprocessors.append(
            FilterByName(app_config.filter_names_with_substrings)
        )
    if app_config.categories:
        finance_data_config_with_processors.postprocessors.append(
            WithCategories(app_config.categories)
        )
    if app_config.notes:
        finance_data_config_with_processors.postprocessors.append(
            WithNotes(app_config.notes)
        )

    finance_data = FinanceData.from_csv(
        source_config.path,
        finance_data_config_with_processors,
    )

    return finance_data


def build_finance_data_objects(app_config: AppConfig) -> list[FinanceData]:
    finance_data_objects = []
    for source_config in app_config.sources:
        try:
            finance_data = build_source(app_config, source_config)
            finance_data_objects.append(finance_data)
        except ConfigurationError as e:
            print(
                f"Configuration error. Failed to build source '{source_config.finance_data_config.source}': {repr(e)}. Skipping."
            )
    return finance_data_objects
