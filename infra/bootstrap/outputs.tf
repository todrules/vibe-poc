output "terraform_state_bucket" {
  description = "S3 bucket name for Terraform state."
  value       = aws_s3_bucket.terraform_state.id
}

output "terraform_state_key" {
  description = "S3 object key for Terraform state."
  value       = "vibe-poc/terraform.tfstate"
}

output "terraform_state_region" {
  description = "AWS region for the Terraform state bucket."
  value       = var.aws_region
}

output "github_actions_role_arn" {
  description = "ARN of the GitHub Actions deployment role."
  value       = aws_iam_role.github_actions.arn
}

output "github_actions_role_name" {
  description = "Name of the GitHub Actions deployment role."
  value       = aws_iam_role.github_actions.name
}

output "github_oidc_provider_arn" {
  description = "ARN of the GitHub OIDC provider."
  value       = aws_iam_openid_connect_provider.github.arn
}

output "setup_summary" {
  description = "Summary of GitHub variables and secrets to configure."
  value = {
    github_variables = {
      AWS_REGION      = var.aws_region
      TF_STATE_BUCKET = aws_s3_bucket.terraform_state.id
      TF_STATE_KEY    = "vibe-poc/terraform.tfstate"
      TF_STATE_REGION = var.aws_region
      OPTNAI_BASE_URL = "# Set this to your OptnAI API base URL"
      OPTNAI_MODEL    = "# Set this to your OptnAI model name"
    }
    github_secrets = {
      AWS_DEPLOY_ROLE_ARN = aws_iam_role.github_actions.arn
      OPTNAI_API_KEY      = "# Set this to your OptnAI API key"
    }
  }
}
