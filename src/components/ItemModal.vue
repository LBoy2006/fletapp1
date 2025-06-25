
<template>
  <div class="fixed inset-0 z-50  flex items-center justify-center bg-black/60 backdrop-blur-sm ">
    <div class="w-full px-1 mx-1 absolute bottom-32">
      <!-- Модалка -->
      <div class="bg-[var(--page-bg-color)] w-full  rounded-2xl shadow-2xl pt-0 pb-5 px-3 overflow-hidden mx-0">
        <!-- Header -->
        <div class="flex items-center justify-between px-5 pt-4 pb-3">
          <span class="text-base text-white font-medium w-1/3 text-left"></span>
          <span class="text-base text-white font-medium w-1/3 text-center">Item</span>
          <button class="w-1/3 flex justify-end" @click="emitClose">
            <svg width="22" height="22" fill="none">
              <path d="M5 5l12 12M17 5L5 17" stroke="white" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
        <!-- Card контент -->
        <div class="card-base w-full shadow-lg p-2 pt-4">


          <div class="relative flex justify-center mb-5">
        <img
          :src="item.photo_url"
          alt="Item"
          class="w-[185px] h-[185px] object-contain border border-[#232226] bg-[#232226] rounded-xl shadow-lg"
        />
        <div class="absolute top-3 right-3 flex gap-1 text-xl items-center">
          <span v-if="item.is_hot">🔥</span>
          <span v-if="item.is_new">🆕</span>
          <span v-if="item.is_high_margin">💰</span>
          <button class="ml-1" @click="toggleFav">
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
      </div>

      <div class="text-center mb-2">
        <div class="text-xl font-extrabold text-white leading-6">{{ item.name }}</div>
        <div class="text-xs text-[#A4A4A8] mt-1 mb-1 leading-snug">{{ item.description }}</div>
      </div>

      <div class="text-center text-2xl font-extrabold text-[#7A65FC] mb-4">{{ priceText }}</div>


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

          :href="item.link || '#'"
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

