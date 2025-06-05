<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Salida Manual de Stock</h1>
    <h2 class="text-2xl font-semibold text-[#8bc34a] mb-6">Busca productos por ID y descuenta stock</h2>

    <!-- Búsqueda por ID -->
    <div class="flex flex-col items-center gap-4 mb-6 w-full max-w-sm">
      <input
        v-model="searchId"
        type="text"
        placeholder="Buscar por ID de producto..."
        class="p-3 w-full text-lg border-2 border-[#8bc34a] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#8bc34a]"
      />
    </div>

    <!-- Tabla con resultados -->
    <table class="min-w-full bg-white rounded-xl shadow overflow-hidden">
      <thead class="bg-[#8bc34a] text-white">
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
          <td class="py-3 px-6">{{ prod.name }}</td>

          <!-- Stock actual con tipo de unidad -->
          <td class="py-3 px-6">
            {{ prod.exit_stock_unit === 'kilo' ? parseFloat(prod.stock).toFixed(3) : parseInt(prod.stock) }}
            <span class="text-sm text-gray-600 ml-1">
              ({{ prod.exit_stock_unit === 'unit' ? 'Unidades' : 'Kilos' }})
            </span>
          </td>

          <!-- Input con validación -->
          <td class="py-3 px-6">
            <input
              :value="prod.stockToRemove"
              @input="validateStockRemoveInput($event, prod)"
              type="number"
              :step="prod.exit_stock_unit === 'unit' ? '1' : '0.01'"
              :min="prod.exit_stock_unit === 'unit' ? '1' : '0.01'"
              :max="parseFloat(prod.stock)"
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

    <!-- Error -->
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
      error: '',
    };
  },
  computed: {
    displayedProducts() {
      if (this.searchId) {
        return this.products.filter((p) =>
          p.id_product.toString().includes(this.searchId.trim())
        );
      }
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
        this.products = data.map((p) => ({ ...p, stockToRemove: 0 }));
      } catch (err) {
        this.error = err.message;
      }
    },
    async removeStock(product) {
      if (product.stockToRemove > 0 && parseFloat(product.stock) >= product.stockToRemove) {
        try {
          const nuevoStock = parseFloat(product.stock) - product.stockToRemove;

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

          product.stock = nuevoStock.toFixed(4);
          product.stockToRemove = 0;
          alert(`Stock actualizado correctamente para ${product.name}`);
        } catch (error) {
          console.error(error);
          alert('Error al actualizar el stock');
        }
      } else {
        alert('Cantidad inválida para quitar');
      }
    },
    validateStockRemoveInput(event, prod) {
      let value = event.target.value;

      if (prod.exit_stock_unit === 'unit') {
        // Solo permitir enteros positivos
        value = value.replace(/\D/g, '');
        prod.stockToRemove = parseInt(value) || 0;
      } else {
        // Permitir decimales con hasta 2 cifras
        value = value.replace(/[^0-9.]/g, '');
        const parts = value.split('.');
        if (parts.length > 2) return;
        if (parts[1]?.length > 2) parts[1] = parts[1].slice(0, 2);
        prod.stockToRemove = parseFloat(parts.join('.')) || 0;
      }
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>
