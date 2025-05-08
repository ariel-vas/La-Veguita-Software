<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-blue-100 p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-blue-900">Sistema de Gestión de Stock</h1>
    <h2 class="text-2xl font-semibold text-blue-800">Bienvenido a la aplicación de gestión de stock</h2>

    <!-- Botón con lógica de carga -->
    <button
      @click="cargarStock"
      class="w-80 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-6 px-2 rounded-2xl text-center shadow-lg transition duration-300 relative"
      :disabled="cargando"
    >
      <span v-if="!cargando">Actualización diaria de Stock</span>
      <span v-else class="flex items-center justify-center">
        <svg class="animate-spin h-6 w-6 text-white mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        Cargando...
      </span>
    </button>

    <!-- Botones normales -->
    <HomeBox title="Ingreso de Stock Manual" to="/agregarstock" />
    <HomeBox title="Salida de Stock Manual" to="/quitarstock" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HomeBox from '@/components/HomeBox.vue'
import { useRouter } from 'vue-router'

const cargando = ref(false)
const router = useRouter()

const cargarStock = async () => {
  cargando.value = true

  try {
    // Simula una llamada al backend que obtiene un archivo desde el servidor
    await fetch('/api/stock/importar', { method: 'POST' })
    
    // Simulamos un tiempo de espera si el backend aún no está listo
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Redirigir a página si querés
    router.push('/')
    alert('Se cargo el archivo correctamente.')
  } catch (error) {
    console.error('Error cargando stock:', error)
    alert('Hubo un error al cargar el archivo.')
  } finally {
    cargando.value = false
  }
}
</script>
