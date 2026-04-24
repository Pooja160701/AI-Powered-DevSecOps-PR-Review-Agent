from fastapi import FastAPI, Request
from app.github_client import get_pr_diff
from app.diff_parser import parse_diff
from rules.secrets import detect_secrets
from app.ai_reviewer import generate_ai_review

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

        # Only process relevant events
        if action not in ["opened", "synchronize"]:
            return {"status": "ignored"}

        pr = payload.get("pull_request", {})
        pr_number = pr.get("number")
        repo_name = payload.get("repository", {}).get("full_name")

        print(f"\nPR Event Detected!")
        print(f"Repo: {repo_name}")
        print(f"PR Number: {pr_number}")
        print(f"Action: {action}")

        # STEP 1: Fetch diff
        diff = get_pr_diff(repo_name, pr_number)

        print("\nPR DIFF:")
        print(diff[:500])

        # STEP 2: Parse diff
        parsed = parse_diff(diff)

        print("\nParsed Diff:")
        for file in parsed:
            print(f"\nFile: {file['file']}")
            for line in file["added_lines"]:
                print(f"  + {line}")

        # STEP 3: Detect secrets
        findings = detect_secrets(parsed)

        print("\nFindings:")
        for f in findings:
            print(f)
            
        # STEP 4: AI Review
        ai_review = generate_ai_review(findings)

        print("\n🧠 AI Review:")
        print(ai_review)

    return {"status": "processed"}