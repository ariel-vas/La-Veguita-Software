<template>
    <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
        <!-- pt-20 es padding-top 5rem = 80px, suficiente para navbar -->
        <h1 class="text-4xl font-extrabold mb-2 text-red-600">Acceso Denegado</h1>

        <p class="text-lg text-gray-700 mb-8 max-w-md mx-auto">
        Para utilizar la aplicación, necesitas iniciar sesión. Por favor, ingresa tus credenciales para continuar.
        </p>

        <NuxtLink
        to="/"
        class="inline-block bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-8 rounded-md shadow-md transition"
        >
        Ir al Inicio de todas formas
        </NuxtLink>
  </div>
</template>

<script setup>
// Sin lógica adicional necesaria
</script>

<style scoped>
/* Puedes agregar animaciones o detalles adicionales aquí si quieres */
</style>
