<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
    <div class="w-full max-w-sm mx-auto">
      <!-- Модалка -->
      <div class="bg-[#1A1A1D] rounded-2xl shadow-2xl pt-0 pb-5 px-0 overflow-hidden">
        <!-- Header -->
        <div class="flex items-center justify-between px-5 pt-4 pb-3">
          <span class="text-base text-white font-medium w-1/3 text-left"> </span>
          <span class="text-base text-white font-medium w-1/3 text-center">Supplier</span>
          <button class="w-1/3 flex justify-end" @click="emitClose">
            <svg width="22" height="22" fill="none">
              <path d="M5 5l12 12M17 5L5 17" stroke="white" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
        <!-- Card контент -->
        <div class="bg-[#29282C] rounded-2xl shadow-lg mx-5 p-5 pt-4 flex flex-col">
          <div class="flex items-start relative">
            <img :src="supplier.photo_url" alt="Supplier"
                 class="w-16 h-16 rounded-full object-cover border-2 border-[#232226] shadow-md" />
            <div class="ml-4 flex-1">
              <div class="flex items-center justify-between">
                <div>
                  <div class="text-lg font-bold text-white leading-5">{{ supplier.name }}</div>
                  <div class="text-xs text-gray-400 mt-0.5 mb-1">{{ supplier.suppliers_count || 0 }} Suppliers</div>
                </div>
                <button @click="toggleFavorite">
                  <svg width="24" height="24" fill="none"
                       :class="supplier.is_favorite ? 'text-[#7A65FC]' : 'text-[#565466]'">
                    <path d="M12 21s-5-4.35-8-7.35C1.38 11.02 1.52 7.36 4.22 5.78A5.13 5.13 0 0112 7.25a5.13 5.13 0 017.78-1.47c2.7 1.58 2.84 5.24.22 7.87C17 16.65 12 21 12 21z"
                          :stroke="supplier.is_favorite ? '#7A65FC' : '#565466'" stroke-width="2"
                          stroke-linecap="round" stroke-linejoin="round"
                          :fill="supplier.is_favorite ? '#7A65FC' : 'none'" />
                  </svg>
                </button>
              </div>
              <!-- Описание -->
              <div class="text-xs text-gray-400 mt-1 mb-2 leading-4">{{ supplier.description }}</div>
              <!-- Категории -->
              <div class="flex flex-wrap gap-x-2 gap-y-0.5">
                <span
                  v-for="cat in supplier.categories"
                  :key="cat"
                  class="text-xs text-[#7A65FC] font-medium cursor-pointer hover:underline"
                >{{ cat }}</span>
              </div>
            </div>
          </div>
          <!-- Разделитель -->
          <div class="my-4 border-t border-[#232226]"></div>
          <!-- Телефон и пароль -->
          <div>
            <div class="flex justify-between items-center py-1">
              <span class="text-sm text-gray-400">Телефон</span>
              <span class="font-extrabold text-lg text-white tracking-wide">{{ supplier.contact_phone || '—' }}</span>
            </div>
            <div class="border-t border-[#232226]"></div>
            <div class="flex justify-between items-center py-1">
              <span class="text-sm text-gray-400">Пароль</span>
              <span class="font-extrabold text-lg text-white tracking-wide">{{ supplier.contact_password || '—' }}</span>
            </div>
          </div>
        </div>
        <!-- Кнопки -->
        <button
          @click="copyLink"
          class="mx-5 mt-4 w-[calc(100%-40px)] flex items-center justify-center gap-2 bg-[#18181B] text-white rounded-lg py-2 font-medium shadow transition hover:bg-[#232226]"
        >
          <svg width="18" height="18" fill="none">
            <rect x="3" y="6" width="12" height="6" rx="1" stroke="currentColor" stroke-width="2"/>
            <path d="M7 10v2a1 1 0 001 1h2a1 1 0 001-1v-2" stroke="currentColor" stroke-width="2"/>
          </svg>
          Скопировать ссылку
        </button>
        <a
          :href="supplier.contact_link || '#'"
          target="_blank"
          class="mx-5 mt-2 w-[calc(100%-40px)] flex items-center justify-center gap-2 bg-[#7A65FC] text-white rounded-lg py-3 font-bold text-base shadow transition hover:bg-[#9984f8]"
        >
          <svg width="20" height="20" fill="none">
            <path d="M9.5 6.5v-2A1.5 1.5 0 0111 3h6a1.5 1.5 0 011.5 1.5v12A1.5 1.5 0 0117 18h-6a1.5 1.5 0 01-1.5-1.5v-2M5 12h11.5m-8-3l-3 3 3 3"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
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
