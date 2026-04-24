def check_python(parsed_diff):
    findings = []

    for file in parsed_diff:
        if file["file"].endswith(".py"):

            for line in file["added_lines"]:
                stripped = line.strip()

                # Skip comments and strings
                if stripped.startswith("#"):
                    continue

                # Skip lines where eval is inside quotes (false positive)
                if '"eval(' in stripped or "'eval(" in stripped:
                    continue

                # Real detection
                if "eval(" in stripped:
                    findings.append({
                        "type": "PYTHON",
                        "severity": "HIGH",
                        "file": file["file"],
                        "line": stripped,
                        "message": "Use of eval() is unsafe"
                    })

    return findings