<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Sistema de Gestión de Stock</h1>
    <h2 class="text-2xl font-semibold text-[#8bc34a]">Bienvenido a la aplicación de gestión de stock</h2>

    <!-- Botón con lógica de carga -->
    <button
      @click="cargarStock"
      class="w-80 bg-[#ff9800] hover:bg-orange-500 text-white font-semibold py-6 px-2 rounded-2xl text-center shadow-lg transition duration-300"
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
    <HomeBox title="Crear un producto" to="/crearproducto" />
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
    await fetch('/api/stock/importar', { method: 'POST' })
    await new Promise(resolve => setTimeout(resolve, 2000))
    router.push('/')
    alert('Se cargó el archivo correctamente.')
  } catch (error) {
    console.error('Error cargando stock:', error)
    alert('Hubo un error al cargar el archivo.')
  } finally {
    cargando.value = false
  }
}
</script>