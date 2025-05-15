<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Listado de Categorías</h1>

    <!-- Botón Agregar Categoría -->
    <button
      @click="$router.push('/crearcategoria/')"
      class="bg-blue-600 text-white py-2 px-4 rounded-lg text-base hover:bg-blue-700 transition"
    >
      + Agregar Categoría
    </button>

    <!-- Tabla con listado -->
    <table class=" bg-white rounded-xl shadow overflow-hid_categoryden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th class="text-left py-3 px-6">Nombre</th>
          <th class="text-left py-3 px-6">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="cat in displayedCategories"
          :key="cat.id_category"
          class="border-b hover:bg-[#f0f8e9]"
        >
          <td class="py-3 px-6">{{ cat.name }}</td>
          <td class="py-3 px-6">
            <button
              @click="navigateToPage(cat.id_category)"
              class="bg-[#8bc34a] text-white px-4 py-1 rounded hover:bg-[#7cb342] transition"
            >
              Ver Detalles
            </button>
          </td>
        </tr>
        <tr v-if="displayedCategories.length === 0">
          <td colspan="2" class="text-center py-4 text-gray-500">
            No hay categorías para mostrar.
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Mensaje de error -->
    <div v-if="error" class="text-2xl font-semibold text-red-600 mt-6">{{ error }}</div>

    <!-- Botón volver atrás -->
    <button
      @click="$router.push('/')"
      class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
    >
      Volver atrás
    </button>
  </div>
</template>

<script>
export default {
  
  data() {
    return {
      categories: [],
      error: '',
    };
  },
  computed: {
    displayedCategories() {
      return this.categories.slice(0, 20);
    },
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/categories/');
        if (!response.ok) throw new Error('Error cargando categorías');
        const data = await response.json();
        this.categories = data;
      } catch (err) {
        this.error = err.message;
      }
    },
    navigateToPage(id_category) {
      this.$router.push({ path: `/detalleCategoria/${id_category}` });
    },
  },
  mounted() {
    this.fetchCategories();
  },
};
</script>
