<template>
  <div class="min-h-screen bg-blue-100">
    <Navbar />
    
    <div class="pt-16">
      <NuxtPage />
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>
