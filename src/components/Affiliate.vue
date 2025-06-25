<template>
   <div class="h-full flex flex-col space-y-1 p-2">
    <!-- 🔒 Фиксированная шапка -->
    <div class="sticky top-0 z-10 bg-[var(--page-bg-color)] px-0 py-4 pb-5 relative overflow-visible">
      <div class="relative flex items-center justify-between px-3">
        <!-- Слева -->
        <span class="text-lg font-bold text-white">Affiliate</span>

        <!-- Центрированный блок -->
        <div class="absolute left-1/2 transform -translate-x-1/2 flex flex-col items-center">
          <span class="text-2xl font-dela text-white">1chn</span>
          <span class="text-sm text-gray-400">[ван чан]</span>
        </div>
      </div>
    </div>
    <!-- Карточка профиля -->
     <div class="flex-col flex gap-2 overflow-y-auto scrollbar-hide font-sans">
    <div class="card-base px-5 py-4 mr-4">
      <div class="flex justify-between items-center">
        <div>
          <div class="font-bold text-base text-[#DFDFDF]">{{ nickname || '—' }}</div>
          <div class="text-xs text-[#DFDFDF] opacity-80 mt-1">{{ stats.motivation || '—' }}</div>
        </div>
        <div class="flex text-white pl-4 py-1 text-xs font-semibold">

                    <svg width="128" height="70" viewBox="0 0 203 48" fill="none">
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
<!--      <div class="flex justify-between items-center mt-4 bg-blue-200" >-->
<!--        <div class="flex items-center gap-2">-->
<!--          <span class="font-semibold text-[13px] bg-gradient-to-r from-yellow-200 via-yellow-100 to-yellow-200 bg-clip-text text-transparent">₽</span>-->
<!--          <span class="font-bold text-sm text-[#DFDFDF]">{{ formatR(stats.earned) }}</span>-->
<!--        </div>-->
<!--        <div class="flex items-center gap-2">-->
<!--          <span class="font-semibold text-[13px] bg-gradient-to-r from-yellow-200 via-yellow-100 to-yellow-200 bg-clip-text text-transparent">₽</span>-->
<!--          <span class="font-bold text-sm text-[#DFDFDF]">{{ formatR(stats.payments_sum) }}</span>-->
<!--        </div>-->
<!--      </div>-->
<!--      прогресбар -->
      <div class="mt-4 bg-[#1f1f1f] rounded-xl px-1 py-1">
  <div class="relative flex justify-between items-center h-10 w-full rounded-lg overflow-hidden">
    <!-- Прогресс -->
    <div
      class="absolute left-0 top-0 h-full bg-[#7B6EF6] transition-all duration-300 rounded-lg"
      :style="{ width: progressPercent + '%' }"
    ></div>

    <!-- Текущая сумма -->
    <div class="flex items-center gap-1 z-10 pl-2">
      <div class="bg-[#7B6EF6] text-white text-sm font-bold px-3 py-1 rounded-lg flex items-center gap-1">
        <span>₽</span> {{ formatR(stats.earned) }}
      </div>
    </div>

    <!-- Целевой уровень -->
    <div class="flex items-center gap-1 z-10 pr-2">
      <div class="bg-[#2b2b2b] text-white text-sm font-bold px-3 py-1 rounded-lg flex items-center gap-1">
        <span>₽</span> {{ formatR(nextLevel) }}
      </div>
    </div>
  </div>
</div>
    </div>



    <!-- Детальная статистика -->
    <div class="card-base px-5 py-5 space-y-3">
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
      <div class="text-[10px] text-[#DFDFDF] mt-1">Минимальная сумма 5 000₽</div>
      <div v-if="withdrawRequested" class="text-green-400 text-xs mt-2">
        Запрос отправлен, с вами свяжется администратор в Telegram
      </div>
    </div>

    <!-- Ссылка и копирование -->
       <button
          @click="copyLink"
          class=" card-base py-2 flex h-10 flex-1 w-full items-center justify-center gap-1 bg-[#18181B] text-white transition hover:bg-[#232226]"
        >
            <svg width="24" height="24" viewBox="-5 -5 64 64" fill="none">
  <!-- Задний (нижний) прямоугольник, только часть обводки -->
  <path d="M 18 42 Q 12 42 12 36 V 18 Q 12 12 18 12 H 36 Q 42 12 42 18 V 36 Q 42 42 36 42 Z M 8 34 H 7 C 6 34 4 33 4 28 V 10 Q 4 4 10 4 H 28 C 33 4 34 6 34 7 V 8"
    stroke="white" stroke-width="4"  stroke-linejoin="round" fill="none"/>

