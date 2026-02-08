<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchIssues } from '../services/githubAPI'
import type { GitHubIssue } from '../types/GitHubIssue'

const issues = ref<GitHubIssue[]>([])

const emit = defineEmits<{
    (e: 'issuesLoaded', issues: GitHubIssue[]): void
}>()

onMounted(async () => {
    issues.value = await fetchIssues()
    emit('issuesLoaded', issues.value)
})

async function refreshIssues(forceRefresh: boolean = false) {
    console.log('Refreshing issues list...')
    issues.value = await fetchIssues(forceRefresh)
    emit('issuesLoaded', issues.value)
}

// Expose the refresh method so parent can call it
defineExpose({ refreshIssues })
</script>

<template>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Number</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Client</th>
                    <th>Priority</th>
                    <th>Type</th>
                    <th>Assigned To</th>
                    <th>State</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="issue in issues" :key="issue.id">
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

<style scoped>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}
table {
  border-collapse: collapse;
  width: 100%;
  table-layout:unset;
  margin: 0;
  padding: 0;
}
th, td {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

td{
    line-clamp: 2;
    overflow: hidden;
    text-overflow: ellipsis;
}

.multiline-truncate {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    line-clamp: 2;
    white-space: normal;
    overflow: hidden;
    text-overflow: ellipsis;
    /* width: 100px; */
    min-height: 50px;
}


.table-container {
    width: 100%;
    padding: 20px;
    box-sizing: border-box;
}

</style>
