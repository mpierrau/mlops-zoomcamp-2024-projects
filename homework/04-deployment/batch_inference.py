#!/usr/bin/env python
# coding: utf-8

import os
from pathlib import Path
import pickle
from typing import Any
import uuid
import pandas as pd
import argparse
from sklearn.feature_extraction import DictVectorizer

def read_data(filename: str):
    df = pd.read_parquet(filename)
    categorical = ['PULocationID', 'DOLocationID']
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def generate_uuids(n:int) -> list[uuid.UUID]:
    return [str(uuid.uuid4()) for _ in range(n)]

def prepare_dictionaries(df: pd.DataFrame, include_target: bool = True) -> dict:
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    numerical = []
    if include_target:
        numerical.append('trip_distance')

    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts

def load_model(model_path: Path) -> tuple[DictVectorizer, Any]:
    with open(model_path, 'rb') as f_in:
        dv, model = pickle.load(f_in)

    return dv, model

def apply_model(year : int, month : int) -> None:
    run_id = os.getenv('RUN_ID', '123456')
    dv, model = load_model("model.bin")
    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')
    dicts = prepare_dictionaries(df)
    X = dv.transform(dicts)
    y_pred = model.predict(X)

    df['ride_id'] = generate_uuids(len(df))
    df['predicted_duration'] = y_pred

    df_result = df.filter([
        "ride_id",
        "predicted_duration",
        "lpep_pickup_datetime",
        "PULocationID",
        "DOLocationID",
        "duration",
        ])
    
    df_result.rename(columns={"duration":"actual_duration"}, inplace=True)
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id
    
    output_dir = f'./output/'
    output_file = f'{output_dir}/{year:04d}-{month:02d}.parquet'
    os.makedirs(output_dir, exist_ok=True)

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

    print(df_result.describe())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, default=2023, help="Which year data to load.")
    parser.add_argument("month", type=int, default=3, help="Which month data to load.")

    p = parser.parse_args()

    apply_model(p.year, p.month)