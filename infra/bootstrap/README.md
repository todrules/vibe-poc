# Terraform Bootstrap Stack

This Terraform stack sets up the AWS infrastructure required for GitHub Actions to deploy the main vibe-poc application:

1. **S3 bucket** for Terraform remote state (with versioning and encryption)
2. **GitHub OIDC provider** for secure, keyless authentication from GitHub Actions
3. **IAM role** with fine-grained permissions for Terraform deployments, ECR pushes, and ECS updates

## Prerequisites

- AWS CLI configured with credentials for your target AWS account
- Terraform `>= 1.6`

## Apply the bootstrap stack

From the `infra/bootstrap` directory:

```bash
cd infra/bootstrap
terraform init
terraform plan
terraform apply
```

This creates the S3 bucket (named `vibe-poc-terraform-state-{ACCOUNT_ID}`), the GitHub OIDC provider, and the `vibe-poc-github-actions` role.

## Configure GitHub

After Terraform apply completes, capture the outputs:

```bash
terraform output -raw terraform_state_bucket
terraform output -raw terraform_state_key
terraform output -raw terraform_state_region
terraform output -raw github_actions_role_arn
```

Or view the full summary:

```bash
terraform output setup_summary
```

### Add repository variables

Go to **Settings** → **Secrets and variables** → **Variables** (in your GitHub repository) and add:

- `AWS_REGION`: `us-west-2` (or your region)
- `TF_STATE_BUCKET`: Output from Terraform (e.g., `vibe-poc-terraform-state-123456789012`)
- `TF_STATE_KEY`: `vibe-poc/terraform.tfstate`
- `TF_STATE_REGION`: `us-west-2` (or your region)
- `OPTNAI_BASE_URL`: Your OptnAI API base URL
- `OPTNAI_MODEL`: Your OptnAI model name (e.g., `gpt-4`)

### Add repository secrets

Go to **Settings** → **Secrets and variables** → **Secrets** and add:

- `AWS_DEPLOY_ROLE_ARN`: Output from Terraform (ARN of the GitHub Actions role)
- `OPTNAI_API_KEY`: Your OptnAI API key

## What the bootstrap stack creates

### S3 bucket
- Bucket name: `vibe-poc-terraform-state-{ACCOUNT_ID}`
- Versioning enabled for state recovery
- Server-side encryption (AES256) for security
- All public access blocked

### GitHub OIDC provider
- Allows GitHub Actions workflows to assume the deploy role without storing long-lived AWS credentials
- Scoped to this repository (`todrules/vibe-poc`)

### IAM role (`vibe-poc-github-actions`)
Permissions for:
- **Terraform state**: Read/write access to the S3 bucket
- **VPC**: Create/modify/delete VPCs, subnets, internet gateways, route tables, security groups
- **ALB**: Create/manage load balancers, target groups, listeners, rules
- **ECR**: Create repositories, push images, scan images
- **ECS**: Create clusters, task definitions, services; update services
- **CloudWatch Logs**: Create/delete log groups, set retention
- **IAM**: Create/delete roles, manage policies, pass roles to ECS tasks

## Cleanup

To remove all bootstrap resources:

```bash
terraform destroy
```

This deletes the S3 bucket, OIDC provider, and IAM role. The GitHub workflows will fail until you reconfigure or re-apply this stack.

## Notes

- The S3 bucket is created with a unique suffix (account ID) to avoid naming collisions.
- The OIDC provider thumbprint is automatically fetched from GitHub's token endpoint.
- The role trust policy is scoped to workflows in this specific repository to prevent cross-repo access.
- Terraform state is stored with the key `vibe-poc/terraform.tfstate`, allowing multiple projects in the same bucket if needed.
