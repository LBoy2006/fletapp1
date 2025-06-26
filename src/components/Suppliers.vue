<!--Suppliers.vue-->
<template>
  <div class="h-full flex flex-col space-y-1 p-2">
    <!-- 🔒 Фиксированная шапка -->
    <div class="sticky top-0 z-10 bg-[var(--page-bg-color)] px-0 py-4 pb-0 relative overflow-visible">
      <div class="relative flex items-center justify-between px-3 ">
        <span class="text-lg font-bold text-white">Suppliers</span>

        <!-- Центрированный заголовок -->
        <div class="absolute left-1/2 transform -translate-x-1/2 flex flex-col items-center">
          <span class="text-2xl  font-dela text-white">1chn</span>
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
            class="absolute -bottom-1 -right-1 font-dela text-white text-[12px]
             rounded-full w-4 h-4 flex items-center justify-center"
          >
            {{ favoritesCount }}
          </span>
        </div>
      </div>

      <!-- Кнопка фильтра -->
      <div class="mt-3 py-2" ref="dropdownArea">
        <button
          @click="filtersOpen = !filtersOpen"
          class="w-full bg-[#3B366B] text-white py-1 rounded-xl text-sm "
        >
          Filters
          <span :class="filtersOpen ? 'rotate-180' : ''" class="inline-block transition-transform ml-1">▼</span>
        </button>


      <!-- Выпадающие фильтры -->
      <transition name="fade">
        <div
          v-if="filtersOpen"
          class="absolute left-0 top-full w-full px-1 py-3 bg-[rgba(16,16,17,0.9)] space-y-3 border-b border-[#2c2c3a] z-20"
        >
          <div>
             <div class="flex flex-wrap gap-2 justify-center">
              <button
                v-for="c in categories"
                :key="c"
                @click="toggleCat(c)"
                :class="[
                  'px-3 py-1 rounded-full text-xs border border-[0.5px] border-[#424242]',
                  selectedCat.includes(c) ? 'bg-[#5E56A5] text-white' : 'bg-[#191919] text-gray-500'
                ]"
              >
                {{ c }}
              </button>
            </div>
          </div>
        </div>
      </transition> </div>
    </div>

    <!-- 📦 Список поставщиков -->
    <div class="flex-1 overflow-y-auto scrollbar-hide font-sans">
      <div v-if="!displayedSuppliers.length" class="text-center text-gray-500 py-10">Нет результатов</div>
      <div v-else class="space-y-2">
  <div
    v-for="s in displayedSuppliers"
    :key="s.id"
    class="card-items  card-base flex m-0 items-center pl-1 pr-3 py-1"
  >
    <!-- Аватар -->
    <img
      :src="s.photo_url"
      class="w-24 h-24 rounded-full object-cover border border border-[0.5px] border-[#424242] m-0 mr-2 "
      alt="avatar"
    />
    <!-- Контент -->
<div class="flex-1 min-w-0 pl-2 h-full flex flex-col justify-between">
  <!-- Верх: имя и избрали -->
  <div>
    <div class="text-gray-400 text-lg font-bold leading-tight truncate">{{ s.name }}</div>
    <div class="text-xs text-gray-400 mt-0.5">В избранном {{ s.favorites_count || 0 }}</div>
  </div>

  <!-- Центр: описание -->
  <div class="text-sm text-gray-400 mt-1 truncate ">{{ s.description }}</div>

  <!-- Низ: категории -->
  <div class="flex flex-wrap gap-x-2 gap-y-0.5 mt-2">
    <span
      v-for="cat in s.categories"
      :key="cat"
      class="text-xs text-[#5E56A5] font-sans font-bold cursor-pointer hover:underline"
    >{{ cat }}</span>
  </div>
</div>

   <div class="flex flex-col gap-10">
     <button @click="toggleFavorite(s)" class="ml-auto">
          <svg
            width="24" height="24" viewBox="0 0 24 24" fill="none"
            :class="s.is_favorite ? 'text-[#7A65FC]' : 'text-[#4B4B50]'"
          >
            <path
              d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5
                2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09
                C13.09 3.81 14.76 3 16.5 3
                19.58 3 22 5.42 22 8.5
                c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
              :fill="s.is_favorite ? '#5E56A5' : 'none'"
              :stroke="s.is_favorite ? '#5E56A5' : '#4B4B50'"
              stroke-width="2"
            />
          </svg>
        </button>
          <button @click="openContacts(s)" class="ml-4">
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
import { ref, computed, onMounted, watch ,onBeforeUnmount} from 'vue'
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
const displayedSuppliers = computed(() => {
  let items = suppliers.value
  if (selectedCat.value.length) {
    items = items.filter(s => s.categories.some(c => selectedCat.value.includes(c)))
  }
  if (showFavOnly.value) {
    items = items.filter(s => s.is_favorite)
  }
  return items
})



const dropdownArea = ref(null)

function handleClickOutside(e) {
  if (filtersOpen.value && dropdownArea.value && !dropdownArea.value.contains(e.target)) {
    filtersOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})


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
    const uid = userData.user.id
    const url = `${API_BASE}/suppliers?user_id=${uid}`
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
      if (data.favorite) {
        s.favorites_count = (s.favorites_count || 0) + 1
      } else {
        s.favorites_count = Math.max(0, (s.favorites_count || 1) - 1)
      }
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
      Object.assign(s, data)
      if (window.showSupplierModal) window.showSupplierModal(s)
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


</script>



