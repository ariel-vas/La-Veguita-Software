<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Crear Categoría</h1>

    <form
      @submit.prevent="crearCategoria"
      class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl space-y-6"
    >
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-center">
        <label for="name" class="font-semibold">Nombre:</label>
        <input
          id="name"
          type="text"
          v-model="categoria.name"
          required
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2"
          placeholder="Ingrese nombre"
        />
      </div>

      <div class="flex justify-center">
        <button
          type="submit"
          class="bg-[#8bc34a] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
        >
          Crear Categoría
        </button>
      </div>

      <div v-if="mensaje" :class="mensajeError ? 'text-red-600' : 'text-green-600'" class="text-center font-semibold">
        {{ mensaje }}
      </div>
    </form>

    <button
      @click="$router.push('/categorias')"
      class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
    >
      Volver atrás
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categoria: {
        id_category: '',
        name: '',
      },
      mensaje: '',
      mensajeError: false,
    };
  },
  methods: {
    async crearCategoria() {
      // Validación: no permitir solo números
      const soloNumeros = /^[0-9]+$/;
      if (soloNumeros.test(this.categoria.name.trim())) {
        this.mensaje = 'El nombre no puede ser solo números.';
        this.mensajeError = true;
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/api/categories/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.categoria),
        });
        if (!response.ok) throw new Error('Error al crear la categoría');
        this.mensaje = 'Categoría creada exitosamente';
        this.mensajeError = false;
        this.categoria.id_category = '';
        this.categoria.name = '';
      } catch (error) {
        this.mensaje = error.message;
        this.mensajeError = true;
      }
    },
  },
};
</script>
