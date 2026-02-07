<template>
    <div class="table-controller">
        <BaseButton
            text="Create Issue"
            @click="openCreateIssueModal"
        />
        <BaseButton
            text="Refresh Issues"
            @click="issuesTable?.refreshIssues(true)"
        />
        <!-- <BaseButton
            text="test-popup"
            @click="showSuccessMessage = true"   
        />
        <BaseButton
            text="test-error-popup"
            @click="popupType = 'error'; showSuccessMessage = true"
        /> -->
        <CreateIssueModal v-if="showModal" @close="closeModal" @submit="onSubmitIssue" />
        <AlertPopup
            v-if="showSuccessMessage"
            :popupName="popupType === 'success' ? 'Issue Created' : 'Error'"
            :popupMessage="popupMessage"
            :issueUrl="issueUrl"
            :condition="showSuccessMessage"
            :type="popupType"
            :errorCode="errorCode"
            @close="showSuccessMessage = false"
        />
    </div>
</template>

<script setup lang="ts">
import { ref, computed, inject } from 'vue'
import BaseButton from "./BaseButton.vue"
import CreateIssueModal from "./CreateIssueModal.vue"
import AlertPopup from "./AlertPopup.vue"
import { createIssue } from '../services/githubAPI'

const issuesTable = inject<any>('issuesTable')

const emit = defineEmits<{
    (e: 'issueCreated'): void
}>()

const showModal = ref(false)
const showSuccessMessage = ref(false)
const issueTitle = ref('')
const issueUrl = ref('')
const successMessage = ref('')
const popupType = ref<'success' | 'error'>('success')
const errorCode = ref<string | number>('')

function openCreateIssueModal() {
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

function onSubmitIssue(payload: Record<string, any>) {
    createIssue(payload)
  .then(response => {
    popupType.value = 'success'
    issueTitle.value = response.title
    issueUrl.value = response.html_url
    successMessage.value = 'Issue created successfully!'
    console.log('Issue submitted')
    showSuccessMessage.value = true;
    console.log(issueUrl.value, response.html_url);
    closeModal();
    // Emit event to tell parent to refresh issues list from cache
    emit('issueCreated')
    setTimeout(() => {
        showSuccessMessage.value = false
        }, 5000) // Hide message after 5 seconds
    })
    .catch(error => {
    console.error('Error creating issue:', error)
    popupType.value = 'error'
    errorCode.value = error.response?.status || 'UNKNOWN'
    issueTitle.value = 'Failed to create issue'
    issueUrl.value = ''
    showSuccessMessage.value = true
    closeModal()
    setTimeout(() => {
        showSuccessMessage.value = false
        }, 5000)
    })
}
const popupMessage = computed(() => {
    if (popupType.value === 'error') {
        return `Failed to create issue. Please try again.`
    }
    return `Issue "${issueTitle.value}" created successfully!`
});
</script>

<style scoped>
    .table-controller {
        display: flex;
        justify-content: flex-end;
        padding: 30px;
    }

    .success-message {
        margin-top: 20px;
        padding: 15px;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        border-radius: 4px;
    }

</style>