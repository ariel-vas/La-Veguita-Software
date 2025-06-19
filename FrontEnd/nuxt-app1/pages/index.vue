<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 pt-0 mt-16">
    <div class="bg-white border border-[#c5e1a5] shadow-md rounded-2xl px-6 sm:px-12 md:px-16 lg:px-25 py-6 text-center w-full max-w-3xl">
      <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a] mb-2">Sistema de Gestión de Stock</h1>
      <h2 class="text-xl sm:text-xl md:text-xl lg:text-xl font-bold text-[#8bc34a]">Bienvenido a la aplicación de gestión de stock de La Veguita</h2>
    </div>


    <!-- Actualización diaria de Stock -->
    <div class="bg-orange-100 border border-orange-300 rounded-2xl p-6 w-full max-w-3xl shadow-md">
      <h2 class="text-2xl font-semibold text-orange-700 mb-4">Actualización de Stock</h2>
      <div class="flex justify-center">
        <button
          @click="cargarStock"
          class="w-80 bg-[#ff9800] hover:bg-orange-400 text-white font-semibold py-6 px-2 rounded-2xl text-center shadow-lg transition duration-300 disabled:opacity-60 disabled:cursor-not-allowed"
          :disabled="cargando"
        >
          <span v-if="!cargando">Actualización diaria de Stock</span>
          <span v-else class="flex items-center justify-center">
            <svg class="animate-spin h-6 w-6 text-white mr-2" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            Cargando...
          </span>
        </button>
      </div>
    </div>

    <!-- Sección: Stock por Lote -->
    <div class="bg-green-100 border border-green-300 rounded-2xl p-6 w-full max-w-3xl shadow-md">
      <h2 class="text-2xl font-semibold text-green-700 mb-4">Gestión por Lote</h2>
      <div class="flex justify-center">
        <HomeBox  title="Ingreso de Stock por Lote" to="/agregarlote" />
      </div>
    </div>

    <!-- Sección: Stock Unitario -->
    <div class="bg-blue-100 border border-blue-300 rounded-2xl p-6 w-full max-w-3xl shadow-md">
      <h2 class="text-2xl font-semibold text-blue-700 mb-4">Gestión Unitaria</h2>
      
      <div class="flex flex-col md:flex-row justify-center gap-4">
        <HomeBox class="w-full md:w-auto" title="Ingreso de Stock Unitario" to="/agregarstock" />
        <HomeBox class="w-full md:w-auto" title="Salida de Stock Unitario" to="/quitarstock" />
      </div>
    </div>

    <!-- Crear producto
    <div class="bg-purple-100 border border-purple-300 rounded-2xl p-6 w-full max-w-3xl shadow-md">
      <h2 class="text-2xl font-semibold text-purple-700 mb-4">Productos</h2>
      <div class="flex justify-center">
        <HomeBox title="Crear un producto" to="/crearproducto" />
      </div>
    </div>-->
  </div> 
</template>

<script setup>
  import { ref } from 'vue'
  import HomeBox from '@/components/HomeBox.vue'
  import { useRouter } from 'vue-router'

  const cargando = ref(false)
  const router = useRouter()
  const config = useRuntimeConfig()
  const cargarNotificaciones = async () => {
  try {
    const res = await fetch(`${config.public.apiBase}/api/batches/expiring/`)
    } catch (error) {
      console.error('Error recargando notificaciones:', error)
    }
  }
  const cargarStock = async () => {
    cargando.value = true

    try {
      await fetch(`${config.public.apiBase}/api/stock/importar`, { method: 'POST' })
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
  onMounted(() => {
    cargarNotificaciones()
  })
</script>