<script setup>
import { RouterView } from 'vue-router'
import ToastContainer from './components/ToastContainer.vue'
</script>

<template>
  <div class="app-wrapper">
    <RouterView />
    <ToastContainer />
  </div>
</template>

<style scoped>
.app-wrapper {
  min-height: 100vh;
}
</style>