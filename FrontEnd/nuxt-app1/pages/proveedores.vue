<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
    <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold text-[#8bc34a] sm:mb-4 md:mb-8 lg:mb-10">Listado de Proveedores</h1>

    <button
      @click="$router.push('/crearproveedor/')"
      class="bg-blue-600 text-white py-2 px-4 rounded-lg text-base hover:bg-blue-700 transition"
    >
      + Agregar Proveedor
    </button>

    <table class="bg-white rounded-xl shadow overflow-hidden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Nombre</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="supplier in displayedSuppliers"
          :key="supplier.id_supplier"
          class="border-b hover:bg-[#f0f8e9]"
        >
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">{{ supplier.name }}</td>
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">
            <button
              @click="navigateToPage(supplier.id_supplier)"
              class="bg-[#8bc34a] text-white px-4 py-1 rounded hover:bg-[#7cb342] transition"
            >
              Ver Detalles
            </button>
          </td>
        </tr>
        <tr v-if="displayedSuppliers.length === 0">
          <td colspan="2" class="text-center py-4 text-gray-500">
            No hay proveedores para mostrar.
          </td>
        </tr>
      </tbody>
    </table>
    <!-- Paginación -->
    <div class="flex flex-col items-center gap-2 mt-6">
      <div class="text-gray-600 font-medium">
        Mostrando {{ currentRange }} de {{ suppliers.length }} proveedores
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
          :key="page"
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

    <div v-if="error" class="text-2xl font-semibold text-red-600 mt-6">{{ error }}</div>

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
      suppliers: [],
      error: '',
      currentPage: 1,
      itemsPerPage: 20,
      maxVisiblePages: 5,
    };
  },

  computed: {
    displayedSuppliers() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.suppliers.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.suppliers.length / this.itemsPerPage);
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
    currentRange() {
      const start = (this.currentPage - 1) * this.itemsPerPage + 1;
      const end = Math.min(start + this.itemsPerPage - 1, this.suppliers.length);
      return `${start}-${end}`;
    },
  },

  methods: {
    async fetchSuppliers() { 
      try {
        const config = useRuntimeConfig();
        const response = await fetch(`${config.public.apiBase}/api/suppliers/`);
        if (!response.ok) throw new Error('Error cargando proveedores');
        const data = await response.json();
        this.suppliers = data;
      } catch (err) {
        this.error = err.message;
      }
    },
    navigateToPage(id_supplier) { 
      this.$router.push({ path: `/detalleProveedor/${id_supplier}` });
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },

  mounted() {
    this.fetchSuppliers(); // Llama a la nueva función al montar el componente
  },
};
</script>

<style scoped>
/* Puedes mantener los estilos existentes ya que la estructura HTML es similar */
</style>