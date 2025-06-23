<template>
  <div class="relative">
    <button class="absolute top-2 left-2 text-xl" @click="goBack"><i class="fas fa-arrow-left"></i></button>
    <!-- user block and info button removed -->
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
      <div class="flex items-center mt-2">
        <span class="mr-2">{{ t.location }}</span>
        <input v-model="location" class="border rounded p-1 flex-1" />
        <button @click="saveLocation" class="ml-2 bg-blue-500 text-white px-3 py-1 rounded">OK</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { userData } from '../state';
import { API_BASE } from '../api';
const props = defineProps({ t: Object });

function goBack() {
  if (window.showPage) window.showPage('profile');
}

const user = ref({});
const location = ref('');
const progress = ref(Math.floor(Math.random() * 100));
const theme = ref(localStorage.getItem('theme') || 'dark');
const fullscreen = ref(false);

async function loadUser() {
  if (!userData.user.id) return;
  try {
    const resp = await fetch(`${API_BASE}/users/${userData.user.id}`);
    if (resp.ok) {
      const data = await resp.json();
      userData.user = data;
      user.value = data;
      location.value = data.location || '';
    }
  } catch (e) {
    console.error(e);
  }
  if (window.Telegram?.WebApp) {
    fullscreen.value = Telegram.WebApp.isFullscreen === true;
  }
}

onMounted(loadUser);

watch(() => userData.user.id, id => {
  if (id) loadUser();
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

async function saveLocation() {
  try {
    await fetch(`${API_BASE}/users/${userData.user.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ location: location.value, agent_number: user.value.agent_number })
    });
  } catch (e) {
    console.error(e);
  }
}

watch(theme, () => {
  document.body.classList.toggle('light', theme.value === 'light');
  localStorage.setItem('theme', theme.value);
});

</script>
