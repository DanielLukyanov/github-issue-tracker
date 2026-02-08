<template>
  <div id="app">
    <HeaderBar />
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
  </div>
</template>

<script setup lang="ts">
import { ref, provide } from 'vue'
import HeaderBar from './components/HeaderBar.vue'
import GitHubIssues from './components/GHITable.vue'
import TableController from './components/TableController.vue'
import FooterBar from './components/FooterBar.vue'
import AlertPopup from './components/AlertPopup.vue'
import { usePopup } from './composables/usePopup'

const issuesTable = ref()
const { popup, showPopup, closePopup } = usePopup()

provide('issuesTable', issuesTable)
provide('popup', { showPopup, closePopup })

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
</style>