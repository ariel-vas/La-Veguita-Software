<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 pt-0 mt-16">
    <h1 class="text-2xl sm:text-3xl md:text-4xl xl:text-5xl font-bold text-[#8bc34a]">Búsqueda y Listado de Productos</h1>
    <h2 class="text-xl sm:text-2xl md:text-3xl xl:text-4xl font-bold text-[#8bc34a] mb-6">Ingresa el ID del producto</h2>

    <div class="flex flex-col items-center gap-4 mb-6 w-full max-w-sm">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar producto por ID o por Nombre..."
        class="p-3 w-full text-lg border-2 border-[#8bc34a] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#8bc34a] text-[#000000]"
      />
      <!--<button
        @click="search"
        class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300 w-full"
      >
        Buscar
      </button>-->
    </div>

    <table class="min-w-full bg-white rounded-xl shadow overflow-hidden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th colspan="2" class="text-left py-3 px-2 sm:px-4 md:px-6 xl:px-8">
            <label class="block text-white font-semibold mb-2">Filtrar por Categoría</label>
            <select 
              v-model="selectedCategory"
              @change="applyFilters"
              class="p-2 w-full text-base border-2 border-white rounded-xl focus:outline-none focus:ring-2 focus:ring-white text-[#000000]"
            >
              <option value="">Todas las categorías</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </th>
          <th colspan="2" class="text-left py-3 px-2 sm:px-4 md:px-6 xl:px-8">
            <label class="block text-white font-semibold mb-2">Filtrar por Subcategoría</label>
            <select 
              v-model="selectedSubcategory"
              @change="applyFilters"
              class="p-2 w-full text-base border-2 border-white rounded-xl focus:outline-none focus:ring-2 focus:ring-white text-[#000000]"
              >
              <option value="">Todas las subcategorías</option>
              <option v-for="subcat in filteredSubcategories" :key="subcat" :value="subcat">
                {{ subcat }}
              </option>
            </select>
          </th>
        </tr>
        <tr>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 xl:px-8">ID</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 xl:px-8">Nombre</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 xl:px-8">Stock Actual</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 xl:px-8">Acción</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prod in displayedProducts" :key="prod.id_product" class="border-b hover:bg-[#f0f8e9]">
          <td class="py-3 px-2 sm:px-4 md:px-6 xl:px-8">{{ prod.id_product }}</td>
          <td class="py-3 px-2 sm:px-4 md:px-6 xl:px-8">{{ prod.description }}</td>
          <td class="py-3 px-2 sm:px-4 md:px-6 xl:px-8">
            {{ prod.exit_stock_unit === 'kilo' ? parseFloat(prod.stock).toFixed(3) : parseInt(prod.stock) }}
            <span class="text-sm text-gray-600 ml-1">
              ({{ prod.exit_stock_unit === 'unit' ? 'Unidades' : 'Kilos' }})
            </span>
          </td>
          <td class="py-3 px-2 sm:px-4 md:px-6 xl:px-8">
            <button
              @click="navigateToPage(prod.id_product)"
              class="bg-[#ff9800] text-white py-1 px-2 sm:px-3 md:px-4 xl:px-6 rounded-xl hover:bg-opacity-90 transition duration-300"
            >
              Ingresar Stock
            </button>
          </td>
        </tr>
        <tr v-if="displayedProducts.length === 0">
          <td colspan="4" class="text-center py-4 text-gray-500">No hay productos para mostrar.</td>
        </tr>
      </tbody>
    </table>

    <div v-if="error" class="text-2xl font-semibold text-red-600 mt-6">{{ error }}</div>
    <button
      @click="$router.push('/')"
      class="bg-[#ff9800] text-white py-2 px-4 sm:px-5 md:px-6 xl:px-8 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
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
      allProducts: [], // Store all fetched products here
      product: null,
      error: '',
      categories: [],
      subcategories: [],
      selectedCategory: '',
      selectedSubcategory: '',
    };
  },
  computed: {
    displayedProducts() {
      // If a product is found by search, display only that one
      if (this.product) return [this.product];

      // Otherwise, filter based on category and subcategory
      let filtered = this.allProducts;
      if (this.searchQuery.trim()) {
          const q = this.searchQuery.trim().toLowerCase();
          filtered = filtered.filter(p =>
            p.id_product.includes(q) || p.description.toLowerCase().includes(q)
          );
        }
      if (this.selectedCategory) {
        filtered = filtered.filter(p => p.category === this.selectedCategory);
      }
      
      if (this.selectedSubcategory) {
        filtered = filtered.filter(p => p.subcategories?.includes(this.selectedSubcategory));
      }
      return filtered.slice(0, 20); // Limit to 20 products
    },
    filteredSubcategories() {
      // This now returns all unique subcategories regardless of selectedCategory
      const allSubcategories = this.allProducts.flatMap(p => p.subcategories || []);
      return [...new Set(allSubcategories)].filter(Boolean);
    }
  },
  methods: {
    async fetchProducts() {
      try {
        const config = useRuntimeConfig();
        const response = await fetch(`${config.public.apiBase}/api/products/`);
        if (!response.ok) throw new Error('Error cargando productos');
        const data = await response.json();
        this.allProducts = data; // Store all products
        this.extractCategories();
      } catch (err) {
        this.error = err.message;
      }
    },
    extractCategories() {
      // Extract unique categories
      this.categories = [...new Set(this.allProducts.map(p => p.category))].filter(Boolean);
      
      // Extract unique subcategories
      const allSubcategories = this.allProducts.flatMap(p => p.subcategories || []);
      this.subcategories = [...new Set(allSubcategories)].filter(Boolean);
    },
    applyFilters() {
      // The computed property `displayedProducts` now handles the filtering logic
      // based on `selectedCategory` and `selectedSubcategory`.
      // No direct product fetching needed here, just ensure `product` is nullified
      this.product = null; 
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
      this.$router.push({ path: `/agregarStock/${id}` });
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>

<style scoped>
/* No changes needed in styles based on the request */
</style>