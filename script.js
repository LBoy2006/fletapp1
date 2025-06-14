const wrapper = document.getElementById('pages-wrapper');
const buttons = document.querySelectorAll('.nav-btn');
const themeToggle = document.getElementById('theme-toggle');
const fullscreenToggle = document.getElementById('fullscreen-toggle');
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
