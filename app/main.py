from fastapi import FastAPI, Request
from app.github_client import (
    get_pr_diff,
    post_pr_comment,
    get_existing_comments,
    update_comment
)
from app.diff_parser import parse_diff
from rules.secrets import detect_secrets
from app.ai_reviewer import generate_ai_review
from rules.docker import check_dockerfile
from rules.k8s import check_k8s

app = FastAPI()

# Unique identifier to avoid duplicate comments
BOT_TAG = "<!-- DEVSECOPS_BOT -->"


@app.post("/webhook")
async def github_webhook(request: Request):
    try:
        payload = await request.json()
        event_type = request.headers.get("X-GitHub-Event")

        # Handle webhook verification
        if event_type == "ping":
            print("Webhook verified successfully!")
            return {"status": "ok"}

        # Handle PR events
        if event_type == "pull_request":
            action = payload.get("action")

            # Only process relevant actions
            if action not in ["opened", "synchronize"]:
                return {"status": "ignored"}

            pr = payload.get("pull_request", {})
            pr_number = pr.get("number")
            repo_name = payload.get("repository", {}).get("full_name")

            print("\nPR Event Detected!")
            print(f"Repo: {repo_name}")
            print(f"PR Number: {pr_number}")
            print(f"Action: {action}")

            # STEP 1: Fetch PR diff
            diff = get_pr_diff(repo_name, pr_number)

            print("\nPR DIFF (truncated):")
            print(diff[:500])

            # STEP 2: Parse diff
            parsed = parse_diff(diff)

            print("\nParsed Diff:")
            for file in parsed:
                print(f"\nFile: {file['file']}")
                for line in file["added_lines"]:
                    print(f"  + {line}")

            # STEP 3: Detect secrets
            all_findings = []

            # Security rules
            all_findings.extend(detect_secrets(parsed))

            # DevOps rules
            all_findings.extend(check_dockerfile(parsed))

            #K8s
            all_findings.extend(check_k8s(parsed))

            findings = all_findings

            print("\nFindings:")
            for f in findings:
                print(f)

            # STEP 4: AI Review
            if not findings:
                ai_review = "✅ No major security issues detected."
            else:
                ai_review = generate_ai_review(findings)

            # Add bot identifier
            ai_review = BOT_TAG + "\n" + ai_review

            print("\nAI Review:")
            print(ai_review)

            # STEP 5: Smart Comment (Create / Update)
            try:
                comments = get_existing_comments(repo_name, pr_number)

                existing_comment = None

                for comment in comments:
                    if BOT_TAG in comment["body"]:
                        existing_comment = comment
                        break

                if existing_comment:
                    update_comment(repo_name, existing_comment["id"], ai_review)
                    print("\nUpdated existing comment")
                else:
                    post_pr_comment(repo_name, pr_number, ai_review)
                    print("\nNew comment posted")

            except Exception as e:
                print(f"\nComment error: {str(e)}")

        return {"status": "processed"}

    except Exception as e:
        print(f"\nWebhook Error: {str(e)}")
        return {"status": "error"}