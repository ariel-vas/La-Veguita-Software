<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a] mb-5 sm:mb-4 md:mb-6 lg:mb-10">Importar listado de proveedores desde Zpos</h1>

    <form @submit.prevent="handleUpload" class="space-y-4">
      <label
      for="file-upload"
      class="flex items-center justify-center gap-3 cursor-pointer
         bg-white border-2 border-dashed border-gray-300
         rounded-xl px-3 sm:px-4 md:px-9 lg:px-16 py-4 text-gray-600 hover:border-[#8bc34a] hover:text-[#8bc34a]
         transition duration-100 text-center text-sm sm:text-base"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none"
             viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M7 16V4m0 0L3 8m4-4l4 4m0 0v8m0 4h8m-4-4h4m-4 0V8" />
        </svg>
        <span>Selecciona un archivo</span>
        <input
          id="file-upload"
          type="file"
          ref="fileInput"
          @change="onFileChange"
          accept=".pdf,.xlsx,.xls,.csv"
          class="hidden"
          required
        />
        
      </label>
      <p v-if="archivo" class="text-sm text-gray-700 mt-2 text-center">
        Archivo seleccionado: <span class="font-medium">{{ archivo.name }}</span>
      </p>
      <button
        type="submit"
        :disabled="subiendo || !archivo"
        class="flex items-center justify-center gap-2
            bg-[#8bc34a] hover:bg-[#7cb342] text-white font-semibold
              px-4 sm:px-4 md:px-9 lg:px-16 py-2 rounded-xl
              transition duration-300 ease-in-out
              disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg
          v-if="subiendo"
          class="animate-spin h-5 w-5 text-white"
          xmlns="http://www.w3.org/2000/svg"
          fill="none" viewBox="0 0 24 24"
        >
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
        </svg>
        {{ subiendo ? 'Subiendo...' : '📤 Importar' }}
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

const onFileChange = (event) => {
  const files = event.target.files
  archivo.value = files && files.length > 0 ? files[0] : null
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
    const response = await fetch(`${config.public.apiBase}/api/suppliers-pdf/`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(errorText || 'Error en el servidor')
    }

    mensaje.value = 'Archivo de proveedores importado correctamente.'
    exito.value = true
    archivo.value = null
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  } catch (error) {
    console.error('Error al subir archivo:', error)
    mensaje.value = 'Error al importar el archivo. Verifica el formato o intenta más tarde.'
    exito.value = false
  } finally {
    subiendo.value = false
  }
}
</script>
