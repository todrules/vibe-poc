# Terraform Deployment (AWS ECS + ALB)

This Terraform stack deploys the full Vibe POC application to AWS:

- VPC with 2 public subnets
- Internet-facing Application Load Balancer
- ECS Fargate cluster with two services:
  - `frontend` (Next.js on port 3000)
  - `backend` (FastAPI on port 8000)
- Path-based routing on one public endpoint:
  - `/generate` and `/healthz` -> backend
  - all other paths -> frontend
- Two ECR repositories for container images
- CloudWatch log groups for both services

## Prerequisites

- Terraform `>= 1.6`
- AWS CLI configured for the target account
- Docker for building/pushing images

## 1. Deploy infrastructure

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with real values.
terraform init
terraform plan
terraform apply
```

After apply, Terraform outputs:

- `alb_dns_name`
- `frontend_url`
- `backend_generate_url`
- `backend_repository_url`
- `frontend_repository_url`

## 2. Build and push images

From repository root, authenticate Docker to ECR and push both images.

```bash
# Set your region (must match terraform variable)
AWS_REGION=us-west-2

# Get AWS account id
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Backend image
BACKEND_REPO=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vibe-poc-backend

docker build -f backend/Dockerfile -t $BACKEND_REPO:latest .
docker push $BACKEND_REPO:latest

# Frontend image
FRONTEND_REPO=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vibe-poc-frontend

docker build -f frontend/Dockerfile -t $FRONTEND_REPO:latest .
docker push $FRONTEND_REPO:latest
```

## 3. Roll ECS services to new image

Re-run Terraform to update task definitions/services if needed:

```bash
cd infra/terraform
terraform apply
```

If tags are unchanged (for example `latest`), force a new deployment from CLI:

```bash
aws ecs update-service --cluster vibe-poc-cluster --service vibe-poc-backend --force-new-deployment
aws ecs update-service --cluster vibe-poc-cluster --service vibe-poc-frontend --force-new-deployment
```

## Notes

- This stack serves HTTP on port 80 for simplicity. For production internet traffic, add ACM + HTTPS listener + Route53.
- `optnai_api_key` is currently passed as a Terraform variable. Prefer AWS Secrets Manager in production.
- Backend prompt templates are loaded from `/app/prompts` in the container.

## GitHub Actions deployment

The repository includes two GitHub Actions workflows:

- `.github/workflows/build.yml` runs on PRs and pushes to `main`. It lints the frontend, builds both frontend and backend Docker images, and validates Docker image builds.
- `.github/workflows/deploy.yml` runs on pushes to `main` (or manual dispatch) when application code or Terraform changes. It uses GitHub OIDC to assume an AWS role, applies Terraform infrastructure, pushes commit-tagged Docker images to ECR, and rolls out updated ECS task definitions.

### Setup steps

1. **Apply the bootstrap stack** (one time):
   ```bash
   cd infra/bootstrap
   terraform init
   terraform apply
   ```
   This creates the S3 state bucket, GitHub OIDC provider, and the `vibe-poc-github-actions` IAM role.

2. **Capture bootstrap outputs** and configure GitHub:
   ```bash
   terraform output setup_summary
   ```
   Follow the output instructions to add repository variables and secrets to GitHub Settings.

3. **Push code** to trigger the workflows:
   - On PR: the build workflow validates your changes.
   - On push to `main`: the deploy workflow applies infrastructure and rolls out the new container images.

### GitHub variables to add

From the bootstrap `terraform output`, add these to **Settings** → **Secrets and variables** → **Variables**:

- `AWS_REGION`: AWS region (e.g., `us-west-2`)
- `TF_STATE_BUCKET`: S3 bucket name created by bootstrap
- `TF_STATE_KEY`: `vibe-poc/terraform.tfstate`
- `TF_STATE_REGION`: AWS region for the state bucket
- `OPTNAI_BASE_URL`: Your OptnAI API base URL
- `OPTNAI_MODEL`: Your OptnAI model name
- `TF_PROJECT_NAME` (optional): defaults to `vibe-poc`

### GitHub secrets to add

From the bootstrap `terraform output`, add these to **Settings** → **Secrets and variables** → **Secrets**:

- `AWS_DEPLOY_ROLE_ARN`: Role ARN created by bootstrap
- `OPTNAI_API_KEY`: Your OptnAI API key

### How the deploy workflow works

1. Assumes the `vibe-poc-github-actions` role via GitHub OIDC (no long-lived credentials).
2. Initializes Terraform with the S3 remote backend (created by bootstrap).
3. Applies the main Terraform stack to create/update VPC, ALB, ECS, ECR, and logging.
4. Builds and pushes Docker images tagged with the commit SHA.
5. Reapplies Terraform with the new image tags, triggering ECS task definition updates.
6. ECS automatically rolls out new tasks with the updated images.

### Cleanup

To tear down all AWS resources and bootstrap infrastructure:

```bash
# Destroy the main stack first
cd infra/terraform
terraform destroy

# Then destroy the bootstrap stack
cd ../bootstrap
terraform destroy
```
