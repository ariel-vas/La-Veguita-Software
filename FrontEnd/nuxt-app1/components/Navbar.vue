<template>
    <nav class="bg-gradient-to-b from-blue-900/95 to-blue-800/80 backdrop-blur-sm text-white w-full fixed top-0 z-50 shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <NuxtLink to="/" class="text-xl font-bold">LVG</NuxtLink>
          <div class="hidden md:flex space-x-4">
            <NuxtLink
              v-for="(item, index) in navItems"
              :key="index"
              :to="item.link"
              class="hover:bg-blue-600/60 px-3 py-2 rounded-md transition"
            >
              {{ item.label }}
            </NuxtLink>
          </div>
          <button @click="toggleMenu" class="md:hidden text-white focus:outline-none text-2xl">
            ☰
          </button>
        </div>
        <div v-if="menuOpen" class="md:hidden flex flex-col mt-2 space-y-2">
          <NuxtLink
            v-for="(item, index) in navItems"
            :key="index"
            :to="item.link"
            class="hover:bg-blue-600/60 px-3 py-2 rounded-md"
            @click="menuOpen = false"
          >
            {{ item.label }}
          </NuxtLink>
        </div>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const menuOpen = ref(false)
  const toggleMenu = () => {
    menuOpen.value = !menuOpen.value
  }
  
  const navItems = [
    { label: 'Productos', link: '/productos' },
    { label: 'Cuentas', link: '/cuentas' },
    { label: 'Insumos', link: '/insumos' },
    { label: 'Devolución', link: '/devolucion' },
    { label: 'Ingresar', link: '/login  ' }
  ]
  </script>
  