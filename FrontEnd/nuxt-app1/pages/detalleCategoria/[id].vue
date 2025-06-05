<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 pt-0 mt-16">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Detalle Categoría</h1>

    <div v-if="categoria" class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl space-y-6">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-start">
        <label class="font-semibold">Nombre:</label>
        <input
          v-model="editado.name"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2"
          placeholder="Nombre de la categoría"
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
          @click="eliminarCategoria"
          class="bg-red-500 text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
        >
          {{ confirmarEliminacion ? 'Confirmar eliminación' : 'Eliminar Categoría' }}
        </button>
      </div>

      <p v-if="confirmarEliminacion" class="text-sm text-red-700 text-center mt-2 max-w-md">
        Esta acción eliminará la categoría y la desvinculará de todos los productos asociados. Haz clic nuevamente para confirmar.
      </p>

      <div v-if="mensaje" :class="mensajeError ? 'text-red-600' : 'text-green-600'" class="text-center font-semibold">
        {{ mensaje }}
      </div>
    </div>

    <div v-else class="text-gray-600 text-lg">Cargando categoría...</div>

    <button
      @click="$router.push('/categorias')"
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
const categoria = ref(null)
const editado = ref({})
const mensaje = ref('')
const mensajeError = ref(false)

const route = useRoute()
const router = useRouter()
const id = route.params.id

onMounted(async () => {
  try {
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBase}/api/categories/${id}`)
    if (!res.ok) throw new Error('Categoría no encontrada')
    const data = await res.json()
    editado.value = { ...data }
    categoria.value = data
  } catch (error) {
    console.error('Error al cargar categoría:', error)
  }
})

const guardarCambios = async () => {
  const soloNumeros = /^[0-9]+$/
  if (soloNumeros.test(editado.value.name.trim())) {
    mensaje.value = 'El nombre no puede ser solo números.'
    mensajeError.value = true
    return
  }

  try {
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBase}/api/categories/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editado.value),
    })
    if (!res.ok) throw new Error('Error al guardar los cambios')
    mensaje.value = 'Categoría actualizada correctamente'
    mensajeError.value = false
    categoria.value = { ...editado.value }
  } catch (err) {
    console.error('Error al guardar:', err)
    mensaje.value = 'Error al guardar los cambios'
    mensajeError.value = true
  }
}

const eliminarCategoria = async () => {
  if (!confirmarEliminacion.value) {
    confirmarEliminacion.value = true
    return
  }

  try {
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBase}/api/categories/${id}`, {
      method: 'DELETE',
    })
    if (!res.ok) throw new Error('Error al eliminar categoría')
    alert('Categoría eliminada correctamente')
    router.push('/categorias')
  } catch (err) {
    console.error('Error al eliminar:', err)
    alert('Error al eliminar la categoría')
  }
}
</script>