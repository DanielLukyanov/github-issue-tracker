import type { GitHubIssue } from "../types/GitHubIssue";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function fetchIssues(forceRefresh: boolean = false): Promise<GitHubIssue[]> {
    try {
        const url = forceRefresh 
            ? `${API_BASE_URL}/issues?force_refresh=true`
            : `${API_BASE_URL}/issues`;
        const res = await fetch(url, {
            credentials: 'include' // Send cookies with request
        });
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
        const res = await fetch(`${API_BASE_URL}/issues`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // Send cookies with request
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