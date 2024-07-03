"""
These tests are expected to be run with the following environmental variables set:
S3_ENDPOINT_URL
INPUT_FILE_PATTERN
OUTPUT_FILE_PATTERN
"""
import os
import pytest
from utils import (
    get_input_path,
    get_output_path,
    read_data,
    save_data,
)
import pandas as pd

def test_s3_read() -> None:
    input_path = get_input_path(2023, 3)
    
    try:
        _ = read_data(input_path)
    except Exception as e:
        pytest.fail(f"Function did not properly read data from S3: {e}")

def test_s3_write() -> None:
    output_path = get_output_path(1900, 1)
    df = pd.DataFrame()

    try:
        save_data(df, output_path)
    except Exception as e:
        pytest.fail(f"Function did not properly write data to S3: {e}")

def test_read_pred_write() -> None:
    # This test requires the file s3://nyc-duration/test/2023-03.parquet to exist
    # This can be setup for example using a conftest file or Makefile
    s3_endpoint_url = "http://localhost:4566"
    input_file_pattern = "s3://nyc-duration/test/{year:04d}-{month:02d}.parquet"
    output_file_pattern = "s3://nyc-duration/test/{year:04d}-{month:02d}-predictions.parquet"
    
    cmd = f"S3_ENDPOINT_URL='{s3_endpoint_url}' INPUT_FILE_PATTERN='{input_file_pattern}' OUTPUT_FILE_PATTERN='{output_file_pattern}' python batch.py 2023 3"
    res = os.system(cmd)

    assert res == 0