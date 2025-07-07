<script setup lang="ts">
import { ref } from 'vue'
import ChunkReview from './ChunkReview.vue'

const question = ref('')
const sessionId = ref(crypto.randomUUID())
const chunks = ref<string[]>([])
const showReview = ref(false)

const prepareChunks = async () => {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/api/ask/prepare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: question.value, session_id: sessionId.value })
  })
  const data = await res.json()
  chunks.value = data.chunks
  showReview.value = true
}
</script>

<template>
  <div class="max-w-md mx-auto p-4">
    <input v-model="question" placeholder="Ask your question..." class="w-full p-2 border rounded mb-2" />
    <button @click="prepareChunks" class="w-full bg-blue-600 text-white py-2 px-4 rounded mb-4">Prepare</button>
    <ChunkReview v-if="showReview" :chunks="chunks" :question="question" :session-id="sessionId" />
  </div>
</template> 