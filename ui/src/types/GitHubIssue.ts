export interface GitHubIssue {
    id: number
    number: number
    title: string
    body: string
    state: string
    created_at: string
    updated_at: string
    labels: string[]
    priority: string[]
    type: string[]
    client: string[]
    assignee: string | null
    url: string
}