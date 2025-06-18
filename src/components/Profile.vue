<template>
  <div>
    <div class="flex items-center bg-gray-600 p-3 rounded mb-4">
      <img :src="user.photo_url || 'assets/icon.png'" class="w-12 h-12 rounded-full mr-3" />
      <div class="flex-1">
        <div class="font-semibold">{{ user.username || user.first_name || 'User' }}</div>
        <div class="text-sm">{{ t.points }}: {{ userData.score }}</div>
        <div class="w-full bg-gray-700 rounded h-2 mt-1">
          <div class="bg-green-500 h-2 rounded" :style="{ width: progress + '%' }"></div>
        </div>
      </div>
    </div>
    <button @click="showInfo()" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">Инфо</button>
    <div class="mt-4 space-y-4">
      <div class="flex items-center justify-between w-full">
        <span class="mr-2">{{ t.theme }}</span>
        <label class="relative inline-flex items-center cursor-pointer ml-auto">
          <input type="checkbox" class="sr-only peer" :checked="theme==='dark'" @change="toggleTheme" />
          <div class="w-11 h-6 bg-gray-300 rounded-full transition-colors duration-300 peer-checked:bg-blue-600 before:content-[''] before:absolute before:top-0.5 before:left-0.5 before:w-5 before:h-5 before:bg-white before:border before:border-gray-300 before:rounded-full before:transition-transform before:duration-300 peer-checked:before:translate-x-full"></div>
        </label>
      </div>
      <div class="flex items-center justify-between w-full">
        <span class="mr-2">{{ t.fullscreen }}</span>
        <label class="relative inline-flex items-center cursor-pointer ml-auto">
          <input type="checkbox" class="sr-only peer" :checked="fullscreen" @change="toggleFullscreen" />
          <div class="w-11 h-6 bg-gray-300 rounded-full transition-colors duration-300 peer-checked:bg-blue-600 before:content-[''] before:absolute before:top-0.5 before:left-0.5 before:w-5 before:h-5 before:bg-white before:border before:border-gray-300 before:rounded-full before:transition-transform before:duration-300 peer-checked:before:translate-x-full"></div>
        </label>
      </div>
      <div class="flex items-center">
        <span class="mr-2">{{ t.language }}</span>
        <select class="border rounded p-1" :value="lang" @change="changeLang">
          <option value="ru">Русский</option>
          <option value="en">English</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { userData } from '../state';
const props = defineProps({ t: Object, showInfo: Function });

const user = ref({});
const progress = ref(Math.floor(Math.random() * 100));
const theme = ref(localStorage.getItem('theme') || 'dark');
const lang = ref(localStorage.getItem('lang') || 'ru');
const fullscreen = ref(false);

onMounted(() => {
  if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
    userData.user = Telegram.WebApp.initDataUnsafe.user;
    user.value = userData.user;
  }
  if (window.Telegram?.WebApp) {
    fullscreen.value = Telegram.WebApp.isFullscreen === true;
  }
});

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark';
  document.body.classList.toggle('light', theme.value === 'light');
  localStorage.setItem('theme', theme.value);
}

function toggleFullscreen() {
  if (!window.Telegram?.WebApp) return;
  if (!fullscreen.value) {
    Telegram.WebApp.requestFullscreen();
    fullscreen.value = true;
  } else {
    Telegram.WebApp.exitFullscreen();
    fullscreen.value = false;
  }
  setTimeout(() => {
    if (window.applySafeInsets) window.applySafeInsets();
  }, 100);
}

function changeLang(e) {
  lang.value = e.target.value;
  localStorage.setItem('lang', lang.value);
  window.dispatchEvent(new CustomEvent('langchange', { detail: lang.value }));
}

watch(theme, () => {
  document.body.classList.toggle('light', theme.value === 'light');
  localStorage.setItem('theme', theme.value);
});

</script>
