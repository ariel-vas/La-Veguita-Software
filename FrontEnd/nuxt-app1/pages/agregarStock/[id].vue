<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 mt-0">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Editar Producto</h1>

    <div v-if="producto" class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl space-y-6">
        <!-- Campos no editables -->
        <div v-for="campo in camposEditables" :key="campo.key" class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-start">
            <label class="font-semibold">{{ campo.label }}:</label>
            <input
            v-model="editado[campo.key]"
            :type="campo.type || 'text'"
            class="border border-gray-200 bg-gray-100 text-gray-600 rounded px-3 py-1 w-full sm:col-span-2"
            :readonly="true"
            disabled
            />
        </div>

        <!-- Sección para agregar lote -->
        <div class="border-t pt-4 mt-4 space-y-4">
            <h3 class="text-xl font-semibold text-gray-700">Agregar nuevo lote</h3>

            <!-- Campo: Cantidad a agregar -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-center">
            <label class="font-semibold">Cantidad a agregar:</label>
            <input
                v-model="cantidadAgregar"
                type="number"
                min="1"
                class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2"
                placeholder="Cantidad"
            />
            </div>

            <!-- Selector de modo de vencimiento -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-center">
              <label class="font-semibold">Tipo de vencimiento:</label>
              <select
                v-model="modoVencimiento"
                class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2"
              >
                <option value="fecha">Fecha específica</option>
                <option value="semanas">Cantidad de semanas</option>
                <option value="dias">Cantidad de días</option>
                <option value="nunca">Sin vencimiento</option>
              </select>
            </div>

            <!-- Campo: Fecha manual -->
            <div
              v-if="modoVencimiento === 'fecha'"
              class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-center"
            >
              <label class="font-semibold">Fecha de vencimiento:</label>
              <input
                v-model="fechaVencimiento"
                type="date"
                class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2"
              />
            </div>

            <!-- Campo: Cantidad de semanas -->
            <div
              v-if="modoVencimiento === 'semanas'"
              class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-center"
            >
              <label class="font-semibold">Semanas hasta vencimiento:</label>
              <input
                v-model="semanasInput"
                type="number"
                min="1"
                class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2"
                placeholder="Ej: 4 semanas"
              />
            </div>
            <!-- Campo: Cantidad de días -->
            <div
              v-if="modoVencimiento === 'dias'"
              class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-center"
            >
              <label class="font-semibold">Días hasta vencimiento:</label>
              <input
                v-model="diasInput"
                type="number"
                min="1"
                class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2"
                placeholder="Ej: 30 días"
              />
            </div>

            <!-- Info para "nunca" -->
            <div
              v-if="modoVencimiento === 'nunca'"
              class="text-sm text-gray-500 sm:col-span-3 px-2 italic"
            >
              Vencimiento fijado a 100 años desde hoy.
            </div>


            <!-- Botón para agregar lote -->
            <div class="flex justify-center pt-4">
            <button
                @click="agregarLote"
                class="bg-[#8bc34a] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
            >
                Confirmar Agregado
            </button>
            </div>
        </div>
    </div>

    <div v-else class="text-gray-600 text-lg">Cargando producto...</div>

    <button
      @click="$router.push('/agregarlote')"
      class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300 mt-4"
    >
    Volver atras
    </button>
  </div> 
</template>
<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const producto = ref(null)
const editado = ref({})
const route = useRoute()
const router = useRouter()
const id = route.params.id

const cantidadAgregar = ref(0)
const fechaVencimiento = ref('')
const modoVencimiento = ref('fecha') // opciones: 'fecha', 'semanas', 'nunca'
const semanasInput = ref(0)
const diasInput = ref(0)

watch([modoVencimiento, semanasInput, diasInput], () => {
  const hoy = new Date()

  if (modoVencimiento.value === 'semanas') {
    hoy.setDate(hoy.getDate() + semanasInput.value * 7)
    fechaVencimiento.value = hoy.toISOString().slice(0, 10)
  } else if (modoVencimiento.value === 'dias') {
    hoy.setDate(hoy.getDate() + diasInput.value)
    fechaVencimiento.value = hoy.toISOString().slice(0, 10)
  } else if (modoVencimiento.value === 'nunca') {
    hoy.setFullYear(hoy.getFullYear() + 100)
    fechaVencimiento.value = hoy.toISOString().slice(0, 10)
  }
})


