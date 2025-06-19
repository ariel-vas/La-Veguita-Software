<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a] mb-5 sm:mb-4 md:mb-6 lg:mb-10">Resumen Semanal de Productos</h1>

    <div class="bg-white rounded-xl shadow-lg p-6 w-full max-w-6xl mt-4 overflow-x-auto">
      <h2 class="text-xl font-semibold text-[#8bc34a] mb-4">Movimientos de Productos</h2>
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-[#dcedc8] text-[#558b2f]">
            <th class="py-2 px-2 sm:px-3 md:px-4 lg:px-6">Producto</th>
            <th class="py-2 px-2 sm:px-3 md:px-4 lg:px-6">Código</th>
            <th class="py-2 px-2 sm:px-3 md:px-4 lg:px-6">Marca</th>
            <th class="py-2 px-2 sm:px-3 md:px-4 lg:px-6">Distribuidor</th>
            <th class="py-2 px-2 sm:px-3 md:px-4 lg:px-6">Entradas (7 días)</th>
            <th class="py-2 px-2 sm:px-3 md:px-4 lg:px-6">Salidas (7 días)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(prod, i) in productos" :key="i" class="border-t border-gray-300">
            <td class="py-2 px-2 sm:px-3 md:px-4 lg:px-6 text-[#33691e]">{{ prod.nombre }}</td>
            <td class="py-2 px-2 sm:px-3 md:px-4 lg:px-6 text-[#33691e]">{{ prod.codigo }}</td>
            <td class="py-2 px-2 sm:px-3 md:px-4 lg:px-6 text-[#33691e]">{{ prod.marca }}</td>
            <td class="py-2 px-2 sm:px-3 md:px-4 lg:px-6 text-[#33691e]">{{ prod.distribuidor }}</td>
            <td class="py-2 px-2 sm:px-3 md:px-4 lg:px-6 text-[#33691e]">{{ prod.entradasSemana }}</td>
            <td class="py-2 px-2 sm:px-3 md:px-4 lg:px-6 text-[#33691e]">{{ prod.salidasSemana }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      productos: [
        {
          nombre: "Manzana",
          codigo: "FRU123",
          marca: "Frutas del Sur",
          distribuidor: "Distribuidor Privado",
          entradasSemana: 30,
          salidasSemana: 25,
        },
        {
          nombre: "Leche",
          codigo: "LCH456",
          marca: "Vaquita Feliz",
          distribuidor: "Lácteos del Norte",
          entradasSemana: 50,
          salidasSemana: 45,
        },
        {
          nombre: "Pan",
          codigo: "PN789",
          marca: "Panadería Central",
          distribuidor: "Distribuidora Sur",
          entradasSemana: 40,
          salidasSemana: 38,
        },
      ],
    };
  },
};
</script>
