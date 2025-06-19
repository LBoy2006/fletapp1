<script setup>
import { ref, computed, onMounted } from 'vue';
import Finds from './components/Finds.vue';
import Suppliers from './components/Suppliers.vue';
import Affiliate from './components/Affiliate.vue';
import Profile from './components/Profile.vue';
import ProfileSettings from './components/ProfileSettings.vue';
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
      username: "test_user"
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

onMounted(() => {
  const pagesEls = innerRef.value.querySelectorAll('.page');
  pagesEls.forEach(page => {
    let sy = null;
    let pulling = false;
    page.addEventListener('touchstart', e => {
      if (e.touches.length !== 1) return;
      sy = e.touches[0].clientY;
      pulling = false;
      page.style.transition = '';
    });
    page.addEventListener('touchmove', e => {
      if (sy === null || isDragging.value) return;
      const cy = e.touches[0].clientY;
      const diff = cy - sy;
      const atTop = page.scrollTop <= 0;
      const atBottom = page.scrollTop + page.clientHeight >= page.scrollHeight;
      if ((atTop && diff > 0) || (atBottom && diff < 0)) {
        e.preventDefault();
        pulling = true;
        page.style.transform = `translateY(${diff / 4}px)`;
      }
    });
    const reset = () => {
      if (!pulling) {
        sy = null;
        return;
      }
      page.style.transition = 'transform 0.3s';
      page.style.transform = 'translateY(0)';
      sy = null;
      pulling = false;
    };
    page.addEventListener('touchend', reset);
    page.addEventListener('touchcancel', reset);
  });
});

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
  showPage('finds');
});
</script>
