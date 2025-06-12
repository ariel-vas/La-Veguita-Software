<template>
  <div class="flex flex-col gap-6">
    <h2 class="text-2xl font-semibold text-[#8bc34a]">Ingresos v/s Costos</h2>

    <!-- Selector -->
    <div class="flex gap-4">
      <button
        @click="modo = 'producto'"
        :class="modo === 'producto' ? activeBtn : inactiveBtn"
      >
        Por Producto
      </button>
      <button
        @click="modo = 'categoria'"
        :class="modo === 'categoria' ? activeBtn : inactiveBtn"
      >
        Por Categoría
      </button>
    </div>

    <!-- Gráfico -->
    <Bar :data="datosGrafico" :options="opcionesGrafico" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
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

const modo = ref('producto')

const activeBtn =
  'bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition'
const inactiveBtn =
  'bg-gray-200 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-300 transition'

// Datos simulados
const datosSimulados = {
  producto: {
    labels: ['Zapatos', 'Camisas', 'Pantalones', 'Chaquetas', 'Gorros'],
    ingresos: [150000, 180000, 120000, 90000, 70000],
    costos: [100000, 120000, 80000, 60000, 50000],
  },
  categoria: {
    labels: ['Ropa', 'Calzado', 'Accesorios'],
    ingresos: [400000, 250000, 120000],
    costos: [300000, 180000, 90000],
  },
}

const datosGrafico = computed(() => {
  const datos = datosSimulados[modo.value]

  return {
    labels: datos.labels,
    datasets: [
      {
        label: 'Ingresos',
        backgroundColor: '#8bc34a',
        data: datos.ingresos,
      },
      {
        label: 'Costos',
        backgroundColor: '#f44336',
        data: datos.costos,
      },
    ],
  }
})

const opcionesGrafico = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: {
      display: true,
      text: 'Comparación de Ingresos y Costos',
      color: '#4a4a4a',
      font: { size: 18 },
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
</script>