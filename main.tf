terraform {
  cloud {
    organization = "github-testing"

    workspaces {
      name = "GitHub-terraform-testing"
    }
  }
}

variable "PAT" {
  description = "GitHub Personal Access Token"
  type        = string
}

provider "github" {
  token = var.PAT
}

resource "github_repository" "repo" {
  name        = "deployment-env"
  description = "Repository managed by Terraform"
  visibility  = "public"
  auto_init   = true
}

resource "github_repository_environment" "Eventstore" {
  count=10
  environment = "production"
  repository  = github_repository.repo.name
  deployment_branch_policy {
    protected_branches     = false
    custom_branch_policies = true
  }
}
