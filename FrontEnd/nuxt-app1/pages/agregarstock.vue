<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 pt-0 mt-16">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a]">Ingreso Manual de Stock</h1>
    <h2 class="text-xl sm:text-2xl md:text-3xl lg:text-4xl font-bold text-[#8bc34a] mb-6">Busca productos por ID y agrega stock</h2>

    <div class="flex flex-col items-center gap-4 mb-6 w-full max-w-sm">
      <input
        v-model="searchId"
        type="text"
        placeholder="Buscar por ID de producto..."
        class="p-3 w-full text-lg border-2 border-[#8bc34a] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#8bc34a]"
      />
      </div>

    <table class="min-w-full bg-white rounded-xl shadow overflow-hidden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th colspan="2" class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">
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
          <th colspan="2" class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">
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
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">ID</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Nombre</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Stock Actual</th>
          <th class="text-left py-3 px-2 sm:px-4 md:px-6 lg:px-8">Agregar Stock</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="prod in displayedProducts"
          :key="prod.id_product"
          class="border-b hover:bg-[#f0f8e9]"
        >
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">{{ prod.id_product }}</td>
          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">{{ prod.description }}</td>

          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">
            {{ prod.exit_stock_unit === 'kilo' ? parseFloat(prod.stock).toFixed(3) : parseInt(prod.stock) }}
            <span class="text-sm text-gray-600 ml-1">
              ({{ prod.exit_stock_unit === 'unit' ? 'Unidades' : 'Kilos' }})
            </span>
          </td>

          <td class="py-3 px-2 sm:px-4 md:px-6 lg:px-8">
            <input
              :value="prod.stockToAdd"
              @input="validateStockInput($event, prod)"
              type="number"
              :step="prod.exit_stock_unit === 'unit' ? '1' : '0.01'"
              :min="prod.exit_stock_unit === 'unit' ? '1' : '0.01'"
              class="w-24 p-1 border border-[#8bc34a] rounded mr-2"
              placeholder="Cant."
            />

            <button
              @click="addStock(prod)"
              class="bg-[#ff9800] text-white py-1 px-2 sm:px-4 md:px-6 lg:px-8 rounded hover:bg-opacity-90 transition"
            >
              Agregar
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
      searchId: '',
      products: [],
      allProducts: [], // To store all fetched products for filtering
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

      // Filter by searchId first
      if (this.searchId) {
        filtered = filtered.filter(
          (p) => p.id_product.toString().includes(this.searchId.trim()) ||
                 p.description.toLowerCase().includes(this.searchId.toLowerCase().trim()) // Added search by description
        );
      }

      // Then apply category filter
      if (this.selectedCategory) {
        filtered = filtered.filter(p => p.category === this.selectedCategory);
      }
      
      // Then apply subcategory filter
      if (this.selectedSubcategory) {
        filtered = filtered.filter(p => p.subcategories?.includes(this.selectedSubcategory));
      }
      return filtered.slice(0, 20); // Limit to 20 products
    },
    filteredSubcategories() {
      // This will return all unique subcategories from all products to allow independent filtering.
      // If you want subcategories to be dependent on the selected category,
      // uncomment the `if (!this.selectedCategory) return [];` line below
      // and adjust the filter accordingly.
      
      // if (!this.selectedCategory) return []; 

      const subcategoriesForSelectedCategory = this.allProducts
        // .filter(p => p.category === this.selectedCategory) // Uncomment this line if you want dependency
        .flatMap(p => p.subcategories || []);
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
        // Initialize stockToRemove for each product
        this.allProducts = data.map((p) => ({ ...p, stockToRemove: 0 })); 
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
      // The computed property `displayedProducts` handles filtering automatically
      // when selectedCategory or selectedSubcategory changes.
      // Resetting searchId if filters are applied, for a cleaner experience
      this.searchId = ''; 
    },
    // The search method is no longer strictly necessary as filtering is reactive
    // but can be kept if you have specific search button logic.
    search() {
      // The filtering is now handled reactively by the computed property `displayedProducts`
      // based on changes in `searchId`.
    },
    async addStock(product) {
      if (product.stockToAdd > 0) {
        try {
          const nuevoStock = parseFloat(product.stock) + product.stockToAdd;

          const updatedProduct = {
            ...product,
            stock: nuevoStock.toFixed(4),
          };
          const config = useRuntimeConfig();
          const response = await fetch(`${config.public.apiBase}/api/products/${product.id_product}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedProduct),
          });

          if (!response.ok) throw new Error('Error al actualizar el stock');

          // Find the product in allProducts and update its stock
          const index = this.allProducts.findIndex(p => p.id_product === product.id_product);
          if (index !== -1) {
            this.allProducts[index].stock = nuevoStock.toFixed(4);
            this.allProducts[index].stockToAdd = 0; // Reset stockToAdd after successful update
          }
          
          alert(`Stock actualizado correctamente para ${product.description}`);
        } catch (error) {
          console.error(error);
          alert('Error al actualizar el stock');
        }
      } else {
        alert('Ingresa una cantidad válida');
      }
    },
    validateStockInput(event, prod) {
      let value = event.target.value;

      if (prod.exit_stock_unit === 'unit') {
        value = value.replace(/\D/g, ''); 
        prod.stockToAdd = parseInt(value) || 0;
      } else {
        value = value.replace(/[^0-9.]/g, '');
        const parts = value.split('.');
        if (parts.length > 2) {
          value = parts[0] + '.' + parts.slice(1).join('');
        }
        if (parts[1] && parts[1].length > 2) {
          value = parts[0] + '.' + parts[1].slice(0, 2);
        }
        prod.stockToAdd = parseFloat(value) || 0;
      }
      event.target.value = prod.stockToAdd === 0 ? '' : prod.stockToAdd; // Update input field
    }
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>

<style scoped>
/* No changes needed in styles based on the request */
</style>