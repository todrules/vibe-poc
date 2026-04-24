variable "aws_region" {
  description = "AWS region for bootstrap resources."
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "vibe-poc"
}

variable "github_owner" {
  description = "GitHub repository owner (organization or username)."
  type        = string
  default     = "todrules"
}

variable "github_repo" {
  description = "GitHub repository name."
  type        = string
  default     = "vibe-poc"
}

variable "github_actions_role_name" {
  description = "Name of the IAM role for GitHub Actions deployments."
  type        = string
  default     = ""
}

locals {
  role_name = var.github_actions_role_name != "" ? var.github_actions_role_name : "${var.project_name}-github-actions"
}
