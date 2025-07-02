import os
import json
import requests

MEMBERS_FILE = '.github/scripts/members.json'
ORG_NAME = os.getenv('ORG_NAME')
REPO_NAME = os.getenv('REPO_NAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}

# Step 1: Load old members
if os.path.exists(MEMBERS_FILE):
    with open(MEMBERS_FILE, 'r') as f:
        old_members = json.load(f)
else:
    old_members = []

# Step 2: Fetch current org members
print(f"Fetching current members for org: {ORG_NAME}")
response = requests.get(f'https://api.github.com/orgs/{ORG_NAME}/members', headers=headers)
response.raise_for_status()
current_members = [member['login'] for member in response.json()]

# Step 3: Find new members
new_members = list(set(current_members) - set(old_members))
print(f"New members detected: {new_members}")

# Step 4: Create issues for new members
for username in new_members:
    issue = {
        "title": f"🎉 Welcome @{username}!",
        "body": f"Hi @{username},\n\nWelcome to the team! Let us know if you need help getting started. 😊"
    }
    print(f"Creating issue for @{username}")
    issue_url = f'https://api.github.com/repos/{ORG_NAME}/{REPO_NAME}/issues'
    issue_response = requests.post(issue_url, headers=headers, json=issue)
    if issue_response.status_code == 201:
        print(f"Issue created successfully for @{username}")
    else:
        print(f"Failed to create issue for @{username}: {issue_response.text}")

# Step 5: Save current member list for next run
with open(MEMBERS_FILE, 'w') as f:
    json.dump(current_members, f, indent=2)
