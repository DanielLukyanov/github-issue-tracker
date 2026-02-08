import type { GitHubIssue } from "../types/GitHubIssue";

export async function fetchIssues(forceRefresh: boolean = false): Promise<GitHubIssue[]> {
    try {
        const url = forceRefresh 
            ? 'https://github-issue-tracker-wzxr.onrender.com/issues?force_refresh=true'
            : 'https://github-issue-tracker-wzxr.onrender.com/issues';
        const res = await fetch(url);
        if (!res.ok) {
            const errorData = await res.json();
            const error: any = new Error(errorData.message || 'Failed to fetch issues');
            error.code = errorData.error;
            error.status = res.status;
            error.details = errorData.details;
            throw error;
        }
        return await res.json();

    } catch (error) {
        console.error("Error fetching issues:", error);
        throw error;
    }

}


export async function createIssue(payload: Record<string, any>): Promise<GitHubIssue> {
    try {
        const res = await fetch('https://github-issue-tracker-wzxr.onrender.com/issues', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            // Parse backend error response
            const errorData = await res.json();
            const error: any = new Error(errorData.message || 'Failed to create issue');
            error.code = errorData.error;
            error.status = res.status;
            error.details = errorData.details;
            throw error;
        }
        
        const data = await res.json();
        console.log("Created issue:", data);
        return data;
    } catch (error) {
        console.error("Error creating issue:", error);
        throw error;
    }
}