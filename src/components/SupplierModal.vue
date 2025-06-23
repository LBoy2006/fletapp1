<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-70">
    <div class="bg-[#232226] rounded-2xl p-5 w-[350px] shadow-xl relative text-white">
      <button class="absolute top-4 right-4 text-white" @click="$emit('close')">
        <svg width="20" height="20" fill="none"><path d="M5 5l10 10M15 5L5 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      </button>
      <div class="flex items-start mb-4">
        <img :src="supplier.photo_url" alt="Supplier" class="w-16 h-16 rounded-full object-cover" />
        <div class="ml-4 flex-1">
          <div class="text-xl font-bold">{{ supplier.name }}</div>
          <div class="text-sm text-gray-400" v-if="supplier.suppliers_count">{{ supplier.suppliers_count }} Suppliers</div>
        </div>
        <button class="ml-2 text-purple-400">
          <svg width="24" height="24" fill="none"><path d="M12 21s-5-4.35-8-7.35C1.38 11.02 1.52 7.36 4.22 5.78A5.13 5.13 0 0112 7.25a5.13 5.13 0 017.78-1.47c2.7 1.58 2.84 5.24.22 7.87C17 16.65 12 21 12 21z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
      </div>
      <div class="mb-4 text-sm text-gray-300" v-if="supplier.description">{{ supplier.description }}</div>
      <div class="flex flex-wrap gap-x-2 gap-y-1 mb-4">
        <span v-if="supplier.category1" class="text-xs text-purple-400">{{ supplier.category1 }}</span>
        <span v-if="supplier.category2" class="text-xs text-purple-400">{{ supplier.category2 }}</span>
      </div>
      <div class="bg-[#1A1A1E] rounded-lg p-3 mb-4">
        <div class="flex justify-between items-center text-gray-400 text-sm mb-2">
          <span>Телефон</span>
          <span class="font-bold text-lg text-white">{{ supplier.contact_phone || '—' }}</span>
        </div>
        <div class="flex justify-between items-center text-gray-400 text-sm">
          <span>Пароль</span>
          <span class="font-bold text-lg text-white">{{ supplier.contact_password || '—' }}</span>
        </div>
      </div>
      <button class="w-full flex items-center justify-center gap-2 bg-[#18181B] text-white rounded-lg py-2 mb-2" @click="copyLink">
        <svg width="18" height="18" fill="none"><rect x="3" y="6" width="12" height="6" rx="1" stroke="currentColor" stroke-width="2"/><path d="M7 10v2a1 1 0 001 1h2a1 1 0 001-1v-2" stroke="currentColor" stroke-width="2"/></svg>
        Скопировать ссылку
      </button>
      <a v-if="supplier.contact_link" :href="supplier.contact_link" target="_blank" class="w-full flex items-center justify-center gap-2 bg-[#7A65FC] text-white rounded-lg py-3 font-semibold text-base mt-1">
        <svg width="20" height="20" fill="none"><path d="M9.5 6.5v-2A1.5 1.5 0 0111 3h6a1.5 1.5 0 011.5 1.5v12A1.5 1.5 0 0117 18h-6a1.5 1.5 0 01-1.5-1.5v-2M5 12h11.5m-8-3l-3 3 3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Перейти на сайт
      </a>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  supplier: { type: Object, default: () => ({}) }
})

function copyLink() {
  if (props.supplier.contact_link) {
    navigator.clipboard?.writeText(props.supplier.contact_link)
  }
}
</script>
