<template>
    <div class="modal-screen" @click.self="onBackdropClick">
        <div class="modal-content">
            <h2>Create New Issue</h2>
            <form class="issue-form" @submit.prevent="onSubmit">
                <div class="form-group">
                    <label for="title">Title</label>
                    <input type="text" id="title" name="title" required />
                </div>
                <div class="form-group">
                    <label for="description">Description</label>
                    <textarea id="description" for="description"/>
                </div>
                <div class="form-group">
                    <label for="assignee">Assignee</label>
                    <input type="text" id="assignee" name="assignee"/>
                </div>
                <div class="issue-options">
                    <div class="form-group">
                        <label for="priority">Priority</label>
                        <select id="priority" name="priority" required>
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="client">Client</label>
                        <select id="client" name="client" required>
                            <option value="low">Low</option>
                            <!-- dynamically load clients here -->
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="type">Type</label>
                        <select id="type" name="type" required>
                            <option value="bug">Bug</option>
                            <option value="feature">Feature</option>
                            <option value="support">Support</option>
                        </select>
                    </div>
                </div>
                <div class="modal-controls">
                    <BaseButton class="cancel-btn" text="Cancel" @click="onBackdropClick" />
                    <BaseButton text="Submit" @click="onSubmit" />
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import BaseButton from "./BaseButton.vue"

const emit = defineEmits<{
    (e: 'close'): void
    (e: 'submit'): void
}>()

function onBackdropClick() {
    emit('close')
}

function onSubmit(e?: Event) {
    if (e && typeof e.preventDefault === 'function') e.preventDefault()
    // TODO: gather form values and pass payload if needed
    emit('submit')
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

    #description {
        height: 100px;
        resize: vertical;
    }
</style>