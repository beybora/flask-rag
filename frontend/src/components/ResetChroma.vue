<script setup lang="ts">
import { useChat } from '../composables/useChat'
import { onMounted } from 'vue'

const { resetChroma, isLoading } = useChat()

onMounted(() => {
  resetChroma()
})
</script>

<template>
  <button
    @click="resetChroma"
    :disabled="isLoading"
    class="text-xs text-red-600 underline hover:text-red-800 disabled:text-gray-400 cursor-pointer"
  >
    Chroma zurücksetzen
  </button>
</template>

<style scoped>
</style>
