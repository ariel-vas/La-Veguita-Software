<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Salida Manual de Stock</h1>
    <h2 class="text-2xl font-semibold text-[#8bc34a] mb-6">Busca productos por ID y descuenta stock</h2>

    <div class="flex flex-col items-center gap-4 mb-6 w-full max-w-sm">
      <input
        v-model="searchId"
        type="text"
        placeholder="Buscar por ID de producto o nombre..."
        class="p-3 w-full text-lg border-2 border-[#8bc34a] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#8bc34a]"
      />
    </div>

    <table class="min-w-full bg-white rounded-xl shadow overflow-hidden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th colspan="2" class="text-left py-3 px-6">
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
          <th colspan="2" class="text-left py-3 px-6">
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
          <th class="text-left py-3 px-6">ID</th>
          <th class="text-left py-3 px-6">Nombre</th>
          <th class="text-left py-3 px-6">Stock Actual</th>
          <th class="text-left py-3 px-6">Quitar Stock</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prod in displayedProducts" :key="prod.id_product" class="border-b hover:bg-[#f0f8e9]">
          <td class="py-3 px-6">{{ prod.id_product }}</td>
          <td class="py-3 px-6">{{ prod.description }}</td>

          <td class="py-3 px-6">
            {{ prod.exit_stock_unit === 'kilo' ? parseFloat(prod.stock).toFixed(3) : parseInt(prod.stock) }}
            <span class="text-sm text-gray-600 ml-1">
              ({{ prod.exit_stock_unit === 'unit' ? 'Unidades' : 'Kilos' }})
            </span>
          </td>

          <td class="py-3 px-6">
            <input
              :value="prod.stockToRemove"
              @input="validateStockRemoveInput($event, prod)"
              type="number"
              :step="prod.exit_stock_unit === 'unit' ? '1' : '0.01'"
              :min="prod.exit_stock_unit === 'unit' ? '1' : '0.01'"
              class="w-24 p-1 border border-[#8bc34a] rounded mr-2"
              placeholder="Cant."
            />
            <button
              @click="removeStock(prod)"
              class="bg-[#ff9800] text-white py-1 px-4 rounded hover:bg-opacity-90 transition"
            >
              Quitar
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
      searchId: '',
      products: [],
      allProducts: [], // Store all fetched products here
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

      // Filter by searchId (and description) first
      if (this.searchId) {
        filtered = filtered.filter(
          (p) => p.id_product.toString().includes(this.searchId.trim()) ||
                 p.description.toLowerCase().includes(this.searchId.toLowerCase().trim())
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
    async removeStock(product) {
      // Use parseFloat consistently for numerical comparison
      const currentStock = parseFloat(product.stock);
      const quantityToRemove = parseFloat(product.stockToRemove);

      if (quantityToRemove > 0 && currentStock >= quantityToRemove) {
        try {
          const nuevoStock = currentStock - quantityToRemove;

          const updatedProduct = {
            ...product,
            stock: nuevoStock.toFixed(4), // Maintain precision
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

          // Find the product in allProducts and update its stock reactively
          const index = this.allProducts.findIndex(p => p.id_product === product.id_product);
          if (index !== -1) {
            this.allProducts[index].stock = nuevoStock.toFixed(4);
            this.allProducts[index].stockToRemove = 0; // Reset stockToRemove after successful update
          }
          
          alert(`Stock actualizado correctamente para ${product.description}`);
        } catch (error) {
          console.error('Error al remover stock:', error);
          alert('Error al actualizar el stock');
        }
      } else {
        // More specific error message
        if (quantityToRemove <= 0) {
          alert('Ingresa una cantidad válida mayor que cero para quitar.');
        } else {
          alert('No puedes quitar más stock del disponible.');
        }
      }
    },
    validateStockRemoveInput(event, prod) {
        let value = event.target.value;
        let numericValue;

        if (prod.exit_stock_unit === 'unit') {
            // Only allow integers for 'unit'
            numericValue = parseInt(value);
            if (isNaN(numericValue) || numericValue < 0) {
                numericValue = 0;
            }
        } else {
            // Allow decimals for 'kilo', ensure max 2 decimal places
            value = value.replace(/[^0-9.]/g, ''); // Keep only numbers and one dot
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join(''); // Handle multiple dots by taking first part and combining rest
            }
            if (parts[1] && parts[1].length > 2) {
                value = parts[0] + '.' + parts[1].slice(0, 2); // Limit to 2 decimal places
            }
            numericValue = parseFloat(value);
            if (isNaN(numericValue) || numericValue < 0) {
                numericValue = 0;
            }
        }

        // Ensure stockToRemove does not exceed current stock
        const currentStock = parseFloat(prod.stock);
        if (numericValue > currentStock) {
            numericValue = currentStock;
        }

        // Update the data model
        prod.stockToRemove = numericValue;
        
        // This ensures the input field visually reflects the corrected value in real-time.
        // It's important for user experience, especially when clipping values (e.g., trying to enter more than available stock).
        event.target.value = numericValue === 0 ? '' : String(numericValue); 
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