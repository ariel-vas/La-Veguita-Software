<template>
  <div>
  <nav class="bg-[#8bc34a] text-white w-full sticky top-0 shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <NuxtLink
          to="/"
          class="flex items-center shrink-0 px-2 py-0 rounded-xl transition-all duration-200"
        >
          <img
            src="/laveguitalogo-removebg-preview.png"
            alt="Icono LVG"
            class="w-12 h-12 sm:w-14 sm:h-14 md:w-16 md:h-16 object-contain mr-2"
          />
          <span class="text-lg sm:text-xl font-bold truncate text-white">La Veguita</span>
        </NuxtLink>

          
        <div class="hidden md:flex space-x-4 flex-grow justify-end min-w-0">
          <div class="flex items-center space-x-2">
            <button
              @click="openAlertModal"
              class="relative group"
              title="Productos por vencer"
            >
              <div class="relative w-9 h-9 flex items-center justify-center rounded-full transition duration-200"
                   :class="notificaciones.length > 0 ? 'bg-yellow-100 group-hover:bg-yellow-200' : 'bg-white/10 group-hover:bg-white/20'">
                <svg xmlns="http://www.w3.org/2000/svg"
                     :class="notificaciones.length > 0 ? 'text-yellow-600' : 'text-white'"
                     class="w-6 h-6 transition"
                     fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V4a2 2 0 00-4 0v1.341C7.67 7.165 7 9.03 7 11v3.159c0 .538-.214 1.055-.595 1.436L5 17h5m5 0v1a3 3 0 01-6 0v-1m6 0H9"/>
                </svg>
                <span v-if="notificaciones.length > 0"
                      class="absolute -top-1 -right-1 bg-red-600 text-white text-[10px] w-5 h-5 rounded-full flex items-center justify-center shadow-md">
                  {{ notificaciones.length }}
                </span>
              </div>
            </button>

            <NuxtLink to="/agregarlote" class="hover:bg-[#7cb342] px-3 py-2 rounded-md transition text-center" :class="activePage === 'agregarlote' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Ingreso x Lote</NuxtLink>
            <NuxtLink to="/agregarstock" class="hover:bg-[#7cb342] px-3 py-2 rounded-md transition text-center" :class="activePage === 'agregarstock' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Ingreso Unitario</NuxtLink>
            <NuxtLink to="/quitarstock" class="hover:bg-[#7cb342] px-3 py-2 rounded-md transition text-center" :class="activePage === 'quitarstock' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Salida Unitaria</NuxtLink>
            <div class="relative" @mouseleave="submenuOpen = false">
              <button
                @click="submenuOpen = !submenuOpen"
                class="hover:bg-[#7cb342] px-3 py-2 rounded-md transition flex items-center space-x-1"
              >
                <span>Organización de Productos</span>
                <svg
                  :class="{ 'rotate-180': submenuOpen }"
                  class="w-4 h-4 transition-transform"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <div
                v-show="submenuOpen"
                class="absolute left-0 top-full w-59 bg-white text-black rounded-md shadow-lg z-50"
                @mouseenter="submenuOpen = true"
                @mouseleave="submenuOpen = false"
              >
                <NuxtLink to="/productos" class="block px-8 py-2 hover:bg-gray-100" :class="activePage === 'productos' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Productos</NuxtLink>
                <NuxtLink to="/categorias" class="block px-8 py-2 hover:bg-gray-100" :class="activePage === 'categorias' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Categorías</NuxtLink>
                <NuxtLink to="/subcategorias" class="block px-8 py-2 hover:bg-gray-100" :class="activePage === 'subcategorias' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Sub-Categorías</NuxtLink>
                <NuxtLink to="/proveedores" class="block px-8 py-2 hover:bg-gray-100" :class="activePage === 'proveedores' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Proveedores</NuxtLink>
                <NuxtLink to="/notificaciones" class="block px-8 py-2 hover:bg-gray-100" :class="activePage === 'notificaciones' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Notificaciones</NuxtLink>
                <NuxtLink to="/crearproducto" class="block px-8 py-2 hover:bg-gray-100" :class="activePage === 'crearproducto' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Crear Producto</NuxtLink>
                <NuxtLink to="/importar-productos" class="block px-8 py-2 hover:bg-gray-100" :class="activePage === 'importar-productos' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Importar Productos</NuxtLink>
                <NuxtLink to="/importar-familias" class="block px-8 py-2 hover:bg-gray-100" :class="activePage === 'importar-familias' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Importar Familias</NuxtLink>
                <NuxtLink to="/importar-proveedores" class="block px-8 py-2 hover:bg-gray-100" :class="activePage === 'importar-proveedores' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Importar Proveedores</NuxtLink>
                <NuxtLink to="/informes" class="block px-8 py-2 hover:bg-gray-100" :class="activePage === 'informes' ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'">Informes</NuxtLink>
              </div>
            </div>
            <div v-if="user" class="flex items-center space-x-2 bg-[#689f38] px-3 py-2 rounded-md transition">
              <span class="text-white">{{ user.username }}</span>
              <button
                @click="logout"
                class="text-white hover:text-red-400 text-sm px-2 py-1 rounded transition"
                title="Cerrar sesión"
              >
                <!-- Puedes usar texto simple -->
                Logout
                <!-- O un icono de salida, por ejemplo SVG -->
                
                <svg xmlns="http://www.w3.org/2000/svg" class="inline w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7" />
                </svg>
              </button>
            </div>
            <div v-else>
              <button
                @click="openLoginModal"
                class="hover:bg-[#7cb342] px-3 py-2 rounded-md transition"
                :class="isLoginModalOpen ? 'bg-[#689f38] font-bold' : ''"
              >
                Ingresar
              </button>
            </div>
          </div>
        </div>
        <!-- Botón campana + hamburguesa en móvil -->
        <div class="flex items-center space-x-2 md:hidden">
          <!-- Bloque central (nombre de sección actual) -->
          <div v-if="mobileActiveSection" class="pointer-events-auto">
            <NuxtLink
              :to="mobileActiveSection.link"
              class="bg-[#689f38] text-white text-sm font-bold px-3 py-1 rounded-md truncate"
            >
              {{ mobileActiveSection.label }}
            </NuxtLink>
          </div>

          <!-- Botón campana -->
          <button
            @click="openAlertModal"
            class="relative group"
            title="Productos por vencer"
          >
            <!-- ... icono campana con notificaciones ... -->
          </button>

          <!-- Botón hamburguesa -->
          <button
            @click="toggleMenu"
            class="text-white focus:outline-none text-2xl z-60 relative"
            aria-label="Abrir menú móvil"
          >
            ☰
          </button>
        </div>
      </div>
    </div>
  </nav>

  <!-- Menú móvil desplegable -->
  <div
    v-if="menuOpen"
    class="md:hidden fixed top-16 right-0 w-64 bg-[#8bc34a] text-white shadow-lg rounded-bl-lg rounded-br-lg z-50 flex flex-col p-4 space-y-2 max-h-[calc(100vh-64px)] overflow-y-auto"
  >
    <!-- Mostrar usuario + logout si hay usuario -->
    <div v-if="user" class="flex items-center space-x-2 bg-[#689f38] px-3 py-2 rounded-md transition mb-4">
      <span class="text-white">{{ user.username }}</span>
      <button
        @click="logout"
        class="text-white hover:text-red-400 text-sm px-2 py-1 rounded transition"
        title="Cerrar sesión"
      >
        Logout
        <svg xmlns="http://www.w3.org/2000/svg" class="inline w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7" />
        </svg>
      </button>
    </div>
    <template v-for="(item, index) in filteredNavItemsMobile ">
      <div
        v-if="!item.action"
        class="flex items-center space-x-2"
        :key="'navitem-noaction-' + item.label + '-' + index"
      >
        <NuxtLink
          :to="item.link"
          class="hover:bg-[#7cb342] px-3 py-2 rounded-md flex-grow"
          :class="activePage === item.link.replace('/', '') ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'"
          @click="menuOpen = false"
        >
          {{ item.label }}
        </NuxtLink>
      </div>

      <button
        v-else
        :key="'navitem-action-' + item.label + '-' + index"
        @click="() => { item.action(); menuOpen = false }"
        :class="isLoginModalOpen ? 'bg-[#689f38] font-bold' : 'hover:bg-[#7cb342]'"
        class="hover:bg-[#7cb342] px-3 py-2 rounded-md text-left"
      >
        {{ item.label }}
      </button>
    </template>
  </div>
  <!-- Modal de Productos por Vencer -->
  <div v-if="showAlertModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-20 z-50" @click="closeAlertModal">
    <div @click.stop class="bg-white p-6 rounded-lg shadow-lg w-96 z-60 absolute top-28 left-1/2 transform -translate-x-1/2 max-h-[70vh] overflow-y-auto">
      <h2 class="text-xl font-bold mb-4">Productos por Vencer</h2>

      <ul class="space-y-4 max-h-[300px] overflow-y-auto">
        <li v-if="notificaciones.filter(n => n.state === 'pending' && !ocultarNotificaciones.has(n.id_notification)).length === 0"
            class="text-center text-green-600 font-semibold bg-green-50 p-4 rounded shadow">
          ¡Todo en orden! 🎉
        </li>

        <li v-for="noti in displayedNotifications"
            :key="noti.id_notification"
            class="border p-3 rounded-md shadow-sm bg-gray-50">
          <div class="flex justify-between items-center">
            <div>
              <p class="font-semibold max-w-[180px] truncate whitespace-nowrap overflow-hidden">{{ noti.name_product }}</p>
              <p class="text-sm text-gray-600">Vence: {{ new Date(noti.expiration_date).toLocaleDateString() }}</p>
              <div v-if="noti.batchDetails && noti.batchDetails.length > 0">
                <div v-for="batch in noti.batchDetails" :key="batch.id_batch">
                  <p class="text-sm text-gray-700">Cantidad por lote: <span class="font-medium">
                    {{ batch.unit === 'kilo' ? parseFloat(batch.quantity).toFixed(3) + " Kilos" : parseInt(batch.quantity) + " Unidades" }}</span></p>
                </div>
              </div>
              <p v-else class="text-sm text-gray-500">No hay detalles de lotes disponibles.</p>
            </div>
            <div class="flex space-x-2">
              <button @click="marcarComoLista(noti.id_notification)" title="Marcar como lista" class="text-green-600 hover:text-green-800 text-xl">
                ✅
              </button>
              <button @click="posponerNotificacion(noti.id_notification)" title="Ocultar temporalmente" class="text-gray-500 hover:text-gray-700 text-xl">
                🕓
              </button>
              <button @click="esconderNotificacion(noti.id_notification)" title="Ocultar" class="text-gray-500 hover:text-gray-700 text-xl">
                😴
              </button>
            </div>
          </div>
        </li>
      </ul>

      <button @click="closeAlertModal" class="mt-4 bg-[#8bc34a] text-white px-4 py-2 rounded-md">Cerrar</button>
    </div>
  </div>
  <!-- Modal de Aviso -->
  <transition name="fade-slide">
    <div
      v-if="mostrarAviso"
      class="fixed bottom-6 right-6 bg-white border-l-4 shadow-xl px-5 py-4 rounded-lg max-w-md z-50 flex items-start space-x-3"
      :class="{
        'border-yellow-500': notificaciones.length > 0,
        'border-green-500': notificaciones.length === 0
      }"
    >
      <div class="text-2xl">
        <span v-if="notificaciones.length > 0" class="text-yellow-500">⚠️</span>
        <span v-else class="text-green-500">✅</span>
      </div>
      <div class="text-gray-800 text-sm">
        <p class="font-semibold mb-1">
          {{ notificaciones.length > 0 ? 'Atención' : 'Todo en orden' }}
        </p>
        <p>{{ mensajeAviso }}</p>
      </div>
    </div>
  </transition>
  <!-- Modal de Login -->
  <div v-if="isLoginModalOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-60" @click="closeLoginModal">
    <div @click.stop class="bg-white p-8 rounded-lg shadow-lg w-96 z-70 absolute top-20 left-1/2 transform -translate-x-1/2">
      <h2 class="text-xl font-bold mb-4">Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700">Email del usuario</label>
          <input
            v-model="email"
            id="email"
            type="text"
            placeholder="ejemplo@correo.com"
            @blur="emailTouched = true"
            class="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-[#8bc34a] focus:border-[#8bc34a]"
            :class="{'border-red-500': emailTouched && !correoValido}"
            required
          />
          <p v-if="emailTouched && !correoValido && email" class="text-red-600 text-sm mt-1">
            Por favor, ingresa un correo válido.
          </p>
        </div>
        <div class="mb-6 relative">
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            id="password"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#8bc34a] focus:border-[#8bc34a]"
            required
          />
          <button
            type="button"
            @click="toggleShowPassword"
            class="absolute right-3 top-9 text-gray-500 hover:text-gray-700 focus:outline-none"
            tabindex="-1"
            aria-label="Mostrar u ocultar contraseña"
          >
            <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.958 9.958 0 012.94-4.46M9.88 9.88a3 3 0 014.24 4.24M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M3 3l18 18" />
            </svg>
          </button>
        </div>
        <div class="flex justify-between items-center">
          <button type="submit" class="bg-[#ff9800] text-white px-4 py-2 rounded-md">Ingresar</button>
          <button type="button" @click="togglePasswordRecovery" class="text-[#ff9800]">¿Recuperar Contraseña?</button>
        </div>
      </form>
      <button @click="closeLoginModal" class="absolute top-2 right-2 text-gray-500">✘</button>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watchEffect, capitalize } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const activePage = ref('')
