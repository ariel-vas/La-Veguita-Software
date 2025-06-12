<template>
  <div class="flex flex-col gap-4">
    <h2 class="text-2xl font-semibold text-[#8bc34a] mb-2">Informe de Cierre - Últimos 28 días</h2>

    <table class="w-full bg-white rounded-xl shadow">
      <thead class="bg-[#8bc34a] text-white">
        <tr>
          <th class="py-2 px-4 text-left">Fecha</th>
          <th class="py-2 px-4 text-left">Ventas Totales</th>
          <th class="py-2 px-4 text-left">Productos Vendidos</th>
          <th class="py-2 px-4 text-left">Ingresos ($)</th>
          <th class="py-2 px-4 text-left">Tiempo Operación</th>
          <th class="py-2 px-4 text-left">Vendedoras</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in reportData" :key="index" class="border-b hover:bg-[#f0f8e9]">
          <td class="py-2 px-4">{{ item.fecha }}</td>
          <td class="py-2 px-4">{{ item.ventasTotales }}</td>
          <td class="py-2 px-4">{{ item.productosVendidos }}</td>
          <td class="py-2 px-4">{{ item.ingresos.toLocaleString('es-CL') }}</td>
          <td class="py-2 px-4">{{ item.tiempoOperacion }}</td>
          <td class="py-2 px-4">{{ item.vendedoras }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Generar datos simulados para los últimos 28 días
const generarDatosSimulados = () => {
  const hoy = new Date()
  const datos = []

  for (let i = 0; i < 28; i++) {
    const fecha = new Date(hoy)
    fecha.setDate(hoy.getDate() - i)

    const formato = fecha.toLocaleDateString('es-CL')
    datos.push({
      fecha: formato,
      ventasTotales: Math.floor(Math.random() * 50 + 10),
      productosVendidos: Math.floor(Math.random() * 200 + 50),
      ingresos: Math.floor(Math.random() * 500000 + 100000),
      tiempoOperacion: `${String(Math.floor(Math.random() * 8 + 8)).padStart(2, '0')}:${String(Math.floor(Math.random() * 60)).padStart(2, '0')}:${String(Math.floor(Math.random() * 60)).padStart(2, '0')}`,
      vendedoras: Math.floor(Math.random() * 3 + 1),
    })
  }

  return datos
}

const reportData = ref(generarDatosSimulados())
</script>