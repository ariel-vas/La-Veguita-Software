<template>
  <nav class="bg-[#8bc34a] text-white w-full sticky top-0 shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <NuxtLink to="/" class="flex items-center shrink-0">
          <img 
            src="/laveguitalogo-removebg-preview.png" 
            alt="Icono LVG" 
            class="w-12 h-12 sm:w-14 sm:h-14 md:w-16 md:h-16 object-contain mr-2" 
          />
          <span class="text-lg sm:text-xl font-bold truncate">La Veguita</span>
        </NuxtLink>

        <!-- Menú escritorio -->
        <div class="hidden md:flex space-x-4 flex-grow justify-end min-w-0">
          <div v-for="(item, index) in navItems" :key="index" class="flex items-center space-x-2">
            <button
              v-if="item.label === 'Productos' && notificaciones.length > 0"
              @click="showAlertModal = true"
              class="relative text-yellow-500 hover:text-yellow-600 transition"
              title="Productos por vencer"
            >
              <!-- Icono de campana -->
              <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V4a2 2 0 00-4 0v1.341C7.67 7.165 7 9.03 7 11v3.159c0 .538-.214 1.055-.595 1.436L5 17h5m5 0v1a3 3 0 01-6 0v-1m6 0H9"/>
              </svg>

              <!-- Badge si hay notificaciones -->
              <span v-if="notificaciones.length > 0" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
                {{ notificaciones.length }}
              </span>
            </button>


            <NuxtLink
              v-if="!item.action"
              :to="item.link"
              class="hover:bg-[#7cb342] px-3 py-2 rounded-md transition"
            >
              {{ item.label }}
            </NuxtLink>

            <button
              v-else
              @click="item.action"
              class="hover:bg-[#7cb342] px-3 py-2 rounded-md transition"
            >
              {{ item.label }}
            </button>
          </div>
        </div>

        <!-- Botón menú móvil -->
        <button @click="toggleMenu" class="md:hidden text-white focus:outline-none text-2xl">
          ☰
        </button>
      </div>

      <!-- Menú móvil -->
      <div v-if="menuOpen" class="md:hidden flex flex-col mt-2 space-y-2">
        <template v-for="(item, index) in navItems" :key="index">
          <div v-if="!item.action" class="flex items-center space-x-2">
            <button
              v-if="item.label === 'Productos' && notificaciones.length > 0"
              @click="showAlertModal = true"
              class="relative text-yellow-500 hover:text-yellow-600 transition"
              title="Productos por vencer"
            >
              <!-- Icono de campana -->
              <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V4a2 2 0 00-4 0v1.341C7.67 7.165 7 9.03 7 11v3.159c0 .538-.214 1.055-.595 1.436L5 17h5m5 0v1a3 3 0 01-6 0v-1m6 0H9"/>
              </svg>

              <!-- Badge si hay notificaciones -->
              <span v-if="notificaciones.length > 0" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
                {{ notificaciones.length }}
              </span>
            </button>
            <NuxtLink
              :to="item.link"
              class="hover:bg-[#7cb342] px-3 py-2 rounded-md flex-grow"
              @click="menuOpen = false"
            >
              {{ item.label }}
            </NuxtLink>
          </div>
          <button
            v-else
            @click="() => { item.action(); menuOpen = false }"
            class="hover:bg-[#7cb342] px-3 py-2 rounded-md text-left"
          >
            {{ item.label }}
          </button>
        </template>
      </div>
    </div>
  </nav>

  <!-- Modal de inicio de sesión -->
  <div v-if="isLoginModalOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-60" @click="closeLoginModal">
    <div @click.stop class="bg-white p-8 rounded-lg shadow-lg w-96 z-70 absolute top-20 left-1/2 transform -translate-x-1/2">
      <h2 class="text-xl font-bold mb-4">Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label for="username" class="block text-sm font-medium text-gray-700">Usuario</label>
          <input v-model="username" id="username" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#8bc34a] focus:border-[#8bc34a]" required />
        </div>
        <div class="mb-6">
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <input v-model="password" id="password" type="password" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#8bc34a] focus:border-[#8bc34a]" required />
        </div>
        <div class="flex justify-between items-center">
          <button type="submit" class="bg-[#ff9800] text-white px-4 py-2 rounded-md">Ingresar</button>
          <button type="button" @click="togglePasswordRecovery" class="text-[#ff9800]">¿Recuperar Contraseña?</button>
        </div>
      </form>
      <button @click="closeLoginModal" class="absolute top-2 right-2 text-gray-500">✘</button>
    </div>
  </div>

  <!-- Modal de alerta de vencimiento -->
  <div v-if="showAlertModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-20 z-50" @click="showAlertModal = false">
    <div @click.stop class="bg-white p-6 rounded-lg shadow-lg w-96 z-60 absolute top-28 left-1/2 transform -translate-x-1/2 max-h-[70vh] overflow-y-auto">
      <h2 class="text-xl font-bold mb-4">Productos por Vencer</h2>

      <ul class="space-y-4 max-h-[300px] overflow-y-auto">
        <li v-for="noti in notificaciones.filter(n => !ocultarNotificaciones.has(n.id_notification))" :key="noti.id_notification" class="border p-3 rounded-md shadow-sm bg-gray-50">
          <div class="flex justify-between items-center">
            <div>
              <p class="font-semibold">{{ noti.name_product }}</p>
              <p class="text-sm text-gray-600">Vence: {{ new Date(noti.expiration_date).toLocaleDateString() }}</p>
            </div>
            <div class="flex space-x-2">
              <!-- Ticket -->
              <button @click="marcarComoLista(noti.id_notification)" title="Marcar como lista" class="text-green-600 hover:text-green-800 text-xl">
                ✅
              </button>
              <!-- Posponer -->
              <button @click="posponerNotificacion(noti.id_notification)" title="Ocultar temporalmente" class="text-gray-500 hover:text-gray-700 text-xl">
                🕓
              </button>
            </div>
          </div>
        </li>
      </ul>

      <button @click="showAlertModal = false" class="mt-4 bg-[#8bc34a] text-white px-4 py-2 rounded-md">Cerrar</button>
    </div>
  </div>
  
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isLoginModalOpen = ref(false)
const showAlertModal = ref(false)
const menuOpen = ref(false)
const username = ref('')
const password = ref('')
const notificaciones = ref([])

