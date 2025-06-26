<!--app.vue-->

<script setup>




import { ref, computed, onMounted } from 'vue';
import Finds from './components/Finds.vue';
import Feed from './components/Feed.vue';
import FeedOverlay from './components/FeedOverlay.vue';
import Suppliers from './components/Suppliers.vue';
import Affiliate from './components/Affiliate.vue';
import Profile from './components/Profile.vue';
import NewUser from './components/NewUser.vue';
import NewUserProfile from './components/NewUserProfile.vue';
import SupplierModal from './components/SupplierModal.vue';
import ItemModal from './components/ItemModal.vue';
import ProfileSettings from './components/ProfileSettings.vue';
import { userData } from './state';
import { translations } from './translations.js';
import { API_BASE } from './api';

const navItems = ['feed', 'suppliers', 'finds', 'affiliate', 'profile'];
const pageOrder = ['feed', 'suppliers', 'finds', 'affiliate', 'profile'];
const svgModules = import.meta.glob('./icons/*.svg', {
  query: '?raw',
  import: 'default',
  eager: true
});
const pageIcons = {};
for (const path in svgModules) {
  const name = path.replace('./icons/', '').replace('.svg', '');
  pageIcons[name] = svgModules[path];
}

const pages = { feed: Feed, finds: Finds, suppliers: Suppliers, affiliate: Affiliate, profile: Profile };

const t = translations.en;
const currentIndex = ref(pageOrder.indexOf('finds'));
const sheetVisible = ref(false);
const sheetLines = ref([]);
const supplierModalVisible = ref(false);
const supplierModalData = ref(null);
const itemModalVisible = ref(false);
const itemModalData = ref(null);
const settingsModalVisible = ref(false);
const feedOverlayVisible = ref(false);
const pagesRef = ref(null);
const innerRef = ref(null);
const navRef = ref(null);
const showLabels = ref(false);
const navBottom = ref(0);
const baseNavBottom = ref(0);
const dragOffset = ref(0);
const isDragging = ref(false);
const showNewUser = ref(false);
const showNewUserProfile = ref(false);
let hideTimer = null;

const dragStyle = computed(() => ({
  transform: `translateX(calc(-${currentIndex.value * 100}% + ${dragOffset.value}%))`,
  transition: isDragging.value ? 'none' : ''
}));



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

function showSupplierModal(data) {
  supplierModalData.value = data;
  supplierModalVisible.value = true;
}

function hideSupplierModal() {
  supplierModalVisible.value = false;
  supplierModalData.value = null;
}

function showItemModal(data) {
  itemModalData.value = data;
  itemModalVisible.value = true;
}

function hideItemModal() {
  itemModalVisible.value = false;
  itemModalData.value = null;
}

function showSettingsModal() {
  settingsModalVisible.value = true;
}

function hideSettingsModal() {
  settingsModalVisible.value = false;
}

function showFeedOverlay() {
  feedOverlayVisible.value = true;
}

function hideFeedOverlay() {
  feedOverlayVisible.value = false;
}

async function onItemToggleFavorite() {
  const item = itemModalData.value;
  if (!item) return;
  try {
    const r = await fetch(`${API_BASE}/finds/${item.id}/favorite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userData.user.id })
    });
    if (r.ok) {
      const data = await r.json();
      item.fav = data.favorite;
      if (data.favorite) {
        item.favorites_count = (item.favorites_count || 0) + 1;
      } else {
        item.favorites_count = Math.max(0, (item.favorites_count || 1) - 1);
      }
    }
  } catch (e) {
    console.error(e);
  }
}

async function onSupplierToggleFavorite() {
  const supplier = supplierModalData.value;
  if (!supplier) return;
  try {
    const r = await fetch(`${API_BASE}/suppliers/${supplier.id}/favorite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userData.user.id })
    });
    if (r.ok) {
      const data = await r.json();
      supplier.is_favorite = data.favorite;
      if (data.favorite) {
        supplier.favorites_count = (supplier.favorites_count || 0) + 1;
      } else {
        supplier.favorites_count = Math.max(0, (supplier.favorites_count || 1) - 1);
      }
    }
  } catch (e) {
    console.error(e);
  }
}

function onLinkCopied() {
  showSheet('Link copied');
}

function onNavClick(item) {
  if (item === 'feed') {
    showFeedOverlay();
    return;
  }
  if (item === 'profile' && !userData.user.is_member) {
    showNewUserProfile.value = true;
  }
  showPage(item);
}

