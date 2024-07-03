
from datetime import datetime
import os
import pandas as pd

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')

def get_input_path(year: int, month: int) -> str:
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)

def get_output_path(year: int, month: int) -> str:
    default_output_pattern = 's3://nyc-duration/out/{year:04d}-{month:02d}.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)

def read_data(input_path: str, options: dict = None) -> pd.DataFrame:
    options = options or {}
    df = pd.read_parquet(input_path, storage_options=options)
    return df

def save_data(df: pd.DataFrame, output_path: str, options: dict = None) -> None:
    options = options or {}

    print(f"Saving to {output_path}")
    print(f"Using options {options}")
    df.to_parquet(
        output_path,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options,
    )

def dt(hour, minute, second=0) -> datetime:
    return datetime(2023, 1, 1, hour, minute, second)

def create_test_df() -> None:
    """Code for generating data for unit test in test_batch.py"""
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    output_path = get_input_path(2023, 3)
    save_data(df, output_path)
