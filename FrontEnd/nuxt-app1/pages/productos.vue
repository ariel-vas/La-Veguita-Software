<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
    <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold text-[#8bc34a]">Búsqueda y Listado de Productos</h1>
    
    <div class="flex flex-col sm:flex-row sm:items-end gap-4 mb-6 w-full max-w-2xl">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar producto por ID o por Nombre..."
        class="p-3 w-full text-lg border-2 border-[#8bc34a] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#8bc34a] text-[#000000]"
      />
    </div>


  <div class="w-full overflow-x-auto rounded-xl shadow">

      <table class="min-w-full bg-white rounded-xl shadow overflow-hidden">
        <thead class="bg-[#8bc34a] text-white">
          <tr>
            <th colspan="2" class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">
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
            <th colspan="1"></th>
            <th colspan="3" class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">
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
            <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">ID</th>
            <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Nombre</th>
            <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Precio</th>
            <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Stock</th>
            <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Acción</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="prod in displayedProducts" :key="prod.id_product" class="border-b hover:bg-[#f0f8e9]">
            <td class="py-3 px-2 sm:px-4 md:px-6 xl:px-8">{{ prod.id_product }}</td>
            <td class="py-3 px-2 sm:px-4 md:px-6 xl:px-8 max-w-[200px] truncate whitespace-nowrap overflow-hidden">{{ prod.description }}</td>
            <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">${{ prod.exit_stock_unit === 'unit'
                                    ? Number(prod.sale_price).toFixed(2)
                                    : Number(prod.sale_price).toFixed(2)}}</td>
            <td class="py-3 px-2 sm:px-4 md:px-6 xl:px-8">
              {{ prod.exit_stock_unit === 'kilo' ? parseFloat(prod.stock).toFixed(3) : parseInt(prod.stock) }}
              <span class="text-sm text-gray-600 ml-1">
                ({{ prod.exit_stock_unit === 'unit' ? 'Unidades' : 'Kilos' }})
              </span>
            </td>
            
            <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">
              <button
                @click="navigateToPage(String(prod.id_product))"
                class="bg-[#ff9800] text-white py-1 px-2 sm:px-3 md:px-4 lg:px-5 rounded-xl hover:bg-opacity-90 transition duration-300"
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
  </div>
  <div class="flex flex-col items-center gap-2 mt-6">
    <div class="text-gray-600 font-medium">
      Mostrando {{ currentRange }} de {{ totalProducts }} productos
    </div>
    <div class="flex flex-wrap items-center justify-center gap-2">
      <!-- Ir al inicio -->
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
      <!-- Ir al final -->
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
      currentPage: 1,
      itemsPerPage: 20,
      maxVisiblePages: 5,
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

      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;

    return filtered.slice(start, end);
    },
    totalProducts() {
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

      return filtered.length;
    },
    totalPages() {
      return Math.ceil(this.totalProducts / this.itemsPerPage);
    },
    currentRange() {
      const start = (this.currentPage - 1) * this.itemsPerPage + 1;
      const end = Math.min(start + this.itemsPerPage - 1, this.totalProducts);
      return `${start}-${end}`;
    },
    filteredSubcategories() {
      const subcategoriesForSelectedCategory = this.allProducts
        .flatMap(p => p.subcategories);
      return [...new Set(subcategoriesForSelectedCategory)].filter(Boolean);
    },
    totalProducts() {
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

      return filtered.length;
    },
    totalPages() {
      return Math.ceil(this.totalProducts / this.itemsPerPage);
    },
    currentRange() {
      const start = (this.currentPage - 1) * this.itemsPerPage + 1;
      const end = Math.min(start + this.itemsPerPage - 1, this.totalProducts);
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
        const response = await fetch(`${config.public.apiBase}/api/products/${encodeURIComponent(this.searchQuery)}`);
        if (!response.ok) throw new Error('Producto no encontrado');
        const data = await response.json();
        this.product = data;
      } catch (err) {
        this.error = err.message;
      }
    },
    navigateToPage(id) {
      this.$router.push({ path: `/detalle/${encodeURIComponent(id)}` });
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>
