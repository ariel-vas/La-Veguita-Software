<template>
  <div class="min-h-screen mt-16 flex flex-col items-center justify-center gap-6 bg-gradient-to-b from-blue-100 via-blue-50 to-gray-100 p-8">
    <h1 class="text-4xl font-bold text-blue-900">Sistema de Gestión de Stock</h1>
    <h2 class="text-2xl font-semibold text-blue-800">Bienvenido a la aplicación de gestión de stock</h2>

      <HomeBox title="Actualización diaria de Stock" to="/productos" />
      <HomeBox title="Ingreso de Stock Individual" to="/productos" />
      <HomeBox title="Administrar Cuentas" to="/cuentas" />
      <HomeBox title="Salida de Stock Manual" to="/devolucion" />
    </div>
  </template>
  
  <script setup>
  import HomeBox from '@/components/HomeBox.vue'
  </script>
  