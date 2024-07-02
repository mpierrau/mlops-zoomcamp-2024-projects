import lambda_function

event = {
  "Records": [
    {
      "kinesis": {
        "kinesisSchemaVersion": "1.0",
        "partitionKey": "1",
        "sequenceNumber": "49653421989601011160162729338971758445021140467343949826",
        "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDI1NgogICAgfQ==",
        "approximateArrivalTimestamp": 1719576400.538
      },
      "eventSource": "aws:kinesis",
      "eventVersion": "1.0",
      "eventID": "shardId-000000000000:49653421989601011160162729338971758445021140467343949826",
      "eventName": "aws:kinesis:record",
      "invokeIdentityArn": "arn:aws:iam::033377438032:role/lambda-kinesis-role",
      "awsRegion": "eu-north-1",
      "eventSourceARN": "arn:aws:kinesis:eu-north-1:033377438032:stream/ride-events"
    }
  ]
}

result = lambda_function.lambda_handler(
    event = event,
    context = None,
)

print(result) 

