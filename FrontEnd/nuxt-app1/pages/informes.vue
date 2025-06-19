<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a] mb-5 sm:mb-4 md:mb-6 lg:mb-10">Informes de ventas</h1>

    <!-- Selector de tipo de informe -->
    <select
      v-model="selectedReport"
      class="w-full max-w-lg p-3 border border-gray-300 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-[#8bc34a]"
    >
      <option disabled value="">Seleccione un informe</option>
      <option v-for="(label, key) in reportOptions" :key="key" :value="key">
        {{ label }}
      </option>
    </select>

    <!-- Contenido del informe seleccionado -->
    <div v-if="selectedReport" class="w-full max-w-5xl bg-white p-6 rounded-xl shadow">
      <component :is="renderedComponent" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Componentes
import InformeCierre from '@/components/informes/informecierre.vue'
import ProductoMasMenosVendido from '@/components/informes/productomasmenosvendido.vue'
import IngresosVsCostos from '@/components/informes/ingresosvscostos.vue'
import GananciaBruta from '@/components/informes/gananciabruta.vue'
import TopProductosRentables from '@/components/informes/topproductosrentables.vue'
import FlujoInventario from '@/components/informes/flujoinventario.vue'
import VarianzaVentas from '@/components/informes/varianzaventas.vue'

// Estado
const selectedReport = ref('')

// Opciones disponibles
const reportOptions = {
  informeCierre: 'Informe de cierre (últimos 28 días)',
  productoMasMenos: 'Producto/Categoría más y menos vendido',
  ingresosCostos: 'Ingresos v/s Costos',
  gananciaBruta: 'Ganancia bruta del año',
  topRentables: 'Top 10 Productos más rentables',
  flujoInventario: 'Flujo de inventario + Promedio de salida',
  //varianzaVentas: 'Varianza de ventas % entre meses',
}

// Render dinámico del componente
const renderedComponent = computed(() => {
  switch (selectedReport.value) {
    case 'informeCierre': return InformeCierre
    case 'productoMasMenos': return ProductoMasMenosVendido
    case 'ingresosCostos': return IngresosVsCostos
    case 'gananciaBruta': return GananciaBruta
    case 'topRentables': return TopProductosRentables
    case 'ventasPorDia': return VentasPorDia
    case 'flujoInventario': return FlujoInventario
    case 'varianzaVentas': return VarianzaVentas
    default: return null
  }
})
</script>