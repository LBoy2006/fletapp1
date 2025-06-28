<!--Feed.vue-->
<template>
  <div class="-mb-3 p-1  m-1 flex flex-col justify-center bg-danger-500 space-y-1 h-full">
    <!-- 🔒 Фиксированная шапка -->
    <div class="absolute fixed top-0 z-99 bg-[var(--page-bg-color)] px-0 py-4 relative pb-5 overflow-visible">
      <div class="relative flex items-center justify-between px-3">
        <!-- Слева -->
        <span class="text-lg font-bold text-white">Feed</span>

        <!-- Центрированный блок -->
        <div class="absolute left-1/2 -translate-x-1/2 flex flex-col items-center">
          <span class="text-2xl z-99 font-dela text-white">1chn</span>
          <span class="text-sm z-99 text-gray-400">[ван чан]</span>
        </div>
      </div>
    </div>


<!--    фейковые товары -->
    <div class=" flex-1 relative pt-1 scrollbar-hide overflow-auto fixed font-sans ">
      <div class="gap-2 top-1 pb-5  ">
        <div
          v-for="f in displayedFinds.slice(0, 6)"
          :key="f.id"
          class="card-items z-9999 relative top-0 card-base flex m-0 items-center "
        >

          <!-- Фото -->
          <div class="relative z-0">
            <img :src="f.photo_url" alt="" class="w-24 h-24 rounded-xl object-cover border border border-[0.5px] border-[#424242] m-0 mr-2 " />
            <div class="absolute -top-1 -left-1 z-1 flex text-[20px] mx-0">
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
            <button class="ml-auto" >
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
            <button class="ml-4">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4B4B50" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="4" y1="12" x2="19" y2="12"/>
  <polyline points="12 5 19 12 12 19"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

        <!-- 🛠️ Блок "в разработке" -->
      <div class="absolute inset-0">
    <div class="flex items-center w-full h-full text-center  backdrop-blur-xl border-0.5rem rounded-xl z-1">
      <div class="flex-col items-center justify-center">
      <div class="flex-col p-1 items-center justify-center space-y-4 ">
        <!-- Эмодзи или картинка -->
        <div class="text-6xl">🚫</div> <!-- Можно заменить на <img> -->

        <!-- Тексты -->
        <div>
          <p class="text-lg font-semibold">Лента находится<br>в разработке</p>
          <p class="text-sm text-gray-400 mt-2">
            Скоро любой агент сможет публиковать свои находки, отчёты и результаты
          </p>
        </div>
      </div></div></div>
    </div>



    </div>


  </div>

</template>


<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { userData } from '../state'
import { API_BASE } from '../api'

// Состояния и данные
const finds = ref([])
const loading = ref(true)
const error = ref(false)

// Отображаем только 10 товаров
const displayedFinds = computed(() => finds.value.slice(0, 10))

// Загрузка данных
async function loadFinds() {
  if (!userData.user.id) return
  loading.value = true
  error.value = false
  try {
    const uid = userData.user.id
    const url = `${API_BASE}/finds?user_id=${uid}`
    const r = await fetch(url)
    if (r.ok) {
      finds.value = await r.json()
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

// Форматирование цены (оставил, т.к. используется в шаблоне)
function formatR(val) {
  if (val === undefined || val === null) return '—'
  return new Intl.NumberFormat('ru-RU').format(val) + ' ₽'
}

// Открыть товар (оставил, т.к. есть кнопка открытия)
function openItem(item) {
  if (window.showItemModal) window.showItemModal(item)
}

// Эффекты
onMounted(() => {
  loadFinds()
})
watch(() => userData.user.id, id => {
  if (id) loadFinds()
})
</script>


