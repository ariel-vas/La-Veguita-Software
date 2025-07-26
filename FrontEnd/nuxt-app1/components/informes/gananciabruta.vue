<template>
  <div class="flex flex-col gap-6">
    <h2 class="text-2xl font-semibold text-[#8bc34a]">Ganancia Bruta Anual</h2>

    <!-- Selector de año -->
    <div class="flex items-center gap-4">
      <label for="year-select" class="font-medium">Año:</label>
      <select
        id="year-select"
        v-model="selectedYear"
        @change="fetchGrossProfitData"
        class="border border-gray-300 rounded-lg p-2 w-40"
      >
        <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
      </select>
    </div>

    <!-- Datos brutos -->
    <div v-if="selectedYear && totalIngreso !== null">
      <p><span class="font-medium">Ingreso total: $</span> {{ formatearNumero(totalIngreso) }}</p>
      <p><span class="font-medium">Costo total: $</span> {{ formatearNumero(totalCosto) }}</p>
      <p><span class="font-medium">Ganancia bruta: $</span> {{ formatearNumero(totalGanancia) }}</p>
    </div>

    <!-- Gráfico -->
    <div v-if="chartData.labels.length">
      <h3 class="text-lg font-medium text-gray-700 mb-2">Ingresos vs Costos</h3>
      <Bar :data="chartData" :options="chartOptions" />
    </div>
    <div v-else class="text-gray-500 italic">
      No hay datos disponibles para este año.
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

const selectedYear = ref(new Date().getFullYear())
const availableYears = Array.from({ length: new Date().getFullYear() - 2020 }, (_, i) => new Date().getFullYear() - i)

const totalIngreso = ref(null)
const totalCosto = ref(null)
const totalGanancia = ref(null)

const chartData = ref({ labels: [], datasets: [] })

function formatPeriod(mesNombreIngles) {
  const meses = {
    January: 'Enero',
    February: 'Febrero',
    March: 'Marzo',
    April: 'Abril',
    May: 'Mayo',
    June: 'Junio',
    July: 'Julio',
    August: 'Agosto',
    September: 'Septiembre',
    October: 'Octubre',
    November: 'Noviembre',
    December: 'Diciembre',
  }
  return meses[mesNombreIngles] || mesNombreIngles
}

function formatearNumero(n) {
  return Number.isInteger(n) ? n.toString() : n.toFixed(2)
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' },
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

async function fetchGrossProfitData() {
  try {
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBase}/api/sales/report/gross-profit/?year=${selectedYear.value}`)
    const data = await res.json()

    const ingresos = data.monthly_gross_profit.map(m => m.ingreso_total)
    const costos = data.monthly_gross_profit.map(m => m.costo_total)
    const labels = data.monthly_gross_profit.map(m => formatPeriod(m.mes_nombre))

    totalIngreso.value = ingresos.reduce((sum, val) => sum + val, 0)
    totalCosto.value = costos.reduce((sum, val) => sum + val, 0)
    totalGanancia.value = totalIngreso.value - totalCosto.value

    const maxValor = Math.max(...ingresos, ...costos)
    const margenExtra = maxValor * 0.1

    chartData.value = {
      labels,
      datasets: [
        {
          label: 'Ingresos',
          backgroundColor: '#4caf50',
          data: ingresos,
        },
        {
          label: 'Costos',
          backgroundColor: '#f44336',
          data: costos,
        },
      ],
    }

    chartOptions.scales.y.suggestedMax = maxValor + margenExtra
  } catch (err) {
    console.error('Error al obtener los datos:', err)
    totalIngreso.value = null
    totalCosto.value = null
    totalGanancia.value = null
    chartData.value = { labels: [], datasets: [] }
  }
}

fetchGrossProfitData()
</script>

<style scoped>
select {
  background-color: white;
}
</style>