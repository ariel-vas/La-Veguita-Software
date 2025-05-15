<template>
  <nav class="bg-[#8bc34a] text-white w-full sticky top-0 shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center ">
        <NuxtLink to="/" class="flex items-center shrink-0">
          <img 
            src="/laveguitalogo-removebg-preview.png" 
            alt="Icono LVG" 
            class="w-12 h-12 sm:w-14 sm:h-14 md:w-16 md:h-16 object-contain mr-2" 
          />
          <span class="text-lg sm:text-xl font-bold truncate">La Veguita</span>
        </NuxtLink>

        <div class="hidden md:flex space-x-4 flex-grow justify-end min-w-0">
          <NuxtLink
            v-for="(item, index) in navItems"
            :key="index"
            :to="item.link"
            class="hover:bg-[#7cb342] px-3 py-2 rounded-md transition"
            @click="item.action"
          >
            {{ item.label }}
          </NuxtLink>
        </div>
        <button @click="toggleMenu" class="md:hidden text-white focus:outline-none text-2xl">
          ☰
        </button>
      </div>
      <div v-if="menuOpen" class="md:hidden flex flex-col mt-2 space-y-2">
        <template v-for="(item, index) in navItems" :key="index">
          <NuxtLink
            v-if="!item.action"
            :to="item.link"
            class="hover:bg-[#7cb342] px-3 py-2 rounded-md"
            @click="menuOpen = false"
          >
            {{ item.label }}
          </NuxtLink>
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

  <!-- Modal (Popup) para Iniciar Sesión -->
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
</template>

<script setup>
import { ref } from 'vue'

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
const isLoginModalOpen = ref(false)
const username = ref('')
const password = ref('')
const menuOpen = ref(false)
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}
const navItems = [
  { label: 'Productos', link: '/productos' },
  { label: 'Categorias', link: '/categorias' },
  { label: 'Sub-Categorias', link: '/subcategorias' },
  { label: 'Ingresar', link: 'javascript:void(0)', action: openLoginModal }
]
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
