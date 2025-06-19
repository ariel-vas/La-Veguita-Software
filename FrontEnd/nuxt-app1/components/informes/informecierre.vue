<template>
  <div class="flex flex-col sm:flex-row sm:items-end gap-4 mb-6 w-full max-w-2xl">
    <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold text-[#8bc34a] mb-2">
      Informe de Cierre - Día Seleccionado
    </h1>

    <!-- Selector de fecha -->
    <select
      v-model="selectedDate"
      @change="fetchReport"
      class="w-60 p-2 border border-gray-300 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-[#8bc34a]"
    >
      <option disabled value="">Seleccione fecha</option>
      <option v-for="d in last28Days" :key="d" :value="d">
        {{ d }}
      </option>
    </select>

    <!-- Mensaje de carga o error -->
    <div v-if="loading" class="text-gray-500">Cargando...</div>
    <div v-if="error" class="text-red-600">{{ error }}</div>

    <!-- Tablas -->
    <div v-if="report">
      <!-- Resumen -->
      <h3 class="text-xl text-center font-semibold text-[#8bc34a] mb-3">
        Resumen General
      </h3>
      <table class="w-full bg-white rounded-xl shadow mb-6">
        <thead class="bg-[#8bc34a] text-white">
          <tr>
            <th class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">Fecha</th>
            <th class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">Productos Vendidos</th>
            <th class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">Ventas Totales</th>
          </tr>
        </thead>
        <tbody>
          <tr class="border-b hover:bg-[#f0f8e9]">
            <td class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">{{ report.report_date }}</td>
            <td class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">{{ report.products_sold.length }}</td>
            <td class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">{{ totalVentas.toLocaleString('es-CL') }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Detalle -->
      <h3 class="text-xl text-center font-semibold text-[#8bc34a] mb-3">
        Detalle por producto
      </h3>
      <table class="w-full bg-white rounded-xl shadow">
        <thead class="bg-[#8bc34a] text-white">
          <tr>
            <th class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">Nombre del Producto</th>
            <th class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">Unidad</th>
            <th class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">Cantidad</th>
            <th class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">Valor</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(p, idx) in report.products_sold"
            :key="idx"
            class="border-b hover:bg-[#f0f8e9]"
          >
            <td class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">{{ p['product__description'] }}</td>
            <td class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">{{ p['product__exit_stock_unit'] }}</td>
            <td class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">{{ p.total_quantity }}</td>
            <td class="py-3 px-2 sm:px-4 md:px-6 text-center border border-gray-300">{{ p.total_subtotal.toLocaleString('es-CL') }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const selectedDate = ref('')
const last28Days = ref([])
const report = ref(null)
const loading = ref(false)
const error = ref('')

// Generar array de fechas
onMounted(() => {
  const today = new Date()
  for (let i = 0; i < 28; i++) {
    const d = new Date(today)
    d.setDate(today.getDate() - i)
    last28Days.value.push(d.toISOString().split('T')[0])
  }
})

// Calcular totalVentas
const totalVentas = computed(() =>
  report.value
    ? report.value.products_sold.reduce((sum, p) => sum + p.total_subtotal, 0)
    : 0
)

// Llamada al backend
async function fetchReport() {
  if (!selectedDate.value) return
  loading.value = true
  error.value = ''
  report.value = null

  try {
    const config = useRuntimeConfig();
    const res = await fetch(
      `${config.public.apiBase}/api/sales/summary/daily-report/?date=${selectedDate.value}`
    )
    if (!res.ok) throw new Error('Error al obtener el reporte')
    report.value = await res.json()
  } catch (err) {
    error.value = err.message || 'Error desconocido'
  } finally {
    loading.value = false
  }
}
</script>