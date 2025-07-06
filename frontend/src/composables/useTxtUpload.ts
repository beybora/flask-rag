import { ref } from 'vue'

const API_URL = import.meta.env.VITE_API_URL

export function useTxtUpload() {
  const file = ref<File | null>(null)
  const uploadStatus = ref<string>('')

  const handleFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement
    if (target.files && target.files.length > 0) {
      file.value = target.files[0]
    }
  }

  const uploadFile = async () => {
    if (!file.value) return
    const formData = new FormData()
    formData.append('file', file.value)
    try {
      const res = await fetch(`${API_URL}/api/upload/file`, {
        method: 'POST',
        body: formData,
      })
      if (res.ok) {
        uploadStatus.value = 'Upload erfolgreich!'
      } else {
        uploadStatus.value = 'Fehler beim Upload.'
      }
    } catch (e) {
      uploadStatus.value = 'Fehler beim Upload.'
    }
  }

  return {
    file,
    uploadStatus,
    handleFileChange,
    uploadFile,
  }
} 