const isLoginModalOpen = ref(false)
const showAlertModal = ref(false)
const menuOpen = ref(false)
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const notificaciones = ref([]) // Este ref ahora almacenará solo las notificaciones pendientes y ordenadas
const mostrarAviso = ref(false)
const mensajeAviso = ref('')
const submenuOpen = ref(false)
const ocultarNotificaciones = ref(new Set()) // Para la funcionalidad de posponer

const user = ref(null)
const toggleShowPassword = () => {
  showPassword.value = !showPassword.value
}
onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/api/whoami/', {
      credentials: 'include',
    })
    if (response.ok) {
      const data = await response.json()
      user.value = data
    }
  } catch (error) {
    console.error('Error obteniendo usuario:', error)
  }
})

watchEffect(() => {
  const path = route.path || ''

  if (path.startsWith('/productos')) {
    activePage.value = 'productos'
  } else if (path.startsWith('/categorias')) {
    activePage.value = 'categorias'
  } else if (path.startsWith('/subcategorias')) {
    activePage.value = 'subcategorias'
  } else if (path.startsWith('/proveedores')) {
    activePage.value = 'proveedores'
  } else if (path.startsWith('/crearproducto')) {
    activePage.value = 'crearproducto'
  } else if (path.startsWith('/importar-productos')) {
    activePage.value = 'importar-productos'
  } else if (path.startsWith('/importar-familias')) {
    activePage.value = 'importar-familias'
  } else if (path.startsWith('/importar-proveedores')) {
    activePage.value = 'importar-proveedores'
  } else if (path.startsWith('/notificaciones')) {
    activePage.value = 'notificaciones'
  } else if (path.startsWith('/informes')) {
    activePage.value = 'informes'
  } else if (path.startsWith('/agregarlote')) {
    activePage.value = 'agregarlote'
  } else if (path.startsWith('/agregarstock')) {
    activePage.value = 'agregarstock'
  } else if (path.startsWith('/quitarstock')) {
    activePage.value = 'quitarstock'
  } else {
    activePage.value = '' // Nada activo
  }
})

