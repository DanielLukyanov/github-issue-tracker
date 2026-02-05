<template>
  <div id="app">
    <HeaderBar />
    <GitHubIssues />
    <FooterBar />
  </div>
</template>

<script setup lang="ts">
import HeaderBar from './components/HeaderBar.vue'
import GitHubIssues from './components/GHITable.vue'
import FooterBar from './components/FooterBar.vue'
</script>

<style>
/* global styles */

</style>