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

    <transition name="modal-fade">
      <div
        v-if="supplierModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10"
        @click.self="closeSupplier"
      >
        <div
          class="p-4 rounded w-64 select-none"
          style="background-color: var(--page-bg-color); color: var(--text-color);"
          @contextmenu.prevent
          @copy.prevent
        >
          <div class="font-semibold mb-1">{{ supplier.name || 'Поставщик' }}</div>
          <div class="text-sm text-gray-400 mb-2">{{ supplier.description }}</div>
          <div class="space-y-1 text-sm">
            <div>
              <span class="text-gray-400">Ссылка:</span>
              {{ supplier.contact_link || '—' }}
            </div>
            <div>
              <span class="text-gray-400">Телефон:</span>
              {{ supplier.contact_phone || '—' }}
            </div>
            <div>
              <span class="text-gray-400">Пароль:</span>
              {{ supplier.contact_password || '—' }}
            </div>
          </div>
          <button
            @click="closeSupplier"
            class="mt-3 px-4 py-2 bg-blue-600 text-white rounded w-full"
          >
            Закрыть
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineProps({ t: Object })

const finds = ref([])
const loading = ref(true)
const error = ref(false)
const supplierModal = ref(false)
const supplier = ref({})

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
      supplier.value = await info.json()
    }
    const cont = await fetch(`http://localhost:8000/suppliers/${id}/contacts`)
    if (cont.ok) {
      const c = await cont.json()
      supplier.value = { ...supplier.value, ...c }
    }
    supplierModal.value = true
  } catch (e) {
    console.error(e)
  }
}

function closeSupplier() {
  supplierModal.value = false
  supplier.value = {}
}

onMounted(loadFinds)
</script>
