<template>
  <div class="flex flex-col gap-6">
    <h2 class="text-2xl font-semibold text-[#8bc34a]">
      Productos más y menos vendidos del mes
    </h2>

    <!-- Selector de mes -->
    <select
      v-model="selectedMonth"
      @change="fetchData"
      class="w-60 border border-gray-300 rounded-lg p-2"
    >
      <option
        v-for="(month, index) in last12Months"
        :key="index"
        :value="month.value"
      >
        {{ month.label }}
      </option>
    </select>

    <!-- Gráfico más vendidos -->
    <div>
      <h3 class="text-lg font-medium text-gray-700 mb-2">Más vendidos</h3>
      <div v-if="chartDataMas.labels.length">
        <Bar :data="chartDataMas" :options="chartOptions" />
      </div>
      <div v-else class="text-gray-500 italic">No hay datos para este mes.</div>
    </div>

    <!-- Gráfico menos vendidos -->
    <div>
      <h3 class="text-lg font-medium text-gray-700 mb-2">Menos vendidos</h3>
      <div v-if="chartDataMenos.labels.length">
        <Bar :data="chartDataMenos" :options="chartOptions" />
      </div>
      <div v-else class="text-gray-500 italic">No hay datos para este mes.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const selectedMonth = ref('')
const chartDataMas = ref({ labels: [], datasets: [] })
const chartDataMenos = ref({ labels: [], datasets: [] })

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: {
      display: false,
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

const last12Months = computed(() => {
  const months = []
  const currentDate = new Date()
  for (let i = 0; i < 12; i++) {
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1)
    months.push({
      label: date.toLocaleString('default', { month: 'long', year: 'numeric' }),
      value: `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`,
    })
  }
  return months
})

async function fetchData() {
  if (!selectedMonth.value) return
  const [year, month] = selectedMonth.value.split('-')

  try {
    const config = useRuntimeConfig();
    const [masRes, menosRes] = await Promise.all([
      fetch(`${config.public.apiBase}/api/sales/summary/MostSales/?month=${month}&year=${year}`),
      fetch(`${config.public.apiBase}/api/sales/summary/LeastSales/?month=${month}&year=${year}`),
    ])

    const masData = await masRes.json()
    const menosData = await menosRes.json()

    chartDataMas.value = {
      labels: masData.top_10_products.map(p => p.product__description),
      datasets: [
        {
          label: 'Total vendido ($)',
          backgroundColor: '#8bc34a',
          data: masData.top_10_products.map(p => p.total_revenue),
        },
      ],
    }

    chartDataMenos.value = {
      labels: menosData.bottom_10_products_by_revenue.map(p => p.product__description),
      datasets: [
        {
          label: 'Total vendido ($)',
          backgroundColor: '#f44336',
          data: menosData.bottom_10_products_by_revenue.map(p => p.total_revenue),
        },
      ],
    }
  } catch (err) {
    console.error('Error al obtener los datos:', err)
    chartDataMas.value = { labels: [], datasets: [] }
    chartDataMenos.value = { labels: [], datasets: [] }
  }
}

onMounted(() => {
  selectedMonth.value = last12Months.value[0].value
  fetchData()
})
</script>

<style scoped>
select {
  background-color: white;
}
</style>