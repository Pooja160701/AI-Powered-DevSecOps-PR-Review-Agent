from unidiff import PatchSet

def parse_diff(diff_text):
    patch = PatchSet(diff_text)

    parsed_files = []

    for file in patch:
        file_data = {
            "file": file.path,
            "added_lines": []
        }

        for hunk in file:
            for line in hunk:
                if line.is_added:
                    file_data["added_lines"].append(line.value.strip())

        parsed_files.append(file_data)

    return parsed_files