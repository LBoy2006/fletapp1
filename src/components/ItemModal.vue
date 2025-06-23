<template>
  <div class="modal-overlay backdrop-blur-sm">
    <div class="absolute bottom-20">
    <div class="item-modal ">
      <button class="absolute top-4 right-4 text-[#A4A4A8] hover:text-white" @click="emitClose">
        <svg width="20" height="20" fill="none"><path d="M5 5l10 10M15 5L5 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      </button>
      <div class="relative flex justify-center mb-5">
        <img
          :src="item.photo_url"
          alt="Item"
          class="w-[185px] h-[185px] object-contain border border-[#232226] bg-[#232226]"
        />
        <span
          v-if="item.is_new"
          class="absolute top-3 left-3 bg-[#406AFF] text-white text-xs font-semibold px-2 py-0.5 rounded-md shadow-[0_2px_8px_rgba(36,106,255,0.23)]"
        >NEW</span>
        <button
          class="absolute top-3 right-3"
          @click="toggleFav"
        >
          <svg
            width="28"
            height="28"
            fill="none"
            :class="item.fav ? 'text-[#7A65FC]' : 'text-[#7367D0]'"
          >
            <path
              d="M14 24s-5.6-4.87-9-8.22C2.07 13.22 2.22 9.29 5.26 7.42A5.77 5.77 0 0114 8.85a5.77 5.77 0 018.74-1.43c3.04 1.87 3.19 5.8.26 8.36C19.6 19.13 14 24 14 24z"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              :fill="item.fav ? 'currentColor' : 'none'"
            />
          </svg>
        </button>
      </div>
      <div class="text-center mb-1">
        <div class="text-xl font-extrabold text-white leading-6">{{ item.name }}</div>
        <div class="text-xs text-[#A4A4A8] mt-1 mb-1 leading-snug">{{ item.desc }}</div>
      </div>
      <div class="text-center text-2xl font-extrabold text-[#7A65FC] mb-4">{{ priceText }}</div>
      <button
        @click="copyLink"
        class="w-full flex items-center justify-center gap-2 border border-[#232226] bg-transparent text-white rounded-lg py-2 mb-3 font-medium hover:bg-[#232226]"
      >
        <svg width="18" height="18" fill="none"><rect x="3" y="6" width="12" height="6" rx="1" stroke="currentColor" stroke-width="2"/><path d="M7 10v2a1 1 0 001 1h2a1 1 0 001-1v-2" stroke="currentColor" stroke-width="2"/></svg>
        Скопировать ссылку
      </button>
      <a
        :href="item.link || '#'"
        target="_blank"
        class="w-full flex items-center justify-center gap-2 bg-[#7A65FC] hover:bg-[#6B53FF] text-white rounded-lg py-3 font-bold text-base transition mt-0.5"
      >
        <svg width="20" height="20" fill="none"><path d="M9.5 6.5v-2A1.5 1.5 0 0111 3h6a1.5 1.5 0 011.5 1.5v12A1.5 1.5 0 0117 18h-6a1.5 1.5 0 01-1.5-1.5v-2M5 12h11.5m-8-3l-3 3 3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Перейти по ссылке
      </a>
    </div></div>
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

