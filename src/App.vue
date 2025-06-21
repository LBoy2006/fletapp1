<script setup>
import { ref, computed, onMounted } from 'vue';
import Finds from './components/Finds.vue';
import Suppliers from './components/Suppliers.vue';
import Affiliate from './components/Affiliate.vue';
import Profile from './components/Profile.vue';
import ProfileSettings from './components/ProfileSettings.vue';
import Payment from './components/Payment.vue';
import { userData } from './state';
import { translations } from './translations.js';

const navItems = ['feed', 'finds', 'suppliers', 'affiliate', 'profile'];
const pageOrder = ['finds', 'suppliers', 'affiliate', 'profile', 'settings'];
const pageIcons = {
  feed: 'fas fa-rss',
  finds: 'fas fa-star',
  suppliers: 'fas fa-truck',
  affiliate: 'fas fa-handshake',
  profile: 'fas fa-user'
};

const pages = { finds: Finds, suppliers: Suppliers, affiliate: Affiliate, profile: Profile, settings: ProfileSettings };

const lang = ref(localStorage.getItem('lang') || 'ru');
const t = computed(() => translations[lang.value] || translations.ru);
const currentIndex = ref(pageOrder.indexOf('finds'));
const sheetVisible = ref(false);
const sheetLines = ref([]);
const pagesRef = ref(null);
const innerRef = ref(null);
const navRef = ref(null);
const showLabels = ref(false);
const navBottom = ref(0);
const dragOffset = ref(0);
const isDragging = ref(false);
const showPayment = ref(false);
let hideTimer = null;

const dragStyle = computed(() => ({
  transform: `translateX(calc(-${currentIndex.value * 100}% + ${dragOffset.value}%))`,
  transition: isDragging.value ? 'none' : ''
}));

function onLangChange(e) {
  lang.value = e.detail || e.target.value || 'ru';
}
window.addEventListener('langchange', onLangChange);

function showPage(page) {
  currentIndex.value = pageOrder.indexOf(page);
  dragOffset.value = 0;
  isDragging.value = false;
  revealLabels();
}

let sheetTimer = null;
function showSheet(lines) {
  sheetLines.value = Array.isArray(lines) ? lines : [lines];
  sheetVisible.value = true;
  clearTimeout(sheetTimer);
  sheetTimer = setTimeout(() => (sheetVisible.value = false), 3000);
}

function hideSheet() {
  sheetVisible.value = false;
}

function onNavClick(item) {
  if (item === 'feed') {
    showSheet(t.value.feedInDev);
    return;
  }
  showPage(item);
}

function onPaid() {
  showPayment.value = false;
  showPage('finds');
}

// --- Блок авторизации Telegram Mini App ---
onMounted(() => {
  // Только при первом запуске приложения
  if (window.Telegram && window.Telegram.WebApp) {
    const tgUser = window.Telegram.WebApp.initDataUnsafe?.user;
    if (tgUser) {
      userData.user = tgUser;

      // Отправляем initData на backend для бесшовной авторизации
      fetch('https://1chn.api.gptbrainbot.ru/auth/telegram', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          initData: window.Telegram.WebApp.initData
        })
      })
        .then(res => res.json())
        .then(data => {
          userData.user.is_member = data.is_member
          if (!data.is_member) {
            showPayment.value = true
          }
          // Если backend вернёт доп. данные — можно сохранить:
          // userData.profile = data;
          // userData.token = data.token;
        })
        .catch(err => {
          console.error('Auth error:', err);
        });
    }
  } else {
    // Для локальной отладки без Telegram
    userData.user = {
      id: 123456,
      first_name: "Тест",
      last_name: "Пользователь",
      username: "test_user",
      is_member: false
    }
  }
});
// --- /Блок авторизации ---

onMounted(() => {
  document.body.classList.toggle('light', (localStorage.getItem('theme') || 'dark') === 'light');
});

