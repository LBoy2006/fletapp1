<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
    <div class="w-full px-1 mx-1 absolute bottom-32">
      <div class="bg-[var(--page-bg-color)] w-full rounded-2xl shadow-2xl pt-0 pb-5 px-3 overflow-hidden mx-0">
        <div class="flex items-center justify-between px-5 pt-4 pb-3">
          <span class="text-base text-white font-medium w-1/3 text-left">&nbsp;</span>
          <span class="text-base text-white font-medium w-1/3 text-center">Оплата</span>
          <button class="w-1/3 flex justify-end" @click="emitClose">
            <svg width="22" height="22" fill="none">
              <path d="M5 5l12 12M17 5L5 17" stroke="white" stroke-width="2" stroke-linecap="round" />
            </svg>
          </button>
        </div>
        <div class="space-y-3 px-4">
          <div v-for="opt in options" :key="opt.months" class="flex items-center text-white">
            <input type="radio" :value="opt" v-model="selected" class="mr-2" />
            <label>{{ opt.months }} мес – {{ formatPrice(opt.price) }}</label>
          </div>
          <button
            v-if="!paymentUrl"
            @click="confirm"
            class="rounded-xl bg-[var(--button-color)] w-full h-10 mt-2 flex items-center justify-center gap-2 text-white text-base shadow"
          >
            Подтвердить
          </button>
          <a
            v-if="paymentUrl"
            :href="paymentUrl"
            target="_blank"
            class="rounded-xl bg-[var(--button-color)] w-full h-10 mt-2 flex items-center justify-center gap-2 text-white text-base shadow"
          >
            Оплатить
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { API_BASE } from '../api'
import { userData } from '../state'

const emit = defineEmits(['close'])

const options = [
  { months: 1, price: 1990 },
  { months: 3, price: 4990 },
  { months: 6, price: 9990 },
  { months: 12, price: 19990 }
]

const selected = ref(options[0])
const paymentUrl = ref('')

function emitClose() {
  emit('close')
}

function formatPrice(p) {
  return new Intl.NumberFormat('ru-RU').format(p) + ' ₽'
}

async function confirm() {
  try {
    const resp = await fetch(`${API_BASE}/payments/membership`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userData.user.id, months: selected.value.months })
    })
    if (resp.ok) {
      const data = await resp.json()
      paymentUrl.value = data.payment_url
    }
  } catch (e) {
    console.error(e)
  }
}
</script>
