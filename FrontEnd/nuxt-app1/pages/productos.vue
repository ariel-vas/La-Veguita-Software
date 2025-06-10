<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Búsqueda y Listado de Productos</h1>
    
    <div class="flex flex-col items-center gap-4 mb-6 w-full max-w-sm">
      <input
        v-model="searchQuery"
        type="number"
        placeholder="Buscar producto por ID..."
        class="p-3 w-full text-lg border-2 border-[#8bc34a] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#8bc34a] text-[#000000]"
      />
      <button
        @click="search"
        class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300 w-full"
      >
        Buscar
      </button>
    </div>

    <table class="min-w-full bg-white rounded-xl shadow overflow-hidden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th colspan="3" class="text-left py-3 px-6">
            <label class="block text-white font-semibold mb-2">Filtrar por Categoría</label>
            <select 
              v-model="selectedCategory"
              @change="applyFilters"
              class="p-2 w-full text-base border-2 border-white rounded-xl focus:outline-none focus:ring-2 focus:ring-white text-black"
            >
              <option value="">Todas las categorías</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </th>
          <th colspan="3" class="text-left py-3 px-6">
            <label class="block text-white font-semibold mb-2">Filtrar por Subcategoría</label>
            <select 
              v-model="selectedSubcategory"
              @change="applyFilters"
              class="p-2 w-full text-base border-2 border-white rounded-xl focus:outline-none focus:ring-2 focus:ring-white text-black"
              
            >
              <option value="">Todas las subcategorías</option>
              <option v-for="subcat in filteredSubcategories" :key="subcat" :value="subcat">
                {{ subcat }}
              </option>
            </select>
          </th>
        </tr>
        <tr>
          <th class="text-left py-3 px-6">ID</th>
          <th class="text-left py-3 px-6">Nombre</th>
          <th class="text-left py-3 px-6">Precio</th>
          <th class="text-left py-3 px-6">Stock</th>
          <th class="text-left py-3 px-6">Unidad de Venta</th>
          <th class="text-left py-3 px-6">Acción</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prod in displayedProducts" :key="prod.id_product" class="border-b hover:bg-[#f0f8e9]">
          <td class="py-3 px-6">{{ prod.id_product }}</td>
          <td class="py-3 px-6">{{ prod.description }}</td>
          <td class="py-3 px-6">${{ prod.exit_stock_unit === 'unit'
                                  ? Number(prod.sale_price).toFixed(2)
                                  : Number(prod.sale_price).toFixed(2)}}</td>
          <td class="py-3 px-6">
            {{ prod.exit_stock_unit === 'kilo' ? parseFloat(prod.stock).toFixed(3) : parseInt(prod.stock) }}
          </td>
          <td class="py-3 px-6">
              {{ prod.exit_stock_unit === 'unit' ? 'Unidad' : 'Kilo' }}
          </td>
          
          <td class="py-3 px-6">
            <button
              @click="navigateToPage(prod.id_product)"
              class="bg-[#ff9800] text-white py-1 px-4 rounded-xl hover:bg-opacity-90 transition duration-300"
            >
              Ver detalle
            </button>
          </td>
        </tr>
        <tr v-if="displayedProducts.length === 0">
          <td colspan="6" class="text-center py-4 text-gray-500">No hay productos para mostrar.</td>
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
      searchQuery: '',
      searchId: '',
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
      if (this.product) return [this.product];

      let filtered = this.allProducts;

      if (this.selectedCategory) {
        filtered = filtered.filter(p => p.category === this.selectedCategory);
      }
      
      if (this.selectedSubcategory) {
        filtered = filtered.filter(p => p.subcategories?.includes(this.selectedSubcategory));
      }
      return filtered.slice(0, 20);
    },
    filteredSubcategories() {
      const subcategoriesForSelectedCategory = this.allProducts
        .flatMap(p => p.subcategories);
      return [...new Set(subcategoriesForSelectedCategory)].filter(Boolean);
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
      this.categories = [...new Set(this.allProducts.map(p => p.category))].filter(Boolean);
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
      this.$router.push({ path: `/detalle/${id}` });
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>