let startX = null;
let startY = null;
const dragThreshold = 20;
onMounted(() => {
  const el = pagesRef.value;
  const width = () => el.clientWidth;
  el.addEventListener('touchstart', e => {
    if (e.touches.length === 1) {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
      isDragging.value = false;
    }
  });
  el.addEventListener('touchmove', e => {
    if (startX === null) return;
    const deltaX = e.touches[0].clientX - startX;
    const deltaY = e.touches[0].clientY - startY;
    if (!isDragging.value) {
      if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > dragThreshold) {
        isDragging.value = true;
      } else {
        return;
      }
    }
    dragOffset.value = (deltaX / width()) * 100;
  });
  el.addEventListener('touchend', e => {
    if (startX === null) return;
    const deltaX = e.changedTouches[0].clientX - startX;
    if (isDragging.value && Math.abs(deltaX) > width() / 4) {
      if (deltaX < 0 && currentIndex.value < pageOrder.length - 1) {
        showPage(pageOrder[currentIndex.value + 1]);
      } else if (deltaX > 0 && currentIndex.value > 0) {
        showPage(pageOrder[currentIndex.value - 1]);
      }
    }
    dragOffset.value = 0;
    isDragging.value = false;
    startX = null;
    startY = null;
  });
});

onMounted(() => {
  const nav = navRef.value;
  let sy = null;
  nav.addEventListener('touchstart', e => {
    if (e.touches.length === 1) sy = e.touches[0].clientY;
  });
  nav.addEventListener('touchend', e => {
    if (sy === null) return;
    const dy = e.changedTouches[0].clientY - sy;
    if (dy < -30) revealLabels();
    sy = null;
  });
});

// disable custom overscroll spring behaviour
// Native scrolling works better without this handler on some devices


function revealLabels() {
  showLabels.value = true;
  clearTimeout(hideTimer);
  hideTimer = setTimeout(() => {
    showLabels.value = false;
  }, 5000);
}

function applySafeInsets() {
  if (window.Telegram?.WebApp) {
    const isFullscreen = Telegram.WebApp.isFullscreen;
    const safeInset = Telegram.WebApp.contentSafeAreaInset;
    if (safeInset) {
      const insetBottom = parseInt(safeInset.bottom) || 0;
      navBottom.value = insetBottom;
    } else {
      navBottom.value = 0;
    }
    document.querySelectorAll('.page').forEach(p => {
      if (isFullscreen && safeInset) {
        const insetTop = parseInt(safeInset.top) || 0;
        const extraOffset = 20;
        p.style.paddingTop = `${insetTop + extraOffset}px`;
      } else {
        p.style.paddingTop = '';
      }
    });
  }
}
window.applySafeInsets = applySafeInsets;
window.showPage = showPage;
window.showSheet = showSheet;
window.hideSheet = hideSheet;

onMounted(() => {
  if (window.Telegram?.WebApp) {
    Telegram.WebApp.ready();
    Telegram.WebApp.disableVerticalSwipes();
    applySafeInsets();
  }
  if (!showPayment.value) {
    showPage('finds');
  }
});
</script>
<template>
  <Payment v-if="showPayment" @paid="onPaid" />
  <div v-else class="h-full flex flex-col">
    <div ref="pagesRef" class="flex-1 overflow-hidden">
      <div ref="innerRef" class="flex" :style="dragStyle">
        <div v-for="p in pageOrder" :key="p" class="page w-full flex-shrink-0 overflow-y-auto">
          <component :is="pages[p]" :t="t" />
        </div>
      </div>
    </div>
    <nav ref="navRef" :class="{'show-labels': showLabels}" :style="{ bottom: navBottom + 'px' }">
      <button v-for="item in navItems" :key="item" class="nav-btn" :class="{ active: pageOrder[currentIndex]===item }" @click="onNavClick(item)">
        <i :class="['icon', pageIcons[item]]"></i>
        <span class="nav-label">{{ t[item] }}</span>
      </button>
    </nav>
    <transition name="modal-fade">
      <div v-if="sheetVisible" class="fixed bottom-20 inset-x-0 mx-4 p-4 bg-gray-800 rounded" @click="hideSheet">
        <p v-for="l in sheetLines" :key="l">{{ l }}</p>
      </div>
    </transition>
  </div>
</template>
