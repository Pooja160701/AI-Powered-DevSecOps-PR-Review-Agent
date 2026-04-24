from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv() 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_review(findings):
    if not findings:
        return "No major security issues detected."

    prompt = f"""
You are a senior DevSecOps engineer.

Analyze the following security findings from a pull request and generate a professional PR review.

Findings:
{findings}

Output format:

## Critical Issues
- Issue
- Why it matters
- Fix

## Summary
Short summary of code health

Be concise and professional.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a DevSecOps expert."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content