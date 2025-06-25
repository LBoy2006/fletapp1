<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
    <div class="relative w-full max-w-sm mx-4 p-6 rounded-2xl bg-white/10 backdrop-blur-lg border border-white/30 text-center">
      <button class="absolute top-3 right-3" @click="$emit('close')">
        <svg width="22" height="22" fill="none">
          <path d="M5 5l12 12M17 5L5 17" stroke="white" stroke-width="2" stroke-linecap="round" />
        </svg>
      </button>
      <div class="flex flex-col items-center space-y-4">
        <div class="text-6xl">🚫</div>
        <div>
          <p class="text-lg font-semibold text-white">Лента находится<br>в разработке</p>
          <p class="text-sm text-gray-300 mt-2">Скоро любой агент сможет публиковать свои находки, отчёты и результаты</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(['close'])
</script>
