<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Listado de Proveedores</h1>

    <button
      @click="$router.push('/crearproveedor/')"
      class="bg-blue-600 text-white py-2 px-4 rounded-lg text-base hover:bg-blue-700 transition"
    >
      + Agregar Proveedor
    </button>

    <table class="bg-white rounded-xl shadow overflow-hidden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th class="text-left py-3 px-6">Nombre</th>
          <th class="text-left py-3 px-6">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="supplier in displayedSuppliers"
          :key="supplier.id_supplier"
          class="border-b hover:bg-[#f0f8e9]"
        >
          <td class="py-3 px-6">{{ supplier.name }}</td>
          <td class="py-3 px-6">
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

    <div v-if="error" class="text-2xl font-semibold text-red-600 mt-6">{{ error }}</div>

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
      suppliers: [],
      error: '',
    };
  },
  computed: {
    displayedSuppliers() { 
      return this.suppliers.slice(0, 20);
    },
  },
  methods: {
    async fetchSuppliers() { 
      try {
        const config = useRuntimeConfig();
        // Endpoint para obtener proveedores
        const response = await fetch(`${config.public.apiBase}/api/suppliers/`);
        if (!response.ok) throw new Error('Error cargando proveedores'); // Mensaje de error
        const data = await response.json();
        this.suppliers = data; // Asigna los datos a 'suppliers'
      } catch (err) {
        this.error = err.message;
      }
    },
    navigateToPage(id_supplier) { 
      // Ruta para ver los detalles de un proveedor. Necesitarás crear esta página también.
      this.$router.push({ path: `/detalleProveedor/${id_supplier}` });
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