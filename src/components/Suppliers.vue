<!--Suppliers.vue-->
<template>
  <div class="h-full flex flex-col space-y-4 p-4">
    <div class="sticky top-0 z-10">
    <h2 class="text-2xl font-bold text-center">Поставщики</h2>

    <div class="space-y-3">
      <div>
        <div class="text-sm mb-1">Категория</div>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="c in categories1"
            :key="c"
            @click="toggleCat1(c)"
            :class="['px-3 py-1 rounded-full text-sm border', selectedCat1.includes(c) ? 'bg-blue-600 text-white' : 'bg-gray-700']"
          >{{ c }}</button>
        </div>
        <div v-if="!categories1.length" class="text-gray-500 text-sm">—</div>
      </div>

      <div>
        <div class="text-sm mb-1">Бренд</div>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="b in categories2"
            :key="b"
            @click="toggleCat2(b)"
            :class="['px-3 py-1 rounded-full text-sm border', selectedCat2.includes(b) ? 'bg-blue-600 text-white' : 'bg-gray-700']"
          >{{ b }}</button>
        </div>
        <div v-if="!categories2.length" class="text-gray-500 text-sm">—</div>
      </div>

      <div class="flex items-center">
        <input id="favOnly" type="checkbox" v-model="showFavOnly" class="mr-2" />
        <label for="favOnly" class="text-sm">Показать только избранное</label>
      </div>
    </div>
</div>
    <div class="h-64 overflow-y-auto">
    <div v-if="!suppliers.length" class="text-center text-gray-500 py-10">Нет результатов</div>
    <div v-else class="space-y-4">
      <div v-for="s in suppliers" :key="s.id" class="bg-gray-800 p-4 rounded flex items-center">
        <img :src="s.photo_url" class="w-12 h-12 rounded-full object-cover mr-3" />
        <div class="flex-1">
          <div class="font-semibold">{{ s.name }}</div>
          <div class="text-sm text-gray-400">{{ s.description }}</div>
        </div>
        <button @click="toggleFavorite(s)" class="text-xl mr-3">
          <i :class="['fas', s.is_favorite ? 'fa-heart text-red-500' : 'fa-heart']"></i>
        </button>
        <button @click="openContacts(s)" class="bg-blue-600 text-white px-3 py-1 rounded text-sm">Контакт</button>
      </div>
    </div>
</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { userData } from '../state'
import { API_BASE } from '../api'

const categories1 = ref([])
const categories2 = ref([])
const selectedCat1 = ref([])
const selectedCat2 = ref([])
const suppliers = ref([])
const showFavOnly = ref(false)

async function loadCategories1() {
  try {
    const r = await fetch(`${API_BASE}/suppliers/categories1`)
    if (r.ok) categories1.value = await r.json()
  } catch (e) { console.error(e) }
}

async function loadCategories2() {
  try {
    const params = selectedCat1.value.join(',')
    const r = await fetch(`${API_BASE}/suppliers/categories2?categories1=${encodeURIComponent(params)}`)
    if (r.ok) categories2.value = await r.json()
  } catch (e) { console.error(e) }
}

async function loadSuppliers() {
  if (!userData.user.id) return
  try {
    const p1 = selectedCat1.value.join(',')
    const p2 = selectedCat2.value.join(',')
    const fav = showFavOnly.value ? 'true' : 'false'
    const uid = userData.user.id
    const url = `${API_BASE}/suppliers?user_id=${uid}&categories1=${encodeURIComponent(p1)}&categories2=${encodeURIComponent(p2)}&favorites_only=${fav}`
    const r = await fetch(url)
    if (r.ok) suppliers.value = await r.json()
  } catch (e) { console.error(e) }
    finally {
    if (window.applySafeInsets) window.applySafeInsets()
  }
}

function toggleCat1(c) {
  const idx = selectedCat1.value.indexOf(c)
  if (idx >= 0) selectedCat1.value.splice(idx, 1)
  else selectedCat1.value.push(c)
}

function toggleCat2(c) {
  const idx = selectedCat2.value.indexOf(c)
  if (idx >= 0) selectedCat2.value.splice(idx, 1)
  else selectedCat2.value.push(c)
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
  } catch (e) { console.error(e) }
}

async function openContacts(s) {
  try {
    const r = await fetch(`${API_BASE}/suppliers/${s.id}/contacts`)
    if (r.ok) {
      const data = await r.json()
      const lines = [
        `Ссылка: ${data.contact_link || '—'}`,
        `Телефон: ${data.contact_phone || '—'}`,
        `Пароль: ${data.contact_password || '—'}`
      ]
      if (window.showSheet) window.showSheet(lines)
    }
  } catch (e) { console.error(e) }
}

onMounted(() => {
  loadCategories1()
  loadCategories2()
  loadSuppliers()
})

watch(() => userData.user.id, id => {
  if (id) loadSuppliers()
})

watch(selectedCat1, () => {
  loadCategories2()
  loadSuppliers()
}, { deep: true })

watch([selectedCat2, showFavOnly], loadSuppliers, { deep: true })
</script>
