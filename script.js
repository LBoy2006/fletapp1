const wrapper = document.getElementById('pages-wrapper');
const buttons = document.querySelectorAll('.nav-btn');
const themeToggle = document.getElementById('theme-toggle');
const fullscreenToggle = document.getElementById('fullscreen-toggle');
const languageSelect = document.getElementById('language-select');
const infoButton = document.getElementById('info-button');
const infoModal = document.getElementById('info-modal');
const infoClose = document.getElementById('info-close');

const translations = {
  ru: {
    leaderboard: 'Лидерборд',
    task: 'Задание',
    home: 'Главная',
    collections: 'Рюкзак',
    settings: 'Настройки',
    theme: 'Темная тема',
    fullscreen: 'Полноэкранный режим',
    language: 'Язык'
  },
  en: {
    leaderboard: 'Leaderboard',
    task: 'Task',
    home: 'Home',
    collections: 'Backpack',
    settings: 'Settings',
    theme: 'Dark theme',
    fullscreen: 'Fullscreen mode',
    language: 'Language'
  }
};
const pageOrder = ['leaderboard', 'task', 'home', 'collections', 'settings'];
let currentIndex = pageOrder.indexOf('home');

function updateTransform() {
  wrapper.style.transform = `translateX(-${currentIndex * 100}%)`;
}

function showPage(id) {
  currentIndex = pageOrder.indexOf(id);
  updateTransform();
  buttons.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.page === id);
  });
}

function applyTheme(theme) {
  document.body.classList.toggle('light', theme === 'light');
}

function applyTranslations(lang) {
  const t = translations[lang] || translations.ru;
  document.documentElement.lang = lang;
  document.getElementById('leaderboard-title').textContent = t.leaderboard;
  document.getElementById('task-title').textContent = t.task;
  document.getElementById('home-title').textContent = t.home;
  document.getElementById('collections-title').textContent = t.collections;
  document.getElementById('settings-title').textContent = t.settings;
  document.getElementById('theme-label').textContent = t.theme;
  document.getElementById('fullscreen-label').textContent = t.fullscreen;
  document.getElementById('language-label').textContent = t.language;
  document.getElementById('nav-leaderboard').textContent = t.leaderboard;
  document.getElementById('nav-task').textContent = t.task;
  document.getElementById('nav-home').textContent = t.home;
  document.getElementById('nav-collections').textContent = t.collections;
  document.getElementById('nav-settings').textContent = t.settings;
  languageSelect.value = lang;
}

function initLanguage() {
  const saved = localStorage.getItem('lang') || 'ru';
  applyTranslations(saved);
}

function initTheme() {
  const saved = localStorage.getItem('theme') || 'dark';
  applyTheme(saved);
  themeToggle.checked = saved === 'dark';
}

function initFullscreen() {
  if (window.Telegram?.WebApp) {
    fullscreenToggle.checked = Telegram.WebApp.isFullscreen === true;
  }
}

function applySafeInsets() {
  const isFullscreen = Telegram.WebApp.isFullscreen;
  const safeInset = Telegram.WebApp.contentSafeAreaInset;

  if (safeInset) {
    document.getElementById('pages').style.paddingBottom = `${safeInset.bottom}px`;
    document.querySelector('nav').style.bottom = `${safeInset.bottom}px`;
  }

  document.querySelectorAll('.page').forEach(page => {
    if (isFullscreen && safeInset) {
      const insetTop = parseInt(safeInset.top) || 0;
      const extraOffset = 20;
      page.style.paddingTop = `${insetTop + extraOffset}px`;
    } else {
      page.style.paddingTop = '';
    }
  });
}

if (window.Telegram?.WebApp) {
  Telegram.WebApp.ready();

  initTheme();
  initFullscreen();
  initLanguage();
  applySafeInsets();
  showPage('home');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => showPage(btn.dataset.page));
  });

  fullscreenToggle.addEventListener('change', async () => {
    if (!window.Telegram?.WebApp) return;
    if (fullscreenToggle.checked) {
      await Telegram.WebApp.requestFullscreen();
    } else {
      await Telegram.WebApp.exitFullscreen();
    }
    setTimeout(() => applySafeInsets(), 100);
  });
}

themeToggle.addEventListener('change', () => {
  const theme = themeToggle.checked ? 'dark' : 'light';
  applyTheme(theme);
  localStorage.setItem('theme', theme);
});

languageSelect.addEventListener('change', () => {
  const lang = languageSelect.value;
  applyTranslations(lang);
  localStorage.setItem('lang', lang);
});

// свайпы
const container = document.getElementById('pages');
let startX = null;

container.addEventListener('touchstart', e => {
  if (e.touches.length === 1) {
    startX = e.touches[0].clientX;
  }
});

container.addEventListener('touchend', e => {
  if (startX === null) return;
  const deltaX = e.changedTouches[0].clientX - startX;
  if (Math.abs(deltaX) > 50) {
    if (deltaX < 0 && currentIndex < pageOrder.length - 1) {
      showPage(pageOrder[currentIndex + 1]);
    } else if (deltaX > 0 && currentIndex > 0) {
      showPage(pageOrder[currentIndex - 1]);
    }
  }
  startX = null;
});

if (infoButton && infoModal && infoClose) {
  infoButton.addEventListener('click', () => {
    infoModal.classList.remove('hidden');
  });

  infoClose.addEventListener('click', () => {
    infoModal.classList.add('hidden');
  });

  infoModal.addEventListener('click', e => {
    if (e.target === infoModal) {
      infoModal.classList.add('hidden');
    }
  });
}
