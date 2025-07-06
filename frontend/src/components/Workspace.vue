<script setup lang="ts">
import { onMounted } from 'vue'
import TxtUpload from './TxtUpload.vue'
import Chat from './Chat.vue'
import ResetChroma from './ResetChroma.vue'


</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-50">
    <ResetChroma />
    <TxtUpload />
    <Chat />
  </div>
</template>

<style scoped>
</style> 