variable "bucket_name" {
  description = "Name of the bucket"
}

output "name" {
  value = aws_s3_bucket.s3_bucket.bucket
}