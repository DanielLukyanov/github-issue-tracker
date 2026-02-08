<template>
  <div id="app">
    <!-- Show login page if not authenticated -->
    <LoginPage v-if="!isAuthenticated && !isLoading" />
    
    <!-- Show main app if authenticated -->
    <template v-else-if="isAuthenticated">
      <HeaderBar :user="user" @logout="handleLogout" />
      <GitHubIssues ref="issuesTable" />
      <TableController @issueCreated="onIssueCreated" />
      <FooterBar />
      <AlertPopup
        v-if="popup.visible"
        :popupName="popup.name"
        :popupMessage="popup.message"
        :issueUrl="popup.issueUrl"
        :condition="popup.visible"
        :type="popup.type"
        :errorCode="popup.errorCode"
        @close="closePopup"
      />
    </template>
    
    <!-- Loading state -->
    <div v-else class="loading">
      <p>Checking authentication...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, provide, onMounted } from 'vue'
import HeaderBar from './components/HeaderBar.vue'
import GitHubIssues from './components/GHITable.vue'
import TableController from './components/TableController.vue'
import FooterBar from './components/FooterBar.vue'
import AlertPopup from './components/AlertPopup.vue'
import LoginPage from './components/LoginPage.vue'
import { usePopup } from './composables/usePopup'
import { checkAuthStatus, logout, type User } from './services/authService'

const issuesTable = ref()
const { popup, showPopup, closePopup } = usePopup()

const isAuthenticated = ref(false)
const isLoading = ref(true)
const user = ref<User | null>(null)

provide('issuesTable', issuesTable)
provide('popup', { showPopup, closePopup })

onMounted(async () => {
  // Check if we just came back from OAuth (look for URL params)
  const params = new URLSearchParams(window.location.search)
  if (params.get('login') === 'success') {
    // Give backend a moment to set the session, then check
    await new Promise(resolve => setTimeout(resolve, 500))
    // Clean up URL
    window.history.replaceState({}, document.title, window.location.pathname)
  }
  
  await checkAuth()
})

async function checkAuth() {
  isLoading.value = true
  const status = await checkAuthStatus()
  isAuthenticated.value = status.authenticated
  user.value = status.user || null
  isLoading.value = false
}

async function handleLogout() {
  await logout()
  isAuthenticated.value = false
  user.value = null
}

function onIssueCreated() {
    console.log('Issue created! Refreshing table from cache...')
    issuesTable.value?.refreshIssues(false) // Use cache since backend already updated it
}

</script>

<style>
#app {
    width: 100%;
    min-height: 100vh;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 1.2rem;
  color: #666;
}
</style>