function onPaid() {
  showNewUser.value = false;
  showPage('finds');
}

function onPaidProfile() {
  showNewUserProfile.value = false;
  showPage('profile');
}


  // Если Telegram есть и пользователь есть
onMounted(async () => {
  // Гарантированно дождаться готовности SDK
  if (window.Telegram?.WebApp) {
    Telegram.WebApp.ready(); // запускает SDK
  }

  // Дождаться полного DOM + viewport, Telegram SDK может подгружаться медленно
  await new Promise(resolve => setTimeout(resolve, 100)); // можно 300–500 мс для подстраховки

  const tgUser = window.Telegram?.WebApp?.initDataUnsafe?.user;
  const initData = window.Telegram?.WebApp?.initData;

  if (tgUser) {
    userData.user = tgUser;
  } else {
    // Локальный тест
    userData.user = {
      id: 123456,
      first_name: "Тест",
      last_name: "Пользователь",
      username: "test_user",
      is_member: false
    };
    initData = 'test_init_data=123';
  }

  try {
    const res = await fetch(`${API_BASE}/auth/telegram`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ initData, user: userData.user })
    });

    const data = await res.json();

    if (res.ok) {
      userData.user.is_member = data.is_member;
      if (!data.is_member) {
        showNewUser.value = true;
      }
    } else {
      console.error('Auth failed:', data);
    }
  } catch (err) {
    console.error('Auth error:', err);
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
    if (startX === null || startY === null) return;

    const touch = e.touches[0];
    const deltaX = touch.clientX - startX;
    const deltaY = touch.clientY - startY;

    const absX = Math.abs(deltaX);
    const absY = Math.abs(deltaY);

    if (!isDragging.value) {
      // ⛔ Прекратить свайп, если жест — вертикальный
      if (absY > absX) {
        startX = null;
        startY = null;
        return;
      }

      // ✅ Если горизонтальный свайп достаточно большой — начинаем
      if (absX > dragThreshold) {
        isDragging.value = true;
      } else {
        return;
      }
    }

    // 🎯 Выполняем свайп
    dragOffset.value = (deltaX / width()) * 100;
    e.preventDefault(); // важно для плавности
  }, { passive: false });

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


// onMounted(() => {
//   const nav = navRef.value;
//   let sy = null;
//   nav.addEventListener('touchstart', e => {
//     if (e.touches.length === 1) sy = e.touches[0].clientY;
//   });
//   nav.addEventListener('touchend', e => {
//     if (sy === null) return;
//     const dy = e.changedTouches[0].clientY - sy;
//     if (dy < -30) revealLabels();
//     sy = null;
//   });
// });

// onMounted(() => {
//   const pagesEls = innerRef.value.querySelectorAll('.page');
//   pagesEls.forEach(page => {
//     let sy = null;
//     let pulling = false;
//     page.addEventListener('touchstart', e => {
//       if (e.touches.length !== 1) return;
//       sy = e.touches[0].clientY;
//       pulling = false;
//       page.style.transition = '';
//     });
//     page.addEventListener('touchmove', e => {
//       if (sy === null || isDragging.value) return;
//       const cy = e.touches[0].clientY;
//       const diff = cy - sy;
//       const atTop = page.scrollTop <= 0;
//       const atBottom = page.scrollTop + page.clientHeight >= page.scrollHeight;
//       if ((atTop && diff > 0) || (atBottom && diff < 0)) {
//         e.preventDefault();
//         pulling = true;
//         page.style.transform = `translateY(${diff / 4}px)`;
//       }
//     });
//     const reset = () => {
//       if (!pulling) {
//         sy = null;
//         return;
//       }
//       page.style.transition = 'transform 0.3s';
//       page.style.transform = 'translateY(0)';
//       sy = null;
//       pulling = false;
//     };
//     page.addEventListener('touchend', reset);
//     page.addEventListener('touchcancel', reset);
//   });
// });

function revealLabels() {
  // Показываем подписи к иконкам в нижней навигации
  showLabels.value = true;
  // Отменяем предыдущий таймер скрытия подписей, если он ещё активен
  clearTimeout(hideTimer);
  // Устанавливаем новый таймер: через 5 секунд подписи автоматически скроются
  hideTimer = setTimeout(() => {
    showLabels.value = false;
  }, 5000);
}


