<template>
  <div class="h-full flex flex-col space-y-1 p-2">
    <div class="sticky top-0 z-10 bg-[var(--page-bg-color)] px-3 py-4 border-b border-[#2c2c3a]">
      <div class="relative flex items-center justify-between">
        <span class="text-lg font-bold text-white">Profile</span>
        <div class="absolute left-1/2 transform -translate-x-1/2 flex flex-col items-center">
          <span class="text-2xl font-extrabold text-white">1chn</span>
          <span class="text-sm text-gray-400">[ван чан]</span>
        </div>
        <button class="text-xl z-10" @click="openSettings">
          <i class="fas fa-cog"></i>
        </button>
      </div>
    </div>
    <div class="relative p-4 space-y-4 overflow-hidden flex-1">
      <div class="bg-gray-800 p-4 rounded text-center">
        <div class="avatar mx-auto mb-3">
          <span class="num">{{ numDisplay }}</span>
        </div>
        <div class="font-semibold text-lg">{{ user.agent_number || '—' }}</div>
        <div>{{ t.daysInClub }}: {{ user.days_in_club ?? '—' }}</div>
        <div>{{ t.location }}: {{ user.location || '—' }}</div>
        <div>{{ t.status }}: {{ user.status || '—' }}</div>
      </div>
      <div class="bg-gray-800 p-4 rounded">
        <h3 class="text-lg font-bold mb-2">{{ t.aboutClub }}</h3>
        <p>Клуб единомышленников, где агенты обмениваются опытом и секретами эффективных продаж. Присоединяйся и расширяй свои возможности.</p>
      </div>
      <div class="flex justify-around">
        <a href="https://t.me/secret_channel" target="_blank" class="bg-blue-600 px-3 py-2 rounded">{{ t.secretChannel }}</a>
        <a href="https://t.me/club_chat" target="_blank" class="bg-blue-600 px-3 py-2 rounded">{{ t.chat }}</a>
        <a href="https://t.me/club_support" target="_blank" class="bg-blue-600 px-3 py-2 rounded">{{ t.support }}</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { userData } from '../state';
import { API_BASE } from '../api';
const props = defineProps({ t: Object });

const user = ref({});

const numDisplay = computed(() => {
  if (!user.value.agent_number) return '---';
  const parts = user.value.agent_number.split('_');
  return parts[1] || user.value.agent_number;
});

async function loadUser() {
  if (!userData.user.id) return;
  try {
    const resp = await fetch(`${API_BASE}/users/${userData.user.id}`);
    if (resp.ok) {
      const data = await resp.json();
      userData.user = data;
      user.value = data;
    }
  } catch (e) {
    console.error(e);
  }
}

function openSettings() {
  if (window.showPage) window.showPage('settings');
}

onMounted(loadUser);

watch(() => userData.user.id, id => {
  if (id) loadUser();
});
</script>

<style scoped>
.avatar {
  width: 96px;
  height: 96px;
  background: url('assets/agent.svg') no-repeat center/contain;
  position: relative;
  margin: auto;
}
.avatar .num {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translateX(-50%);
  font-family: monospace;
  color: var(--active-color);
}
</style>
