import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Optional configs
    TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))