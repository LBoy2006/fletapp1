<template>
  <div class="p-4 text-center space-y-4">
    <p>Вы не являетесь членом клуба.</p>
    <div v-if="step === 'join'">
      <button class="bg-blue-600 text-white px-4 py-2 rounded" @click="step = 'pay'">Вступить в клуб</button>
    </div>
    <div v-else>
      <p>Оплата (тестовый режим)</p>
      <button class="bg-green-600 text-white px-4 py-2 rounded" @click="confirm">Подтвердить оплату</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const step = ref('join');

async function confirm() {
  const initData = window.Telegram?.WebApp?.initData || '';
  await fetch('http://localhost:8000/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ init_data: initData })
  });
  location.reload();
}
</script>
