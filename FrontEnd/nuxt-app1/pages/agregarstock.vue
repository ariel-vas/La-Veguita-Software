<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Ingreso Manual de Stock</h1>
    <h2 class="text-2xl font-semibold text-[#8bc34a] mb-6">Busca productos por ID y agrega stock</h2>

    <!-- Búsqueda por ID -->
    <div class="flex flex-col items-center gap-4 mb-6 w-full max-w-sm">
      <input
        v-model="searchId"
        type="text"
        placeholder="Buscar por ID de producto..."
        class="p-3 w-full text-lg border-2 border-[#8bc34a] rounded-xl focus:outline-none focus:ring-2 focus:ring-[#8bc34a]"
      />

      <!--<button
        @click="search"
        class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300 w-full"
      >
        Buscar
      </button>-->
      
    </div>

    <!-- Tabla con resultados -->
    <table class="min-w-full bg-white rounded-xl shadow overflow-hidden">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th class="text-left py-3 px-6">ID</th>
          <th class="text-left py-3 px-6">Nombre</th>
          <th class="text-left py-3 px-6">Stock Actual</th>
          <th class="text-left py-3 px-6">Agregar Stock</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prod in displayedProducts" :key="prod.id_product" class="border-b hover:bg-[#f0f8e9]">
          <td class="py-3 px-6">{{ prod.id_product }}</td>
          <td class="py-3 px-6">{{ prod.name }}</td>
          <td class="py-3 px-6">{{ parseFloat(prod.stock).toFixed(2) }}</td>
          <td class="py-3 px-6">
            <input
              v-model.number="prod.stockToAdd"
              type="number"
              min="1"
              class="w-24 p-1 border border-[#8bc34a] rounded mr-2"
              placeholder="Cant."
            />
            <button
              @click="addStock(prod)"
              class="bg-[#ff9800] text-white py-1 px-4 rounded hover:bg-opacity-90 transition"
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
        return this.products.filter(
          (p) => p.id_product.toString().includes(this.searchId.trim())
        );
      }
      return this.products.slice(0, 20);
    },
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/products/');
        if (!response.ok) throw new Error('Error cargando productos');
        const data = await response.json();
        this.products = data.map((p) => ({ ...p, stockToAdd: 0 }));
      } catch (err) {
        this.error = err.message;
      }
    },
    search() {
      // El filtrado se realiza en el computed
    },
    async addStock(product) {
      if (product.stockToAdd > 0) {
        try {
          const nuevoStock = parseFloat(product.stock) + product.stockToAdd;

          const updatedProduct = {
            ...product,
            stock: nuevoStock.toFixed(4),
          };

          const response = await fetch(`http://127.0.0.1:8000/api/products/${product.id_product}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedProduct),
          });

          if (!response.ok) throw new Error('Error al actualizar el stock');

          product.stock = nuevoStock.toFixed(4);
          product.stockToAdd = 0;
          alert(`Stock actualizado correctamente para ${product.name}`);
        } catch (error) {
          console.error(error);
          alert('Error al actualizar el stock');
        }
      } else {
        alert('Ingresa una cantidad válida');
      }
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>