</svg>
          Твоя реферальная ссылка
        </button>
     <!-- Рекламные материалы -->
     <button
          @click="openTelegramLink"
          class=" card-base py-2 flex h-10 flex-1 w-full items-center justify-center gap-1 bg-[#18181B] text-white transition hover:bg-[#232226]"
        >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" class="size-6">
  <path fill-rule="evenodd" d="M19.902 4.098a3.75 3.75 0 0 0-5.304 0l-4.5 4.5a3.75 3.75 0 0 0 1.035 6.037.75.75 0 0 1-.646 1.353 5.25 5.25 0 0 1-1.449-8.45l4.5-4.5a5.25 5.25 0 1 1 7.424 7.424l-1.757 1.757a.75.75 0 1 1-1.06-1.06l1.757-1.757a3.75 3.75 0 0 0 0-5.304Zm-7.389 4.267a.75.75 0 0 1 1-.353 5.25 5.25 0 0 1 1.449 8.45l-4.5 4.5a5.25 5.25 0 1 1-7.424-7.424l1.757-1.757a.75.75 0 1 1 1.06 1.06l-1.757 1.757a3.75 3.75 0 1 0 5.304 5.304l4.5-4.5a3.75 3.75 0 0 0-1.035-6.037.75.75 0 0 1-.354-1Z" clip-rule="evenodd" />
</svg>

          Рекламые материалы
        </button>



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
const materialsLink = "https://app.lava.top/products/bee68592-a5ab-49a8-b5e6-f6a576e29255/78fd63a5-1ed5-4f55-900d-b01bf16b6593?paymentParams=CiAgICAgICAgewogICAgICAgICAgImludm9pY2VJZCI6ICI1NjUyMmNjYi1jOGY3LTQ2NzItODU3Yy1jZWZkNTAyOTA2OGEiLAogICAgICAgICAgInBheW1lbnRTZXR0aW5ncyI6IHsiaWQiOiI1NjUyMmNjYi1jOGY3LTQ2NzItODU3Yy1jZWZkNTAyOTA2OGEiLCJ0eXBlIjoiaW52b2ljZSIsInN0YXR1cyI6ImluLXByb2dyZXNzIiwiYW1vdW50X3RvdGFsIjp7ImN1cnJlbmN5IjoiUlVCIiwiYW1vdW50Ijo5OTkwLjB9LCJwcm92aWRlciI6eyJuYW1lIjoiYmFuazEzMSIsInBhcmFtZXRlcnMiOnsicHVibGljX3Rva2VuIjoiMzUwMTEyMGU0NDA5ZGY5Y2I0OWM0OWM1NzUwZTMxMmUwMmE3MzA1MDQ3OGEyNmUyYjI1MjA5OTE2MzQ3YmZhYSIsInN0eWxlc2hlZXQiOiJodHRwczovL3dpZGdldC5iYW5rMTMxLnJ1L3BheW1lbnQtZm9ybS5jc3MiLCJzY3JpcHQiOiJodHRwczovL3dpZGdldC5iYW5rMTMxLnJ1L3BheW1lbnQtZm9ybS5qcyJ9fX0KICAgICAgICB9CiAgICAgIA"



const levels = [1000, 2000, 5000, 10000, 15000, 25000, 35000, 50000, 80000, 100000]

const nextLevel = computed(() => {
  return levels.find(level => level > (stats.value.earned || 0)) || levels[levels.length - 1]
})

const progressPercent = computed(() => {
  const earned = stats.value.earned || 0
  const prev = [...levels].reverse().find(level => level <= earned) || 0
  const next = nextLevel.value
  const progress = (earned - prev) / (next - prev)
  return Math.min(Math.max(progress * 100, 0), 100).toFixed(1)
})

const formatR = (value) => {
  if (value == null) return '—'
  return value.toLocaleString('ru-RU') + '₽'
}

// function formatR(val) {
//   if (val === undefined || val === null) return '—'
//   return new Intl.NumberFormat('ru-RU').format(val) + ' ₽'
// }
const canWithdraw = computed(() => (stats.value.balance || 0) >= 5000)

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

const openTelegramLink = () => {
  const url = 'https://example.com';

  if (window.Telegram?.WebApp?.openLink) {
    window.Telegram.WebApp.openLink(materialsLink);
  } else {
    alert('Telegram WebApp API недоступен');
  }
};

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
