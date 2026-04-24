from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    event_type = request.headers.get("X-GitHub-Event")

    # Ignore ping
    if event_type == "ping":
        print("Webhook verified successfully!")
        return {"status": "ok"}

    # Handle Pull Request events
    if event_type == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})

        pr_number = pr.get("number")
        repo_name = payload.get("repository", {}).get("full_name")

        print(f"\nPR Event Detected!")
        print(f"Repo: {repo_name}")
        print(f"PR Number: {pr_number}")
        print(f"Action: {action}")

    return {"status": "processed"}