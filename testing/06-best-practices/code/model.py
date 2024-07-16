import logging
import os
import json
import base64
from typing import Any

import boto3
import mlflow

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_model_location(run_id):
    model_location = os.getenv('MODEL_LOCATION')

    if model_location is not None:
        return model_location

    experiment_id = os.getenv('MLFLOW_EXPERIMENT_ID', '1')
    model_bucket = os.getenv('MODEL_BUCKET', ' ')

    model_location = f"s3://{model_bucket}/{experiment_id}/{run_id}/artifacts/model"

    return model_location


def load_model(run_id: str):
    model_path = get_model_location(run_id)

    return mlflow.pyfunc.load_model(model_uri=model_path)


class ModelService:
    def __init__(
        self, model: Any, model_version: str = None, callbacks: list = None
    ) -> None:
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def prepare_features(self, ride):
        features = {}
        features['PU_DO'] = f"{ride['PULocationID']}_{ride['DOLocationID']}"
        features['trip_distance'] = ride['trip_distance']
        return features

    def predict(self, features):
        pred = self.model.predict(features)
        return round(float(pred[0]), 1)

    def base64_decode(self, encoded_data: str) -> dict:
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        return json.loads(decoded_data)

    def lambda_handler(self, event, context):
        # pylint: disable=unused-argument

        predictions = []
        for record in event['Records']:
            encoded_data = record['kinesis']['data']
            ride_event = self.base64_decode(encoded_data)

            ride = ride_event['ride']
            ride_id = ride_event['ride_id']

            features = self.prepare_features(ride)
            prediction = self.predict(features)
            prediction_event = {
                'model': 'ride_duration_prediction_model',
                'version': self.model_version,
                'prediction': {
                    'ride_duration': prediction,
                    'ride_id': ride_id,
                },
            }
            predictions.append(prediction_event)
        for callback in self.callbacks:
            callback(prediction_event)
        
        return {'predictions': predictions}


class KinesisCallback:
    def __init__(self, kinesis_client, prediction_stream_name):
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        logger.info("KinesisCallback.put_record")
        ride_id = prediction_event['prediction']['ride_id']
        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey=str(ride_id),
        )


def create_kinesis_client():
    endpoint_url = os.getenv('KINESIS_ENDPOINT_URL')
    if endpoint_url is None:
        logger.info("Creating kinesis client")
        return boto3.client('kinesis')
    return boto3.client('kinesis', endpoint_url=endpoint_url)


def init(
    prediction_stream_name: str,
    run_id: str,
    test_run: bool = False,
) -> ModelService:
    model = load_model(run_id=run_id)

    callbacks = []

    if not test_run:
        logger.info("Not a test run!")
        kinesis_client = create_kinesis_client()
        kinesis_callback = KinesisCallback(
            kinesis_client,
            prediction_stream_name,
        )
        callbacks.append(kinesis_callback.put_record)

    model_service = ModelService(model=model, model_version=run_id, callbacks=callbacks)

    return model_service
