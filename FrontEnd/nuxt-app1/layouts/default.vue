<template>
    <div>
      <Navbar />
      <div class="pt-16 px-4"> <!-- pt-16 para no ocultar contenido bajo la navbar -->
        <NuxtPage />
      </div>
    </div>
  </template>
  
  <script setup>
  import Navbar from '~/components/Navbar.vue'
  </script>
  