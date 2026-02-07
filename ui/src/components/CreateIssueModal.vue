<template>
    <div class="modal-screen" @click.self="onBackdropClick">
        <div class="modal-content">
            <h2>Create New Issue</h2>
            <form class="issue-form" @submit.prevent="onSubmit">
                <div class="form-group">
                    <label for="title">Title</label>
                    <input type="text" id="title" v-model="title" required />
                </div>
                <div class="form-group">
                    <label for="body">Description</label>
                    <textarea id="body" v-model="body"/>
                </div>
                <div class="form-group">
                    <label for="assignee">Assignee</label>
                    <input type="text" id="assignee" v-model="assignee"/>
                </div>
                <div class="issue-options">
                    <div class="form-group">
                        <label for="priority">Select a priority for the issue</label>
                        <select id="priority" v-model="priority" required>
                            <option value="Low">P: Low</option>
                            <option value="Medium">P: Medium</option>
                            <option value="High">P: High</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="client">Select which client this issue is related to</label>
                        <select id="client" v-model="client" required>
                            <option value="ABC">C: ABC</option>
                            <option value="XYZ">C: XYZ</option>
                            <option value="MNO">C: MNO</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="type">Select the type of the issue</label>
                        <select id="type" v-model="type" required>
                            <option value="Bug">T: Bug</option>
                            <option value="Support">T: Support</option>
                            <option value="Enhancement">T: Enhancement</option>
                        </select>
                    </div>
                </div>
                <div class="modal-controls">
                    <BaseButton class="cancel-btn" text="Cancel" @click="onBackdropClick" />
                    <BaseButton text="Submit" />
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import BaseButton from "./BaseButton.vue"
import { ref } from 'vue'

const emit = defineEmits<{
    (e: 'close'): void
    (e: 'submit', payload: Record<string, any>): void
}>()

const title = ref('')
const body = ref('')
const assignee = ref('')
const priority = ref('Low')
const type = ref('Bug')
const client = ref('ABC')

function onSubmit() {
    const payload = {
        title: title.value,
        body: body.value,
        assignee: assignee.value,
        priority: priority.value,
        type: type.value,
        client: client.value
    }

    emit('submit', payload)
}

function onBackdropClick() {
    emit('close')
}
</script>

<style scoped>
.modal-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    position: absolute;
    top: 20%;
    left: 20%;
    width: 60%;
    background-color: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.issue-form .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.issue-form{
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.issue-options {
    display: flex;
    gap: 20px;
    justify-content: flex-start;
    align-items: center;
}

.modal-controls {
    display: flex;
    justify-content: space-between;
    gap: 10px;
}

.cancel-btn {
    background-color: #e55353;
}

.cancel-btn:hover {
    background-color: #d64545;
}

#body {
    height: 100px;
    resize: vertical;
}
</style>