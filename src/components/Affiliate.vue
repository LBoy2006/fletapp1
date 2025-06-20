<template>
  <div class="space-y-4 p-4">
    <div class="bg-gray-800 p-4 rounded">
      <div class="flex items-center justify-between">
        <div>
          <div class="font-semibold">Ник: {{ nickname || '—' }}</div>
          <div class="text-sm text-gray-400">{{ stats.motivation || '—' }}</div>
        </div>
        <div class="bg-green-700 text-white px-3 py-1 rounded-full text-sm font-medium">
          Твоя доля {{ stats.share ?? '—' }}%
        </div>
      </div>
    </div>

    <div class="bg-gray-800 p-4 rounded text-sm space-y-2">
      <div class="flex justify-between">
        <span>Приглашено:</span>
        <span>{{ stats.invited ?? '—' }}</span>
      </div>
      <div class="flex justify-between">
        <span>Доля:</span>
        <span>{{ stats.share ?? '—' }}%</span>
      </div>
      <div class="flex justify-between">
        <span>Сумма оплат:</span>
        <span>{{ formatR(stats.payments_sum) }}</span>
      </div>
      <div class="flex justify-between">
        <span>Заработано:</span>
        <span>{{ formatR(stats.earned) }}</span>
      </div>
      <div class="flex justify-between">
        <span>Выплачено:</span>
        <span>{{ formatR(stats.paid) }}</span>
      </div>
      <div class="flex justify-between font-bold text-green-400">
        <span>Баланс:</span>
        <span>{{ formatR(stats.balance) }}</span>
      </div>
      <button
        class="w-full mt-3 bg-blue-600 text-white py-2 rounded disabled:opacity-50"
        :disabled="!canWithdraw || withdrawRequested"
        @click="onWithdraw"
      >
        Вывести
      </button>
      <div v-if="withdrawRequested" class="text-center text-green-500 text-xs mt-2">
        Запрос отправлен, с вами свяжется администратор в Telegram
      </div>
    </div>

    <div class="bg-gray-800 p-4 rounded">
      <div class="flex items-center">
        <input
          readonly
          :value="stats.referral_link || '—'"
          class="bg-gray-700 p-2 rounded flex-1 mr-2 text-sm"
          @focus="copyLink"
        />
        <button @click="copyLink" class="bg-blue-600 text-white px-3 py-2 rounded text-sm">Скопировать</button>
      </div>
    </div>

    <div class="bg-gray-800 p-4 rounded text-sm">
      <h3 class="font-semibold mb-2">Рекламные материалы</h3>
      <a
        :href="stats.materials_link || materialsLink"
        target="_blank"
        class="text-blue-400 underline"
        >Открыть на Google Drive</a
      >
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { userData } from '../state';
import { API_BASE } from '../api';

const props = defineProps({ t: Object });

const stats = ref({});
const nickname = ref('');
const withdrawRequested = ref(false);
const materialsLink = 'https://drive.google.com/';

function formatR(val) {
  if (val === undefined || val === null) return '—';
  return new Intl.NumberFormat('ru-RU').format(val) + ' ₽';
}

const canWithdraw = computed(() => (stats.value.balance || 0) >= 5000);

async function loadData() {
  try {
    const respUser = await fetch(`${API_BASE}/users/${userData.user.id}`);
    if (respUser.ok) {
      const user = await respUser.json();
      nickname.value = 'Агент ' + (user.agent_number || '—');
    }
  } catch (e) {
    console.error(e);
  }
  try {
    const resp = await fetch(`${API_BASE}/affiliate/${userData.user.id}`);
    if (resp.ok) {
      stats.value = await resp.json();
      withdrawRequested.value = stats.value.withdraw_requested;
    }
  } catch (e) {
    console.error(e);
  }
}

async function onWithdraw() {
  try {
    const resp = await fetch(`${API_BASE}/affiliate/${userData.user.id}/withdraw`, { method: 'POST' });
    if (resp.ok) {
      const data = await resp.json();
      stats.value = data;
      withdrawRequested.value = true;
    }
  } catch (e) {
    console.error(e);
  }
}

function copyLink() {
  navigator.clipboard.writeText(stats.value.referral_link || '').catch(() => {});
}

onMounted(loadData);
</script>
