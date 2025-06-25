<!--Funds.vue-->
<template>
  <div class="h-full flex flex-col space-y-1 p-2">
    <!-- 🔒 Фиксированная шапка -->
    <div class="sticky top-0 z-10 bg-[var(--page-bg-color)] px-0 py-4 pb-0 relative overflow-visible space-y-3">
      <div class="relative flex items-center justify-between px-3">
        <span class="text-lg font-bold text-white">Finds</span>

        <!-- Центрированный заголовок -->
        <div class="absolute left-1/2 transform -translate-x-1/2 flex flex-col items-center">
          <span class="text-2xl font-dela text-white">1chn</span>
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
            class="absolute -bottom-1 -right-1 font-dela text-white text-[12px] rounded-full w-4 h-4 flex items-center justify-center"
          >
            {{ favoritesCount }}
          </span>
        </div>
      </div>

      <!-- Кнопка фильтра -->
      <div class="mt-3 py-2">
        <button
          @click="filtersOpen = !filtersOpen"
          class="w-full bg-[#3B366B] text-white py-1 rounded-xl text-sm"
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
      <div class="flex flex-wrap gap-2 justify-center">
        <button
          v-for="c in categories"
          :key="c"
          @click="toggleCategory(c)"
          :class="[
            'px-3 py-1 rounded-full text-xs border border-[0.5px] border-[#424242]',
            selectedCategories.includes(c) ? 'bg-[#5E56A5] text-white' : 'bg-[#191919] text-gray-500'
          ]"
        >
          {{ c }}
        </button>
      </div>
    </div>

    <!-- Бренды -->
    <div>
      <div class="text-xs mb-1 text-white text-center">Бренд</div>
      <div class="flex flex-wrap gap-2 justify-center">
        <button
          v-for="b in brands"
          :key="b"
          @click="toggleBrand(b)"
          :class="[
            'px-3 py-1 rounded-full text-xs border border-[0.5px] border-[#424242]',
            selectedBrands.includes(b) ? 'bg-[#5E56A5] text-white' : 'bg-[#191919] text-gray-500'
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
    <div class="flex-1 overflow-y-auto scrollbar-hide font-sans">
      <div v-if="error" class="text-center text-red-500 py-10">
        Не удалось загрузить товары дня. Попробуйте позже.
      </div>
      <div v-else-if="loading" class="text-center text-gray-400 py-10">Загрузка...</div>
      <div v-else-if="!displayedFinds.length" class="text-center text-gray-500 py-10">
        Сегодня пока нет новых товаров
      </div>
      <div v-else class="space-y-2">
        <div
          v-for="f in displayedFinds"
          :key="f.id"
          class="card-items  card-base flex m-0 items-center pl-1 pr-3 py-1"
        >

          <!-- Фото -->
          <div class="relative">
            <img :src="f.photo_url" alt="" class="w-24 h-24 rounded-xl object-cover border border border-[0.5px] border-[#424242] m-0 mr-2 " />
            <div class="absolute -top-1 -left-1 flex -gap-1 text-[20px] mx-0">
              <span v-if="f.is_hot">🔥</span>
              <span v-if="f.is_new" >🆕</span>
              <span v-if="f.is_high_margin">💰</span>
            </div>
          </div>

          <!-- Описание -->
          <div class="flex-1 min-w-0 pl-2 h-full flex flex-col justify-between">
            <div>
            <div class="text-gray-400 text-lg font-bold leading-tight truncate">{{ f.name }}</div>
            <div class="text-xs text-gray-400 mt-0.5">В избранном {{ f.favorites_count || 0 }}</div>
  </div>
            <div class="text-sm text-gray-400 mt-1 truncate ">{{ f.description }}</div>
            <div class="flex flex-wrap gap-x-2 gap-y-0.5 mt-2 text-2xl text-[#5E56A5] font-sans font-bold">
              {{ f.price ? formatR(f.price) : '—' }}
            </div>
          </div>

          <!-- Кнопки -->
          <div class="flex flex-col gap-10">
            <button class="ml-auto" @click="toggleFav(f)">
              <svg
            width="24" height="24" viewBox="0 0 24 24" fill="none"
            :class="f.fav ? 'text-[#7A65FC]' : 'text-[#4B4B50]'"
          >  <path
              d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5
                2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09
                C13.09 3.81 14.76 3 16.5 3
                19.58 3 22 5.42 22 8.5
                c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
              :fill="f.fav ? '#5E56A5' : 'none'"
              :stroke="f.fav ? '#5E56A5' : '#4B4B50'"
              stroke-width="2"
            /> </svg>
            </button>
            <button @click="openItem(f)" class="ml-4">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4B4B50" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="4" y1="12" x2="19" y2="12"/>
  <polyline points="12 5 19 12 12 19"/>
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
      if (data.favorite) {
        f.favorites_count = (f.favorites_count || 0) + 1
      } else {
        f.favorites_count = Math.max(0, (f.favorites_count || 1) - 1)
      }
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
