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
AWS_REGION=us-east-1

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
