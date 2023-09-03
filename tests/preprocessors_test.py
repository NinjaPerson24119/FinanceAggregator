import pandas as pd
from finance_aggregator.finance_data import (
    CombineInOutColumnsConfig,
    CombineInOutColumns,
    STANDARD_COLUMNS,
)


def test_CombineInOutColumns():
    input_df = pd.DataFrame(
        [
            {"sent": 1.2, "received": 0.0},
            {"sent": 0.0, "received": 7.8},
            {"sent": 9.0, "received": 0.0},
            {"sent": 13.4, "received": 15.6},
            {"sent": 19.0, "received": 5.0},
        ]
    )
    expected_df = pd.DataFrame(
        [
            {STANDARD_COLUMNS["AMOUNT"]: -1.2},
            {STANDARD_COLUMNS["AMOUNT"]: 7.8},
            {STANDARD_COLUMNS["AMOUNT"]: -9.0},
            {STANDARD_COLUMNS["AMOUNT"]: 2.2},
            {STANDARD_COLUMNS["AMOUNT"]: -14.0},
        ]
    )

    config = CombineInOutColumnsConfig(in_column="received", out_column="sent")
    preprocessor = CombineInOutColumns(config)
    result = preprocessor.preprocess(input_df)

    pd.testing.assert_frame_equal(result, expected_df)
