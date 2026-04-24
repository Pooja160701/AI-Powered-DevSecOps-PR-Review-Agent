from fastapi import FastAPI, Request
from app.github_client import get_pr_diff

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    event_type = request.headers.get("X-GitHub-Event")

    if event_type == "ping":
        print("Webhook verified successfully!")
        return {"status": "ok"}

    if event_type == "pull_request":
        action = payload.get("action")

        # Only act on these
        if action not in ["opened", "synchronize"]:
            return {"status": "ignored"}

        pr = payload.get("pull_request", {})
        pr_number = pr.get("number")
        repo_name = payload.get("repository", {}).get("full_name")

        print(f"\nPR Event Detected!")
        print(f"Repo: {repo_name}")
        print(f"PR Number: {pr_number}")
        print(f"Action: {action}")

        # FETCH DIFF
        diff = get_pr_diff(repo_name, pr_number)

        print("\nPR DIFF:")
        print(diff[:1000])  # print first 1000 chars

    return {"status": "processed"}