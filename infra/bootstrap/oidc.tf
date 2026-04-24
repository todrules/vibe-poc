# GitHub OIDC provider
resource "aws_iam_openid_connect_provider" "github" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]

  thumbprint_list = [data.tls_certificate.github.certificates[0].sha1_fingerprint]

  tags = {
    Name = "${var.project_name}-github-oidc"
  }
}

# IAM role trust policy for GitHub Actions
data "aws_iam_policy_document" "github_assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_owner}/${var.github_repo}:*"]
    }
  }
}

# GitHub Actions IAM role
resource "aws_iam_role" "github_actions" {
  name               = local.role_name
  assume_role_policy = data.aws_iam_policy_document.github_assume_role.json

  tags = {
    Name = "${var.project_name}-github-actions"
  }
}

# Policy for Terraform state bucket access
data "aws_iam_policy_document" "terraform_state_access" {
  statement {
    sid = "TerraformStateBucketAccess"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = [
      "${aws_s3_bucket.terraform_state.arn}/vibe-poc/terraform.tfstate*"
    ]
  }

  statement {
    sid = "TerraformStateBucketList"

    actions = [
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.terraform_state.arn
    ]
  }
}

# Policy for main deployment infrastructure (VPC, ALB, ECS, ECR, CloudWatch, IAM)
data "aws_iam_policy_document" "terraform_deployment" {
  # Full access to the services Terraform manages for this stack.
  # Using service-level wildcards avoids repeated permission failures as the
  # Terraform AWS provider adds new API calls (e.g. ListTagsForResource variants).
  statement {
    sid    = "EC2FullAccess"
    effect = "Allow"
    actions   = ["ec2:*"]
    resources = ["*"]
  }

  statement {
    sid    = "ELBFullAccess"
    effect = "Allow"
    actions   = ["elasticloadbalancing:*"]
    resources = ["*"]
  }

  statement {
    sid    = "ECRFullAccess"
    effect = "Allow"
    actions   = ["ecr:*"]
    resources = ["*"]
  }

  statement {
    sid    = "ECSFullAccess"
    effect = "Allow"
    actions   = ["ecs:*"]
    resources = ["*"]
  }

  statement {
    sid    = "CloudWatchLogsFullAccess"
    effect = "Allow"
    actions   = ["logs:*"]
    resources = ["*"]
  }

  # IAM is kept explicit to prevent unintended privilege escalation.
  statement {
    sid    = "IAMRoleManagement"
    effect = "Allow"

    actions = [
      "iam:GetRole",
      "iam:CreateRole",
      "iam:DeleteRole",
      "iam:GetRolePolicy",
      "iam:PutRolePolicy",
      "iam:DeleteRolePolicy",
      "iam:AttachRolePolicy",
      "iam:DetachRolePolicy",
      "iam:ListRolePolicies",
      "iam:ListAttachedRolePolicies",
      "iam:TagRole",
      "iam:UntagRole",
      "iam:ListRoleTags",
      "iam:PassRole",
    ]

    resources = ["*"]
  }

  statement {
    sid    = "IAMCreateServiceLinkedRoleForELB"
    effect = "Allow"

    actions = [
      "iam:CreateServiceLinkedRole",
    ]

    resources = ["*"]

    condition {
      test     = "StringEquals"
      variable = "iam:AWSServiceName"
      values   = ["elasticloadbalancing.amazonaws.com"]
    }
  }

  statement {
    sid    = "IAMCreateServiceLinkedRoleForECS"
    effect = "Allow"

    actions = [
      "iam:CreateServiceLinkedRole",
    ]

    resources = ["*"]

    condition {
      test     = "StringEquals"
      variable = "iam:AWSServiceName"
      values   = ["ecs.amazonaws.com"]
    }
  }
}

# Attach state bucket policy
resource "aws_iam_role_policy" "terraform_state" {
  name   = "${local.role_name}-terraform-state"
  role   = aws_iam_role.github_actions.id
  policy = data.aws_iam_policy_document.terraform_state_access.json
}

# Attach deployment policy
resource "aws_iam_role_policy" "terraform_deployment" {
  name   = "${local.role_name}-terraform-deployment"
  role   = aws_iam_role.github_actions.id
  policy = data.aws_iam_policy_document.terraform_deployment.json
}
