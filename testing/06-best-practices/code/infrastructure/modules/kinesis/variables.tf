variable "stream_name" {
  type = string
  description = "Kinesis stream name"
}

variable "shard_count" {
  type = number
  description = "Number of Kinesis stream shards"
}

variable "retention_period" {
  type = number
  description = "Kinesis stream retention period"
}

variable "shard_level_metrics" {
  type = list(string)
  description = "shard_level_metrics"
  default = [ 
    "IncomingBytes",
    "OutgoingBytes",
    "OutgoingRecords",
    "ReadProvisionedThroughputExceeded",
    "WriteProvisionedThroughputExceeded",
    "IncomingRecords",
    "IteratorAgeMilliseconds",
    ]
}

variable "tags" {
  description = "Tags for Kinesis stream"
  default = "mlops-zoomcamp"
}