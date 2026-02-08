export interface GitHubLabel {
    name: string
    color: string
}

export interface GitHubIssue {
    id: number
    number: number
    title: string
    body: string
    state: string
    created_at: string
    updated_at: string
    labels: GitHubLabel[]
    priority: string | null
    type: string | null
    client: string | null
    assignee: string | null
    html_url: string
}