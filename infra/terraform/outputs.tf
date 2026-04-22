output "alb_dns_name" {
  description = "Public DNS name for the application load balancer."
  value       = aws_lb.app.dns_name
}

output "frontend_url" {
  description = "Frontend URL over HTTP."
  value       = "http://${aws_lb.app.dns_name}"
}

output "backend_generate_url" {
  description = "Backend generate endpoint URL over HTTP."
  value       = "http://${aws_lb.app.dns_name}/generate"
}

output "backend_repository_url" {
  description = "ECR repository URL for backend image pushes."
  value       = aws_ecr_repository.backend.repository_url
}

output "frontend_repository_url" {
  description = "ECR repository URL for frontend image pushes."
  value       = aws_ecr_repository.frontend.repository_url
}