// Computed property para las notificaciones que se mostrarán en el modal, ya filtradas y ordenadas
const displayedNotifications = computed(() => {
  return notificaciones.value
    .filter(n => n.state === 'pending' && !ocultarNotificaciones.value.has(n.id_notification))
    .sort((a, b) => new Date(a.expiration_date) - new Date(b.expiration_date)); // Ordenar de más cercana a más lejana
});


const openLoginModal = () => {
  isLoginModalOpen.value = true
}
const closeLoginModal = () => {
  isLoginModalOpen.value = false
}
const config = useRuntimeConfig()

const correoValido = computed(() => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email.value)
})

const handleLogin = async () => {
  if (!correoValido.value) {
    alert('Por favor ingresa un correo válido')
    return
  }
  try {
    const response = await fetch(`${config.public.apiBase}/api/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include', // necesario para sesiones
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (response.ok && data.success) {
      // obtener datos reales del usuario desde /whoami
      const whoamiRes = await fetch(`${config.public.apiBase}/api/whoami/`, {
        credentials: 'include'
      })
      if (whoamiRes.ok) {
        const userData = await whoamiRes.json()
        user.value = userData
        closeLoginModal()
      } else {
        console.warn('No se pudo obtener datos del usuario')
      }
    } else {
      alert(data.message || 'Error en el login')
    }
  } catch (err) {
    console.error('Error al hacer login:', err)
    alert('Error de red o servidor')
  }
}

const logout = async () => {
  try {
    await fetch(`${config.public.apiBase}/api/logout/`, {
      method: 'GET',
      credentials: 'include',
    })
    user.value = null
  } catch (error) {
    console.error('Error al cerrar sesión:', error)
  }
}

watch(user, (val) => {
  if (val) {
    localStorage.setItem('user', JSON.stringify(val))
  } else {
    localStorage.removeItem('user')
  }
})

onMounted(() => {
  const stored = localStorage.getItem('user')
  if (stored) {
    user.value = JSON.parse(stored)
  }
})


const togglePasswordRecovery = () => {
  console.log('Recuperación de Contraseña')
}
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

// Abre el modal de alerta, también cierra el submenú si está abierto
const openAlertModal = () => {
  showAlertModal.value = true;
  submenuOpen.value = false; // Cierra el submenú al abrir el modal de alerta
}

const closeAlertModal = () => {
  showAlertModal.value = false;
}

const marcarComoLista = async (id_notification) => {
  const fecha = new Date().toISOString()
  try {
    const config = useRuntimeConfig()
    const response = await fetch(`${config.public.apiBase}/api/notifications/${id_notification}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        state: 'ready',
        date_of_completion: fecha
      })
    })
    if (!response.ok) throw new Error('Error al actualizar la notificación a ready');

    // Remueve de la lista local después de actualizar en la API
    notificaciones.value = notificaciones.value.filter(n => n.id_notification !== id_notification);
  } catch (error) {
    console.error('Error actualizando notificación:', error)
  }
}

