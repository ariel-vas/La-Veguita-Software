<template> 
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a] mb-5 sm:mb-4 md:mb-6 lg:mb-10">Crear Producto</h1>

    <div class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl space-y-6">
      <div
        v-for="campo in camposEditables"
        :key="campo.key"
        class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-start"
      >
        <label class="font-semibold">{{ campo.label }}:</label>

        <!-- Subcategorías como lista editable -->
        <div v-if="campo.key === 'subcategories'" class="sm:col-span-2 space-y-2">
          <div
            v-for="(subcat, index) in editado.subcategories"
            :key="index"
            class="flex gap-2 items-center"
          >
            <select
              v-model="editado.subcategories[index]"
              class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2"
            >
              <option disabled value="">Seleccionar subcategoría</option>
              <option
                v-for="subcatOpt in subcategoriasDisponibles.filter(opt => !editado.subcategories.includes(opt.name) || opt.name === subcat)"
                :key="subcatOpt.id"
                :value="subcatOpt.name"
              >
                {{ subcatOpt.name }}
              </option>
            </select>
            <button
              @click="eliminarSubcategoria(index)"
              class="text-red-600 hover:text-red-800 font-bold"
            >
              ✕
            </button>
          </div>
          <button
            @click="agregarSubcategoria"
            class="text-sm text-blue-600 hover:underline mt-1"
            :disabled="editado.subcategories.length >= subcategoriasDisponibles.length"
          >
            + Agregar subcategoría
          </button>
        </div>

        <!-- Categoría como lista desplegable -->
        <select
          v-else-if="campo.key === 'category'"
          v-model="editado.category"
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2"
        >
          <option disabled value="">Seleccionar categoría</option>
          <option v-for="cat in categoriasDisponibles" :key="cat.id" :value="cat.name">{{ cat.name }}</option>
        </select>

        <!-- Proveedor como lista desplegable -->
        <select
          v-else-if="campo.key === 'supplier'"
          v-model="editado.supplier"
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2"
        >
          <option disabled value="">Seleccionar proveedor</option>
          <option v-for="prov in proveedoresDisponibles" :key="prov.id" :value="prov.name">{{ prov.name }}</option>
        </select>

        <!-- Select para unidad de entrada y salida -->
        <select
          v-else-if="campo.key === 'entry_stock_unit' || campo.key === 'exit_stock_unit'"
          v-model="editado[campo.key]"
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2"
        >
          <option disabled value="">Seleccionar unidad</option>
          <option value="unit">Unidad</option>
          <option value="kilo">Kilo</option>
        </select>

        <!-- Checkbox para producto compuesto 
        <input
          v-else-if="campo.key === 'composed_product'"
          v-model="editado.composed_product"
          type="checkbox"
          class="w-5 h-5 sm:col-span-2"
        /> -->
        <!-- <input
          v-else-if="campo.key === 'checked'"
          v-model="editado.checked"
          type="checkbox"
          class="w-5 h-5 sm:col-span-2"
        />
        Textarea para descripción 
        <textarea
          v-else-if="campo.key === 'description'"
          v-model="editado[campo.key]"
          rows="3"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2 resize-y"
          placeholder="Escribe una descripción detallada..."
          @input="autoResize"
        ></textarea>-->
        <!-- Inputs normales -->
        <input
          v-else
          v-model="editado[campo.key]"
          :type="campo.type || 'text'"
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2"
          :placeholder="campo.label"
        />

        <p v-if="errores[campo.key]" class="text-red-600 text-sm col-span-3 sm:col-span-2">
          {{ errores[campo.key] }}
        </p>
      </div>

      <div class="flex justify-center mt-6">
        <button
          @click="crearProducto"
          class="bg-[#8bc34a] text-white py-2 px-2 sm:px-4 md:px-6 lg:px-8 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
        >
          Crear Producto
        </button>
      </div>
    </div>

    <button
      @click="$router.push('/')"
      class="bg-[#ff9800] text-white py-2 px-2 sm:px-4 md:px-6 lg:px-8 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
    >
      Volver atrás
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const camposBase = [
  { key: 'id_product', label: '*ID Producto' , type: 'number'},
  { key: 'description', label: '*Nombre' },
  { key: 'category', label: '*Categoría' },
  { key: 'subcategories', label: 'Subcategorías' },
  { key: 'supplier', label: '*Proveedor' },
  { key: 'purchase_price', label: '*Precio de compra', type: 'number' },
  { key: 'wholesale_price', label: '*Precio mayoreo', type: 'number' },
  { key: 'wholesale_quantity', label: '*Cantidad mayoreo', type: 'number' },
  { key: 'discount_surcharge', label: '*Descuento / Recargo (%)', type: 'number' },
  { key: 'stock', label: '*Stock Disponible', type: 'number' },
  { key: 'critical_stock', label: '*Stock Crítico', type: 'number' },
  {
    key: 'exit_stock_unit',
    label: '*Unidad Salida Stock',
    type: 'select',
    options: [
      { label: 'Unidad', value: 'unit' },
      { label: 'Kilo', value: 'kilo' },
    ]
  },
]

