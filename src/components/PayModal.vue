<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
    <div class="w-full px-1 mx-1 absolute bottom-32">
      <div class="bg-[var(--page-bg-color)] w-full rounded-2xl shadow-2xl pt-0 pb-5 px-3 overflow-hidden mx-0">
        <!-- Шапка -->
        <div class="flex items-center justify-between px-5 pt-4 pb-3">
          <span class="text-base text-white font-medium w-1/3 text-left"> </span>
          <span class="text-base text-white font-medium w-1/3 text-center">Оплата</span>
          <button class="w-1/3 flex justify-end" @click="emitClose">
            <svg width="22" height="22" fill="none">
              <path d="M5 5l12 12M17 5L5 17" stroke="white" stroke-width="2" stroke-linecap="round" />
            </svg>
          </button>
        </div>

        <!-- Выбор тарифа -->
        <div class="flex flex-col space-y-2 px-3">
          <label
            v-for="p in plans"
            :key="p.months"
            class="flex items-center justify-between p-3 border rounded cursor-pointer transition-all duration-150"
            :class="{ 'bg-[#18181B] border-white': selected === p.months }"
          >
            <div class="flex items-center space-x-3">
              <input
                type="radio"
                :value="p.months"
                v-model="selected"
                :disabled="loading"
                class="form-radio"
              />
              <span class="text-white">{{ p.label }}</span>
            </div>
          </label>

          <!-- Кнопка подтверждения -->
          <button
            v-if="!paymentUrl"
            @click="confirm"
            class="rounded-xl bg-[var(--button-color)] text-white py-2 mt-3"
            :disabled="loading"
          >
            {{ loading ? 'Создание...' : 'Подтвердить' }}
          </button>

          <!-- Кнопка перехода на оплату -->
          <a
            v-if="paymentUrl"
            :href="paymentUrl"
            target="_blank"
            class="rounded-xl bg-[var(--button-color)] text-white py-2 mt-3 text-center block"
          >
            Перейти к оплате
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { userData } from '../state';
import { API_BASE } from '../api';

const emit = defineEmits(['close']);

const plans = [
  { months: 1, label: '1 месяц – 1 990 ₽' },
  { months: 3, label: '3 месяца – 4 990 ₽' },
  { months: 6, label: '6 месяцев – 9 990 ₽' },
  { months: 12, label: '12 месяцев – 19 990 ₽' }
];

const selected = ref(plans[0].months);
const paymentUrl = ref('');
const loading = ref(false);

function emitClose() {
  emit('close');
}

// Сброс ссылки при смене тарифа
watch(selected, () => {
  paymentUrl.value = '';
});

async function confirm() {
  loading.value = true;
  paymentUrl.value = ''; // сбрасываем ссылку на всякий случай
  try {
    const resp = await fetch(`${API_BASE}/payments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userData.user.id,
        months: selected.value
      })
    });

    if (resp.ok) {
      const data = await resp.json();
      paymentUrl.value = data.payment_url;
    } else {
      console.error('Ошибка оплаты:', await resp.text());
    }
  } catch (e) {
    console.error('Ошибка запроса:', e);
  }
  loading.value = false;
}
</script>
