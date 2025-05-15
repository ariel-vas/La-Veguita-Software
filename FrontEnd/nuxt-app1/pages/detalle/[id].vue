<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Detalle del Producto</h1>

    <div v-if="producto" class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl space-y-4">
      <p><strong>Código:</strong> {{ producto.id_product }}</p>
      <p><strong>Nombre:</strong> {{ producto.name }}</p>
      <p><strong>Descripción:</strong> {{ producto.description }}</p>
      <p><strong>Categoría:</strong> {{ producto.category }}</p>
      <p><strong>Proveedor:</strong> {{ producto.supplier }}</p>
      
      <div>
        <strong>Subcategorías:</strong>
        <ul class="list-disc list-inside">
          <li v-for="(sub, idx) in producto.subcategories" :key="idx">{{ sub }}</li>
        </ul>
      </div>

      <p><strong>Precio compra:</strong> ${{ producto.purchase_price }}</p>
      <p><strong>Precio venta por unidad:</strong> ${{ producto.sale_price_unit }}</p>
      <p><strong>Precio venta por kilo:</strong> ${{ producto.sale_price_kilo }}</p>
      <p><strong>Precio por mayoreo:</strong> ${{ producto.wholesale_price }} (mínimo {{ parseInt(producto.wholesale_quantity) }})</p>
      <p><strong>Descuento / Recargo:</strong> ${{ producto.discount_surcharge }}</p>
      <p><strong>Stock disponible:</strong> {{ producto.stock }} {{ producto.stock_unit }}</p>
      <p><strong>Stock crítico:</strong> {{ producto.critical_stock }} {{ producto.stock_unit }}</p>
      <p><strong>Producto compuesto:</strong> {{ producto.composed_product ? 'Sí' : 'No' }}</p>
    </div>

    <div v-else class="text-gray-600 text-lg">Cargando producto...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const producto = ref(null)
const route = useRoute()
const id = route.params.id

onMounted(async () => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/products/${id}`)
    if (!res.ok) throw new Error('Producto no encontrado')
    producto.value = await res.json()
  } catch (error) {
    console.error('Error al cargar producto:', error)
  }
})
</script>