function applySafeInsets() {
  if (window.Telegram?.WebApp) {
    const isFullscreen = Telegram.WebApp.isFullscreen;
    const safeInset = Telegram.WebApp.contentSafeAreaInset || {};
    const insetTop = parseInt(safeInset.top) || 0;
    const insetBottom = parseInt(safeInset.bottom) || 0;
    const navHeight = 90;
    baseNavBottom.value = insetBottom;
    navBottom.value = insetBottom;

    document.querySelectorAll('.page').forEach(p => {
      if (isFullscreen) {
        p.classList.add('safe-area');
        p.style.paddingTop = `${20 + insetTop}px`;
      } else {
        p.classList.remove('safe-area');
        p.style.paddingTop = '';
      }

      p.style.paddingBottom = `${navHeight + insetBottom}px`;
    });
  }
}



onMounted(() => {
  if (window.Telegram?.WebApp) {
    Telegram.WebApp.ready();
    Telegram.WebApp.disableVerticalSwipes();
    applySafeInsets();
    Telegram.WebApp.onEvent('viewportChanged', () => {
      applySafeInsets();
      updateNavForKeyboard();
    });
  }

  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', updateNavForKeyboard);
  }

  updateNavForKeyboard();
});

window.applySafeInsets = applySafeInsets;
window.showPage = showPage;
window.showSheet = showSheet;
window.hideSheet = hideSheet;
window.showSupplierModal = showSupplierModal;
window.hideSupplierModal = hideSupplierModal;
window.showItemModal = showItemModal;
window.hideItemModal = hideItemModal;
window.showSettingsModal = showSettingsModal;
window.hideSettingsModal = hideSettingsModal;
window.showFeedOverlay = showFeedOverlay;
window.hideFeedOverlay = hideFeedOverlay;

function updateNavForKeyboard() {
  const viewport = window.visualViewport;
  if (!viewport) return;

  const keyboardHeight = window.innerHeight - viewport.height - viewport.offsetTop;

  navBottom.value = keyboardHeight > 0
    ? keyboardHeight
    : 0;
}


const navHidden = ref(false);
onMounted(() => {
  const nav = navRef.value;

  window.addEventListener('focusin', (e) => {
    if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) {
      navHidden.value = true;
      nav.style.transition = 'transform 0.3s ease';
      nav.style.transform = 'translateY(200%)';

      document.querySelectorAll('.page').forEach(p => {
        p.style.transition = 'padding-bottom 0.3s ease';
        p.style.paddingBottom = '0px';
      });
    }
  });

  window.addEventListener('focusout', () => {
    navHidden.value = false;
    nav.style.transition = 'transform 0.3s ease';
    nav.style.transform = 'translateY(0)';

    const insetBottom = baseNavBottom.value;
    const navHeight = 90; // точно как в твоём CSS
    document.querySelectorAll('.page').forEach(p => {
      p.style.transition = 'padding-bottom 0.3s ease';
      p.style.paddingBottom = `${navHeight + insetBottom}px`;
    });
  });
});

</script>
<template>
  <NewUser v-if="showNewUser" @paid="onPaid" />
  <NewUserProfile v-if="showNewUserProfile" @paid="onPaidProfile" />
  <SupplierModal
    v-if="supplierModalVisible"
    :supplier="supplierModalData"
    @close="hideSupplierModal"
    @copied="onLinkCopied"
    @toggle-favorite="onSupplierToggleFavorite"
  />
  <ProfileSettings
    v-if="settingsModalVisible"
    :t="t"
    @close="hideSettingsModal"
  />
  <ItemModal
    v-if="itemModalVisible"
    :item="itemModalData"
    @close="hideItemModal"
    @copied="onLinkCopied"
    @toggle-favorite="onItemToggleFavorite"
  />
  <FeedOverlay
    v-if="feedOverlayVisible"
    @close="hideFeedOverlay"
  />
  <div class="min-h-screen flex flex-col overflow-hidden">
    <div ref="pagesRef" class="flex-1 overflow-x-hidden">
      <div ref="innerRef" class="flex h-full " :style="dragStyle">
        <div
          v-for="p in pageOrder"
          :key="p"
          :class="['page w-full flex-shrink-0 scrollbar-hide', { 'no-page-scroll': ['finds', 'suppliers', 'affiliate'].includes(p) }]"
        >
          <component :is="pages[p]" :t="t" />
        </div>
      </div>
    </div>
    <nav ref="navRef" :class="{'show-labels': showLabels} " :style="{ bottom: navBottom + 'px' }">
      <button v-for="item in navItems" :key="item" class="nav-btn" :class="{ active: pageOrder[currentIndex]===item }" @click="onNavClick(item)">
        <span class="icon" v-html="pageIcons[item]"></span>
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
