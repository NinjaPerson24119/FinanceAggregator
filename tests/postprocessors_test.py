import pandas as pd
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


def test_WithNotes():
    input_df = pd.DataFrame(
        [
            {
                StandardColumns.date: "2023-01-01",
                StandardColumns.name: "Some purchase",
                StandardColumns.amount: 10.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "AMAZON",
                StandardColumns.amount: 12.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "EBAY",
                StandardColumns.amount: 13.0,
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "HUSKY",
                StandardColumns.amount: 5,
            },
        ]
    )
    expected_df = pd.DataFrame(
        [
            {
                StandardColumns.date: "2023-01-01",
                StandardColumns.name: "Some purchase",
                StandardColumns.amount: 10.0,
                NOTES_COLUMN: "",
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "AMAZON",
                StandardColumns.amount: 12.0,
                NOTES_COLUMN: "What did you buy on Amazon?, Online Shopping",
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "EBAY",
                StandardColumns.amount: 13.0,
                NOTES_COLUMN: "What did you buy on eBay?, Online Shopping",
            },
            {
                StandardColumns.date: "2023-01-02",
                StandardColumns.name: "HUSKY",
                StandardColumns.amount: 5,
                NOTES_COLUMN: "What did you buy?",
            },
        ]
    )
    config = {
        "What did you buy on Amazon?": ["amazon", "amazon"],
        "What did you buy on eBay?": ["ebay"],
        "Online Shopping": ["amazon", "ebay"],
        "What did you buy?": ["husky"],
    }
    preprocessor = WithNotes(config)
    result = preprocessor.postprocess(input_df)

    pd.testing.assert_frame_equal(result, expected_df)
