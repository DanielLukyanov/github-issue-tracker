<template>
    <div class="table-controller-rack">
        <div class="table-controller-container">
        </div>
        <div class="table-controller-container">
            <div class="table-pagination">
                <div class="pagination-controls">
                    <span class="page-info">Page</span>
                    <input 
                        type="number" 
                        v-model.number="pageInput" 
                        @blur="handlePageInput"
                        @keyup.enter="handlePageInput"
                        :min="1" 
                        :max="totalPages"
                        class="page-input"
                    />
                    <span class="page-info">of {{ totalPages }}</span>
                </div>
                <div class="items-per-page">
                    <label for="items-per-page">Items per page:</label>
                    <select id="items-per-page" v-model.number="selectedItemsPerPage" @change="handleItemsPerPageChange">
                        <option :value="10">10</option>
                        <option :value="25">25</option>
                        <option :value="50">50</option>
                        <option :value="100">100</option>
                    </select>
                </div>
            </div>
        </div>
        <div class="table-controller-container">
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
        </div>
     </div> <!-- END TABLE CONTROLLER RACK -->
</template>

<script setup lang="ts">
import { ref, inject, computed, watch } from 'vue'
import BaseButton from './BaseButton.vue'
import CreateIssueModal from './CreateIssueModal.vue'
import { createIssue } from '../services/githubAPI'

const issuesTable = inject<any>('issuesTable')
const { showPopup } = inject<any>('popup')

const emit = defineEmits<{
    (e: 'issueCreated'): void
}>()

const showModal = ref(false)
const selectedItemsPerPage = ref(10)
const pageInput = ref(1)

// Computed properties for pagination state from the table
const currentPage = computed(() => issuesTable?.value?.currentPage || 1)
const totalPages = computed(() => issuesTable?.value?.totalPages || 1)

// Watch currentPage to sync with pageInput
watch(currentPage, (newPage) => {
    pageInput.value = newPage
})

// Modal handlers
function openCreateIssueModal() {
    showModal.value = true
}

function closeModal() {
    showModal.value = false
}

// Pagination handlers
function handlePageInput() {
    const page = Math.max(1, Math.min(pageInput.value, totalPages.value))
    pageInput.value = page
    issuesTable?.value?.setPage(page)
}

function handleItemsPerPageChange() {
    issuesTable?.value?.setItemsPerPage(selectedItemsPerPage.value)
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
        
        // Check if it's an authentication error
        if (error.status === 401 || error.code === 'unauthorized') {
            console.log('Session expired, redirecting to login')
            // This will trigger the login page to show
            window.location.reload()
            return
        }
        
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

.table-controller-rack {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.table-controller {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding: 30px;
}

.table-controller-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}

.table-pagination {
    display: flex;
    align-items: center;
    gap: 30px;
}

.pagination-controls {
    display: flex;
    align-items: center;
    gap: 8px;
}

.page-info {
    font-size: 14px;
    font-weight: 500;
    color: #333;
}

.page-input {
    width: 60px;
    padding: 5px 8px;
    font-size: 14px;
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.page-input:focus {
    outline: none;
    border-color: #0066cc;
}

.page-input::-webkit-inner-spin-button,
.page-input::-webkit-outer-spin-button {
    opacity: 1;
}

.items-per-page {
    display: flex;
    align-items: center;
    gap: 10px;
}

.items-per-page label {
    font-size: 14px;
    color: #333;
}

.items-per-page select {
    padding: 5px 10px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
    cursor: pointer;
}

.items-per-page select:hover {
    border-color: #999;
}

.items-per-page select:focus {
    outline: none;
    border-color: #0066cc;
}
</style>