const camposBase = [
  { key: 'description', label: 'Nombre' },
  { key: 'stock', label: 'Stock disponible', type: 'number' },
  {
    key: 'exit_stock_unit',
    label: 'Unidad salida stock',
    type: 'select',
    options: [
      { label: 'Unidad', value: 'unit' },
      { label: 'Kilo', value: 'kilo' },
    ]
  },
]

const camposEditables = computed(() => {
  const precioSalida =
    editado.value.exit_stock_unit === 'kilo'
      ? { key: 'sale_price', label: 'Precio venta kilo', type: 'number' }
      : { key: 'sale_price', label: 'Precio venta unidad', type: 'number' }

  const insertIndex = camposBase.findIndex(c => c.key === 'exit_stock_unit') + 1
  const before = camposBase.slice(0, insertIndex)
  const after = camposBase.slice(insertIndex)

  return [...before, precioSalida, ...after]
})

onMounted(async () => {
  try {
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBase}/api/products/${id}`)
    if (!res.ok) throw new Error('Producto no encontrado')
    const data = await res.json()
    if (!Array.isArray(data.subcategories)) data.subcategories = []
    editado.value = { ...data }
    producto.value = data
  } catch (error) {
    console.error('Error al cargar producto:', error)
  }
})

const agregarLote = async () => {
  if (cantidadAgregar.value <= 0) {
    alert('La cantidad debe ser mayor que cero.')
    return
  }

  if (!fechaVencimiento.value) {
    alert('Por favor selecciona una fecha de vencimiento.')
    return
  }

  try {
    // 1. Crear el lote
    const lote = {
      product: producto.value.id_product,
      quantity: cantidadAgregar.value,
      starting_quantity: producto.value.stock,
      unit: producto.value.exit_stock_unit,
      entry_date: new Date().toISOString().slice(0, 10),
      expiration_date: fechaVencimiento.value,
    }
    const config = useRuntimeConfig();
    const resLote = await fetch(`${config.public.apiBase}/api/batches/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(lote),
    })

    if (!resLote.ok) throw new Error('Error al crear lote.')

    // 2. Actualizar el stock (PUT limpio)
    const nuevoStock = parseFloat(producto.value.stock) + parseFloat(cantidadAgregar.value)

    const productoActualizado = {
      id_product: producto.value.id_product,
      description: producto.value.description,
      purchase_price: producto.value.purchase_price,
      sale_price: producto.value.sale_price, // Usa uno de los dos según corresponda
      wholesale_price: producto.value.wholesale_price,
      wholesale_quantity: producto.value.wholesale_quantity,
      discount_surcharge: producto.value.discount_surcharge,
      stock: nuevoStock.toFixed(4),
      critical_stock: producto.value.critical_stock,
      entry_stock_unit: producto.value.entry_stock_unit,
      exit_stock_unit: producto.value.exit_stock_unit,
      composed_product: producto.value.composed_product,
      checked: false,
      category: producto.value.category,
      supplier: producto.value.supplier,
      subcategories: producto.value.subcategories.map(sc => {
          if (typeof sc === 'string') return sc
          if (sc.name) return sc.name
          return ''
      }).filter(Boolean),
    };
    const resProducto = await fetch(`${config.public.apiBase}/api/products/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(productoActualizado),
    })

    if (!resProducto.ok) throw new Error('Error al actualizar producto.')

    const actualizado = await resProducto.json()
    producto.value = actualizado
    editado.value = { ...actualizado }

    alert('Lote agregado y stock actualizado correctamente.')
    cantidadAgregar.value = 0
    fechaVencimiento.value = ''
  } catch (err) {
    console.error(err)
    alert('Ocurrió un error al agregar el lote o actualizar el stock.')
  }
}
</script>