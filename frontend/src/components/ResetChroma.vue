<script setup lang="ts">
import { useChat } from '../composables/useChat'
import { onMounted } from 'vue'

const { resetChroma, isLoading } = useChat()

onMounted(() => {
  resetChroma()
})
</script>

<template>
  <button @click="resetChroma" :disabled="isLoading" class="mb-4 bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed">
    Chroma Storage zurücksetzen
  </button>
</template>

<style scoped>
</style> 