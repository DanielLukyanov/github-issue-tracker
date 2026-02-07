"""
Normalization and translation utilities for converting
external data representations (e.g. GitHub API payloads)
into internal application domain structures, and vice versa.
"""

# ========== Github -> Domain Normalization ==========

def normalize_issue(issue):
    """
    Normalizes the issue data from GitHub API to a consistent format for our app.
    """

    label_names = [label["name"] for label in issue.get("labels", [])]
    parsed = github_labels_to_domain(label_names)

    return {
        "id": issue.get("id"),
        "number": issue.get("number"),
        "title": issue.get("title"),
        "body": issue.get("body"),
        "state": issue.get("state"),
        "created_at": issue.get("created_at"),
        "updated_at": issue.get("updated_at"),
        "labels": issue.get("labels", []),
        "priority": parsed.get("priority"),
        "type": parsed.get("type"),
        "client": parsed.get("client"),
        "assignee": (issue["assignee"]["login"] if issue.get("assignee") else None),
        "url": issue.get("html_url"),
    }

def github_labels_to_domain(labels: list[str]) -> dict:
    """
    Converts a list of GitHub labels into a structured dict with priority, type, and client.
    Expects labels in the format "P:High", "T:Bug", "C:ClientA".
    """
    result = {
        "priority": None,
        "type": None,
        "client": None
    }
    
    for label in labels:
        if label.startswith("P:"):
            # Handle both "P:High" and "P: High" formats
            result["priority"] = label[2:].strip() # remove "P:" prefix and strip whitespace
        elif label.startswith("T:"):
            # Handle both "T:Bug" and "T: Bug" formats  
            result["type"] = label[2:].strip()
        elif label.startswith("C:"):
            # Handle both "C:ClientA" and "C: ClientA" formats
            result["client"] = label[2:].strip()
    
    return result



def serialise_issue(issue: dict) -> dict:
    """
    Serializes a domain issue dict into a format suitable for GitHub API.
    """
    title = issue.get("title", "")
    if not title:
        raise ValueError("Issue title is required")

    return {
        "title": title,
        "body": issue.get("body", ""),
        "assignees": [issue["assignee"]] if issue.get("assignee") else [],
        "labels": domain_to_github_labels(issue),
    }


def domain_to_github_labels(issue: dict) -> list[str]:
    """
    Converts a domain issue dict into a list of GitHub labels.
    Expects keys like "priority", "type", and "client" in the issue dict.
    """
    labels = []
    
    if issue.get("priority"):
        labels.append(f"P: {issue['priority']}")
    if issue.get("type"):
        labels.append(f"T: {issue['type']}")
    if issue.get("client"):
        labels.append(f"C: {issue['client']}")
    
    return labels