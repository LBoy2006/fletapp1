<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-70">
    <div class="bg-[#232226] rounded-2xl p-5 w-[350px] shadow-xl relative">
      <button class="absolute top-4 right-4 text-white" @click="emitClose">
        <svg width="20" height="20" fill="none"><path d="M5 5l10 10M15 5L5 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      </button>
      <div class="relative flex justify-center mb-4">
        <img :src="item.photo_url" alt="Item" class="w-40 h-40 rounded-xl object-cover border border-[#36363C]" />
        <span v-if="item.is_new" class="absolute top-2 left-2 bg-[#406AFF] text-white text-xs px-2 py-0.5 rounded-md font-bold">NEW</span>
        <button class="absolute top-2 right-2 text-purple-400" @click="toggleFav">
          <svg width="24" height="24" fill="none" :class="item.fav ? 'heart-active' : 'heart-inactive'">
            <path d="M12 21s-5-4.35-8-7.35C1.38 11.02 1.52 7.36 4.22 5.78A5.13 5.13 0 0112 7.25a5.13 5.13 0 017.78-1.47c2.7 1.58 2.84 5.24.22 7.87C17 16.65 12 21 12 21z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
      <div class="text-center mb-2">
        <div class="text-xl font-bold text-white">{{ item.name }}</div>
        <div class="text-sm text-gray-400 mt-1">{{ item.desc }}</div>
      </div>
      <div class="text-center text-xl font-bold text-[#7A65FC] mb-5">{{ priceText }}</div>
      <button @click="copyLink" class="w-full flex items-center justify-center gap-2 bg-[#18181B] text-white rounded-lg py-2 mb-2">
        <svg width="18" height="18" fill="none"><rect x="3" y="6" width="12" height="6" rx="1" stroke="currentColor" stroke-width="2"/><path d="M7 10v2a1 1 0 001 1h2a1 1 0 001-1v-2" stroke="currentColor" stroke-width="2"/></svg>
        Скопировать ссылку
      </button>
      <a :href="item.link || '#'" target="_blank" class="w-full flex items-center justify-center gap-2 bg-[#7A65FC] text-white rounded-lg py-3 font-semibold text-base mt-1">
        <svg width="20" height="20" fill="none"><path d="M9.5 6.5v-2A1.5 1.5 0 0111 3h6a1.5 1.5 0 011.5 1.5v12A1.5 1.5 0 0117 18h-6a1.5 1.5 0 01-1.5-1.5v-2M5 12h11.5m-8-3l-3 3 3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Перейти по ссылке
      </a>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  item: { type: Object, required: true }
})

const emit = defineEmits(['close', 'copied', 'toggle-favorite'])

const priceText = computed(() => {
  const p = props.item.price
  if (p === undefined || p === null) return ''
  return new Intl.NumberFormat('ru-RU').format(p) + ' ₽'
})

function emitClose() {
  emit('close')
}

function copyLink() {
  if (props.item.link) {
    navigator.clipboard?.writeText(props.item.link)
    emit('copied')
  }
}

function toggleFav() {
  emit('toggle-favorite')
}
</script>

<style scoped>
.heart-inactive {
  color: #4b4b4b;
  fill: transparent;
}
.heart-active {
  color: #9333ea;
  fill: #9333ea;
}
</style>
