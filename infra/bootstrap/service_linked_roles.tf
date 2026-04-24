resource "aws_iam_service_linked_role" "ecs" {
  aws_service_name = "ecs.amazonaws.com"
  description      = "Service-linked role for ECS services"
}
