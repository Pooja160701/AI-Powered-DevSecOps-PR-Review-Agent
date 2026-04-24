def check_dockerfile(parsed_diff):
    findings = []

    for file in parsed_diff:
        if "Dockerfile" in file["file"]:
            for line in file["added_lines"]:
                if "FROM" in line and "latest" in line:
                    findings.append({
                        "type": "DOCKER",
                        "severity": "HIGH",
                        "message": "Avoid using latest tag in Docker images",
                        "line": line
                    })

    return findings