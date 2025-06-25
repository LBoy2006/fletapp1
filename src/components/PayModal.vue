<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
    <div class="w-full px-1 mx-1 absolute bottom-32">
      <div class="bg-[var(--page-bg-color)] w-full rounded-2xl shadow-2xl pt-0 pb-5 px-3 overflow-hidden mx-0">
        <div class="flex items-center justify-between px-5 pt-4 pb-3">
          <span class="text-base text-white font-medium w-1/3 text-left"> </span>
          <span class="text-base text-white font-medium w-1/3 text-center">Оплата</span>
          <button class="w-1/3 flex justify-end" @click="emitClose">
            <svg width="22" height="22" fill="none">
              <path d="M5 5l12 12M17 5L5 17" stroke="white" stroke-width="2" stroke-linecap="round" />
            </svg>
          </button>
        </div>
        <div class="flex flex-col space-y-2 px-3">
          <label
            v-for="p in plans"
            :key="p.months"
            class="flex items-center justify-between p-2 border rounded cursor-pointer"
            :class="{ 'bg-[#18181B]': selected===p.months }"
          >
            <span class="text-white">{{ p.label }}</span>
            <input type="radio" :value="p.months" v-model="selected" />
          </label>
          <button
            v-if="!paymentUrl"
            @click="confirm"
            class="rounded-xl bg-[var(--button-color)] text-white py-2 mt-2"
          >
            Подтвердить
          </button>
          <a
            v-if="paymentUrl"
            :href="paymentUrl"
            target="_blank"
            class="rounded-xl bg-[var(--button-color)] text-white py-2 mt-2 text-center"
          >
            Оплатить
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { userData } from '../state';
import { API_BASE } from '../api';
const emit = defineEmits(['close']);
const plans = [
  { months: 1, label: '1 месяц - 1 990 руб' },
  { months: 3, label: '3 месяца - 4 990 руб' },
  { months: 6, label: '6 месяцев - 9 990 руб' },
  { months: 12, label: '12 месяцев - 19 990 руб' }
];
const selected = ref(plans[0].months);
const paymentUrl = ref('');

function emitClose() {
  emit('close');
}

async function confirm() {
  try {
    const resp = await fetch(`${API_BASE}/payments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userData.user.id, months: selected.value })
    });
    if (resp.ok) {
      const data = await resp.json();
      paymentUrl.value = data.payment_url;
    }
  } catch (e) {
    console.error(e);
  }
}
</script>
