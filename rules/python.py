import re


def check_python(parsed_diff):
    findings = []

    eval_pattern = re.compile(r"\beval\s*\(")

    for file in parsed_diff:
        if file["file"].endswith(".py"):
            for line in file["added_lines"]:
                stripped = line.strip()

                if stripped.startswith("#"):
                    continue

                if re.search(r'["\'].*eval\s*\(.*["\']', stripped):
                    continue

                if eval_pattern.search(stripped):
                    findings.append(
                        {
                            "type": "PYTHON",
                            "severity": "HIGH",
                            "file": file["file"],
                            "line": stripped,
                            "message": "Use of eval() is unsafe",
                        }
                    )

    return findings
