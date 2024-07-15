import yaml
import requests
import os

# GitHub repository information
OWNER = "Akshaya222"
REPO = "terraform-github-testing"

# Fetch PAT from GitHub secrets
TOKEN = os.getenv('PAT')  # Fetching PAT from environment variables (GitHub secret)

# Fetch environments from GitHub API
api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/environments"
headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}
response = requests.get(api_url, headers=headers)
response.raise_for_status()  # Raise an exception for unsuccessful requests

environments = [env['name'] for env in response.json()['environments']]

# Load the existing deploy.yml file
workflow_file = ".github/workflows/deploy.yml"
with open(workflow_file, 'r') as file:
    workflow = yaml.safe_load(file)

# Update options in workflow_dispatch inputs
workflow['on']['workflow_dispatch']['inputs']['StackName']['options'] = environments

# Write the updated deploy.yml file
with open(workflow_file, 'w') as file:
    yaml.dump(workflow, file)

print(f"Workflow file '{workflow_file}' updated with dynamic options.")
