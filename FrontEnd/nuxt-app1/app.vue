<template>
  <div class="min-h-screen bg-[#f5f5f5]">
    <Navbar />
    
    <div class="pt-16">
      <NuxtPage />
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>
