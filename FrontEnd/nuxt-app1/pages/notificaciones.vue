<template>
  <div class="mt-0 p-6 max-w-6xl mx-auto">
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-[#8bc34a] mb-5 sm:mb-4 md:mb-6 lg:mb-10">Notificaciones</h1>

    <div v-for="estado in ['pending', 'posponed', 'ready']" :key="estado" class="mb-8">
      <h2 class="text-xl sm:text-xl md:text-xl lg:text-2xl font-bold text-orange-700 mb-4">
        {{ estadoLabels[estado] }}
      </h2>

      <div v-if="filtradasPorEstado(estado).length > 0" class="space-y-4">
        <div
          v-for="noti in filtradasPorEstado(estado)"
          :key="noti.id_notification"
          :class="[
            'p-4 rounded shadow border-l-4 transition-colors duration-300 left-0',
            estado === 'pending' ? 'bg-gray-100 text-gray-700 border-gray-400' :
            estado === 'posponed' ? 'bg-orange-100 text-orange-700 border-orange-500' :
            'bg-green-100 text-green-700 border-green-500'
          ]"
        >
          <!-- Botón eliminar -->
          <button
            v-if="estado === 'ready'"
            @click="eliminarNotificacion(noti.id_notification)"
            class="absolute top-2 right-2 text-red-500 hover:text-red-700 text-lg font-bold"
            title="Eliminar notificación"
          >
            ✘
          </button>

          <p class="font-bold max-w-[500px] truncate whitespace-nowrap overflow-hidden">{{ noti.name_product }}</p>
          <p>Fecha de vencimiento: {{ new Date(noti.expiration_date).toLocaleDateString() }}</p>
          <p v-if="estado === 'ready'">Fecha de Visado: {{ new Date(noti.date_of_completion).toLocaleDateString() }}</p>

          <div v-if="noti.batchDetails && noti.batchDetails.length > 0" class="mt-2 text-sm">
            <p class="font-semibold">Lotes:</p>
            <ul class="list-disc ml-5">
              <li
                v-for="batch in noti.batchDetails"
                :key="batch.id_batch"
              >
                {{ batch.unit === 'kilo' ? parseFloat(batch.quantity).toFixed(3) + ' Kilos' : parseInt(batch.quantity) + ' Unidades' }}
              </li>
            </ul>
          </div>

          <!-- BOTONES DE ACCIÓN -->
          <div v-if="estado !== 'ready'" class="mt-4 flex gap-3">
            <button
              @click="actualizarEstado(noti.id_notification, 'ready')"
              class="px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-sm"
            >
              ✅ Marcar como completada
            </button>

            <button
              v-if="estado === 'pending'"
              @click="actualizarEstado(noti.id_notification, 'posponed')"
              class="px-3 py-1 bg-orange-500 hover:bg-orange-600 text-white rounded text-sm"
            >
              🕓 Posponer
            </button>
          </div>
        </div>
      </div>

      <p v-else class="text-gray-400">No hay notificaciones en este estado.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const notificaciones = ref([])

const estadoLabels = {
  pending: 'Pendientes',
  posponed: 'Pospuestas',
  ready: 'Completadas'
}

const filtradasPorEstado = (estado) => {
  return notificaciones.value.filter(n => n.state === estado)
}

const cargarNotificaciones = async () => {
  try {
    const config = useRuntimeConfig()
    const res = await fetch(`${config.public.apiBase}/api/notifications/`)
    const data = await res.json()

    const withBatches = await Promise.all(data.map(async (n) => {
      try {
        const batchRes = await fetch(`${config.public.apiBase}/api/batches/${n.id_notification}`)
        const batchData = await batchRes.json()
        return {
          ...n,
          batchDetails: Array.isArray(batchData)
            ? batchData.filter(b => b && b.quantity != null && b.unit)
            : (batchData && batchData.quantity != null && batchData.unit ? [batchData] : [])
        }

      } catch {
        return { ...n, batchDetails: [] }
      }
    }))

    notificaciones.value = withBatches
  } catch (error) {
    console.error('Error al cargar notificaciones:', error)
  }
}

const actualizarEstado = async (id, nuevoEstado) => {
  try {
    const fecha = new Date().toISOString()
    const config = useRuntimeConfig()

    await fetch(`${config.public.apiBase}/api/notifications/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        state: nuevoEstado,
        date_of_completion: nuevoEstado === 'ready' ? fecha : null
      })
    })

    await cargarNotificaciones()
  } catch (error) {
    console.error(`Error al actualizar notificación ${id}:`, error)
  }
}

const eliminarNotificacion = async (id) => {
  if (!confirm('¿Estás seguro de que querés eliminar esta notificación completada?')) return

  try {
    const config = useRuntimeConfig()
    const res = await fetch(`${config.public.apiBase}/api/notifications/${id}`, {
      method: 'DELETE'
    })

    if (!res.ok) {
      console.error('Error al eliminar notificación:', await res.text())
      alert('Ocurrió un error al eliminar la notificación.')
      return
    }

    await cargarNotificaciones()
  } catch (error) {
    console.error('Error al eliminar notificación:', error)
  }
}

onMounted(() => {
  cargarNotificaciones()
})
</script>
