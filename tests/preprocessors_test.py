import pandas as pd
from finance_aggregator.finance_data import (
    CombineInOutColumnsConfig,
    CombineInOutColumns,
    StandardColumns,
)


def test_CombineInOutColumns():
    input_df = pd.DataFrame(
        [
            {"sent": 1.2, "received": 0.0},
            {"sent": 0.0, "received": 7.8},
            {"sent": 9.0, "received": 0.0},
            {"sent": 13.4, "received": 15.6},
            {"sent": 19.0, "received": 5.0},
            {"received": 14.0},
        ]
    )
    expected_df = pd.DataFrame(
        [
            {StandardColumns.amount: -1.2},
            {StandardColumns.amount: 7.8},
            {StandardColumns.amount: -9.0},
            {StandardColumns.amount: 2.2},
            {StandardColumns.amount: -14.0},
            {StandardColumns.amount: 14.0},
        ]
    )

    config = CombineInOutColumnsConfig(in_column="received", out_column="sent")
    preprocessor = CombineInOutColumns(config)
    result = preprocessor.preprocess(input_df)

    pd.testing.assert_frame_equal(result, expected_df)
