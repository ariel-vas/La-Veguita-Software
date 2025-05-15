<template>
  <NuxtLink
    :to="to"
    class="w-80 bg-[#ff9800] hover:bg-[#fb8c00] text-white font-semibold py-6 px-2 rounded-2xl text-center shadow-lg transition duration-300"
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
