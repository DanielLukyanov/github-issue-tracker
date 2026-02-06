<template>
    <button class="base-button" @click="$emit('click')">
        {{ text }}
    </button>
</template>

<script setup lang="ts">
defineProps({
  text: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
    .base-button {
        padding: 0.6rem 1.2rem;
        border-radius: 6px;
        border: none;
        background: #2da44e; /* GitHub green vibes */
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s ease;
    }

    .base-button:hover {
        background: #2c974b;
    }

    .base-button:disabled {
        background: #9be9a8;
        cursor: not-allowed;
    }

    .base-button:active {
        background: #144923;
    }


</style>