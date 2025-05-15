<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Busqueda de Productos</h1>
    <h2 class="text-2xl font-semibold text-[#8bc34a] mb-6">Encuentra los productos rápidamente</h2>

    <!-- Sección de búsqueda -->
    <div class="flex flex-col items-center gap-4 mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar producto por nombre..."
        class="p-3 w-80 text-lg border-2 border-[#8bc34a] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#8bc34a] text-[#000000]"
      />
      <button @click="search" class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300">
        Buscar
      </button>
    </div>
    <div class="flex flex-col items-center gap-4 mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar producto por codigo..."
        class="p-3 w-80 text-lg border-2 border-[#8bc34a] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#8bc34a] text-[#000000]"
      />
      <button @click="search" class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300">
        Buscar
      </button>
    </div>

    <!-- Sección de resultados -->
    <div v-if="results.length > 0" class="flex flex-col items-center gap-4">
      <button
        v-for="(result, index) in results"
        :key="index"
        @click="navigateToPage(result)"
        class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg w-80 hover:bg-opacity-90 transition duration-300"
      >
        {{ result }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      results: []
    };
  },
  methods: {
    search() {
      if (this.searchQuery.trim() !== '') {
        this.results = [
          `${this.searchQuery} Resultado 1`,
          `${this.searchQuery} Resultado 2`,
          `${this.searchQuery} Resultado 3`
        ];
      } else {
        this.results = [];
      }
    },
    navigateToPage(result) {
      this.$router.push({ path: `/detalle` });
    }
  }
};
</script>

<style scoped>
</style>
