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
      <div class="card-base p-3 flex flex-row justify-start">
        <img :src="avatarUrl" class="w-24 h-24 mr-4 rounded-full object-cover border border-[0.5px] border-[#424242] " />
        <div class="flex-row flex-1 flex justify-between">
          <div class="flex-col justify-between text-start">
            <div class="text-sm text-[#DFDFDF] pt-2">Агент:</div>
            <div class="text-sm text-[#DFDFDF]">{{ t.daysInClub }}:</div>
            <div class="text-sm text-[#DFDFDF]">{{ t.location }}:</div>
            <div class="text-sm text-[#DFDFDF]">{{ t.status }}:</div>
          </div>
           <div class="flex-col justify-between text-end">
            <div class="font-semibold text-lg text-[#DFDFDF]">{{ numDisplay }}</div>
            <div class="text-sm text-[#DFDFDF]">{{ user.days_in_club ?? '—' }}</div>
            <div class="text-sm text-[#DFDFDF]">{{ user.location || '—' }}</div>
            <div class="text-sm text-[#DFDFDF]">{{ user.status || '—' }}</div>
           </div>
        </div>
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
import av1 from '../img/1.webp';
import av2 from '../img/2.webp';
import av3 from '../img/3.webp';
import av4 from '../img/4.webp';
import av5 from '../img/5.webp';
const props = defineProps({ t: Object });

const user = ref({});

const numDisplay = computed(() => {
  if (!user.value.agent_number) return '---';
  // const parts = user.value.agent_number.split('_');
  return user.value.agent_number;
});

const avatarMap = {
  'Новобранец': av1,
  'Агент': av2,
  'Резидент': av3,
  'Куратор': av4,
  'Легенда': av5
};

const avatarUrl = computed(() => {
  return avatarMap[user.value.status] || av1;
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
