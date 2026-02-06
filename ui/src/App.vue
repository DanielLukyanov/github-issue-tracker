<template>
  <div id="app">
    <HeaderBar />
    <GitHubIssues />
    <TableController />
    <FooterBar />
  </div>
</template>

<script setup lang="ts">
import HeaderBar from './components/HeaderBar.vue'
import GitHubIssues from './components/GHITable.vue'
import TableController from './components/TableController.vue';
import FooterBar from './components/FooterBar.vue'
</script>

<style>
/* global styles */

</style>