variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "vibe-poc"
}

variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.42.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "Two public subnet CIDR blocks for ALB and ECS tasks."
  type        = list(string)
  default     = ["10.42.1.0/24", "10.42.2.0/24"]

  validation {
    condition     = length(var.public_subnet_cidrs) == 2
    error_message = "Provide exactly two public subnet CIDRs."
  }
}

variable "backend_cpu" {
  description = "Backend Fargate task CPU units."
  type        = number
  default     = 512
}

variable "backend_memory" {
  description = "Backend Fargate task memory in MiB."
  type        = number
  default     = 1024
}

variable "frontend_cpu" {
  description = "Frontend Fargate task CPU units."
  type        = number
  default     = 512
}

variable "frontend_memory" {
  description = "Frontend Fargate task memory in MiB."
  type        = number
  default     = 1024
}

variable "backend_desired_count" {
  description = "Desired number of backend tasks."
  type        = number
  default     = 1
}

variable "frontend_desired_count" {
  description = "Desired number of frontend tasks."
  type        = number
  default     = 1
}

variable "backend_image_tag" {
  description = "Docker image tag to deploy for the backend service."
  type        = string
  default     = "latest"
}

variable "frontend_image_tag" {
  description = "Docker image tag to deploy for the frontend service."
  type        = string
  default     = "latest"
}

variable "optnai_base_url" {
  description = "OptnAI API base URL passed to the backend container."
  type        = string
}

variable "optnai_api_key" {
  description = "OptnAI API key passed to the backend container."
  type        = string
  sensitive   = true
}

variable "optnai_model" {
  description = "OptnAI model name passed to the backend container."
  type        = string
}

variable "allowed_cidr_ingress" {
  description = "CIDR blocks allowed to access the public ALB listener."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
