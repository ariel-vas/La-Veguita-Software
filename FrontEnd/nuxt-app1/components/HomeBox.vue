<template>
    <NuxtLink
      :to="to"
      class="w-80 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-6 px-2 rounded-2xl text-center shadow-lg transition duration-300"
    >
      {{ title }}
    </NuxtLink>
  </template>
  
  <script setup>
  defineProps({
    title: String,
    to: String,
  })
  </script>
  