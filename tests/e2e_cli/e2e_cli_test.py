import pytest
import pandas as pd
import os
import tempfile
import subprocess


@pytest.mark.parametrize(
    "config_filename,output_csv_filename,expected_output_csv_filename",
    [
        (
            "missing_header_config.json",
            "missing_header_output.csv",
            "missing_header_expected_output.csv",
        ),
    ],
)
def test_e2e_cli(config_filename, output_csv_filename, expected_output_csv_filename):
    test_dir = os.path.dirname(os.path.realpath(__file__))
    temp_dir = tempfile.gettempdir()

    config_path = os.path.join(test_dir, config_filename)
    output_path = os.path.join(temp_dir, output_csv_filename)

    if os.path.exists(output_path):
        os.remove(output_path)

    command = f"finance-aggregator --config '{config_path}' --output '{output_path}'"
    output = subprocess.check_output(command, shell=True, text=True)
    print(output)
    assert os.path.exists(output_path), f"Output file {output_path} does not exist"

    output_csv = pd.read_csv(output_path)
    expected_output_csv = pd.read_csv(
        os.path.join(test_dir, expected_output_csv_filename)
    )

    pd.testing.assert_frame_equal(output_csv, expected_output_csv)
