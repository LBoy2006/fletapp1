import { createApp } from 'vue';
import App from './App.vue';
import './style.css';

// Set initial app height to prevent layout shift when the on-screen
// keyboard appears on mobile devices. The value is taken once on load
// and when the device orientation changes so the navigation bar remains
// anchored to the bottom of the screen.
const setAppHeight = () => {
  document.documentElement.style.setProperty(
    '--app-height', `${window.innerHeight}px`
  );
};

setAppHeight();
window.addEventListener('orientationchange', setAppHeight);

createApp(App).mount('#app');
