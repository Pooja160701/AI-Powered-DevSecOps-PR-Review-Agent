def check_k8s(parsed_diff):
    findings = []

    for file in parsed_diff:
        if file["file"].endswith((".yaml", ".yml")):
            for line in file["added_lines"]:
                if "privileged: true" in line:
                    findings.append(
                        {
                            "type": "K8S",
                            "severity": "CRITICAL",
                            "message": "Privileged container detected",
                            "line": line,
                        }
                    )

    return findings
