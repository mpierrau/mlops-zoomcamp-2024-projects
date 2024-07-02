import json
import base64
import pickle
import boto3
import os
import mlflow

kinesis_client = boto3.client('kinesis')
PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'ride_predictions')
RUN_ID = os.getenv('RUN_ID')
EXP_ID = os.getenv('EXP_ID')
S3_URI = os.getenv('S3_BUCKET', 'mlflow-models-magnus-dev')

logged_model = f's3://{S3_URI}/{EXP_ID}/{RUN_ID}/artifacts/model'
model = mlflow.pyfunc.load_model(model_uri=logged_model)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features):
    pred = model.predict(features)
    return float(pred[0])

def lambda_handler(event, context):
    
    predictions = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)
        
        ride = ride_event['ride']
        ride_id = ride_event['ride_id']

        features = prepare_features(ride)
        prediction = predict(features)
        prediction_event = {
            'model': 'ride_duration_prediction_model',
            'version': RUN_ID,
            'prediction': {
                'ride_duration':prediction,
                'ride_id': ride_id
            }
        }
        predictions.append(prediction_event)
    
    TEST_RUN = (os.getenv('TEST_RUN', 'True') == 'True')
    print(TEST_RUN)
    if not TEST_RUN:
        kinesis_client.put_record(
            StreamName=PREDICTIONS_STREAM_NAME,
            Data=json.dumps(prediction_event),
            PartitionKey=str(ride_id),
            )
            
    return {
        'predictions':predictions
    }
