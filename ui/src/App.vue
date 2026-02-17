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
    // Clean up URL first
    window.history.replaceState({}, document.title, window.location.pathname)
    
    // Retry auth check with exponential backoff to ensure cookie is set
    let retries = 0
    const maxRetries = 5
    
    while (retries < maxRetries) {
      await checkAuth()
      
      if (isAuthenticated.value) {
        console.log('Authentication successful after OAuth callback')
        break
      }
      
      // Wait with exponential backoff: 100ms, 200ms, 400ms, 800ms, 1600ms
      const delay = 100 * Math.pow(2, retries)
      console.log(`Waiting ${delay}ms before retry ${retries + 1}/${maxRetries}...`)
      await new Promise(resolve => setTimeout(resolve, delay))
      retries++
    }
    
    if (!isAuthenticated.value) {
      console.error('Authentication failed after OAuth callback - session may not be persisted')
    }
  } else {
    await checkAuth()
  }
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