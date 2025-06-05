<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Listado de Sub-Categorías</h1>

    <!-- Botón Agregar Categoría -->
    <button
      @click="$router.push('/crearsubcategoria/')"
      class="bg-blue-600 text-white py-2 px-4 rounded-lg text-base hover:bg-blue-700 transition"
    >
      + Agregar Sub-Categoría
    </button>

    <!-- Tabla con listado -->
    <table class=" bg-white rounded-xl shadow overflow-hid_subcategoryden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th class="text-left py-3 px-6">Nombre</th>
          <th class="text-left py-3 px-6">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="cat in displayedSubCategories"
          :key="cat.id_subcategory"
          class="border-b hover:bg-[#f0f8e9]"
        >
          <td class="py-3 px-6">{{ cat.name }}</td>
          <td class="py-3 px-6">
            <button
              @click="navigateToPage(cat.id_subcategory)"
              class="bg-[#8bc34a] text-white px-4 py-1 rounded hover:bg-[#7cb342] transition"
            >
              Ver Detalles
            </button>
          </td>
        </tr>
        <tr v-if="displayedSubCategories.length === 0">
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
      subcategories: [],
      error: '',
    };
  },
  computed: {
    displayedSubCategories() {
      return this.subcategories.slice(0, 20);
    },
  },
  methods: {
    async fetchSubCategories() {
      try {
        const config = useRuntimeConfig();
        const response = await fetch(`${config.public.apiBase}/api/subcategories/`);
        if (!response.ok) throw new Error('Error cargando categorías');
        const data = await response.json();
        this.subcategories = data;
      } catch (err) {
        this.error = err.message;
      }
    },
    navigateToPage(id_subcategory) {
      this.$router.push({ path: `/detalleSubCategoria/${id_subcategory}` });
    },
  },
  mounted() {
    this.fetchSubCategories();
  },
};
</script>
