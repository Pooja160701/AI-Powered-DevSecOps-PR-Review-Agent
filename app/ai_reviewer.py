from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def format_findings(findings):
    """
    Group findings by severity
    """
    grouped = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": []}

    for finding in findings:
        severity = finding.get("severity", "MEDIUM")
        grouped.setdefault(severity, []).append(finding)

    return grouped


def generate_ai_review(findings):
    """
    Generate structured AI PR review
    """
    if not findings:
        return "No major security issues detected."

    formatted = json.dumps(format_findings(findings), indent=2)

    prompt = f"""
You are a senior DevSecOps engineer reviewing a pull request.

Analyze the following findings and produce a professional PR review.

Findings (grouped by severity):
{formatted}

Output STRICTLY in this format:

## Critical Issues
- Issue
- Why it matters
- Fix

## High Priority Issues
- ...

## Medium Issues
- ...

## Low Issues
- ...

## Summary
Short summary of overall code health.

Be concise, clear, and professional.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a DevSecOps expert."},
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"AI Review failed: {str(error)}"
