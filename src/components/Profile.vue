<template>
  <div class="relative p-4 space-y-4">
    <button class="absolute top-2 right-2 text-xl" @click="openSettings">
      <i class="fas fa-cog"></i>
    </button>
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
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { userData } from '../state';
const props = defineProps({ t: Object });

const user = ref({});

const numDisplay = computed(() => {
  if (!user.value.agent_number) return '---';
  const parts = user.value.agent_number.split('_');
  return parts[1] || user.value.agent_number;
});

async function loadUser() {
  try {
    const resp = await fetch('http://localhost:8000/users/1');
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
