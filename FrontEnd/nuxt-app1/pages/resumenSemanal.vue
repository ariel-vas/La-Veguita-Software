<template>
    <div class="flex flex-col items-center justify-center gap-6 bg-blue-100 p-8 pt-0 mt-16">
      <h1 class="text-4xl font-bold text-blue-900">Resumen Semanal de Productos</h1>
  
      <div class="bg-white rounded-xl shadow-lg p-6 w-full max-w-6xl mt-4 overflow-x-auto">
        <h2 class="text-xl font-semibold text-blue-800 mb-4">Movimientos de Productos</h2>
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-blue-200 text-blue-900">
              <th class="py-2 px-4">Producto</th>
              <th class="py-2 px-4">Código</th>
              <th class="py-2 px-4">Marca</th>
              <th class="py-2 px-4">Distribuidor</th>
              <th class="py-2 px-4">Entradas (7 días)</th>
              <th class="py-2 px-4">Salidas (7 días)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(prod, i) in productos" :key="i" class="border-t">
              <td class="py-2 px-4">{{ prod.nombre }}</td>
              <td class="py-2 px-4">{{ prod.codigo }}</td>
              <td class="py-2 px-4">{{ prod.marca }}</td>
              <td class="py-2 px-4">{{ prod.distribuidor }}</td>
              <td class="py-2 px-4">{{ prod.entradasSemana }}</td>
              <td class="py-2 px-4">{{ prod.salidasSemana }}</td>
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
  