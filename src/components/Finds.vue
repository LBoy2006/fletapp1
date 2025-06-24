<!--Funds.vue-->
<template>
  <div class="h-full flex flex-col space-y-1 p-2">
    <!-- 🔒 Фиксированная шапка -->
    <div class="sticky top-0 z-10 bg-[var(--page-bg-color)] space-y-3 px-3 py-4 border-b border-[#2c2c3a] relative overflow-visible">
      <div class="relative flex items-center justify-between">
        <span class="text-lg font-bold text-white">Finds</span>

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
  <div
    v-if="filtersOpen"
    class="absolute left-0 top-full w-full px-1 py-3 bg-[rgba(16,16,17,0.9)] space-y-3 border-b border-[#2c2c3a] z-20 max-h-[50vh] overflow-y-auto scrollbar-hide"
  >
    <!-- Цена -->
    <div class="flex gap-2">
      <div class="flex flex-col flex-1">
        <label class="text-xs text-white">Цена от</label>
        <input type="number" v-model.number="priceMin" class="bg-gray-700 text-white text-xs px-2 py-1 rounded" /></div>
      <div class="flex flex-col flex-1">
        <label class="text-xs text-white">до</label>
        <input type="number" v-model.number="priceMax" class="bg-gray-700 text-white text-xs px-2 py-1 rounded" />
      </div>
    </div>

    <!-- Категории -->
    <div>
      <div class="text-xs mb-1 text-white text-center">Категория</div>
      <div class="flex flex-wrap justify-center gap-2">
        <button
          v-for="c in categories"
          :key="c"
          @click="toggleCategory(c)"
          :class="[
            'px-3 py-1 rounded-full text-xs border',
            selectedCategories.includes(c) ? 'bg-blue-600 text-white' : 'bg-gray-700 text-white'
          ]"
        >
          {{ c }}
        </button>
      </div>
    </div>

    <!-- Бренды -->
    <div>
      <div class="text-xs mb-1 text-white text-center">Бренд</div>
      <div class="flex flex-wrap justify-center gap-2">
        <button
          v-for="b in brands"
          :key="b"
          @click="toggleBrand(b)"
          :class="[
            'px-3 py-1 rounded-full text-xs border',
            selectedBrands.includes(b) ? 'bg-blue-600 text-white' : 'bg-gray-700 text-white'
          ]"
        >
          {{ b }}
        </button>
      </div>
    </div>
  </div>
</transition>

    </div>

    <!-- 🔁 Прокручиваемый контент -->
    <div class="flex-1 overflow-y-auto px-3 pb-2 space-y-4 scrollbar-hide">
      <div v-if="error" class="text-center text-red-500 py-10">
        Не удалось загрузить товары дня. Попробуйте позже.
      </div>
      <div v-else-if="loading" class="text-center text-gray-400 py-10">Загрузка...</div>
      <div v-else-if="!displayedFinds.length" class="text-center text-gray-500 py-10">
        Сегодня пока нет новых товаров
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="f in displayedFinds"
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
          <div class="relative">
            <img :src="f.photo_url" alt="" class="w-16 h-16 rounded-xl object-cover bg-[#111]" />
            <div class="absolute top-0 right-0 flex gap-0.5 text-[13px]">
              <span v-if="f.is_hot">🔥</span>
              <span v-if="f.is_new">🆕</span>
              <span v-if="f.is_high_margin">💰</span>
            </div>
          </div>

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
            <button @click="openItem(f)" class="rounded-full p-2 text-white bg-[#353666] hover:bg-[#5567c9]">
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
import { ref, computed, onMounted, watch } from 'vue'
import { userData } from '../state'
import { API_BASE } from '../api'

const finds = ref([])
const loading = ref(true)
const error = ref(false)
const categories = ref([])
const brands = ref([])
const selectedCategories = ref([])
const selectedBrands = ref([])
const showFavOnly = ref(false)
const filtersOpen = ref(false)
const priceMin = ref(null)
const priceMax = ref(null)

const favoritesCount = computed(() => finds.value.filter(f => f.fav).length)
const displayedFinds = computed(() =>
  showFavOnly.value ? finds.value.filter(f => f.fav) : finds.value
)

function toggleCategory(c) {
  const idx = selectedCategories.value.indexOf(c)
  if (idx >= 0) selectedCategories.value.splice(idx, 1)
  else selectedCategories.value.push(c)
}

function toggleBrand(c) {
  const idx = selectedBrands.value.indexOf(c)
  if (idx >= 0) selectedBrands.value.splice(idx, 1)
  else selectedBrands.value.push(c)
}

async function loadCategories() {
  try {
    const r = await fetch(`${API_BASE}/finds/categories`)
    if (r.ok) categories.value = await r.json()
  } catch (e) {
    console.error(e)
  }
}

async function loadBrands() {
  try {
    const params = selectedCategories.value.join(',')
    const r = await fetch(`${API_BASE}/finds/brands?categories=${encodeURIComponent(params)}`)
    if (r.ok) brands.value = await r.json()
  } catch (e) {
    console.error(e)
  }
}

function formatR(val) {
  if (val === undefined || val === null) return '—'
  return new Intl.NumberFormat('ru-RU').format(val) + ' ₽'
}

async function loadFinds() {
  if (!userData.user.id) return
  loading.value = true
  error.value = false
  try {
    const p1 = selectedCategories.value.join(',')
    const p2 = selectedBrands.value.join(',')
    const fav = showFavOnly.value ? 'true' : 'false'
    const uid = userData.user.id
    let url = `${API_BASE}/finds?user_id=${uid}&categories=${encodeURIComponent(p1)}&brands=${encodeURIComponent(p2)}&favorites_only=${fav}`
    if (priceMin.value !== null) url += `&price_min=${priceMin.value}`
    if (priceMax.value !== null) url += `&price_max=${priceMax.value}`
    const r = await fetch(url)
    if (r.ok) {
      finds.value = (await r.json()).map(f => ({
        ...f,
        fav: f.is_favorite || false,
        badge: f.badge || null
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

async function toggleFav(f) {
  try {
    const r = await fetch(`${API_BASE}/finds/${f.id}/favorite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userData.user.id })
    })
    if (r.ok) {
      const data = await r.json()
      f.fav = data.favorite
    }
  } catch (e) {
    console.error(e)
  }
}

function openItem(item) {
  if (window.showItemModal) window.showItemModal(item)
}

async function openSupplier(id) {
  try {
    let sData = {}
    const info = await fetch(`${API_BASE}/suppliers/${id}`)
    if (info.ok) {
      sData = await info.json()
    }
    const cont = await fetch(`${API_BASE}/suppliers/${id}/contacts`)
    if (cont.ok) {
      const c = await cont.json()
      const modalData = { ...sData, ...c }
      if (window.showSupplierModal) window.showSupplierModal(modalData)
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadCategories()
  loadBrands()
  loadFinds()
})

watch(() => userData.user.id, id => {
  if (id) loadFinds()
})

watch(selectedCategories, () => {
  loadBrands()
  loadFinds()
}, { deep: true })

watch([selectedBrands, showFavOnly], loadFinds, { deep: true })
watch([priceMin, priceMax], loadFinds)
</script>
