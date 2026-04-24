from fastapi import APIRouter, Request
from app.logger import logger

router = APIRouter()


@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    action = payload.get("action")
    pr = payload.get("pull_request", {})

    logger.info(f"Received PR event: {action}")

    if action in ["opened", "synchronize"]:
        return {"message": "PR received and will be processed"}

    return {"message": "Event ignored"}