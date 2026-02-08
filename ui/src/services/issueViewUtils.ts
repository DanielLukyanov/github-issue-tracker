import type { GitHubIssue } from '../types/GitHubIssue.ts'

export type SortKey =
    | 'created_at'
    | 'updated_at'
    | 'priority'
    | 'client'
    | 'title'
    | 'number'
    | 'type'
    | 'state'

export type SortDirection = 'asc' | 'desc'


function getPriorityValue(priority: string | null): number {
    if (priority == null) return -1 // Nulls go to the end
    const normalizedPriority = priority.toLowerCase()
    if (normalizedPriority === 'low') return 0
    if (normalizedPriority === 'medium') return 1
    if (normalizedPriority === 'high') return 2
    return -1
}

export function sortIssues(
    issues: GitHubIssue[],
    key: SortKey,
    direction: SortDirection = 'asc'
): GitHubIssue[] {
    return [...issues].sort((a, b) => {
        let aVal: any = a[key]
        let bVal: any = b[key]

        
        if (key === 'priority') {
            aVal = getPriorityValue(aVal)
            bVal = getPriorityValue(bVal)
        }

        if (aVal == null) return 1
        if (bVal == null) return -1

        if (aVal < bVal) return direction === 'asc' ? -1 : 1
        if (aVal > bVal) return direction === 'asc' ? 1 : -1
        return 0
    })
}
