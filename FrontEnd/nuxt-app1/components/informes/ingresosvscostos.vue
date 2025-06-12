<template>
  <div class="flex flex-col gap-6">
    <h2 class="text-2xl font-semibold text-[#8bc34a]">Ingresos vs Costos</h2>

    <div class="flex gap-4 items-center">
      <label class="font-medium">Ver por:</label>
      <select v-model="mode" class="border p-2 rounded-lg">
        <option value="producto">Producto</option>
        <option value="categoria">Categoría</option>
      </select>
    </div>

    <div v-if="mode === 'producto'" class="flex flex-col gap-2">
      <input
        v-model="productName"
        @keyup.enter="fetchProductData"
        placeholder="Nombre del producto"
        class="border p-2 rounded-lg w-full max-w-md"
      />
      <button @click="fetchProductData" class="bg-[#8bc34a] text-white px-4 py-2 rounded-lg w-max">
        Buscar producto
      </button>
    </div>

    <div v-else class="flex flex-col gap-2">
      <select v-model="selectedCategory" @change="fetchCategoryData" class="border p-2 rounded-lg w-full max-w-md">
        <option disabled value="">Selecciona una categoría</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
    </div>

    <div v-if="chartData.labels.length">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
    <div v-else class="text-gray-500 italic">No hay datos para mostrar.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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

const mode = ref('producto')
const productName = ref('')
const selectedCategory = ref('')
const categories = ref([])
const chartData = ref({ labels: [], datasets: [] })

const now = new Date()
const currentYear = now.getFullYear()
const currentMonth = now.getMonth() + 1

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
  if (!productName.value) return
  const config = useRuntimeConfig();
  const res = await fetch(`${config.public.apiBase}/api/sales/report/product/?product_description=${productName.value}&year=${currentYear}&month=${currentMonth}`)
  const data = await res.json()
  updateChart(data.monthly_report)
}

async function fetchCategoryData() {
  if (!selectedCategory.value) return
  const config = useRuntimeConfig();
  const res = await fetch(`${config.public.apiBase}/api/sales/report/category/?category=${selectedCategory.value}&year=${currentYear}&month=${currentMonth}`)
  const data = await res.json()
  updateChart(data.monthly_report)
}

async function loadCategories() {
  const config = useRuntimeConfig();
  const res = await fetch(`${config.public.apiBase}/api/categories/`)
  const data = await res.json()
  categories.value = data.map(cat => cat.name)
}

function updateChart(report) {
  const labels = report.map(r => r.mes_nombre)
  const ingresos = report.map(r => r.ingreso)
  const costos = report.map(r => r.costo)

  chartData.value = {
    labels,
    datasets: [
      {
        label: 'Ingresos ($)',
        backgroundColor: '#4caf50',
        data: ingresos,
      },
      {
        label: 'Costos ($)',
        backgroundColor: '#f44336',
        data: costos,
      },
    ],
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
select, input {
  background-color: white;
}
</style>