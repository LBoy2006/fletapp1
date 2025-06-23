<template>
  <div class="modal-overlay backdrop-blur-sm ">
    <div class="absolute bottom-20">
    <div class="supplier-modal">
      <!-- Header -->
      <div class="flex items-center px-1 pt-2 pb-2 relative">
  <!-- Пустой блок для выравнивания -->
  <div class="w-6"></div>
  <div class="flex-1 text-center text-white text-base font-medium">Supplier</div>
  <button class="text-white pr-3 " @click="emitClose">
    <svg width="20" height="20" fill="none">
      <path d="M5 5l10 10M15 5L5 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>
  </button>
</div>
      <!-- Card -->
      <div class="bg-[#29282C] mx-5 mt-0 mb-4 rounded-2xl p-4 pt-3 flex flex-col overflow-hidden">
  <!-- Верхняя часть: фото, имя, категории, избранное -->
  <div class="flex items-start relative">
    <img :src="supplier.photo_url" alt="Supplier"
         class="w-16 h-16 rounded-3xl object-cover border-2 border-[#232226]" />
    <div class="ml-3 flex-1">
      <div class="text-lg font-semibold text-white leading-5">{{ supplier.name }}</div>
      <div class="text-xs text-gray-400 mb-2">{{ supplier.suppliers_count || 0 }} Suppliers</div>
      <div class="text-s absolute font-semibold text-gray-400 leading-4">{{ supplier.description }}</div>
      <div class="flex flex-wrap gap-x-1 gap-y-0.5">
        <span
          v-for="cat in supplier.categories"
          :key="cat"
          class="text-xs text-[#7A65FC] font-medium cursor-pointer hover:underline"
        >{{ cat }}</span>
      </div>
    </div>
    <button class="ml-2" @click="toggleFavorite">
      <svg width="24" height="24" fill="none" :class="supplier.is_favorite ? 'text-[#7A65FC]' : 'text-[#565466]'">
        <path d="M12 21s-5-4.35-8-7.35
        C1.38 11.02 1.52 7.36 4.22 5.78
        A5.13 5.13 0 0112 7.25
        a5.13 5.13 0 017.78-1.47
        c2.7 1.58 2.84 5.24.22 7.87
        C17 16.65 12 21 12 21
        z"
          :stroke="supplier.is_favorite ? '#7A65FC' : '#565466'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" :fill="supplier.is_favorite ? '#7A65FC' : 'none'" />
      </svg>
    </button>
  </div>

  <!-- Разделитель -->
  <div class="my-3 border-t border-[#232226]"></div>

  <!-- Телефон и пароль -->
  <div>
    <div class="flex justify-between items-center py-2">
      <span class="text-sm text-gray-400">Телефон</span>
      <span class="font-bold text-lg text-white tracking-wide">{{ supplier.contact_phone || '—' }}</span>
    </div>
    <div class="border-t border-[#232226]"></div>
    <div class="flex justify-between items-center py-2">
      <span class="text-sm text-gray-400">Пароль</span>
      <span class="font-bold text-lg text-white tracking-wide">{{ supplier.contact_password || '—' }}</span>
    </div>
  </div>
</div>

      <!-- Кнопки -->
      <button @click="copyLink"
        class="mx-5 w-[calc(100%-40px)] flex items-center justify-center gap-2 bg-[#18181B] text-white rounded-lg py-2 font-medium mb-2">
        <svg width="18" height="18" fill="none"><rect x="3" y="6" width="12" height="6" rx="1" stroke="currentColor" stroke-width="2"/><path d="M7 10v2a1 1 0 001 1h2a1 1 0 001-1v-2" stroke="currentColor" stroke-width="2"/></svg>
        Скопировать ссылку
      </button>
      <a
        :href="supplier.contact_link || '#'"
        target="_blank"
        class="mx-5 w-[calc(100%-40px)] flex items-center justify-center gap-2 bg-[#7A65FC] text-white rounded-lg py-3 font-semibold text-base transition-colors duration-150 hover:bg-[#9984f8]">
        <svg width="20" height="20" fill="none"><path d="M9.5 6.5v-2A1.5 1.5 0 0111 3h6a1.5 1.5 0 011.5 1.5v12A1.5 1.5 0 0117 18h-6a1.5 1.5 0 01-1.5-1.5v-2M5 12h11.5m-8-3l-3 3 3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Перейти на сайт
      </a>
    </div>
     </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close']);
const props = defineProps({
  supplier: {
    type: Object,
    required: true,
  }
});
const emitClose = () => emit('close');
const copyLink = () => {
  if (props.supplier.contact_link) {
    navigator.clipboard.writeText(props.supplier.contact_link);
  }
};
const toggleFavorite = () => {
  props.supplier.is_favorite = !props.supplier.is_favorite;
};
</script>