const posponerNotificacion = (id_notification) => {
  // Esta funcionalidad se mantiene para "ocultar temporalmente"
  // Si deseas que "posponer" cambie el estado a 'viewed' en la API, necesitarías otra función PUT
  ocultarNotificaciones.value.add(id_notification);
  // Recargamos las notificaciones para que el contador de la campana se actualice si la notificación pospuesta era la única.
  // Podrías hacer un filtro más eficiente en el computed property si la lista es muy grande
  // para evitar recargar de la API solo por posponer.
  // Por ahora, solo la quitamos de la lista visible con 'ocultarNotificaciones'.
}
const esconderNotificacion = async (id_notification) => {
  const fecha = new Date().toISOString()
  try {
    const config = useRuntimeConfig()
    const response = await fetch(`${config.public.apiBase}/api/notifications/${id_notification}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        state: 'posponed',
        date_of_completion: fecha
      })
    })
    if (!response.ok) throw new Error('Error al actualizar la notificación a posponed');

    // Remueve de la lista local después de actualizar en la API
    notificaciones.value = notificaciones.value.filter(n => n.id_notification !== id_notification);
  } catch (error) {
    console.error('Error actualizando notificación:', error)
  }
}
const navItemsMobile = [ // Para la vista móvil, se mantienen individuales
  { label: 'Ingreso x Lote', link: '/agregarlote' },
  { label: 'Ingreso Unitario', link: '/agregarstock' },
  { label: 'Salida Unitaria', link: '/quitarstock' },
  { label: 'Productos', link: '/productos' },
  { label: 'Categorias', link: '/categorias' },
  { label: 'Sub-Categorias', link: '/subcategorias' },
  { label: 'Proveedores', link: '/proveedores' },
  { label: 'Informes', link: '/informes' },
  { label: 'Notificaciones', link: '/notificaciones' },
  { label: 'Importar Productos', link: '/importar-productos' },
  { label: 'Importar Familias', link: '/importar-familias' },
  { label: 'Importar Proveedores', link: '/importar-proveedores' },
  { label: 'Organización de Productos', link: 'javascript:void(0)' }, // Este es un botón que abre el submenú
  { label: 'Crear Producto', link: '/crearproducto' },
  { label: 'Ingresar', link: 'javascript:void(0)', action: openLoginModal }
];
const filteredNavItemsMobile = computed(() => {
  if (user.value) {
    // Si hay usuario, quitar el item "Ingresar"
    return navItemsMobile.filter(item => item.label !== 'Ingresar')
  }
  return navItemsMobile
})

const cargarNotificaciones = async () => {
  try {
    const config = useRuntimeConfig()
    const res = await fetch(`${config.public.apiBase}/api/notifications/`)
    const data = await res.json()

    // Filtra directamente las notificaciones que están en estado 'pending'
    const pendingNotifications = data.filter(n => n.state === 'pending');
    const notificationsWithBatches = await Promise.all(
      pendingNotifications.map(async (noti) => {
        try {
          const batchRes = await fetch(`${config.public.apiBase}/api/batches/${noti.id_notification}`);
          if (!batchRes.ok) {
            console.warn(`No se encontraron lotes para la notificación ${noti.id_notification} o error al cargar.`);
            return { ...noti, batchDetails: [] };
          }
          const batchData = await batchRes.json();
          return { ...noti, batchDetails: Array.isArray(batchData) ? batchData : [batchData] };
        } catch (batchError) {
          console.error(`Error al cargar lotes para la notificación ${noti.id_notification}:`, batchError);
          return { ...noti, batchDetails: [] };
        }
      })
    );

    // Asigna y ordena las notificaciones pendientes con sus lotes
    notificaciones.value = notificationsWithBatches.sort((a, b) => {
      // Ordena de la fecha más cercana a la más lejana
      return new Date(a.expiration_date) - new Date(b.expiration_date);
    });
    // Mostrar aviso
    const cantidad = notificaciones.value.length; // Usa la lista ya filtrada y ordenada
    mensajeAviso.value =
      cantidad > 0
        ? `¡Hay ${cantidad} producto${cantidad === 1 ? '' : 's'} cercano${cantidad === 1 ? 'o' : 's'} al vencimiento!`
        : '¡No hay productos cercanos al vencimiento!';

    mostrarAviso.value = true;

    // Ocultarlo luego de 6 segundos
    setTimeout(() => {
      mostrarAviso.value = false;
    }, 6000);
  } catch (error) {
    console.error('Error cargando notificaciones principales:', error)
  }
}
const ingresoLabel = computed(() => {
  if (activePage.value === 'agregarlote') return 'Ingreso x Lote'
  if (activePage.value === 'agregarstock') return 'Ingreso Unitario'
  if (activePage.value === 'quitarstock') return 'Salida Unitaria'
  return ''
})
const allPagesLabels = {
  agregarlote: { label: 'Ingreso x Lote', link: '/agregarlote' },
  agregarstock: { label: 'Ingreso Unitario', link: '/agregarstock' },
  quitarstock: { label: 'Salida Unitaria', link: '/quitarstock' },
  productos: { label: 'Productos', link: '/productos' },
  categorias: { label: 'Categorías', link: '/categorias' },
  subcategorias: { label: 'Sub-Categorías', link: '/subcategorias' },
  proveedores: { label: 'Proveedores', link: '/proveedores' },
  informes: { label: 'Informes', link: '/informes' },
  notificaciones: { label: 'Notificaciones', link: '/notificaciones' },
  'importar-productos': { label: 'Importar Productos', link: '/importar-productos' },
  'importar-familias': { label: 'Importar Familias', link: '/importar-familias' },
  'importar-proveedores': { label: 'Importar Proveedores', link: '/importar-proveedores' },
  crearproducto: { label: 'Crear Producto', link: '/crearproducto' }
};
const mobileActiveSection = computed(() => {
  return allPagesLabels[activePage.value] || null;
});

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

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>