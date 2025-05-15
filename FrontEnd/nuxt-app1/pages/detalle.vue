<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Detalle del Producto</h1>

    <div class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl">
      <div class="text-lg text-[#8bc34a] space-y-3">
        <p><strong class="text-[#8bc34a]">Nombre:</strong> {{ producto.nombre }}</p>
        <p><strong class="text-[#8bc34a]">Código:</strong> {{ producto.codigo }}</p>
        <p><strong class="text-[#8bc34a]">Fecha de Entrada:</strong> {{ producto.fechaEntrada }}</p>
        <p><strong class="text-[#8bc34a]">Fecha de Vencimiento:</strong> {{ producto.fechaVencimiento }}</p>
        <p><strong class="text-[#8bc34a]">Cantidad:</strong> {{ producto.cantidad }}</p>
        <p><strong class="text-[#8bc34a]">Marca:</strong> {{ producto.marca }}</p>
        <p><strong class="text-[#8bc34a]">Distribuidor:</strong> {{ producto.distribuidor }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      producto: {
        nombre: "Manzana",
        codigo: "FRU123",
        fechaEntrada: "2023-10-01",
        fechaVencimiento: "2023-10-15",
        cantidad: 50,
        marca: "Frutas del Sur",
        distribuidor: "Distribuidor Privado",
      },
    };
  },
};
</script>

<style scoped>
</style>
