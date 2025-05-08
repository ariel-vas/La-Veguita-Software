<template>
    <div class="flex flex-col items-center justify-center gap-6 bg-blue-100 p-8 pt-0 mt-16">
      <h1 class="text-4xl font-bold text-blue-900">Busqueda de Productos</h1>
      <h2 class="text-2xl font-semibold text-blue-800 mb-6">Encuentra los productos rápidamente</h2>
  
      <!-- Sección de búsqueda -->
      <div class="flex flex-col items-center gap-4 mb-6">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar producto por nombre..."
          class="p-3 w-80 text-lg border-2 border-blue-400 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-600"
        />
        <button @click="search" class="bg-blue-600 text-white py-2 px-6 rounded-xl text-lg hover:bg-blue-700 transition duration-300">
          Buscar
        </button>
      </div>
      <div class="flex flex-col items-center gap-4 mb-6">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar producto por codigo..."
          class="p-3 w-80 text-lg border-2 border-blue-400 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-600"
        />
        <button @click="search" class="bg-blue-600 text-white py-2 px-6 rounded-xl text-lg hover:bg-blue-700 transition duration-300">
          Buscar
        </button>
      </div>
      <!-- Sección de resultados -->
      <div v-if="results.length > 0" class="flex flex-col items-center gap-4">
        <button
          v-for="(result, index) in results"
          :key="index"
          @click="navigateToPage(result)"
          class="bg-blue-600 text-white py-2 px-6 rounded-xl text-lg w-80 hover:bg-blue-700 transition duration-300"
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
        // Simulación de resultados de búsqueda
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
        // Redirige a la página de detalle de cada producto
        this.$router.push({ path: `/detalle` });
      }
    }
  };
  </script>
  
  <style scoped>
  /* Puedes personalizar más los estilos si lo necesitas. El uso de Tailwind CSS se encarga de la mayoría del diseño. */
  </style>
  