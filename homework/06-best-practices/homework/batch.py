#!/usr/bin/env python
# coding: utf-8

import argparse
import os
from pathlib import Path
import pickle
import pandas as pd
from utils import (
    get_input_path,
    get_output_path,
    save_data,
    read_data,
)

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')

def prepare_data(df: pd.DataFrame, categorical_features: list[str]) -> pd.DataFrame:
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical_features] = df[categorical_features].fillna(-1).astype('int').astype('str')

    return df

def main(year: int, month: int, input_path: Path = None, output_path: Path = None) -> None:
    """
    Args:
        year (int): _description_
        month (int): _description_
    """
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
            }
    } if S3_ENDPOINT_URL is not None else {}

    input_path = input_path or get_input_path(year, month)
    output_path = output_path or get_output_path(year, month)

    input_options = options if input_path[:5] == 's3://' else {}
    output_options = options if output_path[:5] == 's3://' else {}

    df = read_data(input_path, input_options)
    
    print("read data", input_path)
    print(df)

    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ['PULocationID', 'DOLocationID']

    preprocessed_df = prepare_data(df, categorical_features=categorical)
    
    preprocessed_df['ride_id'] = f'{year:04d}/{month:02d}_' + preprocessed_df.index.astype('str')
    dicts = preprocessed_df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print('predicted mean duration:', y_pred.mean())
    df_result = pd.DataFrame()
    df_result['ride_id'] = preprocessed_df['ride_id']
    df_result['predicted_duration'] = y_pred

    save_data(df_result, output_path, output_options)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("year", type=int)
    parser.add_argument("month", type=int, choices=list(range(1,13)))
    parser.add_argument("--input-file", type=Path, default=None)
    parser.add_argument("--output-file", type=Path, default=None)
    p = parser.parse_args()

    main(p.year, p.month, p.input_file, p.output_file)
    