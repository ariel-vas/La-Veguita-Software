<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a] sm:mb-4 md:mb-6 lg:mb-10">Búsqueda y Listado de Productos</h1>
    <h2 class="text-2xl font-semibold text-[#8bc34a] mb-6">Ingresa el ID del producto</h2>

    <!-- Input de búsqueda -->
    <div class="flex flex-col items-center gap-4 mb-6 w-full max-w-sm">
      <input
        v-model="searchQuery"
        type="number"
        placeholder="Buscar producto por ID..."
        class="p-3 w-full text-lg border-2 border-[#8bc34a] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#8bc34a] text-[#000000]"
      />
      <button
        @click="search"
        class="bg-[#ff9800] text-white py-2 px-2 sm:px-4 md:px-6 lg:px-8 rounded-xl text-lg hover:bg-opacity-90 transition duration-300 w-full"
      >
        Buscar
      </button>
    </div>

    <!-- Tabla con listado -->
    <table class="min-w-full bg-white rounded-xl shadow overflow-hidden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">ID</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Nombre</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Precio</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Unidad de Venta</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Acción</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prod in displayedProducts" :key="prod.id_product" class="border-b hover:bg-[#f0f8e9]">
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">{{ prod.id_product }}</td>
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">{{ prod.name }}</td>
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">${{ prod.exit_stock_unit === 'unit'
                                  ? Number(prod.sale_price_unit)
                                  : Number(prod.sale_price_kilo)}}</td>
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">
              {{ prod.exit_stock_unit === 'unit' ? 'Unidad' : 'Kilo' }}
          </td>
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">
            <button
              @click="navigateToPage(prod.id_product)"
              class="bg-[#ff9800] text-white py-1 px-2 sm:px-3 md:px-4 lg:px-5 rounded-xl hover:bg-opacity-90 transition duration-300"
            >
              Ver detalle
            </button>
          </td>
        </tr>
        <tr v-if="displayedProducts.length === 0">
          <td colspan="4" class="text-center py-4 text-gray-500">No hay productos para mostrar.</td>
        </tr>
      </tbody>
    </table>

    <!-- Mensaje de error -->
    <div v-if="error" class="text-2xl font-semibold text-red-600 mt-6">{{ error }}</div>
  <button
    @click="$router.push('/')"
    class="bg-[#ff9800] text-white py-2 px-2 sm:px-4 md:px-6 lg:px-8 rounded-xl text-lg hover:bg-opacity-90 transition duration-300 "
  >
    Volver atrás
  </button>
</div>
  
</template>

<script>

export default {
  data() {
    return {
      searchQuery: '',
      products: [],
      product: null,
      error: '',
    };
  },
  computed: {
    displayedProducts() {
      // Si hay producto encontrado por búsqueda, mostrar solo ese, si no los primeros 20 productos
      if (this.product) return [this.product];
      return this.products.slice(0, 20);
    },
  },
  methods: {
    async fetchProducts() {
      try {
        const config = useRuntimeConfig();
        const response = await fetch(`${config.public.apiBase}/api/products/`);
        if (!response.ok) throw new Error('Error cargando productos');
        const data = await response.json();
        this.products = data;
      } catch (err) {
        this.error = err.message;
      }
    },
    async search() {
      this.error = '';
      this.product = null;

      if (String(this.searchQuery).trim() === '') {
        this.error = 'Por favor ingresa un ID válido.';
        return;
      }

      try {
        const config = useRuntimeConfig();
        const response = await fetch(`${config.public.apiBase}/api/products/${this.searchQuery}`);
        if (!response.ok) throw new Error('Producto no encontrado');
        const data = await response.json();
        this.product = data;
      } catch (err) {
        this.error = err.message;
      }
    },
    navigateToPage(id) {
      this.$router.push({ path: `/detalle/${id}` });
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>
