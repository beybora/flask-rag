<script setup lang="ts">
import { useChat } from '../composables/useChat'

const { question, chatHistory, isLoading, handleAsk } = useChat()
</script>

<template>
  <div class="bg-white p-8 rounded shadow-md w-full max-w-md mt-8">
    <h2 class="text-xl font-semibold mb-4 text-center">Frage stellen</h2>
    <textarea
      v-model="question"
      placeholder="Stelle eine Frage zum hochgeladenen Text..."
      rows="4"
      class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
    ></textarea>
    <button
      @click="handleAsk"
      :disabled="!question || isLoading"
      class="w-full mt-2 bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
    >
      Frage absenden
    </button>
    <div v-if="chatHistory.length" class="mt-6">
      <div v-for="(msg, idx) in chatHistory" :key="idx" class="mb-2">
        <span :class="msg.role === 'user' ? 'font-bold text-blue-700' : 'text-gray-700'">
          {{ msg.role === 'user' ? 'Du' : 'Assistant' }}:
        </span>
        <span>{{ msg.content }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style> 