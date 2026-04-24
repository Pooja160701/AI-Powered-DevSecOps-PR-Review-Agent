def check_python(parsed_diff):
    findings = []

    for file in parsed_diff:
        if file["file"].endswith(".py"):
            for line in file["added_lines"]:
                if "eval(" in line:
                    findings.append({
                        "type": "PYTHON",
                        "severity": "HIGH",
                        "message": "Use of eval() is unsafe",
                        "line": line
                    })

    return findings