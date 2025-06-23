<!--Suppliers.vue-->
<template>
  <div class="h-full flex flex-col space-y-1 p-2">
    <!-- 🔒 Фиксированная шапка -->
    <div class="sticky top-0 z-10 bg-[var(--page-bg-color)] space-y-3 px-3 py-4 border-b border-[#2c2c3a]">
      <div class="relative flex items-center justify-between">
        <span class="text-lg font-bold text-white">Suppliers</span>

        <!-- Центрированный заголовок -->
        <div class="absolute left-1/2 transform -translate-x-1/2 flex flex-col items-center">
          <span class="text-2xl font-extrabold text-white">1chn</span>
          <span class="text-sm text-gray-400">[ван чан]</span>
        </div>

        <!-- Сердце с счётчиком -->
        <div class="relative w-6 h-6">
          <svg
            @click="showFavOnly = !showFavOnly"
            class="heart-icon"
            :class="showFavOnly ? 'heart-active' : 'heart-inactive'"
            viewBox="0 0 24 24"
          >
            <path
              d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5
              2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09
              C13.09 3.81 14.76 3 16.5 3
              19.58 3 22 5.42 22 8.5
              c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
            />
          </svg>
          <span
            class="absolute -bottom-1 -right-2 bg-black text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center border border-white"
          >
            {{ favoritesCount }}
          </span>
        </div>
      </div>

      <!-- Кнопка фильтра -->
      <div class="mt-3">
        <button
          @click="filtersOpen = !filtersOpen"
          class="w-full bg-purple-700 text-white font-semibold py-1 rounded text-sm"
        >
          Filters
          <span :class="filtersOpen ? 'rotate-180' : ''" class="inline-block transition-transform ml-1">▼</span>
        </button>
      </div>

      <!-- Выпадающие фильтры -->
      <transition name="fade">
        <div v-if="filtersOpen" class="px-1 py-3 bg-[var(--page-bg-color)] space-y-3 border-b border-[#2c2c3a]">
          <div>
            <div class="text-sm mb-1 text-white">Категория</div>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="c in categories"
                :key="c"
                @click="toggleCat(c)"
                :class="[
                  'px-3 py-1 rounded-full text-sm border',
                  selectedCat.includes(c) ? 'bg-blue-600 text-white' : 'bg-gray-700 text-white'
                ]"
              >
                {{ c }}
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- 📦 Список поставщиков -->
    <div class="flex-1 overflow-y-auto scrollbar-hide">
      <div v-if="!suppliers.length" class="text-center text-gray-500 py-10">Нет результатов</div>
      <div v-else class="space-y-4">
        <div v-for="s in suppliers" :key="s.id" class="bg-gray-800 p-4 rounded flex items-center">
          <img :src="s.photo_url" class="w-12 h-12 rounded-full object-cover mr-3" />
          <div class="flex-1">
            <div class="font-semibold text-white">{{ s.name }}</div>
            <div class="text-sm text-gray-400">{{ s.description }}</div>
            <div class="flex flex-wrap gap-1 mt-1">
              <span v-for="cat in s.categories" :key="cat" class="text-xs text-purple-400">{{ cat }}</span>
            </div>
          </div>
          <!-- Сердце внутри карточки -->
          <button @click="toggleFavorite(s)" class="relative w-6 h-6 mr-3">
            <svg
              class="heart-icon"
              :class="s.is_favorite ? 'heart-active' : 'heart-inactive'"
              viewBox="0 0 24 24"
            >
              <path
                d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5
                2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09
                C13.09 3.81 14.76 3 16.5 3
                19.58 3 22 5.42 22 8.5
                c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
              />
            </svg>
          </button>
          <button @click="openContacts(s)" class="bg-blue-600 text-white px-3 py-1 rounded text-sm">Контакт</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { userData } from '../state'
import { API_BASE } from '../api'

const categories = ref([])
const selectedCat = ref([])
const suppliers = ref([])
const showFavOnly = ref(false)
const filtersOpen = ref(false)

const favoritesCount = computed(() =>
  suppliers.value.filter(s => s.is_favorite).length
)

function toggleCat(c) {
  const idx = selectedCat.value.indexOf(c)
  if (idx >= 0) selectedCat.value.splice(idx, 1)
  else selectedCat.value.push(c)
}

async function loadCategories() {
  try {
    const r = await fetch(`${API_BASE}/suppliers/categories`)
    if (r.ok) categories.value = await r.json()
  } catch (e) {
    console.error(e)
  }
}

async function loadSuppliers() {
  if (!userData.user.id) return
  try {
    const p1 = selectedCat.value.join(',')
    const fav = showFavOnly.value ? 'true' : 'false'
    const uid = userData.user.id
    const url = `${API_BASE}/suppliers?user_id=${uid}&categories=${encodeURIComponent(p1)}&favorites_only=${fav}`
    const r = await fetch(url)
    if (r.ok) suppliers.value = await r.json()
  } catch (e) {
    console.error(e)
  } finally {
    if (window.applySafeInsets) window.applySafeInsets()
  }
}

async function toggleFavorite(s) {
  try {
    const r = await fetch(`${API_BASE}/suppliers/${s.id}/favorite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userData.user.id })
    })
    if (r.ok) {
      const data = await r.json()
      s.is_favorite = data.favorite
    }
  } catch (e) {
    console.error(e)
  }
}

async function openContacts(s) {
  try {
    const r = await fetch(`${API_BASE}/suppliers/${s.id}/contacts`)
    if (r.ok) {
      const data = await r.json()
      const info = { ...s, ...data }
      if (window.showSupplierModal) window.showSupplierModal(info)
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadCategories()
  loadSuppliers()
})

watch(() => userData.user.id, id => {
  if (id) loadSuppliers()
})

watch([selectedCat, showFavOnly], loadSuppliers, { deep: true })
</script>


