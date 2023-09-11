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
    Preprocessor,
    Postprocessor,
)
from finance_aggregator.finance_data.preprocessors import CombineInOutColumns
from finance_aggregator.config import AppConfig, SourceConfig
from datetime import datetime
from typing import List, Tuple

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

    ConditionalPreprocessorType = Tuple[Preprocessor, bool]
    conditional_preprocessors: List[ConditionalPreprocessorType] = [
        # source specific pre-processors
        [
            CombineInOutColumns(source_config.combine_in_out_amount_config),
            source_config.combine_in_out_amount_config,
        ],
    ]
    for preprocessor, condition in conditional_preprocessors:
        if condition:
            finance_data_config_with_processors.preprocessors.append(preprocessor)

    ConditionalPostprocessorType = Tuple[Postprocessor, bool]
    conditional_postprocessors: List[ConditionalPostprocessorType] = [
        # global post-processors
        [FilterByDate(start_date, end_date), True],
        [
            FilterByName(app_config.filter_names_with_substrings),
            app_config.filter_names_with_substrings,
        ],
        [WithCategories(app_config.categories), app_config.categories],
        [WithNotes(app_config.notes), app_config.notes],
        # source specific post-processors
        [NegateAmount(), source_config.negate_amount],
        [
            FilterByName(source_config.filter_names_with_substrings),
            source_config.filter_names_with_substrings,
        ],
    ]
    for postprocessor, condition in conditional_postprocessors:
        if condition:
            finance_data_config_with_processors.postprocessors.append(postprocessor)

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
