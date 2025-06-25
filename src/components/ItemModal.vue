
<template>
  <div class="fixed inset-0 z-50  flex items-center justify-center bg-black/60 backdrop-blur-sm ">
    <div class="w-full px-1 mx-1 absolute bottom-32">
      <!-- Модалка -->
      <div class="bg-[var(--page-bg-color)] w-full  rounded-2xl shadow-2xl pt-0 pb-5 px-3 overflow-hidden mx-0">
        <!-- Header -->
        <div class="flex items-center justify-between px-5 pt-4 pb-3">
          <span class="text-base text-white font-medium w-1/3 text-left"> </span>
          <span class="text-base text-white font-medium w-1/3 text-center">Item</span>
          <button class="w-1/3 flex justify-end" @click="emitClose">
            <svg width="22" height="22" fill="none">
              <path d="M5 5l12 12M17 5L5 17" stroke="white" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
        <!-- Card контент -->
<div class="card-base w-full bg-[#1C1B1F] rounded-xl p-4 pb-6 relative justify-center">


<div class="relative flex justify-center mb-4">
  <div class="relative w-48 h-48 rounded-2xl overflow-hidden">

    <!-- Само изображение -->
    <img
      :src="item.photo_url"
      alt="Item"
      class="w-full h-full object-cover z-0 relative"
    />

    <!-- Виньетка эффект -->
<div class="absolute inset-0 z-10 pointer-events-none rounded-xl"
     style="
       background: radial-gradient(circle, rgba(0,0,0,0.1) 20%, rgba(0,0,0,0.9) 100%);
     ">
</div>

    <!-- Бейджи (на изображении, сверху слева) -->
    <div class="absolute top-2 left-2 flex flex-col items-start z-20">
      <span
        v-if="item.is_new"
        class="text-[16px] px-1 py-0.5"
      >🆕</span>
      <span
        v-if="item.is_hot"
        class="text-[16px] px-1 py-0.5"
      >🔥</span>
      <span
        v-if="item.is_high_margin"
        class="text-[16px] px-1 py-0.5"
      >💰</span>
    </div>
  </div>


  <!-- Иконка избранного (сердце) -->
  <div class="absolute right-3">
   <button  @click="toggleFav">
                  <svg width="24" height="24" fill="none"
                       :class="item.fav ? 'text-[#7A65FC]' : 'text-[#565466]'">
                    <path d="M12 21s-5-4.35-8-7.35C1.38 11.02 1.52 7.36 4.22 5.78A5.13 5.13 0 0112 7.25a5.13 5.13 0 017.78-1.47c2.7 1.58 2.84 5.24.22 7.87C17 16.65 12 21 12 21z"
                          :stroke="item.fav ? '#5E56A5' : '#4B4B50'" stroke-width="2"
                          stroke-linecap="round" stroke-linejoin="round"
                          :fill="item.fav ? '#5E56A5' : 'none'" />
                  </svg>
                </button>
  </div>
</div>
  <!-- Название и описание -->
  <div class="text-center mb-3">
    <div class="text-xl font-bold text-white leading-tight">{{ item.name }}</div>
    <div class="text-base text-[#A4A4A8] leading-snug mt-1">
      {{ item.description }}
    </div>
  </div>

  <!-- Цена -->
  <div class="text-center text-2xl font-bold text-[#7A65FC]">{{ priceText }}</div>
</div>
        <!-- Кнопки -->
        <button
          @click="copyLink"
          class="card-base py-2 flex mt-4 h-10 flex-1 w-full items-center justify-center gap-1 bg-[#18181B] text-white  transition hover:bg-[#232226]"
        >
            <svg width="24" height="24" viewBox="-5 -5 64 64" fill="none">
  <!-- Задний (нижний) прямоугольник, только часть обводки -->
  <path d="M 18 42 Q 12 42 12 36 V 18 Q 12 12 18 12 H 36 Q 42 12 42 18 V 36 Q 42 42 36 42 Z M 8 34 H 7 C 6 34 4 33 4 28 V 10 Q 4 4 10 4 H 28 C 33 4 34 6 34 7 V 8"
    stroke="white" stroke-width="4"  stroke-linejoin="round" fill="none"/>

</svg>
          Скопировать ссылку
        </button>

        <a

          :href="item.link || '#'"
          target="_blank"
          class="rounded-xl bg-[var(--button-color)] w-full h-10 mt-2 flex flex-1 items-center justify-center gap-2 text-white py-3  text-base shadow transition"
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
</div>
<!--         <transition name="fade">-->
<!--  <div-->
<!--    v-if="copied"-->
<!--    class="fixed top-36 mt-2 text-center text-sm text-white py-1 px-3 shadow-sm"-->
<!--  >-->
<!--    Скопировано!-->
<!--  </div>-->
<!--</transition>-->

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

