export interface GitHubIssue {
    id: number
    number: number
    title: string
    body: string
    state: string
    created_at: string
    updated_at: string
    labels: string[]
    priority: string | null
    type: string | null
    client: string | null
    assignee: string | null
    html_url: string
}