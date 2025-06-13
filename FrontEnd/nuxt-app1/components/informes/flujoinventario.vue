<template>
  <div class="flex flex-col gap-6">
    <h2 class="text-2xl font-semibold text-[#8bc34a]">Flujo de Inventario por Producto</h2>

    <!-- Buscador por código de producto -->
    <div class="flex items-center gap-4">
      <label for="product-id" class="font-medium">Código de producto:</label>
      <input
        id="product-id"
        v-model="productId"
        type="number"
        class="border border-gray-300 rounded-lg p-2 w-40"
        placeholder="Ej: 1"
      />
      <button
        @click="fetchProductData"
        class="bg-[#8bc34a] text-white px-4 py-2 rounded-lg hover:bg-[#7cb342]"
      >
        Buscar
      </button>
      <div v-if="errorMessage" class="flex items-center text-red-600 mt-2 gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M5.07 18H18.93a2 2 0 001.84-2.75l-6.93-12a2 2 0 00-3.68 0l-6.93 12A2 2 0 005.07 18z" />
        </svg>
        <span>{{ errorMessage }}</span>
      </div>
    </div>

    <!-- Info del producto -->
    <div v-if="productDescription" class="mt-4">
      <p><span class="font-medium">Producto:</span> {{ productDescription }}</p>
      <p><span class="font-medium">Stock actual:</span> {{ currentStock }}</p>
      <p>
        <span class="font-medium">Periodo:</span>
        {{ formattedPeriod }}
      </p>
    </div>

    <!-- Gráfico del flujo -->
    <div v-if="chartData.labels.length">
      <h3 class="text-lg font-medium text-gray-700 mb-2">Ingresos de productos vs Salidas de productos</h3>
      <Bar :data="chartData" :options="chartOptions" />
    </div>
    <div v-else-if="productDescription" class="text-gray-500 italic">
      No hay datos para este producto.
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ChartDataLabels)

const errorMessage = ref('')
const productId = ref('')
const productDescription = ref('')
const currentStock = ref(0)
const formattedPeriod = ref('')
const chartData = ref({ labels: [], datasets: [] })

function formatPeriod(mesNombreIngles, año) {
  const meses = {
    January: 'Ene',
    February: 'Feb',
    March: 'Mar',
    April: 'Abr',
    May: 'May',
    June: 'Jun',
    July: 'Jul',
    August: 'Ago',
    September: 'Sep',
    October: 'Oct',
    November: 'Nov',
    December: 'Dic',
  }
  return `${meses[mesNombreIngles]} ${año}`
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: false },
    datalabels: {
      anchor: 'end',
      align: 'top',
      formatter: value => (value === 0 ? '0' : value),
      color: '#000',
      font: { weight: 'bold' },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { color: '#4a4a4a' },
    },
    x: {
      ticks: { color: '#4a4a4a' },
    },
  },
}

async function fetchProductData() {
  if (!productId.value) return
    errorMessage.value = ''
  try {
    
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBase}/api/sales/report/ProductInventoryFlow/product/${productId.value}`)
    const data = await res.json()

    productDescription.value = data.product_description
    currentStock.value = data.current_stock
    formattedPeriod.value = `${formatPeriod(data.period.from.split(' ')[0], data.period.from.split(' ')[1])} a ${formatPeriod(data.period.to.split(' ')[0], data.period.to.split(' ')[1])}`

    const labels = data.inventory_flow.map(item => formatPeriod(item.mes_nombre, item.año))
    const ingresos = data.inventory_flow.map(item => item.cantidad_ingresada)
    const ventas = data.inventory_flow.map(item => item.cantidad_vendida)

    chartData.value = {
      labels,
      datasets: [
        {
          label: 'Ingresos',
          backgroundColor: '#4caf50',
          data: ingresos,
        },
        {
          label: 'Salidas',
          backgroundColor: '#f44336',
          data: ventas,
        },
      ],
    }
  } catch (err) {
    console.error('Error al obtener los datos del producto:', err)
    errorMessage.value = 'No se encontró un producto con ese código.'
    productDescription.value = ''
    currentStock.value = 0
    formattedPeriod.value = ''
    chartData.value = { labels: [], datasets: [] }
  }
}
</script>

<style scoped>
input {
  background-color: white;
}
</style>