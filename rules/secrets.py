import re

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",  # AWS Access Key
    r"(?i)secret\s*=\s*['\"].+['\"]",
    r"(?i)api_key\s*=\s*['\"].+['\"]",
]


def detect_secrets(parsed_diff):
    findings = []

    for file in parsed_diff:
        filename = file["file"]

        for line in file["added_lines"]:
            for pattern in SECRET_PATTERNS:
                if re.search(pattern, line):
                    findings.append(
                        {
                            "type": "SECRET",
                            "file": filename,
                            "line": line,
                            "severity": "CRITICAL",
                            "message": "Potential hardcoded secret detected",
                        }
                    )

    return findings
