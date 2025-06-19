<template>
  <div class="space-y-4 p-4">
    <h2 class="text-2xl font-bold text-center">Товары дня</h2>

    <div v-if="error" class="text-center text-red-500 py-10">
      Не удалось загрузить товары дня. Попробуйте позже.
    </div>
    <div v-else-if="loading" class="text-center text-gray-400 py-10">Загрузка...</div>
    <div v-else-if="!finds.length" class="text-center text-gray-500 py-10">
      Сегодня пока нет новых товаров
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="f in finds"
        :key="f.id"
        class="bg-gray-800 p-4 rounded"
      >
        <img
          :src="f.photo_url"
          alt=""
          class="w-full h-48 object-cover rounded mb-3"
        />
        <div class="font-semibold truncate mb-1">{{ f.name }}</div>
        <div class="text-lg font-bold mb-2">{{ formatR(f.price) }}</div>
        <button
          @click="openSupplier(f.supplier_id)"
          class="w-full bg-blue-600 text-white py-2 rounded text-sm"
        >
          Смотреть у поставщика
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineProps({ t: Object })

const finds = ref([])
const loading = ref(true)
const error = ref(false)

function formatR(val) {
  if (val === undefined || val === null) return '—'
  return new Intl.NumberFormat('ru-RU').format(val) + ' ₽'
}

async function loadFinds() {
  loading.value = true
  error.value = false
  try {
    const r = await fetch('http://localhost:8000/finds')
    if (r.ok) {
      finds.value = await r.json()
    } else {
      error.value = true
    }
  } catch (e) {
    console.error(e)
    error.value = true
  } finally {
    loading.value = false
  }
}

async function openSupplier(id) {
  try {
    const info = await fetch(`http://localhost:8000/suppliers/${id}`)
    if (info.ok) {
      await info.json()
    }
    const cont = await fetch(`http://localhost:8000/suppliers/${id}/contacts`)
    if (cont.ok) {
      const c = await cont.json()
      const lines = [
        `Ссылка: ${c.contact_link || '—'}`,
        `Телефон: ${c.contact_phone || '—'}`,
        `Пароль: ${c.contact_password || '—'}`
      ]
      if (window.showSheet) window.showSheet(lines)
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(loadFinds)
</script>
