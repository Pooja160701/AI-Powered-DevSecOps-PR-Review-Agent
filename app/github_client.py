import os
import requests

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_pr_diff(repo_full_name, pr_number):
    url = f"{GITHUB_API}/repos/{repo_full_name}/pulls/{pr_number}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch PR diff: {response.text}")

    return response.text


def post_pr_comment(repo_full_name, pr_number, comment_body):
    url = f"{GITHUB_API}/repos/{repo_full_name}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "body": comment_body
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 201:
        raise Exception(f"Failed to post comment: {response.text}")

    return response.json()

def get_existing_comments(repo_full_name, pr_number):
    url = f"{GITHUB_API}/repos/{repo_full_name}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch comments: {response.text}")

    return response.json()


def update_comment(repo_full_name, comment_id, new_body):
    url = f"{GITHUB_API}/repos/{repo_full_name}/issues/comments/{comment_id}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.patch(url, headers=headers, json={"body": new_body})

    if response.status_code != 200:
        raise Exception(f"Failed to update comment: {response.text}")

    return response.json()