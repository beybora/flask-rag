<script setup lang="ts">
import { useTxtUpload } from '../composables/useTxtUpload'
import ResetChroma from './ResetChroma.vue'

const { file, uploadStatus, handleFileChange, uploadFile } = useTxtUpload()
</script>

<template>
  <div class="bg-white p-8 rounded shadow-md w-full max-w-md">
    <h1 class="text-xl font-semibold mb-4 text-center">Upload</h1>
    <input
      type="file"
      accept=".txt,.pdf"
      @change="handleFileChange"
      class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 mb-4"
    />

    <button
      @click="uploadFile"
      :disabled="!file"
      class="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
    >
      Hochladen
    </button>

    <div v-if="uploadStatus" class="mt-4 text-center text-green-600">{{ uploadStatus }}</div>

    <div class="mt-6 text-center">
      <p class="text-xs text-gray-500 mb-2 text-center">Lade PDF- oder TXT-Datei hoch</p>
      <ResetChroma />
    </div>
  </div>
</template>

<style scoped>
</style>
