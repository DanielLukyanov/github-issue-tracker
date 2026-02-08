<template>
    <div class="table-controller">
        <BaseButton
            text="Create Issue"
            @click="openCreateIssueModal"
        />
        <BaseButton
            text="Refresh Issues"
            @click="handleRefreshIssues"
        />
        <CreateIssueModal 
            v-if="showModal" 
            @close="closeModal" 
            @submit="onSubmitIssue" 
        />
    </div>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue'
import BaseButton from './BaseButton.vue'
import CreateIssueModal from './CreateIssueModal.vue'
import { createIssue } from '../services/githubAPI'

const issuesTable = inject<any>('issuesTable')
const { showPopup } = inject<any>('popup')

const emit = defineEmits<{
    (e: 'issueCreated'): void
}>()

const showModal = ref(false)

// Modal handlers
function openCreateIssueModal() {
    showModal.value = true
}

function closeModal() {
    showModal.value = false
}

// Action handlers
async function handleRefreshIssues() {
    try {
        await issuesTable?.value?.refreshIssues(true)
        showPopup({
            type: 'success',
            message: 'Issues refreshed successfully!'
        })
    } catch (error: any) {
        console.error('Error refreshing issues:', error)
        showPopup({
            type: 'error',
            message: error.message || 'Unable to connect to server. Please try again.',
            errorCode: error.code || error.status || 'CONNECTION_ERROR'
        })
    }
}

async function onSubmitIssue(payload: Record<string, any>) {
    try {
        const response = await createIssue(payload)
        
        showPopup({
            type: 'success',
            message: `Issue "${response.title}" created successfully!`,
            issueUrl: response.html_url
        })
        
        closeModal()
        emit('issueCreated')
    } catch (error: any) {
        console.error('Error creating issue:', error)
        
        showPopup({
            type: 'error',
            message: error.message || 'Failed to create issue. Please try again.',
            errorCode: error.code || error.status || 'UNKNOWN'
        })
        
        closeModal()
    }
}
</script>

<style scoped>
.table-controller {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding: 30px;
}
</style>