const openLoginModal = () => {
  isLoginModalOpen.value = true
}
const closeLoginModal = () => {
  isLoginModalOpen.value = false
}
const handleLogin = () => {
  console.log('Usuario:', username.value)
  console.log('Contraseña:', password.value)
  closeLoginModal()
}
const togglePasswordRecovery = () => {
  console.log('Recuperación de Contraseña')
}
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}
const ocultarNotificaciones = ref(new Set())
const marcarComoLista = async (id_notification) => {
  const fecha = new Date().toISOString()
  try {
    await fetch(`http://localhost:8000/api/notifications/${id_notification}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        state: 'ready',
        date_of_completion: fecha
      })
    })
    // Remueve de la lista luego de actualizar
    notificaciones.value = notificaciones.value.filter(n => n.id_notification !== id_notification)
  } catch (error) {
    console.error('Error actualizando notificación:', error)
  }
}


const posponerNotificacion = (id_notification) => {
  ocultarNotificaciones.value.add(id_notification)
}

const navItems = [
  { label: 'Productos', link: '/productos' },
  { label: 'Categorias', link: '/categorias' },
  { label: 'Sub-Categorias', link: '/subcategorias' },
  { label: 'Ingresar', link: 'javascript:void(0)', action: openLoginModal }
]

const cargarNotificaciones = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/notifications/')
    const data = await res.json()
    notificaciones.value = data.filter(n => n.state === 'pending')
  } catch (error) {
    console.error('Error cargando notificaciones:', error)
  }
}

onMounted(() => {
  cargarNotificaciones()
})
</script>

<style scoped>
nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
}
</style>
