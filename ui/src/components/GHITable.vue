<template>
    <div class="table-container">
        <div class="pagination-info">
            <strong>{{ paginationInfo }}</strong>
        </div>
        <table>
            <thead>
                <tr>
                    <th @click="handleSort('number')" class="sortable">
                        Number{{ getSortIndicator('number') }}
                    </th>
                    <th @click="handleSort('title')" class="sortable">
                        Title{{ getSortIndicator('title') }}
                    </th>
                    <th>Description</th>
                    <th @click="handleSort('client')" class="sortable">
                        Client{{ getSortIndicator('client') }}
                    </th>
                    <th @click="handleSort('priority')" class="sortable">
                        Priority{{ getSortIndicator('priority') }}
                    </th>
                    <th @click="handleSort('type')" class="sortable">
                        Type{{ getSortIndicator('type') }}
                    </th>
                    <th>Assigned To</th>
                    <th @click="handleSort('state')" class="sortable">
                        State{{ getSortIndicator('state') }}
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr 
                    v-for="issue in issues" 
                    :key="issue.id"
                    :style="{ backgroundColor: getRowColor(issue) }"
                >
                    <td>{{ issue.number }}</td>
                    <td>
                        <div class="multiline-truncate">
                            {{ issue.title }}
                        </div>
                    </td>
                    <td>
                        <div class="multiline-truncate">
                            {{ issue.body }}
                        </div>
                    </td>
                    <td>Client {{ issue.client }}</td>
                    <td>{{ issue.priority }}</td>
                    <td>{{ issue.type }}</td>
                    <td>{{ issue.assignee }}</td>
                    <td>{{ issue.state }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>


<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { fetchIssues } from '../services/githubAPI'
import type { GitHubIssue } from '../types/GitHubIssue'
import { sortIssues, type SortKey, type SortDirection } from '../services/issueViewUtils'

const rawIssues = ref<GitHubIssue[]>([])
const currentSortKey = ref<SortKey | null>(null)
const currentSortDirection = ref<SortDirection>('asc')
const currentPage = ref(1)
const itemsPerPage = ref(10)

const emit = defineEmits<{
    (e: 'issuesLoaded', issues: GitHubIssue[]): void
}>()

// Computed property that returns sorted issues
const sortedIssues = computed(() => {
    if (!currentSortKey.value) {
        return rawIssues.value // No sorting, return original
    }
    return sortIssues(rawIssues.value, currentSortKey.value, currentSortDirection.value)
})

// Computed property for paginated issues
const issues = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value
    const end = start + itemsPerPage.value
    return sortedIssues.value.slice(start, end)
})

// Total pages
const totalPages = computed(() => {
    return Math.ceil(sortedIssues.value.length / itemsPerPage.value)
})

// Pagination info text
const paginationInfo = computed(() => {
    const start = sortedIssues.value.length === 0 ? 0 : (currentPage.value - 1) * itemsPerPage.value + 1
    const end = Math.min(currentPage.value * itemsPerPage.value, sortedIssues.value.length)
    return `${start}-${end} of ${sortedIssues.value.length} issues`
})

// Handle column header clicks
function handleSort(key: SortKey) {
    if (currentSortKey.value === key) {
        // Already sorting by this column
        if (currentSortDirection.value === 'asc') {
            // First click was asc, now go desc
            currentSortDirection.value = 'desc'
        } else {
            // Second click was desc, now reset
            currentSortKey.value = null
            currentSortDirection.value = 'asc'
        }
    } else {
        // New column, start with ascending
        currentSortKey.value = key
        currentSortDirection.value = 'asc'
    }
}

// Get sort indicator for column header
function getSortIndicator(key: SortKey): string {
    if (currentSortKey.value !== key) return ''
    return currentSortDirection.value === 'asc' ? ' ▲' : ' ▼'
}
// Get label color for row based on current sort
function getRowColor(issue: GitHubIssue): string {
    if (!currentSortKey.value) return '' // No sort = no color
    
    let labelPrefix = ''
    if (currentSortKey.value === 'priority') labelPrefix = 'P:'
    else if (currentSortKey.value === 'client') labelPrefix = 'C:'
    else if (currentSortKey.value === 'type') labelPrefix = 'T:'
    else return '' // Other sorts don't have label colors
    
    // Find the matching label
    const matchingLabel = issue.labels.find(label => 
        label.name.startsWith(labelPrefix)
    )
    
    if (matchingLabel) {
        // Return color with transparency
        return `#${matchingLabel.color}20` // Append '20' for transparency
    }
    
    return ''
}
onMounted(async () => {
    rawIssues.value = await fetchIssues()
    emit('issuesLoaded', rawIssues.value)
})

async function refreshIssues(forceRefresh: boolean = false) {
    console.log('Refreshing issues list...')
    rawIssues.value = await fetchIssues(forceRefresh)
    currentPage.value = 1 // Reset to first page on refresh
    emit('issuesLoaded', rawIssues.value)
}

// Pagination methods
function setPage(page: number) {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
    }
}

function nextPage() {
    if (currentPage.value < totalPages.value) {
        currentPage.value++
    }
}

function prevPage() {
    if (currentPage.value > 1) {
        currentPage.value--
    }
}

function setItemsPerPage(count: number) {
    itemsPerPage.value = count
    currentPage.value = 1 // Reset to first page when changing items per page
}

// Expose methods and state for parent components
defineExpose({ 
    refreshIssues, 
    currentPage, 
    totalPages, 
    itemsPerPage,
    setPage, 
    nextPage, 
    prevPage, 
    setItemsPerPage 
})
</script>


<style scoped>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}
table {
  border-collapse: collapse;
  width: 100%;
  table-layout: auto;
  margin: 0;
  padding: 0;
}
th.sortable {
    cursor: pointer;
    user-select: none;
}

th.sortable:hover {
    background-color: #f0f0f0;
}

th, td {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 5px;
    max-width: 300px;
}

td{
    overflow: hidden;
    text-overflow: ellipsis;
}

.multiline-truncate {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    white-space: normal;
    overflow: hidden;
    text-overflow: ellipsis;
    word-wrap: break-word;
    overflow-wrap: break-word;
    word-break: break-all;
    min-height: 50px;
}


.table-container {
    width: 100%;
    padding: 20px;
    box-sizing: border-box;
    overflow-x: auto;
}

.pagination-info {
    margin-bottom: 15px;
    font-size: 14px;
    color: #333;
}

</style>
