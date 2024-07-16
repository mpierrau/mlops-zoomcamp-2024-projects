variable "aws_region" {
    description = "AWS region to create resources"
    default = "us-east-1"
}

variable "project_id" {
    description = "project_id"
    default = "mlops-zoomcamp"
}

variable "source_stream_name" {
    description = "Name of source Kinesis stream"
}

variable "output_stream_name" {
    description = "Name of output Kinesis stream"
}

variable "model_bucket_name" {
    description = "Name of the S3 bucket holding the model"
}

variable "ecr_repo_name" {
    description = "Name of ECR repository"
}

variable "ecr_image_tag" {
    description = "Tag of ECR docker image"
}

variable "lambda_function_local_path" {
    description = "Path to lambda_function.py"
}

variable "python_module_local_path" {
  description = "Path to model.py"
}

variable "docker_image_local_path" {
    description = "Path to Dockerfile"
}

variable "pipenv_local_path" {
  description = "Path to Pipenv.lock"
}

variable "lambda_function_name" {
  description = "Name of lambda function"
}