import pytest
import pandas as pd
import datetime
from typing import Optional
from finance_aggregator.finance_data import (
    CategoriesConfig,
    WithCategories,
    CATEGORY_COLUMN,
    NotesConfig,
    WithNotes,
    NOTES_COLUMN,
    FilterByDate,
    FilterByName,
    NegateAmount,
    StandardColumns,
)


@pytest.mark.parametrize(
    "input_df,expected_df,start_date,end_date",
    [
        (
            pd.DataFrame(
                [
                    {
                        StandardColumns.date: datetime.datetime(2023, 1, 1),
                        StandardColumns.name: "A&W",
                        StandardColumns.amount: -10.0,
                    },
                    {
                        StandardColumns.date: datetime.datetime(2023, 2, 1),
                        StandardColumns.name: "AMAZON",
                        StandardColumns.amount: -12.0,
                    },
                ]
            ),
            pd.DataFrame(
                [
                    {
                        StandardColumns.date: datetime.datetime(2023, 1, 1),
                        StandardColumns.name: "A&W",
                        StandardColumns.amount: -10.0,
                    },
                ]
            ),
            datetime.datetime(2023, 1, 1),
            None,
        ),
        (
            pd.DataFrame(
                [
                    {
                        StandardColumns.date: datetime.datetime(2023, 1, 1),
                        StandardColumns.name: "A&W",
                        StandardColumns.amount: -10.0,
                    },
                    {
                        StandardColumns.date: datetime.datetime(2023, 2, 1),
                        StandardColumns.name: "AMAZON",
                        StandardColumns.amount: -12.0,
                    },
                    {
                        StandardColumns.date: datetime.datetime(2023, 2, 17),
                        StandardColumns.name: "Insurance",
                        StandardColumns.amount: -12.0,
                    },
                ]
            ),
            pd.DataFrame(
                [
                    {
                        StandardColumns.date: datetime.datetime(2023, 1, 1),
                        StandardColumns.name: "A&W",
                        StandardColumns.amount: -10.0,
                    },
                    {
                        StandardColumns.date: datetime.datetime(2023, 2, 1),
                        StandardColumns.name: "AMAZON",
                        StandardColumns.amount: -12.0,
                    },
                ]
            ),
            datetime.datetime(2023, 1, 1),
            datetime.datetime(2023, 2, 5),
        ),
    ],
    ids=["Missing end date inferred as end of month", "Explicit end date over a month"],
)
def test_FilterByDate(
    input_df: pd.DataFrame,
    expected_df: pd.DataFrame,
    start_date: datetime.datetime,
    end_date: Optional[datetime.datetime],
):
    preprocessor = FilterByDate(start_date, end_date)
    result = preprocessor.postprocess(input_df)

    pd.testing.assert_frame_equal(result, expected_df)


def test_NegateAmount():
    input_df = pd.DataFrame(
        [
            {
                StandardColumns.date: "2023-01-01",
                StandardColumns.name: "Card Payment",
                StandardColumns.amount: -10.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "AMAZON",
                StandardColumns.amount: 12.0,
            },
        ]
    )
    expected_df = pd.DataFrame(
        [
            {
                StandardColumns.date: "2023-01-01",
                StandardColumns.name: "Card Payment",
                StandardColumns.amount: 10.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "AMAZON",
                StandardColumns.amount: -12.0,
            },
        ]
    )
    preprocessor = NegateAmount()
    result = preprocessor.postprocess(input_df)

    pd.testing.assert_frame_equal(result, expected_df)


def test_WithCategories():
    input_df = pd.DataFrame(
        [
            {
                StandardColumns.date: "2023-01-01",
                StandardColumns.name: "Unknown Vendor",
                StandardColumns.amount: -10.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "AMAZON",
                StandardColumns.amount: -12.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "EBAY",
                StandardColumns.amount: -13.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "McDonalds",
                StandardColumns.amount: -5,
            },
        ]
    )
    expected_df = pd.DataFrame(
        [
            {
                StandardColumns.date: "2023-01-01",
                StandardColumns.name: "Unknown Vendor",
                StandardColumns.amount: -10.0,
                CATEGORY_COLUMN: "",
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "AMAZON",
                StandardColumns.amount: -12.0,
                CATEGORY_COLUMN: "Online Shopping",
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "EBAY",
                StandardColumns.amount: -13.0,
                CATEGORY_COLUMN: "Online Shopping",
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "McDonalds",
                StandardColumns.amount: -5,
                CATEGORY_COLUMN: "Fast food",
            },
        ]
    )
    config: CategoriesConfig = {
        "Fast food": ["mcdonalds"],
        "Online Shopping": ["amazon", "ebay"],
    }
    preprocessor = WithCategories(config)
    result = preprocessor.postprocess(input_df)

    pd.testing.assert_frame_equal(result, expected_df)


def test_WithNotes():
    input_df = pd.DataFrame(
        [
            {
                StandardColumns.date: "2023-01-01",
                StandardColumns.name: "Some purchase",
                StandardColumns.amount: -10.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "AMAZON",
                StandardColumns.amount: -12.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "EBAY",
                StandardColumns.amount: -13.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "HUSKY",
                StandardColumns.amount: -5,
            },
        ]
    )
    expected_df = pd.DataFrame(
        [
            {
                StandardColumns.date: "2023-01-01",
                StandardColumns.name: "Some purchase",
                StandardColumns.amount: -10.0,
                NOTES_COLUMN: "",
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "AMAZON",
                StandardColumns.amount: -12.0,
                NOTES_COLUMN: "What did you buy on Amazon?, Online Shopping",
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "EBAY",
                StandardColumns.amount: -13.0,
                NOTES_COLUMN: "What did you buy on eBay?, Online Shopping",
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "HUSKY",
                StandardColumns.amount: -5,
                NOTES_COLUMN: "What did you buy?",
            },
        ]
    )
    config: NotesConfig = {
        "What did you buy on Amazon?": ["amazon", "amazon"],
        "What did you buy on eBay?": ["ebay"],
        "Online Shopping": ["amazon", "ebay"],
        "What did you buy?": ["husky"],
    }
    preprocessor = WithNotes(config)
    result = preprocessor.postprocess(input_df)

    pd.testing.assert_frame_equal(result, expected_df)
