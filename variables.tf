variable "github_token" {
  description = "GitHub personal access token"
  type        = string
  sensitive   = true
}

variable "repository_name" {
  description = "terraform"
  type        = string
}
