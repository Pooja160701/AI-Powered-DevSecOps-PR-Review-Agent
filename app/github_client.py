import os
import requests

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

TIMEOUT = 10


def get_headers(accept_type="application/vnd.github.v3+json"):
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": accept_type,
    }


def get_pr_diff(repo_full_name, pr_number):
    url = f"{GITHUB_API}/repos/{repo_full_name}/pulls/{pr_number}"

    response = requests.get(
        url,
        headers=get_headers("application/vnd.github.v3.diff"),
        timeout=TIMEOUT,
    )

    if response.status_code != 200:
        raise Exception(f"Failed to fetch PR diff: {response.text}")

    return response.text


def post_pr_comment(repo_full_name, pr_number, comment_body):
    url = f"{GITHUB_API}/repos/{repo_full_name}/issues/{pr_number}/comments"

    data = {"body": comment_body}

    response = requests.post(
        url,
        headers=get_headers(),
        json=data,
        timeout=TIMEOUT,
    )

    if response.status_code != 201:
        raise Exception(f"Failed to post comment: {response.text}")

    return response.json()


def get_existing_comments(repo_full_name, pr_number):
    url = f"{GITHUB_API}/repos/{repo_full_name}/issues/{pr_number}/comments"

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=TIMEOUT,
    )

    if response.status_code != 200:
        raise Exception(f"Failed to fetch comments: {response.text}")

    return response.json()


def update_comment(repo_full_name, comment_id, new_body):
    url = f"{GITHUB_API}/repos/{repo_full_name}/issues/comments/{comment_id}"

    response = requests.patch(
        url,
        headers=get_headers(),
        json={"body": new_body},
        timeout=TIMEOUT,
    )

    if response.status_code != 200:
        raise Exception(f"Failed to update comment: {response.text}")

    return response.json()
