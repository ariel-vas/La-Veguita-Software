<template>
  <div class="p-6 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">Importar listado de familias desde Zpos</h1>

    <form @submit.prevent="handleUpload" class="space-y-4">
      <input
        type="file"
        ref="fileInput"
        @change="onFileChange"
        accept=".pdf,.xlsx,.xls,.csv"
        class="block w-full border border-gray-300 rounded p-2 text-sm"
        required
      />

      <button
        type="submit"
        :disabled="subiendo || !archivo"
        class="bg-[#8bc34a] hover:bg-[#7cb342] text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {{ subiendo ? 'Subiendo...' : 'Importar' }}
      </button>

      <p v-if="mensaje" :class="exito ? 'text-green-600' : 'text-red-600'" class="text-sm mt-2">
        {{ mensaje }}
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const archivo = ref(null)
const subiendo = ref(false)
const mensaje = ref('')
const exito = ref(false)

const fileInput = ref(null)

const onFileChange = () => {
  archivo.value = fileInput.value.files[0] || null
  mensaje.value = ''
}

const handleUpload = async () => {
  if (!archivo.value) return

  subiendo.value = true
  mensaje.value = ''
  exito.value = false

  try {
    const formData = new FormData()
    formData.append('file', archivo.value)

    const config = useRuntimeConfig()
    const response = await fetch(`${config.public.apiBase}/api/categories-pdf/`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(errorText || 'Error en el servidor')
    }

    mensaje.value = 'Archivo de familias importado correctamente.'
    exito.value = true
    archivo.value = null
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  } catch (error) {
    console.error('Error al subir archivo:', error)
    mensaje.value = 'Error al importar el archivo. Verificá el formato o intentá más tarde.'
    exito.value = false
  } finally {
    subiendo.value = false
  }
}
</script>
