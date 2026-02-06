
<template>
    <div class="table-controller">
        <BaseButton
            text="Create Issue"
            @click="openCreateIssueModal"
        />
        <CreateIssueModal v-if="showModal" @close="closeModal" @submit="onSubmitIssue" />
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseButton from "./BaseButton.vue"
import CreateIssueModal from "./CreateIssueModal.vue"

const showModal = ref(false)

function openCreateIssueModal() {
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

function onSubmitIssue() {
  // handle the created issue here (API call, state update...)
  console.log('Issue submitted')
  showModal.value = false
}
</script>

<style scoped>
    .table-controller {
        display: flex;
        justify-content: flex-end;
        padding: 30px;
    }

</style>