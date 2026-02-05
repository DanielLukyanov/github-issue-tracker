import type { GitHubIssue } from "../types/GitHubIssue";

export async function fetchIssues(): Promise<GitHubIssue[]> {
    const res = await fetch('http://localhost:8000/issues');
    if (!res.ok) {
        throw new Error(`Failed to fetch issues: ${res.statusText}`);
    }
    return await res.json();

}