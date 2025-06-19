<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a] mb-5 sm:mb-4 md:mb-6 lg:mb-10">Crear Categoría</h1>

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
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2"
          placeholder="Ingrese nombre de la categoría"
          pattern="^(?![0-9]+$).*$"
          title="El nombre no puede ser solo números."
        />
      </div>

      <div class="flex justify-center">
        <button
          type="submit"
          class="bg-[#8bc34a] text-white py-2 px-2 sm:px-4 md:px-6 lg:px-8 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
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
      class="bg-[#ff9800] text-white py-2 px-2 sm:px-4 md:px-6 lg:px-8 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
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
        const config = useRuntimeConfig();
        const response = await fetch(`${config.public.apiBase}/api/categories/`, {
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
