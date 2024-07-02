import json
import os
import time
import requests 
from deepdiff import DeepDiff

print("opening event file...")
with open("event.json", 'rt', encoding='utf-8') as f_in:
    event = json.load(f_in)
       
url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
print("posting...")
t1 = time.time()
response = requests.post(url, json=event, timeout=1000)
print("took", time.time() - t1, "seconds")

actual_response = response.json()

expected_response = {
    'predictions': [
            {
                'model': 'ride_duration_prediction_model',
                'version': os.getenv("RUN_ID", "2eb44a3db0f24d45b76bb6f0e1a71ab5"),
                'prediction': {
                    'ride_duration': 16.7,
                    'ride_id': 256,
                },
            }
    ]
}
diff = DeepDiff(actual_response, expected_response, significant_digits=1)
assert not diff , f"{diff=}\n{actual_response=}"

print(actual_response)