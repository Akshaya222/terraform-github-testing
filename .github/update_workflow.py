import yaml
import requests
import os

# GitHub repository information
OWNER = "Akshaya222"
REPO = "terraform-github-testing"

# Fetch PAT from GitHub secrets
TOKEN = os.getenv('PAT')

# Fetch environments from GitHub API
api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/environments"
headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}
response = requests.get(api_url, headers=headers)
response.raise_for_status()

environments = [env['name'] for env in response.json()['environments']]

# Define the path to deploy.yml
workflow_file = ".github/workflows/deploy.yml"

# Load the existing deploy.yml file
with open(workflow_file, 'r') as file:
    try:
        workflow = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

# Ensure 'on' key and 'workflow_dispatch' are present
if 'on' in workflow and 'workflow_dispatch' in workflow['on']:
    # Update options in workflow_dispatch inputs
    if 'inputs' in workflow['on']['workflow_dispatch'] and 'StackName' in workflow['on']['workflow_dispatch']['inputs']:
        workflow['on']['workflow_dispatch']['inputs']['StackName']['options'] = environments
    else:
        print("Error: 'StackName' inputs not found in workflow_dispatch.")
        exit(1)
else:
    print("Error: 'on' or 'workflow_dispatch' key not found in deploy.yml.")
    exit(1)

# Write the updated deploy.yml file
with open(workflow_file, 'w') as file:
    yaml.dump(workflow, file)

print(f"Workflow file '{workflow_file}' updated with dynamic options.")
