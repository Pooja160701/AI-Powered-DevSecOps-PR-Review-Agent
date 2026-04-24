def format_review_comment(issues: list[str]) -> str:
    if not issues:
        return "No issues found. Great job!"

    formatted = "## PR Review Summary\n\n"
    for i, issue in enumerate(issues, 1):
        formatted += f"{i}. {issue}\n"

    return formatted