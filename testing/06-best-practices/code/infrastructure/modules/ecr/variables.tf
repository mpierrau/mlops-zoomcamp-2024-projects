variable "ecr_repo_name" {
  type = string
  description = "ECR repo name"
}

variable "lambda_function_local_path" {
  description = "Path to lambda_function.py"
}

variable "docker_image_local_path" {
  description = "Path to Dockerfile"
}

variable "pipenv_local_path" {
  description = "Path to Pipfile.lock"
}

variable "region" {
  type = string
  description = "AWS region to use"
  default = "us-east-1"
}

variable "ecr_image_tag" {
  description = "Docker image tag to use"
  default = "latest"
}

variable "account_id" { 
}