const editado = ref({
  id_product: '',
  description: '',
  category: '',
  subcategories: [],
  supplier: '',
  purchase_price: '',
  sale_price: 0,
  wholesale_price: '',
  wholesale_quantity: '',
  discount_surcharge: 0,
  stock: '',
  critical_stock: '',
  entry_stock_unit: '',
  exit_stock_unit: '',
  composed_product: false,
  checked: false,
})

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

const categoriasDisponibles = ref([])
const subcategoriasDisponibles = ref([])
const proveedoresDisponibles = ref([])

onMounted(async () => {
  try {
    const config = useRuntimeConfig();
    const [catRes, subcatRes, provRes] = await Promise.all([
      fetch(`${config.public.apiBase}/api/categories/`),
      fetch(`${config.public.apiBase}/api/subcategories/`),
      fetch(`${config.public.apiBase}/api/suppliers/`),
    ])

    categoriasDisponibles.value = await catRes.json()
    subcategoriasDisponibles.value = await subcatRes.json()
    proveedoresDisponibles.value = await provRes.json()
  } catch (err) {
    console.error('Error al cargar datos auxiliares:', err)
  }
})

const errores = ref({})

const validarCamposRequeridos = () => {
  errores.value = {}

  if (!editado.value.id_product)
    errores.value.id_product = 'El campo ID Producto es obligatorio.'
  if (!editado.value.description)
    errores.value.description = 'El campo Nombre es obligatorio.'
  else if (!/^[\p{L}0-9_\-\s]+$/u.test(editado.value.description))
    errores.value.description = 'El nombre solo puede contener letras, números, espacios, guiones y guiones bajos.'
  if (!editado.value.category)
    errores.value.category = 'El campo Categoria es obligatorio.'
  if (!editado.value.supplier)
    errores.value.supplier = 'El campo Proveedor es obligatorio.'
  if (!editado.value.purchase_price)
    errores.value.purchase_price = 'El campo Precio de compra es obligatorio.'
  if (!editado.value.wholesale_price)
    errores.value.wholesale_price = 'El campo Precio Mayoreo es obligatorio.'
  if (!editado.value.wholesale_quantity)
    errores.value.wholesale_quantity = 'El campo Cantidad Mayoreo es obligatorio.'
  if (!editado.value.discount_surcharge || editado.value.discount_surcharge === 0)
    errores.value.discount_surcharge = 'El campo Descuento / Recargo (%) es obligatorio.'
  if (!editado.value.stock)
    errores.value.stock = 'El campo Stock disponible es obligatorio.'
  if (!editado.value.critical_stock)
    errores.value.critical_stock = 'El campo Stock Crítico es obligatorio.'
  if (!editado.value.entry_stock_unit)
    errores.value.entry_stock_unit = 'El campo Unidad de entrada es obligatorio.'
  if (!editado.value.exit_stock_unit)
    errores.value.exit_stock_unit = 'El campo Unidad de salida es obligatorio.'

  return Object.keys(errores.value).length === 0
}

const crearProducto = async () => {
  if (!validarCamposRequeridos()) {
    alert('Por favor completa los campos obligatorios.')
    return
  }

  try {
    console.log('Creando producto:', editado.value)
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBase}/api/products/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editado.value),
    })
    if (!res.ok) throw new Error('Error al crear el producto')

    alert('Producto creado correctamente')
    router.push('/productos')
  } catch (err) {
    console.error('Error al crear producto:', err)
    alert('Error al crear el producto')
  }
}

const agregarSubcategoria = () => {
  editado.value.subcategories.push('')
}

const eliminarSubcategoria = (index) => {
  editado.value.subcategories.splice(index, 1)
}
const autoResize = (event) => {
  const el = event.target
  el.style.height = 'auto'
  el.style.height = el.scrollHeight + 'px'
}

</script>

