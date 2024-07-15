#!/bin/bash

# GitHub repository information
OWNER="Akshaya222"
REPO="terraform-github-testing"
TOKEN=$1

# Fetch environments from GitHub API
ENVIRONMENTS=$(curl -s -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/environments" \
  | jq -r '.environments[].name')

# Generate YAML formatted options list
OPTIONS=$(printf "  - %s\n" $ENVIRONMENTS)

echo "Options - $OPTIONS"

# Define the workflow file path
WORKFLOW_FILE=".github/workflows/deploy.yml"

echo "file - $WORKFLOW_FILE"

# Use awk to update options under StackName in deploy.yml
awk -v options="$OPTIONS" '
  /^ *StackName:/ {
    print $0
    getline
    if ($0 ~ /^ *options:/) {
      print options
      skip = 1
    }
  }
  !skip { print }
  { skip = 0 }
' "$WORKFLOW_FILE" > temp.yml && mv temp.yml "$WORKFLOW_FILE"

echo "Workflow file updated with dynamic options."
