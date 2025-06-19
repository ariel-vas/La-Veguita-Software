<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a] mb-5 sm:mb-4 md:mb-6 lg:mb-10">Listado de Categorías</h1>

    <!-- Botón Agregar Categoría -->
    <button
      @click="$router.push('/crearcategoria/')"
      class="bg-blue-600 text-white py-2 px-2 sm:px-3 md:px-4 rounded-lg text-base hover:bg-blue-700 transition"
    >
      + Agregar Categoría
    </button>

    <!-- Tabla con listado -->
    <table class=" bg-white rounded-xl shadow overflow-hid_categoryden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Nombre</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="cat in displayedCategories"
          :key="cat.id_category"
          class="border-b hover:bg-[#f0f8e9]"
        >
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">{{ cat.name }}</td>
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">
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
    <!-- Paginación -->
    <div class="flex flex-col items-center gap-2 mt-6">
      <div class="text-gray-600 font-medium">
        Mostrando {{ currentRange }} de {{ totalCategories }} categorías
      </div>
      <div class="flex flex-wrap items-center justify-center gap-2">
        <button
          @click="changePage(1)"
          :disabled="currentPage === 1"
          class="px-3 py-1 rounded-md bg-[#8bc34a] text-white hover:bg-[#7cb342] disabled:opacity-50"
        >
          &laquo;
        </button>
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-1 rounded-md bg-[#8bc34a] text-white hover:bg-[#7cb342] disabled:opacity-50"
        >
          &lt;
        </button>

        <button
          v-for="page in visiblePages"
          :key="'page-' + page"
          @click="changePage(page)"
          :class="[
            'px-3 py-1 rounded-md',
            page === currentPage
              ? 'bg-[#ff9800] text-white'
              : 'bg-white text-[#8bc34a] border border-[#8bc34a] hover:bg-[#f0f0f0]'
          ]"
        >
          {{ page }}
        </button>

        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 rounded-md bg-[#8bc34a] text-white hover:bg-[#7cb342] disabled:opacity-50"
        >
          &gt;
        </button>
        <button
          @click="changePage(totalPages)"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 rounded-md bg-[#8bc34a] text-white hover:bg-[#7cb342] disabled:opacity-50"
        >
          &raquo;
        </button>
      </div>
    </div>

    <!-- Mensaje de error -->
    <div v-if="error" class="text-2xl font-semibold text-red-600 mt-6">{{ error }}</div>

    <!-- Botón volver atrás -->
    <button
      @click="$router.push('/')"
      class="bg-[#ff9800] text-white py-2 px-2 sm:px-4 md:px-6 lg:px-8 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
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
      currentPage: 1,
      itemsPerPage: 10, // o 20, según prefieras
      maxVisiblePages: 5,
    };
  },
  computed: {
    totalCategories() {
      return this.categories.length;
    },
    totalPages() {
      return Math.ceil(this.totalCategories / this.itemsPerPage);
    },
    currentRange() {
      const start = (this.currentPage - 1) * this.itemsPerPage + 1;
      const end = Math.min(start + this.itemsPerPage - 1, this.totalCategories);
      return `${start}-${end}`;
    },
    visiblePages() {
      const pages = [];
      const half = Math.floor(this.maxVisiblePages / 2);
      let start = Math.max(1, this.currentPage - half);
      let end = Math.min(this.totalPages, start + this.maxVisiblePages - 1);

      if (end - start + 1 < this.maxVisiblePages) {
        start = Math.max(1, end - this.maxVisiblePages + 1);
      }

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      return pages;
    },
    displayedCategories() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.categories.slice(start, end);
    },
  },

  methods: {
    async fetchCategories() {
      try {
        const config = useRuntimeConfig();
        const response = await fetch(`${config.public.apiBase}/api/categories/`);
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
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
  mounted() {
    this.fetchCategories();
  },
};
</script>
