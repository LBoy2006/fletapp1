<template>
  <div class="h-full flex flex-col space-y-1 p-2">
    <div class="sticky top-0 z-10 bg-[var(--page-bg-color)] px-0 py-4 pb-5 relative overflow-visible">
      <div class="relative flex items-center justify-between px-3">
        <span class="text-lg font-bold text-white">Profile</span>
        <div class="absolute left-1/2 transform -translate-x-1/2 flex flex-col items-center">
          <span class="text-2xl font-dela text-white">1chn</span>
          <span class="text-sm text-gray-400">[ван чан]</span>
        </div>
        <button class="text-xl z-10" @click="openSettings">
          <i class="fas fa-cog"></i>
        </button>
      </div>
    </div>
    <div class="relative h-full flex flex-col gap-2 justify-between overflow-y-auto scrollbar-hide flex-col">
      <div class="card-base px-5 py-4 text-center flex flex-col items-center">
        <div class="avatar mx-auto mb-3">
          <span class="num">{{ numDisplay }}</span>
        </div>
        <div class="font-semibold text-lg text-[#DFDFDF]">{{ user.agent_number || '—' }}</div>
        <div class="text-sm text-[#DFDFDF]">{{ t.daysInClub }}: {{ user.days_in_club ?? '—' }}</div>
        <div class="text-sm text-[#DFDFDF]">{{ t.location }}: {{ user.location || '—' }}</div>
        <div class="text-sm text-[#DFDFDF]">{{ t.status }}: {{ user.status || '—' }}</div>
      </div>
      <div class=" px-5 py-4">
        <h3 class="text-lg font-bold mb-2 text-[#DFDFDF]">{{ t.aboutClub }}</h3>
        <p class="text-sm text-[#DFDFDF]">Клуб единомышленников, где агенты обмениваются опытом и секретами эффективных продаж. Присоединяйся и расширяй свои возможности.</p>
      </div>
      <div class="flex flex-col gap-2">
        <a href="https://t.me/secret_channel" target="_blank" class="card-base py-2 flex h-10 w-full items-center justify-center gap-1 bg-[#18181B] text-white transition hover:bg-[#232226]">{{ t.secretChannel }}</a>
        <a href="https://t.me/club_chat" target="_blank" class="card-base py-2 flex h-10 w-full items-center justify-center gap-1 bg-[#18181B] text-white transition hover:bg-[#232226]">{{ t.chat }}</a>
        <a href="https://t.me/club_support" target="_blank" class="card-base py-2 flex h-10 w-full items-center justify-center gap-1 bg-[#18181B] text-white transition hover:bg-[#232226]">{{ t.support }}</a>
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
  if (window.showSettingsModal) window.showSettingsModal();
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
