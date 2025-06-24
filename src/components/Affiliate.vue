<template>
   <div class="h-full p-0 flex flex-col space-y-1 p-2 ">
    <!-- 🔒 Фиксированная шапка -->
    <div class="sticky top-0 z-10 bg-[var(--page-bg-color)] px-3 py-4 border-b border-[#2c2c3a]">
      <div class="relative flex items-center justify-between">
        <!-- Слева -->
        <span class="text-lg font-bold z-10">Affiliate</span>

        <!-- Центрированный блок -->
        <div class="absolute left-1/2 transform -translate-x-1/2 flex flex-col items-center">
          <span class="text-2xl font-extrabold">1chn</span>
          <span class="text-sm text-gray-400">[ван чан]</span>
        </div>
      </div>
    </div>
    <!-- Карточка профиля -->
    <div class="bg-[#191919] border border-[#42424280] rounded-[10px] px-5 py-4">
      <div class="flex justify-between items-center">
        <div>
          <div class="font-bold text-base text-[#DFDFDF]">{{ nickname || '—' }}</div>
          <div class="text-xs text-[#DFDFDF] opacity-80 mt-1">{{ stats.motivation || '—' }}</div>
        </div>
        <div class=" text-white px-4 py-1 text-xs font-semibold">

                    <svg width="128" height="64" viewBox="0 0 256 48" fill="none">
                      <text x="16" y="40" fill="white"
      font-size="2em"
      font-family="sans-serif"
      font-weight="bold"

      alignment-baseline="middle">
    Твоя доля {{ stats.share ?? '—' }}%
  </text>
  <!-- Задний (нижний) прямоугольник, только часть обводки -->
  <path d="

 M 20 16 H 184 Q 200 16 200 32 V 72 C 200 72 200 76 192 72
 L 180 64 C 177.3332 62.6668 176 60 172 60 H 20
 Q 4 60 4 44 V 32 Q 4 16 20 16 Z

"
        stroke="#5E56A5" stroke-width="4"  fill="none"/></svg>
        </div>
      </div>

      <!-- Баланс и метрики -->
      <div class="flex justify-between items-center mt-4">
        <div class="flex items-center gap-2">
          <span class="font-semibold text-[13px] bg-gradient-to-r from-yellow-200 via-yellow-100 to-yellow-200 bg-clip-text text-transparent">₽</span>
          <span class="font-bold text-sm text-[#DFDFDF]">{{ formatR(stats.earned) }}</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="font-semibold text-[13px] bg-gradient-to-r from-yellow-200 via-yellow-100 to-yellow-200 bg-clip-text text-transparent">₽</span>
          <span class="font-bold text-sm text-[#DFDFDF]">{{ formatR(stats.payments_sum) }}</span>
        </div>
      </div>
    </div>

    <!-- Детальная статистика -->
    <div class="bg-[#191919] border border-[#42424280] rounded-[10px] px-5 py-5 space-y-3">
      <div class="flex justify-between text-sm">
        <span class="text-[#FFFFFFBF] font-medium">Приглашено пользователей</span>
        <span class="font-extrabold text-[#DFDFDF]">{{ stats.invited ?? '—' }}</span>
      </div>
      <div class="w-full border-t border-[#2E2A54] my-1"></div>
      <div class="flex justify-between text-sm">
        <span class="text-[#FFFFFFBF] font-medium">Твоя комиссия</span>
        <span class="font-extrabold text-[#DFDFDF]">{{ stats.share ?? '—' }}%</span>
      </div>
      <div class="w-full border-t border-[#2E2A54] my-1"></div>
      <div class="flex justify-between text-sm">
        <span class="text-[#FFFFFFBF] font-medium">Сумма оплат</span>
        <span class="font-extrabold text-[#DFDFDF]">{{ formatR(stats.payments_sum) }}</span>
      </div>
      <div class="w-full border-t border-[#2E2A54] my-1"></div>
      <div class="flex justify-between text-sm">
        <span class="text-[#FFFFFFBF] font-medium">Заработано</span>
        <span class="font-extrabold text-[#DFDFDF]">{{ formatR(stats.earned) }}</span>
      </div>
      <div class="w-full border-t border-[#2E2A54] my-1"></div>
      <div class="flex justify-between text-sm">
        <span class="text-[#FFFFFFBF] font-medium">Выплачено</span>
        <span class="font-extrabold text-[#DFDFDF]">{{ formatR(stats.paid) }}</span>
      </div>
      <div class="w-full border-t border-[#2E2A54] my-1"></div>
      <div class="flex justify-between items-center mt-2">
        <span class="font-bold text-[#8B81F5] text-base">Баланс</span>
        <span class="font-extrabold text-[#8B81F5] text-base">{{ formatR(stats.balance) }}</span>
      </div>
    </div>

    <!-- Кнопка "Вывести" -->
    <div class="bg-[#3B366B] border border-white/20 rounded-[10px] px-6 py-3 text-center flex flex-col items-center">
      <button
        class="w-full bg-[#5E56A5] rounded-[8px] text-white font-bold py-2 disabled:opacity-50"
        :disabled="!canWithdraw || withdrawRequested"
        @click="onWithdraw"
      >Вывести</button>
      <div class="text-[10px] text-[#DFDFDF] mt-1">Минимальная сумма 15 000₽</div>
      <div v-if="withdrawRequested" class="text-green-400 text-xs mt-2">
        Запрос отправлен, с вами свяжется администратор в Telegram
      </div>
    </div>

    <!-- Ссылка и копирование -->
    <div class="bg-[#191919] border border-[#292929] rounded-[10px] px-5 py-3 flex flex-col gap-2">
      <div class="flex items-center gap-2">
        <span class="font-semibold text-[#DFDFDF] text-sm">Твоя реферальная ссылка</span>
        <button @click="copyLink" class="w-20 h-20 flex items-center justify-center">
          <svg width="24" height="24" viewBox="0 0 64 64" fill="none">
  <!-- Задний (нижний) прямоугольник, только часть обводки -->
  <path d="M 18 42 Q 12 42 12 36 V 18 Q 12 12 18 12 H 36 Q 42 12 42 18 V 36 Q 42 42 36 42 Z M 8 34 H 7 C 6 34 4 33 4 28 V 10 Q 4 4 10 4 H 28 C 33 4 34 6 34 7 V 8"
    stroke="white" stroke-width="4"  stroke-linejoin="round" fill="none"/>

