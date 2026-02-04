def extract_labels(labels, prefix):
    """
    Finds and extracts labels from the issue data.
    """
    for label in labels:
        name = label.get("name", "");
        if name.startswith(prefix):
            return name.replace(prefix, "").strip()
    return None

def normalize_issue(issue):
    """
    Normalizes the issue data from GitHub API to a consistent format for our app.
    """
    return {
        "id": issue.get("id"),
        "number": issue.get("number"),
        "title": issue.get("title"),
        "body": issue.get("body"),
        "state": issue.get("state"),
        "created_at": issue.get("created_at"),
        "updated_at": issue.get("updated_at"),
        "labels": [label.get("name") for label in issue.get("labels", [])],
        "priority": extract_labels(issue.get("labels", []), "P:"),
        "type": extract_labels(issue.get("labels", []), "T:"),
        "client": extract_labels(issue.get("labels", []), "C:"),
        "assignee": (issue["assignee"]["login"] if issue.get("assignee") else None),
        "url": issue.get("html_url"),
    }
