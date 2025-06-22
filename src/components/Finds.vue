<!--Funds.vue-->
<template>
  <div class="finds-container h-full flex flex-col">
    <!-- 🔒 Фиксированная шапка -->
    <div class="sticky top-0 z-10 bg-[var(--page-bg-color)] px-3 py-4 border-b border-[#2c2c3a]">
      <div class="flex items-center justify-between">
        <span class="text-lg font-bold">Finds</span>
        <span class="text-2xl font-extrabold">1chn</span>
        <button class="text-purple-400 text-sm font-bold flex items-center gap-1">
          <span>Filters</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 🔁 Прокручиваемый контент -->
    <div class="flex-1 overflow-y-auto px-3 pb-2 space-y-4">
      <div v-if="error" class="text-center text-red-500 py-10">
        Не удалось загрузить товары дня. Попробуйте позже.
      </div>
      <div v-else-if="loading" class="text-center text-gray-400 py-10">Загрузка...</div>
      <div v-else-if="!finds.length" class="text-center text-gray-500 py-10">
        Сегодня пока нет новых товаров
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="f in finds"
          :key="f.id"
          class="find-card relative bg-[#222227] rounded-2xl px-3 py-3 flex items-center gap-3 shadow-sm"
        >
          <!-- Статус -->
          <div v-if="f.badge" class="absolute left-2 top-2 z-10">
            <span v-if="f.badge === 'NEW'" class="inline-block bg-blue-800 text-xs text-white rounded-lg px-2 py-0.5 font-bold">NEW</span>
            <span v-else-if="f.badge === 'HOT'" class="inline-block bg-orange-700 text-xs text-white rounded-lg px-2 py-0.5 font-bold">🔥</span>
            <span v-else-if="f.badge === 'GOLD'" class="inline-block bg-yellow-500 text-xs text-black rounded-lg px-2 py-0.5 font-bold">$</span>
          </div>

          <!-- Фото -->
          <img :src="f.photo_url" alt="" class="w-16 h-16 rounded-xl object-cover bg-[#111]" />

          <!-- Описание -->
          <div class="flex-1 min-w-0">
            <div class="font-bold text-base text-white truncate">{{ f.name }}</div>
            <div class="text-xs text-gray-400 mb-1 truncate">{{ f.desc }}</div>
            <div class="text-[#6e9fff] text-lg font-extrabold">
              {{ f.price ? formatR(f.price) : '—' }}
            </div>
          </div>

          <!-- Кнопки -->
          <div class="flex flex-col items-end justify-between h-full min-w-[32px] gap-3">
            <button @click="openSupplier(f.supplier_id)" class="rounded-full p-2 text-white bg-[#353666] hover:bg-[#5567c9]">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
              </svg>
            </button>
            <button class="like-btn" @click="toggleFav(f)">
              <svg v-if="f.fav" class="w-5 h-5" fill="#a5b4fc" viewBox="0 0 20 20">
                <path d="M3.172 5.172a4 4 0 0 1 5.656 0l.172.172.172-.172a4 4 0 1 1 5.656 5.656L10 17.657l-5.828-5.829a4 4 0 0 1 0-5.656z" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="#a5b4fc" stroke-width="1.5" viewBox="0 0 20 20">
                <path d="M3.172 5.172a4 4 0 0 1 5.656 0l.172.172.172-.172a4 4 0 1 1 5.656 5.656L10 17.657l-5.828-5.829a4 4 0 0 1 0-5.656z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { API_BASE } from '../api'

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
    const r = await fetch(`${API_BASE}/finds`)
    if (r.ok) {
      finds.value = (await r.json()).map(f => ({
        ...f,
        fav: false, // инициализация лайка
        badge: f.badge || null // badge: 'NEW' | 'HOT' | 'GOLD'
      }))
    } else {
      error.value = true
    }
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
        if (window.applySafeInsets) window.applySafeInsets()
  }
}

function toggleFav(f) {
  f.fav = !f.fav
}

async function openSupplier(id) {
  try {
    const info = await fetch(`${API_BASE}/suppliers/${id}`)
    if (info.ok) {
      await info.json()
    }
    const cont = await fetch(`${API_BASE}/suppliers/${id}/contacts`)
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
