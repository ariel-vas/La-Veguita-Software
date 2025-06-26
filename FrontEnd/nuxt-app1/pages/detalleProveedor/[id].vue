<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 mt-0">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Editar Proveedor</h1>

    <div v-if="proveedor" class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl space-y-6">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-start">
        <label class="font-semibold mb-3">RUT del Proveedor</label>
        <input
          v-model="editado.rut"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2 mb-3"
          placeholder="RUT del Proveedor"
        />
        <label class="font-semibold mb-3">Nombre</label>
        <input
          v-model="editado.name"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Nombre del proveedor"
        />
        <label class="font-semibold mb-3">Giro</label>
        <input
          v-model="editado.line"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Giro del proveedor"
        />
        <label class="font-semibold mb-3">Dirección</label>
        <input
          v-model="editado.address"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Dirección del proveedor"
        />
        <label class="font-semibold mb-3">Comuna</label>
        <input
          v-model="editado.commune"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Comuna del proveedor"
        />
        <label class="font-semibold mb-3">Ciudad</label>
        <input
          v-model="editado.city"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Ciudad del proveedor"
        />
        <label class="font-semibold mb-3">Teléfono Fijo</label>
        <input
          v-model="editado.telephone"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Teléfono Fijo del proveedor"
        />
        <label class="font-semibold mb-3">Celular</label>
        <input
          v-model="editado.cellphone"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Celular del proveedor"
        />
        <label class="font-semibold mb-3">Correo</label>
        <input
          v-model="editado.email"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2 mb-3"
          placeholder="Correo del proveedor"
        />
      </div>

      <div class="flex justify-center gap-4 mt-4">
        <button
          @click="guardarCambios"
          class="bg-[#8bc34a] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
        >
          Guardar Cambios
        </button>

        <button
          @click="eliminarProveedor"
          class="bg-red-500 text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
        >
          {{ confirmarEliminacion ? 'Confirmar eliminación' : 'Eliminar Proveedor' }}
        </button>
      </div>

      <p v-if="confirmarEliminacion" class="text-sm text-red-700 text-center mt-2 max-w-md">
        Esta acción eliminará el proveedor. Haz clic nuevamente para confirmar.
      </p>

      <div v-if="mensaje" :class="mensajeError ? 'text-red-600' : 'text-green-600'" class="text-center font-semibold">
        {{ mensaje }}
      </div>
    </div>

    <div v-else class="text-gray-600 text-lg">Cargando proveedor...</div>

    <button
      @click="$router.push('/proveedores')"
      class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
    >
      Volver atrás
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const confirmarEliminacion = ref(false)
const proveedor = ref(null) 
const editado = ref({})
const mensaje = ref('')
const mensajeError = ref(false)

const route = useRoute()
const router = useRouter()
const id = route.params.id // El ID del proveedor vendrá de la URL

onMounted(async () => {
  try {
    const config = useRuntimeConfig();
    // Endpoint para obtener un proveedor por ID
    const res = await fetch(`${config.public.apiBase}/api/suppliers/${id}`)
    if (!res.ok) throw new Error('Proveedor no encontrado')
    const data = await res.json()
    editado.value = { ...data } // Carga los datos del proveedor para editar
    proveedor.value = data // Almacena los datos originales del proveedor
  } catch (error) {
    console.error('Error al cargar proveedor:', error)
    mensaje.value = 'Error al cargar los datos del proveedor.'
    mensajeError.value = true
  }
})

const guardarCambios = async () => {
  const soloNumeros = /^[0-9]+$/
  if (soloNumeros.test(editado.value.name.trim())) {
    mensaje.value = 'El nombre del proveedor no puede ser solo números.'
    mensajeError.value = true
    return
  }

  try {
    const config = useRuntimeConfig();
    // Endpoint para actualizar un proveedor por ID
    const res = await fetch(`${config.public.apiBase}/api/suppliers/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editado.value), // Envía los datos editados
    })
    if (!res.ok) {
        const errorData = await res.json().catch(() => ({ message: 'Error desconocido al guardar.' }));
        throw new Error(errorData.message || 'Error al guardar los cambios');
    }
    mensaje.value = 'Proveedor actualizado correctamente'
    mensajeError.value = false
    proveedor.value = { ...editado.value } // Actualiza los datos originales con los cambios
  } catch (err) {
    console.error('Error al guardar:', err)
    mensaje.value = err.message
    mensajeError.value = true
  }
}

const eliminarProveedor = async () => { 
  if (!confirmarEliminacion.value) {
    confirmarEliminacion.value = true
    return
  }

  try {
    const config = useRuntimeConfig();
    // Endpoint para eliminar un proveedor por ID
    const res = await fetch(`${config.public.apiBase}/api/suppliers/${id}`, {
      method: 'DELETE',
    })
    if (!res.ok) {
        const errorData = await res.json().catch(() => ({ message: 'Error desconocido al eliminar.' }));
        throw new Error(errorData.message || 'Error al eliminar el proveedor');
    }
    alert('Proveedor eliminado correctamente')
    router.push('/proveedores') // Redirige a la lista de proveedores
  } catch (err) {
    console.error('Error al eliminar:', err)
    alert(err.message || 'Error al eliminar el proveedor')
  }
}
</script>

<style scoped>
/* Los estilos existentes son perfectamente reutilizables */
</style>