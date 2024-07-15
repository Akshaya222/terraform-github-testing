terraform {
  cloud {
    organization = "github-testing"

    workspaces {
      name = "GitHub-terraform-testing"
    }
  }
}

variable "PAT" {
  description = "GitHub"
  type        = string
}

provider "github" {
  token = var.PAT
}

resource "github_repository_environment" "Eventstore" {
  count=10
  environment = "production-${count.index}"
  repository  = "terraform-github-testing"
  deployment_branch_policy {
    protected_branches     = false
    custom_branch_policies = true
  }
}
