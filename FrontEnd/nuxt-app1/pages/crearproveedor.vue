<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-4 sm:p-4 md:p-6 lg:p-8 mt-0">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a] mb-5 sm:mb-4 md:mb-6 lg:mb-10">Crear Proveedor</h1>

    <form
      @submit.prevent="crearProveedor"
      class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl space-y-6"
    >
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-center">
        <!-- RUT -->
        <label for="name" class="font-semibold mb-3">RUT</label>
        <input
          id="rut"
          type="text"
          v-model="proveedor.rut"
          required
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Formato válido: 12.345.678-9 o 12.345.678-K"
          pattern="^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$"
          title="El RUT debe seguir el formato."
        />
        <!-- Nombre -->
        <label for="name" class="font-semibold mb-3">Nombre</label>
        <input
          id="name"
          type="text"
          v-model="proveedor.name"
          required
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Ingrese nombre del proveedor"
          pattern="^(?![0-9]+$).*$"
          title="El nombre no puede tener solo números."
        />
        <!-- Giro -->
        <label for="name" class="font-semibold mb-3">Giro</label>
        <input
          id="line"
          type="text"
          v-model="proveedor.line"
          required
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Ingrese giro del proveedor"
          pattern="^(?![0-9]+$).*$"
          title="El giro no puede tener solo números."
        />
        <!-- Dirección -->
        <label for="name" class="font-semibold mb-3">Dirección</label>
        <input
          id="address"
          type="text"
          v-model="proveedor.address"
          required
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Ingrese la dirección del proveedor"
          pattern="^(?![0-9]+$).*$"
          title="La dirección no puede ser solo números."
        />
        <!-- Comuna -->
        <label for="name" class="font-semibold mb-3">Comuna</label>
        <input
          id="commune"
          type="text"
          v-model="proveedor.commune"
          required
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Ingrese la comuna del proveedor"
          pattern="^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
          title="La comuna debe ser solo letras."
        />
        <!-- Ciudad -->
        <label for="name" class="font-semibold mb-3">Ciudad</label>
        <input
          id="city"
          type="text"
          v-model="proveedor.city"
          required
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Ingrese la ciudad del proveedor"
          pattern="^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
          title="El nombre debe ser solo letras."
        />
        <!-- Teléfono Fijo -->
        <label for="name" class="font-semibold mb-3">Teléfono Fijo</label>
        <input
          id="telephone"
          type="text"
          v-model="proveedor.telephone"
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Ejemplo: 223456789 (campo opcional)"
          pattern="^[0-9 ]+$"
          title="El teléfono puede ser solo números."
        />
        <!-- Celular -->
        <label for="name" class="font-semibold mb-3">Celular</label>
        <input
          id="cellphone"
          type="text"
          v-model="proveedor.cellphone"
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Ejemplo 2233 4455 (campo opcional)"
          pattern="^[0-9 ]+$"
          title="El celular puede ser solo números."
        />
        <!-- Correo -->
        <label for="name" class="font-semibold mb-3">Correo</label>
        <input
          id="email"
          type="text"
          v-model="proveedor.email"
          class="border border-gray-300 rounded px-1 sm:px-2 md:px-3 lg:px-4 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Ingrese correo del proveedor (opcional)"
          pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
          title="El correo debe seguir un formato válido."
        />
      </div>

      <div class="flex justify-center">
        <button
          type="submit"
          class="bg-[#8bc34a] text-white py-2 px-2 sm:px-4 md:px-6 lg:px-8 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
        >
          Crear Proveedor
        </button>
      </div>

      <div v-if="mensaje" :class="mensajeError ? 'text-red-600' : 'text-green-600'" class="text-center font-semibold">
        {{ mensaje }}
      </div>
    </form>

    <button
      @click="$router.push('/proveedores')"
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
      proveedor: { // Cambiado de 'categoria' a 'proveedor'
        name: '', // Solo necesitamos 'name' para el POST
      },
      mensaje: '',
      mensajeError: false,
    };
  },
  methods: {
    async crearProveedor() { // Cambiado de 'crearCategoria' a 'crearProveedor'
      // Validación: no permitir solo números
      const soloNumeros = /^[0-9]+$/;
      if (soloNumeros.test(this.proveedor.name.trim())) {
        this.mensaje = 'El nombre del proveedor no puede ser solo números.';
        this.mensajeError = true;
        return;
      }

      try {
        const config = useRuntimeConfig();
        // Endpoint para crear proveedores
        const response = await fetch(`${config.public.apiBase}/api/suppliers/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          // Envía solo el objeto 'proveedor' que contiene 'name'
          body: JSON.stringify(this.proveedor),
        });

        if (!response.ok) {
            // Intenta leer el error del cuerpo de la respuesta si está disponible
            const errorData = await response.json().catch(() => ({ message: 'Error desconocido' }));
            throw new Error(errorData.message || 'Error al crear el proveedor');
        }

        this.mensaje = 'Proveedor creado exitosamente';
        this.mensajeError = false;
        this.proveedor.rut = ''; // Limpia el campo después de crear
        this.proveedor.name = ''; // Limpia el campo después de crear
        this.proveedor.line = ''; // Limpia el campo después de crear
        this.proveedor.address = ''; // Limpia el campo después de crear
        this.proveedor.commune = ''; // Limpia el campo después de crear
        this.proveedor.city = ''; // Limpia el campo después de crear
        this.proveedor.cellphone = ''; // Limpia el campo después de crear
        this.proveedor.telephone = ''; // Limpia el campo después de crear
        this.proveedor.email = ''; // Limpia el campo después de crear
      } catch (error) {
        this.mensaje = error.message;
        this.mensajeError = true;
      }
    },
  },
};
</script>

<style scoped>
/* Los estilos existentes son perfectamente reutilizables */
</style>    