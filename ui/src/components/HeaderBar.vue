<template>
    <div class="header">
        <h1>GitHub Issue Tracker</h1>
        <div v-if="user" class="user-info">
            <img :src="user.avatar_url" :alt="user.login" class="avatar" />
            <span class="username">{{ user.name || user.login }}</span>
            <button @click="$emit('logout')" class="logout-btn">Logout</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { User } from '../services/authService'

defineProps<{
  user: User | null
}>()

defineEmits<{
  logout: []
}>()
</script>

<style scoped>
.header {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e1e4e8;
}

h1 {
    margin: 0;
    font-size: 2rem;
    color: #333;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid #e1e4e8;
}

.username {
    font-weight: 500;
    color: #333;
}

.logout-btn {
    padding: 6px 16px;
    background: #d73a49;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 500;
    transition: background 0.2s;
}

.logout-btn:hover {
    background: #cb2431;
}
</style>