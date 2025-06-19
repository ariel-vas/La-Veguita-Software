<template>
  <div class="flex flex-col items-center justify-center gap-6 bg-[#f5f5f5] p-8 mt-0">
    <h1 class="text-4xl font-bold text-[#8bc34a]">Editar Subcategoría</h1>

    <div v-if="subcategoria" class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl space-y-6">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-start">
        <label class="font-semibold">Nombre:</label>
        <input
          v-model="editado.name"
          type="text"
          class="border border-gray-300 rounded px-3 py-1 w-full sm:col-span-2"
          placeholder="Nombre de la subcategoría"
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
          @click="eliminarSubcategoria"
          class="bg-red-500 text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
        >
          {{ confirmarEliminacion ? 'Confirmar eliminación' : 'Eliminar Subcategoría' }}
        </button>
      </div>

      <p v-if="confirmarEliminacion" class="text-sm text-red-700 text-center mt-2 max-w-md">
        Esta acción eliminará la subcategoría y la desvinculará de todos los productos asociados. Haz clic nuevamente para confirmar.
      </p>
    </div>

    <div v-else class="text-gray-600 text-lg">Cargando subcategoría...</div>

    <button
      @click="$router.push('/subcategorias')"
      class="bg-[#ff9800] text-white py-2 px-6 rounded-xl text-lg hover:bg-opacity-90 transition duration-300"
    >
      Volver atrás
    </button>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const subcategoria = ref(null)
const editado = ref({})
const confirmarEliminacion = ref(false)

const route = useRoute()
const router = useRouter()
const id = route.params.id

onMounted(async () => {
  try {
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBase}/api/subcategories/${id}`)
    if (!res.ok) throw new Error('Subcategoría no encontrada')
    const data = await res.json()
    editado.value = { ...data }
    subcategoria.value = data
  } catch (error) {
    console.error('Error al cargar subcategoría:', error)
  }
})

const guardarCambios = async () => {
  try {
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBase}/api/subcategories/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editado.value),
    })
    if (!res.ok) throw new Error('Error al guardar los cambios')
    alert('Subcategoría actualizada correctamente')
    subcategoria.value = { ...editado.value }
  } catch (err) {
    console.error('Error al guardar:', err)
    alert('Error al guardar los cambios')
  }
}

const eliminarSubcategoria = async () => {
  if (!confirmarEliminacion.value) {
    confirmarEliminacion.value = true
    return
  }

  try {
    const config = useRuntimeConfig();
    const res = await fetch(`${config.public.apiBase}/api/subcategories/${id}`, {
      method: 'DELETE',
    })
    if (!res.ok) throw new Error('Error al eliminar subcategoría')
    alert('Subcategoría eliminada correctamente')
    router.push('/subcategorias')
  } catch (err) {
    console.error('Error al eliminar:', err)
    alert('Error al eliminar la subcategoría')
  }
}
</script>