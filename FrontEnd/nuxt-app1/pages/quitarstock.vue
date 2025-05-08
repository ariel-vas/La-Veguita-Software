<template>
    <div class="flex flex-col items-center justify-center gap-6 bg-blue-100 p-8 pt-0 mt-16">
      <h1 class="text-4xl font-bold text-blue-900">Salida de Productos Manual</h1>
      <h2 class="text-2xl font-semibold text-blue-800 mb-6">Encuentra los productos rápidamente</h2>
  
      <!-- Búsqueda por nombre -->
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
  
      <!-- Búsqueda por código -->
      <div class="flex flex-col items-center gap-4 mb-6">
        <input
          v-model="searchCodeQuery"
          type="text"
          placeholder="Buscar producto por código..."
          class="p-3 w-80 text-lg border-2 border-blue-400 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-600"
        />
        <button @click="searchByCode" class="bg-blue-600 text-white py-2 px-6 rounded-xl text-lg hover:bg-blue-700 transition duration-300">
          Buscar
        </button>
      </div>
  
      <!-- Resultados con campo de stock -->
      <div v-if="results.length > 0" class="flex flex-col items-center gap-6">
        <div
          v-for="(item, index) in results"
          :key="index"
          class="bg-white p-4 rounded-xl shadow w-80 flex flex-col gap-2"
        >
          <span class="font-semibold text-blue-900 text-lg">{{ item.name }}</span>
          <input
            v-model.number="item.stockToAdd"
            type="number"
            min="1"
            placeholder="Cantidad a quitar"
            class="p-2 border border-blue-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            @click="addStock(item)"
            class="bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition"
          >
            Quitar stock
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchQuery: '',
        searchCodeQuery: '',
        results: []
      };
    },
    methods: {
      search() {
        if (this.searchQuery.trim() !== '') {
          this.results = [
            { name: `${this.searchQuery} Resultado 1`, stockToAdd: 0 },
            { name: `${this.searchQuery} Resultado 2`, stockToAdd: 0 },
            { name: `${this.searchQuery} Resultado 3`, stockToAdd: 0 }
          ];
        } else {
          this.results = [];
        }
      },
      searchByCode() {
        if (this.searchCodeQuery.trim() !== '') {
          this.results = [
            { name: `Código ${this.searchCodeQuery} Resultado 1`, stockToAdd: 0 }
          ];
        } else {
          this.results = [];
        }
      },
      addStock(item) {
        if (item.stockToAdd > 0) {
          console.log(`Agregado ${item.stockToAdd} al producto: ${item.name}`);
          // Aquí podrías hacer un fetch/post al backend, por ejemplo.
          item.stockToAdd = 0; // Reinicia el campo
        } else {
          alert('Ingresa una cantidad válida');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Sin cambios adicionales, todo manejado con Tailwind */
  </style>
  