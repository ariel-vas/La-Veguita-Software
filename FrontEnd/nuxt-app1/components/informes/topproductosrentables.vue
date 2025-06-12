<template>
  <div class="flex flex-col gap-6">
    <h2 class="text-2xl font-semibold text-[#8bc34a]">
      Top 10 productos más rentables del mes
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

    <!-- Gráfico de rentabilidad -->
    <div>
      <h3 class="text-lg font-medium text-gray-700 mb-2">Productos más rentables</h3>
      <div v-if="chartData.labels.length">
        <Bar :data="chartData" :options="chartOptions" />
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
import ChartDataLabels from 'chartjs-plugin-datalabels'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ChartDataLabels)

const selectedMonth = ref('')
const chartData = ref({ labels: [], datasets: [] })

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    datalabels: {
      color: '#000',
      anchor: 'end',
      align: 'top',
      formatter: (value) => (value === 0 ? '0' : value),
    },
    title: {
      display: false,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { color: '#4a4a4a' },
      grid: {
        color: '#e0e0e0',
        borderDash: [5, 5],
      },
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
    const res = await fetch(`${config.public.apiBase}/api/sales/report/MostProfitable/?year=${year}&month=${month}`)
    const data = await res.json()

    chartData.value = {
      labels: data.top_10_most_profitable_products.map(p => p.product_description),
      datasets: [
        {
          label: 'Ingresos ($)',
          backgroundColor: '#4caf50',
          data: data.top_10_most_profitable_products.map(p => p.ingreso_total),
        },
        {
          label: 'Costos ($)',
          backgroundColor: '#f44336',
          data: data.top_10_most_profitable_products.map(p => p.costo_total),
        },
      ],
    }
  } catch (err) {
    console.error('Error al obtener los datos:', err)
    chartData.value = { labels: [], datasets: [] }
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