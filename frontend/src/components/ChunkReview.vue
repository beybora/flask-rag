<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ chunks: string[], question: string, sessionId: string }>()
const editedChunks = ref([...props.chunks])
const answer = ref('')
const loading = ref(false)

const rewriteChunk = async (idx: number) => {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/api/chunks/rewrite`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chunk: editedChunks.value[idx] })
  })
  const data = await res.json()
  editedChunks.value[idx] = data.rewritten
}

const deleteChunk = (idx: number) => {
  editedChunks.value.splice(idx, 1)
}

const submitQuestion = async () => {
  loading.value = true
  const res = await fetch(`${import.meta.env.VITE_API_URL}/api/ask/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: props.sessionId,
      question: props.question,
      chunks: editedChunks.value
    })
  })
  const data = await res.json()
  answer.value = data.answer
  loading.value = false
}
</script>

<template>
  <div>
    <div v-for="(chunk, idx) in editedChunks" :key="idx" class="mb-4">
      <textarea v-model="editedChunks[idx]" class="w-full p-2 border rounded"></textarea>
      <div class="flex gap-2 mt-1">
        <button @click="() => rewriteChunk(idx)" class="bg-yellow-500 text-white px-2 py-1 rounded">Rewrite</button>
        <button @click="() => deleteChunk(idx)" class="bg-red-500 text-white px-2 py-1 rounded">Delete</button>
      </div>
    </div>
    <button @click="submitQuestion" class="w-full bg-green-600 text-white py-2 px-4 rounded mt-4" :disabled="loading">Submit question</button>
    <div v-if="answer" class="mt-4 p-4 bg-green-100 rounded">{{ answer }}</div>
  </div>
</template> 