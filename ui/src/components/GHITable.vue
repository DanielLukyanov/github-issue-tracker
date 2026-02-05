<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchIssues } from '../services/githubAPI'
import type { GitHubIssue } from '../types/GitHubIssue'

const issues = ref<GitHubIssue[]>([])

onMounted(async () => {
    issues.value = await fetchIssues()
})
</script>

<template>
    <table>
        <thead>
            <tr>
                <th>Number</th>
                <th>Title</th>
                <th>Status</th>
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
                <td>{{ issue.title }}</td>
                <td>{{ issue.body }}</td>
                <td>Client {{ issue.client }}</td>
                <td>{{ issue.priority }}</td>
                <td>{{ issue.type }}</td>
                <td>{{ issue.assignee }}</td>
                <td>{{ issue.state }}</td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
}
th, td {
  padding: 8px;
  border: 1px solid #ddd;
}
</style>
