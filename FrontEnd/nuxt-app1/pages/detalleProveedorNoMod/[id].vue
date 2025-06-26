<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 mt-0">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Información del Proveedor</h1>

    <div v-if="editado" class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl">
      <table class="w-full text-left text-gray-800">
        <tbody>
          <tr><td class="font-semibold py-2">RUT:</td><td>{{ editado.rut }}</td></tr>
          <tr><td class="font-semibold py-2">Nombre:</td><td>{{ editado.name }}</td></tr>
          <tr><td class="font-semibold py-2">Giro:</td><td>{{ editado.line }}</td></tr>
          <tr><td class="font-semibold py-2">Dirección:</td><td>{{ editado.address }}</td></tr>
          <tr><td class="font-semibold py-2">Comuna:</td><td>{{ editado.commune }}</td></tr>
          <tr><td class="font-semibold py-2">Ciudad:</td><td>{{ editado.city }}</td></tr>
          <tr><td class="font-semibold py-2">Teléfono fijo:</td><td>{{ editado.telephone || 'No informado' }}</td></tr>
          <tr><td class="font-semibold py-2">Celular:</td><td>{{ editado.cellphone || 'No informado' }}</td></tr>
          <tr><td class="font-semibold py-2">Correo:</td><td>{{ editado.email || 'No informado' }}</td></tr>
          <tr>
            <td class="font-semibold pt-6 align-top">Contactar:</td>
            <td class="pt-6">
              <div class="flex flex-col gap-3 w-full">
                <!-- WhatsApp -->
                <a
                  :href="editado.cellphone ? `https://wa.me/${editado.cellphone}` : '#'"
                  target="_blank"
                  class="flex items-center justify-center gap-2 bg-green-500 text-white text-lg py-3 px-6 rounded-lg hover:bg-green-600 transition w-full sm:w-auto text-center"
                  :class="{ 'opacity-50 cursor-not-allowed': !editado.cellphone }"
                  :disabled="!editado.cellphone"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.5 3.5A11.8 11.8 0 0 0 12 0a12 12 0 0 0-10.4 18L0 24l6.3-1.7A12 12 0 0 0 12 24a11.8 11.8 0 0 0 8.5-3.5A12 12 0 0 0 24 12a11.8 11.8 0 0 0-3.5-8.5Zm-8.5 18a9.9 9.9 0 0 1-5.1-1.4l-.4-.3-3.7 1 1-3.6-.3-.4a10 10 0 1 1 8.5 4.7Zm5.5-7c-.3-.2-1.6-.8-1.8-.9s-.4-.2-.6.2-.7.9-.9 1c-.2.1-.4.1-.7 0a7.9 7.9 0 0 1-2.3-1.4 8.6 8.6 0 0 1-1.6-2c-.2-.4 0-.6.1-.8l.4-.5c.1-.2.2-.4.4-.6a.7.7 0 0 0 0-.7c-.1-.2-.7-1.7-1-2.3s-.6-.5-.8-.5h-.6a1.2 1.2 0 0 0-1 .4 4 4 0 0 0-1.3 3c0 .3.1.7.2 1a12.1 12.1 0 0 0 2.3 4 11.6 11.6 0 0 0 4.3 3.3c.6.3 1.2.5 1.7.6a4 4 0 0 0 1.6.1c.5-.1 1.6-.6 1.9-1.2s.3-1.1.2-1.2-.3-.2-.6-.3Z"/>
                  </svg>
                  WhatsApp
                </a>
              
                <!-- Correo -->
                <a
                  :href="editado.email ? `mailto:${editado.email}` : '#'"
                  class="flex items-center justify-center gap-2 bg-blue-500 text-white text-lg py-3 px-6 rounded-lg hover:bg-blue-600 transition w-full sm:w-auto text-center"
                  :class="{ 'opacity-50 cursor-not-allowed': !editado.email }"
                  :disabled="!editado.email"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M4 4h16v16H4z" stroke="none"/><path d="m4 4 8 8 8-8" />
                  </svg>
                  Correo
                </a>
              
                <!-- Llamar -->
                <a
                  :href="editado.telephone ? `tel:${editado.telephone}` : '#'"
                  class="flex items-center justify-center gap-2 bg-indigo-500 text-white text-lg py-3 px-6 rounded-lg hover:bg-indigo-600 transition w-full sm:w-auto text-center"
                  :class="{ 'opacity-50 cursor-not-allowed': !editado.telephone }"
                  :disabled="!editado.telephone"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2A19.8 19.8 0 0 1 3.1 5.18 2 2 0 0 1 5 3h3a2 2 0 0 1 2 1.72 12.4 12.4 0 0 0 .57 2.57 2 2 0 0 1-.45 2L9 11a16 16 0 0 0 4.9 4.9l1.71-1.11a2 2 0 0 1 2 .45 12.4 12.4 0 0 0 2.57.57A2 2 0 0 1 22 16.92z"/>
                  </svg>
                  Llamar
                </a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="mensaje" :class="mensajeError ? 'text-red-600' : 'text-green-600'" class="text-center font-semibold mt-4">
        {{ mensaje }}
      </div>
    </div>

    <div v-else class="text-gray-600 text-lg">Cargando proveedor...</div>

    <button
      @click="$router.push('/proveedores')"
      class="mt-6 bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
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