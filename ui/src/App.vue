<template>
  <div id="app">
    <HeaderBar />
    <GitHubIssues ref="issuesTable" />
    <TableController @issueCreated="onIssueCreated" />
    <FooterBar />
  </div>
</template>

<script setup lang="ts">
import { ref, provide } from 'vue'
import HeaderBar from './components/HeaderBar.vue'
import GitHubIssues from './components/GHITable.vue'
import TableController from './components/TableController.vue';
import FooterBar from './components/FooterBar.vue'

const issuesTable = ref()

provide('issuesTable', issuesTable)

function onIssueCreated() {
    console.log('Issue created! Refreshing table from cache...')
    issuesTable.value?.refreshIssues(false) // Use cache since backend already updated it
}

</script>

<style>
/* global styles */

</style>