</svg>

        </button>
      </div>
      <input
        readonly
        :value="stats.referral_link || '—'"
        class="bg-[#232323] rounded px-2 py-1 w-full text-xs text-[#DFDFDF] select-all"
        @focus="copyLink"
      />
    </div>

    <!-- Рекламные материалы -->
    <div class="bg-[#191919] border border-[#292929] rounded-[10px] px-5 py-3">
      <div class="flex items-center gap-2">
        <svg fill="currentColor" class="w-4 h-4 text-[#8B81F5]">
          <circle cx="8" cy="8" r="8"/>
        </svg>
        <span class="font-semibold text-[#DFDFDF] text-sm">Рекламные материалы</span>
      </div>
      <a
        :href="stats.materials_link || materialsLink"
        target="_blank"
        class="block mt-2 text-blue-400 underline text-sm"
      >Открыть на Google Drive</a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { userData } from '../state'
import { API_BASE } from '../api'

const stats = ref({})
const nickname = ref('')
const withdrawRequested = ref(false)
const materialsLink = 'https://drive.google.com/'

function formatR(val) {
  if (val === undefined || val === null) return '—'
  return new Intl.NumberFormat('ru-RU').format(val) + ' ₽'
}
const canWithdraw = computed(() => (stats.value.balance || 0) >= 15000)

async function loadData() {
  if (!userData.user.id) return
  try {
    const respUser = await fetch(`${API_BASE}/users/${userData.user.id}`)
    if (respUser.ok) {
      const user = await respUser.json()
      nickname.value = 'Агент ' + (user.agent_number || '—')
    }
  } catch (e) {
    console.error(e)
  }
  try {
    const resp = await fetch(`${API_BASE}/affiliate/${userData.user.id}`)
    if (resp.ok) {
      stats.value = await resp.json()
      withdrawRequested.value = stats.value.withdraw_requested
    }
  } catch (e) {
    console.error(e)
  }
}
async function onWithdraw() {
  try {
    const resp = await fetch(`${API_BASE}/affiliate/${userData.user.id}/withdraw`, { method: 'POST' })
    if (resp.ok) {
      const data = await resp.json()
      stats.value = data
      withdrawRequested.value = true
    }
  } catch (e) {
    console.error(e)
  }
}
function copyLink() {
  navigator.clipboard.writeText(stats.value.referral_link || '').catch(() => {})
}
onMounted(loadData)
watch(() => userData.user.id, id => { if (id) loadData() })
</script>
