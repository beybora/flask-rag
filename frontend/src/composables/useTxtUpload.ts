import { ref } from 'vue'

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
      const res = await fetch('http://127.0.0.1:5000/api/upload/file', {
        method: 'POST',
        body: formData,
      })
      if (res.ok) {
        uploadStatus.value = 'Uploaded!'
      } else {
        uploadStatus.value = 'Uploading failed!'
      }
    } catch (e) {
      uploadStatus.value = 'Uploading failed!'
    }
  }

  return {
    file,
    uploadStatus,
    handleFileChange,
    uploadFile,
  }
} 