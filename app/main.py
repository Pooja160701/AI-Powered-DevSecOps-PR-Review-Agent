from fastapi import FastAPI, Request
from app.github_client import get_pr_diff
from app.diff_parser import parse_diff
from rules.secrets import detect_secrets

app = FastAPI()

# after parsing

findings = detect_secrets(parsed)

print("\n🚨 Findings:")
for f in findings:
    print(f)
    
# after fetching diff

parsed = parse_diff(diff)

print("\nParsed Diff:")
for file in parsed:
    print(f"\nFile: {file['file']}")
    for line in file["added_lines"]:
        print(f"  + {line}")

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