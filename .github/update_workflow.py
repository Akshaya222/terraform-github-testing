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
try:
    with open(workflow_file, 'r') as file:
        workflow = yaml.safe_load(file)
except FileNotFoundError:
    print(f"Error: {workflow_file} not found.")
    exit(1)
except yaml.YAMLError as exc:
    print(exc)
    exit(1)

# Ensure 'on' and 'workflow_dispatch' keys exist and are dictionaries
if 'on' not in workflow or not isinstance(workflow['on'], dict) or \
   'workflow_dispatch' not in workflow['on'] or not isinstance(workflow['on']['workflow_dispatch'], dict):
    print("Error: 'on' or 'workflow_dispatch' key not found or not a dictionary in deploy.yml.")
    exit(1)

# Ensure 'inputs' key exists under 'workflow_dispatch' and is a dictionary
if 'inputs' not in workflow['on']['workflow_dispatch'] or not isinstance(workflow['on']['workflow_dispatch']['inputs'], dict):
    print("Error: 'inputs' key not found or not a dictionary under 'workflow_dispatch' in deploy.yml.")
    exit(1)

# Update options in StackName inputs
if 'StackName' in workflow['on']['workflow_dispatch']['inputs']:
    workflow['on']['workflow_dispatch']['inputs']['StackName']['options'] = environments
else:
    print("Error: 'StackName' inputs not found under 'workflow_dispatch' in deploy.yml.")
    exit(1)

# Write the updated deploy.yml file
try:
    with open(workflow_file, 'w') as file:
        yaml.dump(workflow, file)
except yaml.YAMLError as exc:
    print(exc)
    exit(1)

print(f"Workflow file '{workflow_file}' updated with dynamic options.")
