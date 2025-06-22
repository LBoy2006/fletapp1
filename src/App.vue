<!--app.vue-->

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
import { API_BASE } from './api';

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
  let tgUser = null;
  let initData = null;

  if (window.Telegram && window.Telegram.WebApp) {
    tgUser = window.Telegram.WebApp.initDataUnsafe?.user;
    initData = window.Telegram.WebApp.initData;
  }

  // Если Telegram есть и пользователь есть
  if (tgUser) {
    userData.user = tgUser;
  } else {
    // Локальная отладка
    tgUser = {
      id: 123456,
      first_name: "Тест",
      last_name: "Пользователь",
      username: "test_user",
      is_member: false
    };
    initData = 'test_init_data=123'; // Любая строка-заглушка
    userData.user = tgUser;
  }

  // Отправляем данные на backend
  fetch(`${API_BASE}/auth/telegram`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      initData,
      user: tgUser  // <-- добавляем также user, если нужно
    })
  })
    .then(res => res.json())
    .then(data => {
      userData.user.is_member = data.is_member
      if (!data.is_member) {
        showPayment.value = true
      }
      // userData.token = data.token;
    })
    .catch(err => {
      console.error('Auth error:', err);
    });
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
  // Проверяем, доступно ли Telegram WebApp API
  if (window.Telegram?.WebApp) {
    // Проверка, открыт ли WebApp в полноэкранном режиме
    const isFullscreen = Telegram.WebApp.isFullscreen;
    // Получаем "безопасные отступы" (например, для устройств с вырезами/ноутчами или панелями)
    const safeInset = Telegram.WebApp.contentSafeAreaInset;
    // Получаем нижний отступ (если есть), иначе 0
    const insetBottom = safeInset ? parseInt(safeInset.bottom) || 0 : 0;
    // Сохраняем нижний отступ в реактивную переменную (используется для позиционирования нижней навигации)
    navBottom.value = insetBottom;
    // Устанавливаем высоту нижней навигации (возможно, ты тестировал с завышенным значением — 1000)
    const navHeight = 70;
    // Проходимся по всем элементам с классом `.page`
    document.querySelectorAll('.page').forEach(p => {
      // Если полноэкранный режим и есть данные об отступах
      if (isFullscreen && safeInset) {
        // Получаем верхний отступ и добавляем немного пространства (например, чтобы не перекрывал статус-бар)
        const insetTop = parseInt(safeInset.top) || 0;
        const extraOffset = 20;
        p.style.paddingTop = `${insetTop + extraOffset}px`;
      } else {
        // В остальных случаях убираем верхний отступ
        p.style.paddingTop = '';
      }
      // Добавляем нижний отступ, равный высоте навигации + безопасный нижний отступ устройства
      p.style.paddingBottom = `${navHeight + insetBottom}px`;
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
  <div v-else class="min-h-screen flex flex-col">
    <div ref="pagesRef" class="flex-1 overflow-x-hidden">
      <div ref="innerRef" class="flex" :style="dragStyle">
        <div
          v-for="p in pageOrder"
          :key="p"
          :class="['page w-full flex-shrink-0', { 'no-page-scroll': ['finds', 'suppliers'].includes(p) }]"
        >
          <component :is="pages[p]" :t="t" />
        </div>
      </div>
    </div>
    <nav ref="navRef" :class="{'show-labels': showLabels} " :style="{ bottom: navBottom + 'px' }">
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
