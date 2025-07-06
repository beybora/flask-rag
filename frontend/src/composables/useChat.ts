import { ref } from 'vue'

export function useChat() {
  const question = ref('')
  const chatHistory = ref<{ role: string; content: string }[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const handleAsk = async () => {
    if (!question.value.trim()) return
    isLoading.value = true
    error.value = null
    chatHistory.value.push({ role: 'user', content: question.value })
    try {
      const res = await fetch('http://127.0.0.1:5000/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question.value })
      })
      const data = await res.json()
      if (res.ok && data.answer) {
        chatHistory.value.push({ role: 'assistant', content: data.answer })
      } else if (data.error) {
        chatHistory.value.push({ role: 'assistant', content: 'Fehler: ' + data.error })
      } else {
        chatHistory.value.push({ role: 'assistant', content: 'Unbekannte Antwort vom Server.' })
      }
    } catch (e: any) {
      chatHistory.value.push({ role: 'assistant', content: 'Netzwerkfehler: ' + e.message })
    } finally {
      isLoading.value = false
      question.value = ''
    }
  }

  return {
    question,
    chatHistory,
    isLoading,
    handleAsk,
    error,
  }
} 