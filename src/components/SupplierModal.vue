<template>
  <div class="fixed inset-0 z-50  flex items-center justify-center bg-black/60 backdrop-blur-sm ">
    <div class="w-full px-1 mx-1 absolute bottom-32">
      <!-- Модалка -->
      <div class="bg-[var(--page-bg-color)] w-full  rounded-2xl shadow-2xl pt-0 pb-5 px-3 overflow-hidden mx-0">
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
        <div class="card-base w-full shadow-lg p-2 pt-4">
          <div class="flex relative">
            <div class="flex flex-row pb-5">
              <img :src="supplier.photo_url" alt="Supplier"
                 class="w-24 h-24 rounded-full object-cover border border border-[0.5px] border-[#424242] m-0 mr-2 " />

               <div class="ml-1 flex flex-col justify-start ">


                  <div class="text-lg font-bold text-white leading-5">{{ supplier.name }}</div>
                  <div class="text-xs text-gray-400 mt-0.5 mb-1">Избрали {{ supplier.favorites_count || 0 }}</div>
                <!-- Описание -->
              <div class="text-xs text-gray-400 mt-1 mb-2 leading-4">{{ supplier.description }}</div>
                  <div>
                  <div class="flex flex-wrap gap-x-2 gap-y-0.5 mt-2">
                <span
                  v-for="cat in supplier.categories"
                  :key="cat"
                  class="text-xs text-[#5E56A5] font-sans font-bold cursor-pointer hover:underline"
                >{{ cat }}</span></div>
              </div>


              <!-- Категории -->
              </div>
              <div class="absolute right-3">
              <button  @click="toggleFavorite">
                  <svg width="24" height="24" fill="none"
                       :class="supplier.is_favorite ? 'text-[#7A65FC]' : 'text-[#565466]'">
                    <path d="M12 21s-5-4.35-8-7.35C1.38 11.02 1.52 7.36 4.22 5.78A5.13 5.13 0 0112 7.25a5.13 5.13 0 017.78-1.47c2.7 1.58 2.84 5.24.22 7.87C17 16.65 12 21 12 21z"
                          :stroke="supplier.is_favorite ? '#5E56A5' : '#4B4B50'" stroke-width="2"
                          stroke-linecap="round" stroke-linejoin="round"
                          :fill="supplier.is_favorite ? '#5E56A5' : 'none'" />
                  </svg>
                </button></div>
            </div>
          </div>


          <!-- Телефон и пароль -->
          <div>
            <div class="flex justify-between items-center p-1">

              <span class="text-sm text-gray-400">Телефон</span>
              <span class="font-extrabold text-lg text-white tracking-wide">{{ supplier.contact_phone || '—' }}</span>
            </div>
            <!-- Разделитель -->
            <div class="border-t border-[#232226]"></div>
            <div class="flex justify-between items-center p-1">
              <span class="text-sm text-gray-400">Пароль</span>
              <span class="font-extrabold text-lg text-white tracking-wide">{{ supplier.contact_password || '—' }}</span>
            </div>
          </div>
        </div>
        <!-- Кнопки -->
        <button
          @click="copyLink"
          class="card-base py-2 flex mt-4 h-10 flex-1 w-full items-center justify-center gap-1 bg-[#18181B] text-white font-medium transition hover:bg-[#232226]"
        >
            <svg width="24" height="24" viewBox="-5 -5 64 64" fill="none">
  <!-- Задний (нижний) прямоугольник, только часть обводки -->
  <path d="M 18 42 Q 12 42 12 36 V 18 Q 12 12 18 12 H 36 Q 42 12 42 18 V 36 Q 42 42 36 42 Z M 8 34 H 7 C 6 34 4 33 4 28 V 10 Q 4 4 10 4 H 28 C 33 4 34 6 34 7 V 8"
    stroke="white" stroke-width="4"  stroke-linejoin="round" fill="none"/>

</svg>
          Скопировать ссылку
        </button>

        <a

          :href="supplier.contact_link || '#'"
          target="_blank"
          class="rounded-xl bg-[var(--button-color)] w-full h-10 mt-2 flex flex-1 items-center justify-center gap-2 text-white py-3 font-bold text-base shadow transition"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" >
            <path d="
            M 15 2 H 21 Q 22 2 22 3 V 8 M 11 13 L 21 3 M 11 4 H 7 Q 4 4 4 7 V 17 Q 4 20 7 20 H 17 Q 20 20 20 17 V 13
"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Перейти на сайт
        </a>
      </div>

    </div>     <transition name="fade">
  <div
    v-if="copied"
    class="fixed top-36 mt-2 text-center text-sm text-white py-1 px-3 shadow-sm"
  >
    Скопировано!
  </div>
</transition></div>


</template>



<script setup>
import { ref } from 'vue';

const emit = defineEmits(['close']);
const props = defineProps({
  supplier: {
    type: Object,
    required: true,
  }
});

const copied = ref(false);

const emitClose = () => emit('close');

const copyLink = async () => {
  if (props.supplier.contact_link) {
    await navigator.clipboard.writeText(props.supplier.contact_link);
    copied.value = true;
    setTimeout(() => copied.value = false, 1500); // скрыть через 1.5 сек
  }
};

const toggleFavorite = () => {
  props.supplier.is_favorite = !props.supplier.is_favorite;
};

</script>
